# Moveread Labels

> Annotating and exporting labels

## Usage

```python
import moveread.labels as lab

ann = lab.Annotations(language='DE', styles=lab.StylesNA(pawn_capture='de', piece_capture='NxN'))
lab.export(['e4', 'e5', 'Nf3', 'Nc6', 'd4', 'exd4', 'Nxd4', 'Nf6', 'Nxc6', 'bxc6'], ann)
# Right(value=['e4', 'e5', 'Sf3', 'Sc6', 'd4', 'ed', 'SxB', 'Sf6', 'SxS', 'bc'])

lab.export(['e4', 'e4'], ann)
# Left(value=IllegalMoveError("illegal san: 'e4' in rnbqkbnr/[...]"))
```