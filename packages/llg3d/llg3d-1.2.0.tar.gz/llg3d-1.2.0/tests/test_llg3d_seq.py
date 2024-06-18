"""A comprehensive testing of the llg3d_seq module"""

import os
import shutil
from pathlib import Path

import pytest

from llg3d import llg3d_seq

this_dir = Path(__file__).resolve().parent


@pytest.fixture
def run_args(tmp_path):
    os.chdir(tmp_path)
    shutil.copy(this_dir / "m1_integral_space_T1100_300x11x11_ref.txt", tmp_path)
    args = {k: v[0] for k, v in llg3d_seq.parameters.items()}
    return args


def test_llg3d_seq_Cobalt(run_args):
    N = 500
    run_args["element"] = llg3d_seq.Cobalt
    run_args["Jy"] = 11
    run_args["Jz"] = 11
    run_args["N"] = N
    grid, _ = llg3d_seq.simulate(**run_args)
    # Comparison with reference solution should succeed
    assert llg3d_seq.check_solution(grid, run_args["T"])


def test_llg3d_seq_Iron(run_args):
    run_args["element"] = llg3d_seq.Iron
    run_args["Jy"] = 11
    run_args["Jz"] = 11
    run_args["N"] = 100
    grid, _ = llg3d_seq.simulate(**run_args)
    # Comparison with reference solution (Cobalt) should fail
    assert not llg3d_seq.check_solution(grid, run_args["T"])


def test_parse_args():
    args = llg3d_seq.parse_args(["-N", "100"])
    assert args.N == 100


def test_main(run_args):
    llg3d_seq.main(["-N", "10", "-element", "Iron"])
    llg3d_seq.main(["-N", "100", "-Jy", "11", "-Jz", "11", "-element", "Cobalt", "-c"])
