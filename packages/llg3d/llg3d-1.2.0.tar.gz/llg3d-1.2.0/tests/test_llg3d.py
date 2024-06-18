"""
For parallel tests, it is preferable to use a number of processes that is a divisor of 60 (2, 3, 6, etc.).
"""

import os
from pathlib import Path

import numpy as np
from mpi4py import MPI
from pytest import approx, mark

from llg3d import llg3d

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

this_dir = Path(__file__).resolve().parent


def test_parameter_list():
    d = {
        "element": "Cobalt",
        "blocking": False,
        "N": 500,
        "dt": 1e-14,
        "Jx": 300,
        "Jy": 21,
        "Jz": 21,
        "Lx": 3e-07,
        "Ly": 2e-08,
        "Lz": 2e-08,
        "T": 1100,
        "H_ext": 0.0,
        "n_moy": 2000,
        "n_integrale": 1,
        "n_profils": 100,
    }
    expected = """\
element     : Cobalt
blocking    = False
N           = 500
dt          = 1e-14
Jx          = 300
Jy          = 21
Jz          = 21
Lx          = 3e-07
Ly          = 2e-08
Lz          = 2e-08
T           = 1100
H_ext       = 0.0
n_moy       = 2000
n_integrale = 1
n_profils   = 100
"""
    assert llg3d.parameter_list(d) == expected


def test_get_element_class():
    assert llg3d.get_element_class("Iron") == llg3d.Iron
    assert llg3d.get_element_class("Cobalt") == llg3d.Cobalt


def test_Grid():
    g = llg3d.Grid(Jx=301, Jy=11, Jz=21, dx=2.0)

    assert g.dx == 2.0
    assert g.dy == 2.0
    assert g.dz == 2.0
    assert g.dV == 8.0
    assert g.V == 480000.0
    assert g.ntot == 301 * 11 * 21
    assert (
        g.get_filename(1234) == f"m1_integral_space_T1234_301x11x21_np{size}.txt"
    )

    g = llg3d.Grid(Jx=3 * size, Jy=3, Jz=3, dx=1.0)
    x, y, z = g.get_mesh(loc=True)
    assert x.shape == (3, 3, 3)
    assert y.shape == (3, 3, 3)
    assert z.shape == (3, 3, 3)
    xg, yg, zg = g.get_mesh(loc=False)
    assert xg.shape == (3 * size, 3, 3)
    assert yg.shape == (3 * size, 3, 3)
    assert zg.shape == (3 * size, 3, 3)


@mark.skipif(60 % size != 0, reason=f"np = {size} is not a divisor of 60")
def test_integral():
    def check_integral(m, expected):
        """Check that the mean of m is approximately equal to expected"""
        mean = llg3d.integral(g, m)
        if rank == 0:
            assert mean == expected

    g = llg3d.Grid(Jx=size * 30, Jy=4, Jz=4, dx=2.0)

    check_integral(np.zeros(g.dims), 0.0)  # zero constant field
    check_integral(np.ones(g.dims), 1.0)  # unit constant field

    # Check the integral of f(x, y, z) = x(1-x)y(1-y)z(1-z)
    # over [0, 1]x[0, 1]x[0, 1] which is 1/6**3
    g = llg3d.Grid(Jx=60, Jy=60, Jz=60, dx=1 / 59.0)

    x, y, z = g.get_mesh()
    m = x * (1 - x) * y * (1 - y) * z * (1 - z)

    check_integral(m, approx(1 / 6**3, rel=1e-3))  # 1e-3 relative tolerance


def test_integral_yz():
    def check_integral(m, expected):
        """Check that the mean of m is approximately equal to expected"""
        mean = llg3d.integral_yz(m)
        assert np.all(mean == expected)

    g = llg3d.Grid(Jx=size * 30, Jy=4, Jz=4, dx=2.0)

    check_integral(np.zeros(g.dims), np.zeros(g.dims[0]))  # zero constant field
    check_integral(np.ones(g.dims), np.ones(g.dims[0]))  # unit constant field

    # Check the integral of f(x, y, z) = x(1-x)y(1-y)z(1-z)
    # in y and z over [0, 1]x[0, 1] which is x(1-x)*1/6**2
    g = llg3d.Grid(Jx=60, Jy=60, Jz=60, dx=1 / 59.0)
    x, y, z = g.get_mesh()
    m = x * (1 - x) * y * (1 - y) * z * (1 - z)
    m_yz = llg3d.integral_yz(m)
    expected = x[:, 0, 0] * (1 - x[:, 0, 0]) * 1 / 6**2
    assert m_yz == approx(expected, rel=1e-3)


def test_profile():
    g = llg3d.Grid(Jx=60, Jy=60, Jz=60, dx=1 / 59.0)
    x, y, z = g.get_mesh()
    # m = x * (1 - x) * y * (1 - y) * z * (1 - z)
    m = y * (1 - y) * z * (1 - z)
    m_xprof = np.zeros(g.Jx)  # global coordinates
    llg3d.profile(m, m_xprof)
    # expected = x[:, 0, 0] * (1 - x[:, 0, 0]) * 1/6**2
    expected = np.ones(g.Jx) * 1 / 6**2
    if rank == 0:
        assert m_xprof == approx(expected, rel=1e-3)


def laplacian(g, m):
    class E:
        """Mockup class for Element"""

        coeff_1 = 1.0

    boundaries = llg3d.get_boundaries_x(g, m)
    laplacian = llg3d.calculate_laplacian(E(), g, m, *boundaries)
    return laplacian


