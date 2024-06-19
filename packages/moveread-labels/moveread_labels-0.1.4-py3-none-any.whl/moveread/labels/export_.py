from typing import Sequence
from functools import partial
from haskellian.either import Either, Left, Right
import chess
from chess import IllegalMoveError, InvalidMoveError, AmbiguousMoveError
from chess_notation.styles import Styles, style
from chess_notation.language import translate, Language
from chess_utils import captured_piece
from .annotations import Annotations, StylesNA

ChessError = IllegalMoveError | InvalidMoveError | AmbiguousMoveError

def verified_styles(pgn: Sequence[str], styles: Styles) -> Either[ChessError, list[str]]:
  """Apply `styles` but keeping track of the current position, so that the captured piece can be used"""
  board = chess.Board()
  moves = []
  try:
    for san in pgn:
      move = board.parse_san(san)
      moves.append(style(san, styles, captured_piece(board, move)))
      board.push(move)
    return Right(moves)
  except (IllegalMoveError, InvalidMoveError, AmbiguousMoveError) as e:
    return Left(e)
  
def apply_styles(pgn: Sequence[str], styles: StylesNA | None, verify_legal: bool = True) -> Either[ChessError, Sequence[str]]:
  """Apply `styles` to `pgn`. If some style required a captured piece (or `verify_legal`), the game position is kept track of"""
  if styles is None:
    return Right(pgn)
  elif styles.pawn_capture == 'PxN' or styles.piece_capture == 'NxN' or verify_legal:
    return verified_styles(pgn, styles.without_na())
  else:
    return Right([style(san, styles.without_na()) for san in pgn])

def apply_lang(moves: Sequence[str], lang: Language | None) -> Sequence[str]:
  """Map translate if `lang is not None`"""
  return moves if lang is None else [translate(san, lang) for san in moves]

def apply_manual(moves: Sequence[str], manual_labels: dict[int, str] | None) -> Sequence[str]:
  if manual_labels is None:
    return moves
  output = [*moves]
  for i, lab in sorted(manual_labels.items()):
    if i < len(moves):
      output[i] = lab
    elif i == len(moves):
      output.append(lab)
  return output

def export(pgn: Sequence[str], ann: Annotations) -> Either[ChessError, Sequence[str]]:
  """Export `pgn` into `labels` as described by the annotations"""
  moves = pgn if ann.end_correct is None else pgn[:ann.end_correct]
  return apply_styles(moves, ann.styles) \
    | partial(apply_lang, lang=ann.language_no_na) \
    | partial(apply_manual, manual_labels=ann.manual_labels)


