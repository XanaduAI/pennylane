import os

import numpy as np
import pennylane as qml
import pytest
from openfermion.ops._qubit_operator import QubitOperator

from pennylane import qchem


@pytest.mark.parametrize(
    ("mol_name", "terms_ref"),
    [
        ("empty", None),
        (
            "lih [jordan_WIGNER]",
            {
                (): (-7.50915719389077 + 0j),
                ((0, "Z"),): (0.155924093421341 + 0j),
                ((0, "Y"), (1, "Z"), (2, "Y")): (0.01401593800246412 + 0j),
                ((0, "X"), (1, "Z"), (2, "X")): (0.01401593800246412 + 0j),
                ((1, "Z"),): (0.1559240934213409 + 0j),
                ((1, "Y"), (2, "Z"), (3, "Y")): (0.014015938002464118 + 0j),
                ((1, "X"), (2, "Z"), (3, "X")): (0.014015938002464118 + 0j),
                ((2, "Z"),): (-0.01503982573626933 + 0j),
                ((3, "Z"),): (-0.015039825736269333 + 0j),
                ((0, "Z"), (1, "Z")): (0.12182774218528421 + 0j),
                ((0, "Y"), (2, "Y")): (0.012144893851836855 + 0j),
                ((0, "X"), (2, "X")): (0.012144893851836855 + 0j),
                ((0, "Z"), (1, "Y"), (2, "Z"), (3, "Y")): (0.012144893851836855 + 0j),
                ((0, "Z"), (1, "X"), (2, "Z"), (3, "X")): (0.012144893851836855 + 0j),
                ((0, "Y"), (1, "X"), (2, "X"), (3, "Y")): (0.00326599398593671 + 0j),
                ((0, "Y"), (1, "Y"), (2, "X"), (3, "X")): (-0.00326599398593671 + 0j),
                ((0, "X"), (1, "X"), (2, "Y"), (3, "Y")): (-0.00326599398593671 + 0j),
                ((0, "X"), (1, "Y"), (2, "Y"), (3, "X")): (0.00326599398593671 + 0j),
                ((0, "Z"), (2, "Z")): (0.052636515240899254 + 0j),
                ((0, "Z"), (3, "Z")): (0.05590250922683597 + 0j),
                ((0, "Y"), (1, "Z"), (2, "Y"), (3, "Z")): (-0.0018710418360866883 + 0j),
                ((0, "X"), (1, "Z"), (2, "X"), (3, "Z")): (-0.0018710418360866883 + 0j),
                ((1, "Z"), (2, "Z")): (0.05590250922683597 + 0j),
                ((1, "Y"), (3, "Y")): (-0.0018710418360866883 + 0j),
                ((1, "X"), (3, "X")): (-0.0018710418360866883 + 0j),
                ((1, "Z"), (3, "Z")): (0.052636515240899254 + 0j),
                ((2, "Z"), (3, "Z")): (0.08447056917218312 + 0j),
            },
        ),
        (
            "lih [BRAVYI_kitaev]",
            {
                (): (-7.50915719389077 + 0j),
                ((0, "Z"),): (0.155924093421341 + 0j),
                ((0, "X"), (1, "Y"), (2, "Y")): (0.01401593800246412 + 0j),
                ((0, "Y"), (1, "Y"), (2, "X")): (-0.01401593800246412 + 0j),
                ((0, "Z"), (1, "Z")): (0.1559240934213409 + 0j),
                ((0, "Z"), (1, "X"), (3, "Z")): (-0.014015938002464118 + 0j),
                ((1, "X"), (2, "Z")): (0.014015938002464118 + 0j),
                ((2, "Z"),): (-0.01503982573626933 + 0j),
                ((1, "Z"), (2, "Z"), (3, "Z")): (-0.015039825736269333 + 0j),
                ((1, "Z"),): (0.12182774218528421 + 0j),
                ((0, "Y"), (1, "X"), (2, "Y")): (0.012144893851836855 + 0j),
                ((0, "X"), (1, "X"), (2, "X")): (0.012144893851836855 + 0j),
                ((1, "X"), (3, "Z")): (-0.012144893851836855 + 0j),
                ((0, "Z"), (1, "X"), (2, "Z")): (0.012144893851836855 + 0j),
                ((0, "Y"), (1, "Z"), (2, "Y"), (3, "Z")): (0.00326599398593671 + 0j),
                ((0, "X"), (1, "Z"), (2, "X")): (0.00326599398593671 + 0j),
                ((0, "X"), (1, "Z"), (2, "X"), (3, "Z")): (0.00326599398593671 + 0j),
                ((0, "Y"), (1, "Z"), (2, "Y")): (0.00326599398593671 + 0j),
                ((0, "Z"), (2, "Z")): (0.052636515240899254 + 0j),
                ((0, "Z"), (1, "Z"), (2, "Z"), (3, "Z")): (0.05590250922683597 + 0j),
                ((0, "X"), (1, "X"), (2, "X"), (3, "Z")): (0.0018710418360866883 + 0j),
                ((0, "Y"), (1, "X"), (2, "Y"), (3, "Z")): (0.0018710418360866883 + 0j),
                ((0, "Z"), (1, "Z"), (2, "Z")): (0.05590250922683597 + 0j),
                ((0, "Z"), (1, "X"), (2, "Z"), (3, "Z")): (0.0018710418360866883 + 0j),
                ((1, "X"),): (-0.0018710418360866883 + 0j),
                ((0, "Z"), (2, "Z"), (3, "Z")): (0.052636515240899254 + 0j),
                ((1, "Z"), (3, "Z")): (0.08447056917218312 + 0j),
            },
        ),
        (
            "h2_psycf [jordan_WIGNER]",
            {
                (): (-0.04207897647782188 + 0j),
                ((0, "Z"),): (0.17771287465139934 + 0j),
                ((1, "Z"),): (0.1777128746513993 + 0j),
                ((2, "Z"),): (-0.24274280513140484 + 0j),
                ((3, "Z"),): (-0.24274280513140484 + 0j),
                ((0, "Z"), (1, "Z")): (0.17059738328801055 + 0j),
                ((0, "Y"), (1, "X"), (2, "X"), (3, "Y")): (0.04475014401535161 + 0j),
                ((0, "Y"), (1, "Y"), (2, "X"), (3, "X")): (-0.04475014401535161 + 0j),
                ((0, "X"), (1, "X"), (2, "Y"), (3, "Y")): (-0.04475014401535161 + 0j),
                ((0, "X"), (1, "Y"), (2, "Y"), (3, "X")): (0.04475014401535161 + 0j),
                ((0, "Z"), (2, "Z")): (0.12293305056183801 + 0j),
                ((0, "Z"), (3, "Z")): (0.1676831945771896 + 0j),
                ((1, "Z"), (2, "Z")): (0.1676831945771896 + 0j),
                ((1, "Z"), (3, "Z")): (0.12293305056183801 + 0j),
                ((2, "Z"), (3, "Z")): (0.176276408043196 + 0j),
            },
        ),
        (
            "h2_psycf [BRAVYI_kitaev]",
            {
                (): (-0.04207897647782188 + 0j),
                ((0, "Z"),): (0.17771287465139934 + 0j),
                ((0, "Z"), (1, "Z")): (0.1777128746513993 + 0j),
                ((2, "Z"),): (-0.24274280513140484 + 0j),
                ((1, "Z"), (2, "Z"), (3, "Z")): (-0.24274280513140484 + 0j),
                ((1, "Z"),): (0.17059738328801055 + 0j),
                ((0, "Y"), (1, "Z"), (2, "Y"), (3, "Z")): (0.04475014401535161 + 0j),
                ((0, "X"), (1, "Z"), (2, "X")): (0.04475014401535161 + 0j),
                ((0, "X"), (1, "Z"), (2, "X"), (3, "Z")): (0.04475014401535161 + 0j),
                ((0, "Y"), (1, "Z"), (2, "Y")): (0.04475014401535161 + 0j),
                ((0, "Z"), (2, "Z")): (0.12293305056183801 + 0j),
                ((0, "Z"), (1, "Z"), (2, "Z"), (3, "Z")): (0.1676831945771896 + 0j),
                ((0, "Z"), (1, "Z"), (2, "Z")): (0.1676831945771896 + 0j),
                ((0, "Z"), (2, "Z"), (3, "Z")): (0.12293305056183801 + 0j),
                ((1, "Z"), (3, "Z")): (0.176276408043196 + 0j),
            },
        ),
        (
            "h2o_psi4 [jordan_WIGNER]",
            {
                (): (-73.3320453921657 + 0j),
                ((0, "Z"),): (0.5152794751801038 + 0j),
                ((0, "Y"), (1, "Z"), (2, "Z"), (3, "Z"), (4, "Y")): (0.07778754984633934 + 0j),
                ((0, "X"), (1, "Z"), (2, "Z"), (3, "Z"), (4, "X")): (0.07778754984633934 + 0j),
                ((1, "Z"),): (0.515279475180104 + 0j),
                ((1, "Y"), (2, "Z"), (3, "Z"), (4, "Z"), (5, "Y")): (0.07778754984633934 + 0j),
                ((1, "X"), (2, "Z"), (3, "Z"), (4, "Z"), (5, "X")): (0.07778754984633934 + 0j),
                ((2, "Z"),): (0.4812925883672432 + 0j),
                ((3, "Z"),): (0.48129258836724326 + 0j),
                ((4, "Z"),): (0.09030949181042286 + 0j),
                ((5, "Z"),): (0.09030949181042283 + 0j),
                ((0, "Z"), (1, "Z")): (0.1956590715408106 + 0j),
                ((0, "Y"), (2, "Z"), (3, "Z"), (4, "Y")): (0.030346614024840804 + 0j),
                ((0, "X"), (2, "Z"), (3, "Z"), (4, "X")): (0.030346614024840804 + 0j),
                ((0, "Y"), (1, "X"), (2, "X"), (3, "Y")): (0.013977596555816168 + 0j),
                ((0, "Y"), (1, "Y"), (2, "X"), (3, "X")): (-0.013977596555816168 + 0j),
                ((0, "X"), (1, "X"), (2, "Y"), (3, "Y")): (-0.013977596555816168 + 0j),
                ((0, "X"), (1, "Y"), (2, "Y"), (3, "X")): (0.013977596555816168 + 0j),
                ((0, "Z"), (1, "Y"), (2, "Z"), (3, "Z"), (4, "Z"), (5, "Y")): (
                    0.030346614024840804 + 0j
                ),
                ((0, "Z"), (1, "X"), (2, "Z"), (3, "Z"), (4, "Z"), (5, "X")): (
                    0.030346614024840804 + 0j
                ),
                ((0, "Y"), (1, "X"), (4, "X"), (5, "Y")): (0.01718525123891425 + 0j),
                ((0, "Y"), (1, "Y"), (4, "X"), (5, "X")): (-0.01718525123891425 + 0j),
                ((0, "X"), (1, "X"), (4, "Y"), (5, "Y")): (-0.01718525123891425 + 0j),
                ((0, "X"), (1, "Y"), (4, "Y"), (5, "X")): (0.01718525123891425 + 0j),
                ((0, "Z"), (2, "Z")): (0.16824174504299702 + 0j),
                ((0, "Y"), (1, "Z"), (3, "Z"), (4, "Y")): (0.029512711807110188 + 0j),
                ((0, "X"), (1, "Z"), (3, "Z"), (4, "X")): (0.029512711807110188 + 0j),
                ((0, "Z"), (3, "Z")): (0.18221934159881317 + 0j),
                ((0, "Y"), (1, "Z"), (2, "Z"), (4, "Y")): (0.029077593893863385 + 0j),
                ((0, "X"), (1, "Z"), (2, "Z"), (4, "X")): (0.029077593893863385 + 0j),
                ((0, "Y"), (1, "Z"), (2, "Y"), (3, "Y"), (4, "Z"), (5, "Y")): (
                    0.00043511791324680473 + 0j
                ),
                ((0, "Y"), (1, "Z"), (2, "Y"), (3, "X"), (4, "Z"), (5, "X")): (
                    0.00043511791324680473 + 0j
                ),
                ((0, "X"), (1, "Z"), (2, "X"), (3, "Y"), (4, "Z"), (5, "Y")): (
                    0.00043511791324680473 + 0j
                ),
                ((0, "X"), (1, "Z"), (2, "X"), (3, "X"), (4, "Z"), (5, "X")): (
                    0.00043511791324680473 + 0j
                ),
                ((0, "Z"), (4, "Z")): (0.12008313883007578 + 0j),
                ((0, "Z"), (5, "Z")): (0.13726839006899005 + 0j),
                ((0, "Y"), (1, "Z"), (2, "Z"), (3, "Z"), (4, "Y"), (5, "Z")): (
                    0.011149373109704066 + 0j
                ),
                ((0, "X"), (1, "Z"), (2, "Z"), (3, "Z"), (4, "X"), (5, "Z")): (
                    0.011149373109704066 + 0j
                ),
                ((1, "Z"), (2, "Z")): (0.18221934159881317 + 0j),
                ((1, "Y"), (3, "Z"), (4, "Z"), (5, "Y")): (0.029077593893863385 + 0j),
                ((1, "X"), (3, "Z"), (4, "Z"), (5, "X")): (0.029077593893863385 + 0j),
                ((1, "Y"), (2, "X"), (3, "X"), (4, "Y")): (0.00043511791324680484 + 0j),
                ((1, "Y"), (2, "Y"), (3, "X"), (4, "X")): (-0.00043511791324680484 + 0j),
                ((1, "X"), (2, "X"), (3, "Y"), (4, "Y")): (-0.00043511791324680484 + 0j),
                ((1, "X"), (2, "Y"), (3, "Y"), (4, "X")): (0.00043511791324680484 + 0j),
                ((1, "Z"), (3, "Z")): (0.16824174504299702 + 0j),
                ((1, "Y"), (2, "Z"), (4, "Z"), (5, "Y")): (0.029512711807110188 + 0j),
                ((1, "X"), (2, "Z"), (4, "Z"), (5, "X")): (0.029512711807110188 + 0j),
                ((1, "Z"), (4, "Z")): (0.13726839006899005 + 0j),
                ((1, "Y"), (2, "Z"), (3, "Z"), (5, "Y")): (0.011149373109704066 + 0j),
                ((1, "X"), (2, "Z"), (3, "Z"), (5, "X")): (0.011149373109704066 + 0j),
                ((1, "Z"), (5, "Z")): (0.12008313883007578 + 0j),
                ((2, "Z"), (3, "Z")): (0.22003977334376118 + 0j),
                ((2, "Y"), (3, "X"), (4, "X"), (5, "Y")): (0.009647475282106617 + 0j),
                ((2, "Y"), (3, "Y"), (4, "X"), (5, "X")): (-0.009647475282106617 + 0j),
                ((2, "X"), (3, "X"), (4, "Y"), (5, "Y")): (-0.009647475282106617 + 0j),
                ((2, "X"), (3, "Y"), (4, "Y"), (5, "X")): (0.009647475282106617 + 0j),
                ((2, "Z"), (4, "Z")): (0.13758959215600186 + 0j),
                ((2, "Z"), (5, "Z")): (0.1472370674381085 + 0j),
                ((3, "Z"), (4, "Z")): (0.1472370674381085 + 0j),
                ((3, "Z"), (5, "Z")): (0.13758959215600186 + 0j),
                ((4, "Z"), (5, "Z")): (0.1492827559305538 + 0j),
            },
        ),
        (
            "h2o_psi4 [BRAVYI_kitaev]",
            {
                (): (-73.3320453921657 + 0j),
                ((0, "Z"),): (0.5152794751801038 + 0j),
                ((0, "X"), (1, "X"), (3, "Y"), (4, "Y"), (5, "X")): (0.07778754984633934 + 0j),
                ((0, "Y"), (1, "X"), (3, "Y"), (4, "X"), (5, "X")): (-0.07778754984633934 + 0j),
                ((0, "Z"), (1, "Z")): (0.515279475180104 + 0j),
                ((0, "Z"), (1, "X"), (3, "Y"), (5, "Y")): (0.07778754984633934 + 0j),
                ((1, "Y"), (3, "Y"), (4, "Z"), (5, "X")): (-0.07778754984633934 + 0j),
                ((2, "Z"),): (0.4812925883672432 + 0j),
                ((1, "Z"), (2, "Z"), (3, "Z")): (0.48129258836724326 + 0j),
                ((4, "Z"),): (0.09030949181042286 + 0j),
                ((4, "Z"), (5, "Z")): (0.09030949181042283 + 0j),
                ((1, "Z"),): (0.1956590715408106 + 0j),
                ((0, "Y"), (1, "Y"), (3, "Y"), (4, "Y"), (5, "X")): (-0.030346614024840804 + 0j),
                ((0, "X"), (1, "Y"), (3, "Y"), (4, "X"), (5, "X")): (-0.030346614024840804 + 0j),
                ((0, "Y"), (1, "Z"), (2, "Y"), (3, "Z")): (0.013977596555816168 + 0j),
                ((0, "X"), (1, "Z"), (2, "X")): (0.013977596555816168 + 0j),
                ((0, "X"), (1, "Z"), (2, "X"), (3, "Z")): (0.013977596555816168 + 0j),
                ((0, "Y"), (1, "Z"), (2, "Y")): (0.013977596555816168 + 0j),
                ((1, "X"), (3, "Y"), (5, "Y")): (0.030346614024840804 + 0j),
                ((0, "Z"), (1, "Y"), (3, "Y"), (4, "Z"), (5, "X")): (-0.030346614024840804 + 0j),
                ((0, "Y"), (4, "Y"), (5, "Z")): (0.01718525123891425 + 0j),
                ((0, "X"), (1, "Z"), (4, "X")): (0.01718525123891425 + 0j),
                ((0, "X"), (4, "X"), (5, "Z")): (0.01718525123891425 + 0j),
                ((0, "Y"), (1, "Z"), (4, "Y")): (0.01718525123891425 + 0j),
                ((0, "Z"), (2, "Z")): (0.16824174504299702 + 0j),
                ((0, "X"), (1, "X"), (2, "Z"), (3, "Y"), (4, "Y"), (5, "X")): (
                    0.029512711807110188 + 0j
                ),
                ((0, "Y"), (1, "X"), (2, "Z"), (3, "Y"), (4, "X"), (5, "X")): (
                    -0.029512711807110188 + 0j
                ),
                ((0, "Z"), (1, "Z"), (2, "Z"), (3, "Z")): (0.18221934159881317 + 0j),
                ((0, "X"), (1, "Y"), (2, "Z"), (3, "X"), (4, "Y"), (5, "X")): (
                    0.029077593893863385 + 0j
                ),
                ((0, "Y"), (1, "Y"), (2, "Z"), (3, "X"), (4, "X"), (5, "X")): (
                    -0.029077593893863385 + 0j
                ),
                ((0, "X"), (1, "X"), (2, "X"), (3, "Y"), (5, "Y")): (-0.00043511791324680473 + 0j),
                ((0, "X"), (1, "Y"), (2, "Y"), (3, "X"), (4, "Z"), (5, "X")): (
                    0.00043511791324680473 + 0j
                ),
                ((0, "Y"), (1, "X"), (2, "Y"), (3, "Y"), (5, "Y")): (-0.00043511791324680473 + 0j),
                ((0, "Y"), (1, "Y"), (2, "X"), (3, "X"), (4, "Z"), (5, "X")): (
                    -0.00043511791324680473 + 0j
                ),
                ((0, "Z"), (4, "Z")): (0.12008313883007578 + 0j),
                ((0, "Z"), (4, "Z"), (5, "Z")): (0.13726839006899005 + 0j),
                ((0, "X"), (1, "X"), (3, "Y"), (4, "X"), (5, "Y")): (0.011149373109704066 + 0j),
                ((0, "Y"), (1, "X"), (3, "Y"), (4, "Y"), (5, "Y")): (0.011149373109704066 + 0j),
                ((0, "Z"), (1, "Z"), (2, "Z")): (0.18221934159881317 + 0j),
                ((0, "Z"), (1, "X"), (2, "Z"), (3, "Y"), (5, "Y")): (0.029077593893863385 + 0j),
                ((1, "Y"), (2, "Z"), (3, "Y"), (4, "Z"), (5, "X")): (-0.029077593893863385 + 0j),
                ((0, "Z"), (1, "Y"), (2, "X"), (3, "X"), (4, "Y"), (5, "X")): (
                    0.00043511791324680484 + 0j
                ),
                ((0, "Z"), (1, "Y"), (2, "Y"), (3, "X"), (4, "X"), (5, "X")): (
                    -0.00043511791324680484 + 0j
                ),
                ((1, "Y"), (2, "Y"), (3, "Y"), (4, "Y"), (5, "X")): (0.00043511791324680484 + 0j),
                ((1, "Y"), (2, "X"), (3, "Y"), (4, "X"), (5, "X")): (0.00043511791324680484 + 0j),
                ((0, "Z"), (2, "Z"), (3, "Z")): (0.16824174504299702 + 0j),
                ((0, "Z"), (1, "Y"), (2, "Z"), (3, "X"), (5, "Y")): (0.029512711807110188 + 0j),
                ((1, "X"), (2, "Z"), (3, "X"), (4, "Z"), (5, "X")): (0.029512711807110188 + 0j),
                ((0, "Z"), (1, "Z"), (4, "Z")): (0.13726839006899005 + 0j),
                ((0, "Z"), (1, "X"), (3, "Y"), (4, "Z"), (5, "Y")): (0.011149373109704066 + 0j),
                ((1, "Y"), (3, "Y"), (5, "X")): (-0.011149373109704066 + 0j),
                ((0, "Z"), (1, "Z"), (4, "Z"), (5, "Z")): (0.12008313883007578 + 0j),
                ((1, "Z"), (3, "Z")): (0.22003977334376118 + 0j),
                ((2, "Y"), (4, "Y"), (5, "Z")): (0.009647475282106617 + 0j),
                ((1, "Z"), (2, "X"), (3, "Z"), (4, "X")): (0.009647475282106617 + 0j),
                ((2, "X"), (4, "X"), (5, "Z")): (0.009647475282106617 + 0j),
                ((1, "Z"), (2, "Y"), (3, "Z"), (4, "Y")): (0.009647475282106617 + 0j),
                ((2, "Z"), (4, "Z")): (0.13758959215600186 + 0j),
                ((2, "Z"), (4, "Z"), (5, "Z")): (0.1472370674381085 + 0j),
                ((1, "Z"), (2, "Z"), (3, "Z"), (4, "Z")): (0.1472370674381085 + 0j),
                ((1, "Z"), (2, "Z"), (3, "Z"), (4, "Z"), (5, "Z")): (0.13758959215600186 + 0j),
                ((5, "Z"),): (0.1492827559305538 + 0j),
            },
        ),
    ],
)
def test_load_hamiltonian(mol_name, terms_ref, monkeypatch):

    r"""Test the correctness of the QubitOperator Hamiltonian conversion from
    OpenFermion to Pennylane.

    The parametrized inputs are `.terms` attribute of the output `QubitOperator`s based on
    the same set of test molecules as `test_gen_hamiltonian_pauli_basis`.

    The equality checking is implemented in the `qchem` module itself as it could be
    something useful to the users as well.
    """
    qOp = QubitOperator()
    if terms_ref is not None:
        monkeypatch.setattr(qOp, "terms", terms_ref)

    vqe_hamiltonian = qchem.load_hamiltonian(qOp)

    assert qchem._qubit_operators_equivalent(qOp, vqe_hamiltonian)


