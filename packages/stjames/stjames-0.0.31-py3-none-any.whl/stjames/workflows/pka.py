from typing import Optional

from ..base import Base
from .workflow import DBCalculation, Workflow


class pKaMicrostate(Base):
    atom_index: int
    structures: list[DBCalculation] = []
    delta_G: float
    pKa: float


class pKaWorkflow(Workflow):
    pka_range: tuple[float, float] = (2, 12)
    deprotonate_elements: list[int] = [7, 8, 16]
    deprotonate_atoms: list[int] = []
    protonate_elements: list[int] = [7]
    protonate_atoms: list[int] = []

    reasonableness_buffer: float = 5

    structures: list[DBCalculation] = []
    conjugate_acids: list[pKaMicrostate] = []
    conjugate_bases: list[pKaMicrostate] = []
    strongest_acid: Optional[float] = None
    strongest_base: Optional[float] = None