@mark.skipif(600 % size != 0, reason=f"np = {size} is not a divisor of 600")
def test_calculate_laplacian():
    g = llg3d.Grid(Jx=300, Jy=11, Jz=11, dx=1.0)

    # Laplacian of a zero field is zero
    m = np.zeros((g.Jx, g.Jy, g.Jz))

    assert laplacian(g, m).all() == 0.0

    # Laplacian of a constant field is zero
    m = np.ones((g.Jx, g.Jy, g.Jz))

    assert laplacian(g, m).all() == 0.0


@mark.skipif(60 % size != 0, reason=f"np = {size} is not a divisor of 60")
def test_heat_1d():
    """
    We test the Laplacian by solving the unsteady 1D heat equation.
    The initial condition is m(x, t=0) = cos(2πx)
    and the boundary condition is zero flux.
    The analytical solution is m(x, t) = cos(2πx) * exp(-4π²t).
    """
    g = llg3d.Grid(Jx=60, Jy=20, Jz=20, dx=1 / 59.0)

    x, _, _ = g.get_mesh(loc=True)  # Get local x
    xg, _, _ = g.get_mesh(loc=False)  # Get global x

    # Create global buffers
    mg = np.empty_like(xg)
    mg_ana = np.empty_like(mg)

    # Initial conditions
    m = np.cos(2 * np.pi * x)
    m_0 = m.copy()

    dx = min(g.dx, g.dy, g.dz)  # smallest space step
    # Time step calculated by applying CFL condition
    dt = 0.5 * dx**2

    for i in range(100000):  # (we exit this time loop with break)
        t = i * dt
        integral = llg3d.integral(g, m)

        # Calculation of local analytical solution
        m_ana = np.exp(-4 * np.pi**2 * t) * m_0

        # Gather numerical and analytical solutions on proc 0
        comm.Gather(m, mg, root=0)
        comm.Gather(m_ana, mg_ana, root=0)

        error = np.linalg.norm(mg[:, 0, 0] - mg_ana[:, 0, 0], ord=2)

        # Update numerical solution
        m += dt * laplacian(g, m)
        if t > 1 / (4 * np.pi**2):
            break

    if rank == 0:
        assert integral == approx(0.0, rel=1e-15)
        assert error == approx(0.0038482190460058345, 1e-15)


@mark.skipif(300 % size != 0, reason=f"np = {size} is not a divisor of 300")
def test_simulate_mpi(tmp_path):
    N = 500 if size == 1 else 4000
    n_average = 1000

    # Switch to a temporary directory to avoid cluttering
    # the current directory
    os.chdir(tmp_path)
    print()  # only for pretty printing
    _, filenames, m1_avg = llg3d.simulate(
        N=N,
        Jx=300,
        Jy=11,
        Jz=11,
        dx=1e-9,
        T=1100.0,
        H_ext=0.0,
        dt=1e-14,
        n_average=n_average,
        n_integral=1,
        n_profile=100,
    )

    ref_arr = np.loadtxt(this_dir / "m1_integral_space_T1100_300x11x11_ref.txt")

    if size == 1:
        # On a single process, we check that the solution is the same as the
        # reference run
        test_arr = np.loadtxt(filenames[0])
        L2_error = np.linalg.norm(ref_arr[:N] - test_arr, ord=2)
        assert L2_error == 0.0
    elif rank == 0:
        # In parallel, we check that the temporal average is close to
        # the reference solution
        m1_ref = ref_arr[:, 1]
        m1_avg_ref = m1_ref[n_average:].mean()
        assert m1_avg == approx(m1_avg_ref, 4e-2)



@mark.skipif(300 % size != 0, reason=f"np = {size} is not a divisor of 300")
def test_simulate_temperature(tmp_path):
    # Switch to a temporary directory to avoid cluttering
    # the current directory
    os.chdir(tmp_path)

    params = {
        "H_ext": 0.0,
        "Jx": 300,
        "Jy": 21,
        "Jz": 21,
        "dx": 1e-9,
        "N": 500,
        "T": 1100,
        "blocking": False,
        "dt": 1e-14,
        "element": "Cobalt",
        "n_integral": 1,
        "n_profile": 100,
        "n_average": 250,
    }

    run = llg3d.simulate_temperature(params)
    if rank == 0:
        assert run["params"] == {
            "H_ext": 0.0,
            "Jx": 300,
            "Jy": 21,
            "Jz": 21,
            "dx": 1e-9,
            "N": 500,
            "T": 1100,
            "blocking": False,
            "dt": 1e-14,
            "element": "Cobalt",
            "n_integral": 1,
            "n_profile": 100,
            "n_average": 250,
            "np": size,
        }
        for k in "integral_file", "m1_mean", "total_time":
            assert k in run["results"][1100]


@mark.skipif(60 % size != 0, reason=f"np = {size} is not a divisor of 300")
def test_temperature_variation(tmp_path):
    os.chdir(tmp_path)
    params = {
        "H_ext": 0.0,
        "Jx": 60,
        "Jy": 21,
        "Jz": 21,
        "dx": 1e-9,
        "N": 500,
        "T": [1100, 1200, 1300],
        "blocking": False,
        "dt": 1e-14,
        "element": "Cobalt",
        "n_integral": 1,
        "n_profile": 100,
        "n_average": 250,
    }
    run = llg3d.temperature_variation(params)

    if rank == 0:
        assert run["params"] == {
            "H_ext": 0.0,
            "Jx": 60,
            "Jy": 21,
            "Jz": 21,
            "dx": 1e-9,
            "N": 500,
            "T": [1100, 1200, 1300],
            "blocking": False,
            "dt": 1e-14,
            "element": "Cobalt",
            "n_integral": 1,
            "n_profile": 100,
            "n_average": 250,
        }
        assert list(run["results"].keys()) == [1100, 1200, 1300]