def test_not_xyz_terms_to_qubit_operator():
    r"""Test if the conversion complains about non Pauli matrix observables"""
    with pytest.raises(
        ValueError,
        match="Expected only PennyLane observables PauliX/Y/Z or Identity, but also got {"
        "'QuadOperator'}.",
    ):
        qchem._terms_to_qubit_operator(
            np.array([0.1 + 0.0j, 0.0]),
            [
                qml.operation.Tensor(qml.PauliX(0)),
                qml.operation.Tensor(qml.PauliZ(0), qml.QuadOperator(0.1, wires=1)),
            ],
        )


@pytest.mark.parametrize(
    ("mol_name", "terms_ref", "expected_cost"),
    [
        ("empty", None, 0),
        (
            "h2_psycf [jordan_WIGNER]",
            {
                (): (-0.04207897647782188 + 0j),
                ((0, "Z"),): (0.17771287465139934 + 0j),
                ((1, "Z"),): (0.1777128746513993 + 0j),
                ((2, "Z"),): (-0.24274280513140484 + 0j),
                ((3, "Z"),): (-0.24274280513140484 + 0j),
                ((0, "Z"), (1, "Z")): (0.17059738328801055 + 0j),
                ((0, "Y"), (1, "X"), (2, "X"), (3, "Y")): (0.04475014401535161 + 0j),
                ((0, "Y"), (1, "Y"), (2, "X"), (3, "X")): (-0.04475014401535161 + 0j),
                ((0, "X"), (1, "X"), (2, "Y"), (3, "Y")): (-0.04475014401535161 + 0j),
                ((0, "X"), (1, "Y"), (2, "Y"), (3, "X")): (0.04475014401535161 + 0j),
                ((0, "Z"), (2, "Z")): (0.12293305056183801 + 0j),
                ((0, "Z"), (3, "Z")): (0.1676831945771896 + 0j),
                ((1, "Z"), (2, "Z")): (0.1676831945771896 + 0j),
                ((1, "Z"), (3, "Z")): (0.12293305056183801 + 0j),
                ((2, "Z"), (3, "Z")): (0.176276408043196 + 0j),
            },
            (0.7384971473437577 + 0j),
        ),
    ],
)
def test_integration_hamiltonian_to_vqe_cost(monkeypatch, mol_name, terms_ref, expected_cost):
    r"""Test if `load_hamiltonian()` in qchem integrates with `vqe.cost()` in pennylane"""

    qOp = QubitOperator()
    if terms_ref is not None:
        monkeypatch.setattr(qOp, "terms", terms_ref)
    vqe_hamiltonian = qchem.load_hamiltonian(qOp)

    # maybe make num_qubits a @property of the Hamiltonian class?
    num_qubits = max(1, len(set([w for op in vqe_hamiltonian.ops for ws in op.wires for w in ws])))

    dev = qml.device("default.qubit", wires=num_qubits)
    print(vqe_hamiltonian.terms)

    # can replace the ansatz with more suitable ones later.
    def dummy_ansatz(*phis, wires):
        for phi, w in zip(phis, wires):
            qml.RX(phi, wires=w)

    dummy_cost = qml.beta.vqe.cost(
        [0.1 * i for i in range(num_qubits)], dummy_ansatz, vqe_hamiltonian, dev
    )

    assert dummy_cost == expected_cost


