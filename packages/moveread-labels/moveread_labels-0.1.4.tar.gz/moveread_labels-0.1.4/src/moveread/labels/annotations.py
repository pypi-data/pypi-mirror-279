from typing import Literal
from pydantic import BaseModel, RootModel
from chess_notation.language import Language
from chess_notation.styles import Check, Mate, Castle, PawnCapture, PieceCapture, Styles

NA = Literal['N/A']
"""Not Applicable"""

def no_na(x):
  return x if x != 'N/A' else None

class StylesNA(BaseModel):
  """Like `chess_notation.Styles`, but with possibly `'N/A'` annotations"""
  check: Check | NA | None = None
  mate: Mate | NA | None = None
  castle: Castle | NA | None = None
  pawn_capture: PawnCapture | NA | None = None
  piece_capture: PieceCapture | NA | None = None

  def without_na(self) -> Styles:
    return Styles(
      castle=no_na(self.castle), check=no_na(self.check), mate=no_na(self.mate),
      pawn_capture=no_na(self.pawn_capture), piece_capture=no_na(self.piece_capture)
    )

class Annotations(BaseModel):
  language: Language | NA | None = None
  styles: StylesNA | None = None
  end_correct: int | None = None
  manual_labels: dict[int, str] | None = None

  @property
  def language_no_na(self) -> Language | None:
    if self.language != 'N/A':
      return self.language

AnnotationSchemas = dict(
  language=RootModel[Language],
  style=StylesNA,
  end_correct=RootModel[int],
  manual_labels=RootModel[dict[int, str]]
)
