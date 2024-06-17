"""Pybind11 Bindings for SCINE Swoose"""
import scine_swoose
import typing
from typing import Union
import scine_utilities
import scine_utilities.core

__all__ = [
    "Parametrizer",
    "QmRegionSelector",
    "calculate_mm",
    "calculate_qmmm",
    "md_simulate_mm",
    "md_simulate_qmmm",
    "optimize_mm",
    "optimize_qmmm",
    "parametrize",
    "prepare_analyze",
    "prepare_finalize",
    "prepare_protonate",
    "select_qm_region",
    "topology_utilities",
    "utilities"
]


class Parametrizer():
    def __init__(self) -> None: 
        """
                                Initialize the Parametrizer object.
                              
        """
    def parametrize_mm(self, structure: scine_utilities.AtomCollection) -> None: 
        """
                                   Perform an MM parametrization.
                                   :param structure: The initial molecular structure for the simulation.
                                 
        """
    @property
    def log(self) -> scine_utilities.core.Log:
        """
        Logger of the MM parametrizer.

        :type: scine_utilities.core.Log
        """
    @log.setter
    def log(self, arg1: scine_utilities.core.Log) -> None:
        """
        Logger of the MM parametrizer.
        """
    @property
    def settings(self) -> scine_utilities.Settings:
        """
        Settings of the mm parametrizer.

        :type: scine_utilities.Settings
        """
    @settings.setter
    def settings(self, arg1: scine_utilities.Settings) -> None:
        """
        Settings of the mm parametrizer.
        """
    pass
class QmRegionSelector():
    def __init__(self) -> None: 
        """
                                Initialize the QmRegionSelector object.
                              
        """
    def generate_qm_region(self, structure: scine_utilities.AtomCollection) -> None: 
        """
                                   Generates a (spherical) QM region around a central atom.
                                   :param structure: The initial molecular structure.
                                 
        """
    def get_qm_region_charge_multiplicity(self) -> typing.Tuple[int, int]: 
        """
                                   Getter for the atom indices of the generated QM region.
                                   :return A pair of charge and multiplicity for the QM region.
                                 
        """
    def get_qm_region_indices(self) -> typing.List[int]: 
        """
                                   Getter for the atom indices of the generated QM region.
                                   :return A list of QM region indices.
                                 
        """
    def get_qm_region_structure(self) -> scine_utilities.AtomCollection: 
        """
                                   Getter for the structure of the generated QM region.
                                   :return The QM region structure.
                                 
        """
    def set_underlying_calculator(self, qmmmCalculator: scine_utilities.core.Calculator) -> None: 
        """
                                   Sets the underlying calculator for the QM region selection task.
                                   :param structure: The QMMM calculator.
                                 
        """
    @property
    def settings(self) -> scine_utilities.Settings:
        """
        Settings of the qm region selector.

        :type: scine_utilities.Settings
        """
    @settings.setter
    def settings(self, arg1: scine_utilities.Settings) -> None:
        """
        Settings of the qm region selector.
        """
    pass
class topology_utilities():
    @staticmethod
    def generate_lists_of_neighbors(natoms: int, bond_order_matrix: scine_utilities.BondOrderCollection, minimal_bond_order_to_consider: float = 0.5) -> typing.List[typing.List[int]]: ...
    pass
class utilities():
    @staticmethod
    def write_connectivity_file(filename: str, lists_of_neighbors: typing.List[typing.List[int]]) -> None: ...
    pass
def calculate_mm(structure_file: str, **kwargs) -> None:
    """
    Calculation with a molecular mechanics model. Settings can be set as keyword arguments.
    """
def calculate_qmmm(structure_file: str, **kwargs) -> None:
    """
    Calculation with the QM/MM hybrid model. Settings can be set as keyword arguments.
    """
def md_simulate_mm(structure_file: str, **kwargs) -> None:
    """
    Molecular dynamics simulation with a molecular mechanics model. Settings can be set as keyword arguments.
    """
def md_simulate_qmmm(structure_file: str, **kwargs) -> None:
    """
    Molecular dynamics simulation with a QM/MM model. Settings can be set as keyword arguments.
    """
def optimize_mm(structure_file: str, **kwargs) -> None:
    """
    Structure optimization with a molecular mechanics model. Settings can be set as keyword arguments.
    """
def optimize_qmmm(structure_file: str, **kwargs) -> None:
    """
    Structure optimization with the QM/MM hybrid model. Settings can be set as keyword arguments.
    """
def parametrize(structure_file: str, **kwargs) -> None:
    """
    Parametrizes the SFAM model. Settings can be set as keyword arguments.
    """
def prepare_analyze(structure_file: str, **kwargs) -> None:
    """
    Analyzes a given input structure. Settings can be set as keyword arguments.
    """
def prepare_finalize(structure_file: str, **kwargs) -> None:
    """
    Merges the substructures and generates Atomic Info File. Settings can be set as keyword arguments. 
    """
def prepare_protonate(structure_file: str, **kwargs) -> None:
    """
    Protonates protein and nonRegContainer separately. Settings can be set as keyword arguments.
    """
def select_qm_region(structure_file: str, **kwargs) -> None:
    """
    Automated QM region selection. Settings can be set as keyword arguments.
    """