@pytest.mark.parametrize(
    ("hf_filename", "docc_mo", "act_mo", "type_of_transformation", "expected_cost"),
    [
        ("lih", [0], [1, 2], "jordan_WIGNER", -7.255500051039507),
        ("lih", [0], [1, 2], "BRAVYI_kitaev", -7.246409364088741),
        ("h2_pyscf", list(range(0)), list(range(2)), "jordan_WIGNER", 0.19364907363263958),
        ("h2_pyscf", list(range(0)), list(range(2)), "BRAVYI_kitaev", 0.16518000728327564),
        ("gdb3", list(range(11)), [11, 12], "jordan_WIGNER", -130.59816885313248),
        ("gdb3", list(range(11)), [11, 12], "BRAVYI_kitaev", -130.6156540164148),
    ],
)
def test_integration_mol_file_to_vqe_cost(
    hf_filename, docc_mo, act_mo, type_of_transformation, expected_cost, tol
):
    r"""Test if the output of `gen_hamiltonian_pauli_basis()` works with `load_hamiltonian()`
    to generate `vqe.cost()`"""
    ref_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_ref_files")

    transformed_hamiltonian = qchem.gen_hamiltonian_pauli_basis(
        hf_filename,
        ref_dir,
        mapping=type_of_transformation,
        docc_mo_indices=docc_mo,
        active_mo_indices=act_mo,
    )

    vqe_hamiltonian = qchem.load_hamiltonian(transformed_hamiltonian)
    assert len(vqe_hamiltonian.ops) > 1  # just to check if this runs

    num_qubits = max(1, len(set([w for op in vqe_hamiltonian.ops for ws in op.wires for w in ws])))
    assert num_qubits == 2 * len(act_mo)

    dev = qml.device("default.qubit", wires=num_qubits)

    # can replace the ansatz with more suitable ones later.
    def dummy_ansatz(*phis, wires):
        for phi, w in zip(phis, wires):
            qml.RX(phi, wires=w)

    phis = np.load(os.path.join(ref_dir, "dummy_ansatz_parameters.npy"))

    dummy_cost = qml.beta.vqe.cost(phis, dummy_ansatz, vqe_hamiltonian, dev)

    assert np.abs(dummy_cost - expected_cost) < tol["atol"]