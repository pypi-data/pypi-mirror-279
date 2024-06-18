"""
Solver for the stochastic Landau-Lifshitz-Gilbert equation in 3D
(sequential version for history)
"""
import argparse
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np

# Create a random number generator by setting the seed
rng = np.random.default_rng(0)

# Initialize a sequence of random seeds
# See: https://numpy.org/doc/stable/reference/random/parallel.html#seedsequence-spawning
ss = np.random.SeedSequence(12345)

# Deploy size x SeedSequence to be passed to child processes
child_seeds = ss.spawn(1)
rng = np.random.default_rng(child_seeds[0])


# Parameters: default value and description
parameters = {
    "N": (500, "Number of temporal iterations"),
    "dt": (1.0e-14, "Time step"),
    "Jx": (300, "Number of points in x"),
    "Jy": (21, "Number of points in y"),
    "Jz": (21, "Number of points in z"),
    "Lx": (2.99e-7, "Length in x"),
    "Ly": (1.0e-8, "Length in y"),
    "Lz": (1.0e-8, "Length in z"),
    "T": (1100, "Temperature"),
    "H_ext": (0.0, "External field"),
    "n_average": (2000, "Starting index of temporal averaging"),
}


def progress_bar(it, prefix="", size=60, out=sys.stdout):
    """
    Displays a progress bar
    (Source: https://stackoverflow.com/a/34482761/16593179)
    """

    count = len(it)

    def show(j):
        x = int(size * j / count)
        print(
            f"{prefix}[{u'█'*x}{('.'*(size-x))}] {j}/{count}",
            end="\r",
            file=out,
            flush=True,
        )

    show(0)
    for i, item in enumerate(it):
        yield item
        # To avoid slowing down the computation, we do not display at every iteration
        if i % 5 == 0:
            show(i + 1)
    show(i + 1)
    print("\n", flush=True, file=out)


@dataclass
class Grid:
    """Stores grid data"""

    # Parameters refer to the entire grid
    Jx: int
    Jy: int
    Jz: int
    Lx: float
    Ly: float
    Lz: float

    def __post_init__(self) -> None:
        """Calculates grid characteristics"""
        self.dx = self.Lx / (self.Jx - 1)
        self.dy = self.Ly / (self.Jy - 1)
        self.dz = self.Lz / (self.Jz - 1)
        # Shape of the local array for the process
        self.dims = self.Jx, self.Jy, self.Jz
        # Volume of a grid cell
        self.dV = self.dx * self.dy * self.dz
        # Total volume
        self.V = self.Lx * self.Ly * self.Lz
        # Total number of points
        self.ntot = self.Jx * self.Jy * self.Jz
        self.ncell = (self.Jx - 1) * (self.Jy - 1) * (self.Jz - 1)

    def __repr__(self):
        s = "\t" + "\t\t".join(("x", "y", "z")) + "\n"
        s += f"J =\t{self.Jx}\t\t{self.Jy}\t\t{self.Jz}\n"
        s += f"L =\t{self.Lx}\t\t{self.Ly}\t\t{self.Lz}\n"
        s += f"d =\t{self.dx:.08e}\t{self.dy:.08e}\t{self.dz:.08e}\n\n"
        s += f"dV   = {self.dV:.08e}\n"
        s += f"V    = {self.V:.08e}\n"
        s += f"ntot = {self.ntot:d}\n"

        return s

    def get_filename(self, T: float) -> str:
        """Returns the output file name for a given temperature"""
        suffix = f"T{int(T)}_{self.Jx}x{self.Jy}x{self.Jz}"
        return f"m1_integral_space_{suffix}.txt"


class Element:
    """Abstract class for an element"""

    A = 0.0
    K = 0.0
    gamma = 0.0
    mu_0 = 0.0
    k_B = 0.0
    lambda_G = 0.0
    M_s = 0.0
    a_eff = 0.0

    def __init__(self, T: float, H_ext, g: Grid, dt: float) -> None:
        self.g = g
        self.dt = dt
        self.gamma_0 = self.gamma * self.mu_0

        # --- Characteristic scales ---
        self.coeff_1 = self.gamma_0 * 2.0 * self.A / (self.mu_0 * self.M_s)
        self.coeff_2 = self.gamma_0 * 2.0 * self.K / (self.mu_0 * self.M_s)
        self.coeff_3 = self.gamma_0 * H_ext

        # corresponds to the temperature actually put into the random field
        T_simu = T * self.g.dx / self.a_eff
        # calculation of the random field related to temperature
        # (we only take the volume over one mesh)
        h_alea = np.sqrt(
            2
            * self.lambda_G
            * self.k_B
            / (self.gamma_0 * self.mu_0 * self.M_s * self.g.dV)
        )
        H_alea = h_alea * np.sqrt(T_simu) * np.sqrt(1.0 / self.dt)
        self.coeff_4 = H_alea * self.gamma_0

    def get_CFL(self) -> float:
        """Returns the value of the CFL"""
        return self.dt * self.coeff_1 / self.g.dx**2


class Cobalt(Element):
    A = 30.0e-12
    K = 520.0e3
    gamma = 1.76e11
    mu_0 = 1.26e-6
    k_B = 1.38e-23
    # #mu_B=9.27e-24
    lambda_G = 0.5
    M_s = 1400.0e3
    a_eff = 0.25e-9


class Iron(Element):
    A = 21.0e-12
    K = 48.0e3
    gamma = 1.76e11
    mu_0 = 1.26e-6
    gamma_0 = gamma * mu_0  # 2.34e+5
    k_B = 1.38e-23
    # mu_B=9.27e-24
    lambda_G = 0.5
    M_s = 1700.0e3
    a_eff = 0.286e-9


def calculate_laplacian(e: Element, g: Grid, m):
    """Returns the laplacian of m (* coeff_1) in 3D"""

    # Extract slices for Neumann boundary conditions
    m_start_x = m[1:2, :, :]
    m_end_x = m[-2:-1, :, :]

    m_start_y = m[:, 1:2, :]
    m_end_y = m[:, -2:-1, :]

    m_start_z = m[:, :, 1:2]
    m_end_z = m[:, :, -2:-1]

    laplacian = (
        (
            np.concatenate((m[1:, :, :], m_end_x), axis=0)
            + np.concatenate((m_start_x, m[:-1, :, :]), axis=0)
        )
        / g.dx ** 2
        + (
            np.concatenate((m[:, 1:, :], m_end_y), axis=1)
            + np.concatenate((m_start_y, m[:, :-1, :]), axis=1)
        )
        / g.dy ** 2
        + (
            np.concatenate((m[:, :, 1:], m_end_z), axis=2)
            + np.concatenate((m_start_z, m[:, :, :-1]), axis=2)
        )
        / g.dz ** 2
        - 2 * (1 / g.dx ** 2 + 1 / g.dy ** 2 + 1 / g.dz ** 2) * m
    )

    return e.coeff_1 * laplacian


def calculate_si(
    e: Element, m1, m2, m3, laplacian_m1, laplacian_m2, laplacian_m3, R_alea
):
    """Returns the s_i = a_i + b_i"""

    # Precalculate terms that appear multiple times

    R_1 = laplacian_m1 + e.coeff_2 * m1 + e.coeff_3 + e.coeff_4 * R_alea[0]
    R_2 = laplacian_m2 + e.coeff_4 * R_alea[1]
    R_3 = laplacian_m3 + e.coeff_4 * R_alea[2]

    l_G_m1m2 = e.lambda_G * m1 * m2
    l_G_m1m3 = e.lambda_G * m1 * m3
    l_G_m2m3 = e.lambda_G * m2 * m3

    m1m1 = m1 * m1
    m2m2 = m2 * m2
    m3m3 = m3 * m3

    s1 = (
        (-m2 - l_G_m1m3) * R_3
        + +(m3 - l_G_m1m2) * R_2
        + +e.lambda_G * (m2m2 + m3m3) * R_1
    )

    s2 = (
        (-m3 - l_G_m1m2) * R_1
        + (m1 - l_G_m2m3) * R_3
        + e.lambda_G * (m1m1 + m3m3) * R_2
    )

    s3 = (
        (-m1 - l_G_m2m3) * R_2
        + (m2 - l_G_m1m3) * R_1
        + e.lambda_G * (m1m1 + m2m2) * R_3
    )

    return s1, s2, s3


def integral(g, m: np.ndarray) -> float:
    """
    Returns the spatial average of m with shape (g.dims)
    using the midpoint method
    """

    # copy m to avoid modifying its value
    mm = m.copy()

    # on the edges, we divide the contribution by 2
    # x
    mm[0, :, :] /= 2
    mm[-1, :, :] /= 2
    # y
    mm[:, 0, :] /= 2
    mm[:, -1, :] /= 2
    # z
    mm[:, :, 0] /= 2
    mm[:, :, -1] /= 2

    return mm.sum() / g.ncell



def simulate(N, Jx, Jy, Jz, Lx, Ly, Lz, T, H_ext, dt, n_average, element):
    """Simulates the system over N iterations"""

    g = Grid(Jx=Jx, Jy=Jy, Jz=Jz, Lx=Lx, Ly=Ly, Lz=Lz)
    print(g)

    dims = g.dims

    e = element(T, H_ext, g, dt)
    print(f"CFL = {e.get_CFL()}")

    # --- Initialization ---

    def theta_init(shape):
        """Initialization of theta"""
        return np.zeros(shape)

    def phi_init(t, shape):
        """Initialization of phi"""
        return np.zeros(shape) + e.gamma_0 * H_ext * t

    m1 = np.zeros((2,) + dims)
    m2 = np.zeros_like(m1)
    m3 = np.zeros_like(m1)

    theta = theta_init(dims)
    phi = phi_init(0, dims)

    m1[0] = np.cos(theta)
    m2[0] = np.sin(theta) * np.cos(phi)
    m3[0] = np.sin(theta) * np.sin(phi)

    # Output file
    f = open(g.get_filename(T), "w")

    t = 0.0
    m1_mean = 0.0

    start_time = time.perf_counter()

    for n in progress_bar(range(1, N + 1), "Iteration : ", 40):
        t += dt

        # Adding randomness: temperature effect
        R_alea = rng.standard_normal((3,) + dims)

        # Prediction phase

        laplacian_m1 = calculate_laplacian(e, g, m1[0])
        laplacian_m2 = calculate_laplacian(e, g, m2[0])
        laplacian_m3 = calculate_laplacian(e, g, m3[0])

        s1_pre, s2_pre, s3_pre = calculate_si(
            e, m1[0], m2[0], m3[0], laplacian_m1, laplacian_m2, laplacian_m3, R_alea
        )

        # Update
        m1[1] = m1[0] + dt * s1_pre
        m2[1] = m2[0] + dt * s2_pre
        m3[1] = m3[0] + dt * s3_pre

        # Correction phase

        laplacian_m1 = calculate_laplacian(e, g, m1[1])
        laplacian_m2 = calculate_laplacian(e, g, m2[1])
        laplacian_m3 = calculate_laplacian(e, g, m3[1])

        s1_cor, s2_cor, s3_cor = calculate_si(
            e, m1[1], m2[1], m3[1], laplacian_m1, laplacian_m2, laplacian_m3, R_alea
        )

        # Update
        m1[1] = m1[0] + dt * 0.5 * (s1_pre + s1_cor)
        m2[1] = m2[0] + dt * 0.5 * (s2_pre + s2_cor)
        m3[1] = m3[0] + dt * 0.5 * (s3_pre + s3_cor)

        # We renormalize to check the constraint of being on the sphere
        norm = np.sqrt(m1[1] ** 2 + m2[1] ** 2 + m3[1] ** 2)
        m1[1] /= norm
        m2[1] /= norm
        m3[1] /= norm

        m1[0] = m1[1]
        m2[0] = m2[1]
        m3[0] = m3[1]

        # Midpoint method
        m1_integral = integral(g, m1[0])
        if n >= n_average:
            m1_mean += m1_integral

        f.write(f"{t:10.8e} {m1_integral:10.8e}\n")

    m1_mean /= N - n_average

    print(f"Output in {g.get_filename(T)}")
    f.close()

    print(f"{t = :e} T_f = {N * dt}")
    if m1_mean != 0.0:
        print(f"{m1_mean = :e}")

    return g, (time.perf_counter() - start_time)


def check_solution(g: Grid, T: float) -> bool:
    """
    Verifies that the solution is identical to m1_integral_space_T1100_ref.txt,
    obtained with the reference code using np.random.default_rng(0)
    """
    filename = g.get_filename(T)
    ref_filename = Path(filename).stem + "_ref.txt"
    try:
        with open(filename) as f:
            with open(ref_filename) as f_ref:
                for line, line_ref in zip(f, f_ref):
                    assert line == line_ref
        print("Check OK")
        return True
    except AssertionError:
        # The solution is not identical: we calculate the L2 norm of the error
        data = np.loadtxt(filename)
        ref = np.loadtxt(ref_filename)
        nmax = min(data.shape[0], ref.shape[0])
        error = np.linalg.norm(data[:nmax, 1] - ref[:nmax, 1], ord=2)
        norm = np.linalg.norm(ref[:nmax, 1], ord=2)
        print(f"Relative error (L2 norm): {error/norm = :08e}")
        return False


def parse_args(args) -> argparse.Namespace:
    """Argument parser for llg3d_seq"""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-c", "--check", action="store_true", help="Check against the reference"
    )
    parser.add_argument(
        "-element", type=str, default="Cobalt", help="Element of the sample"
    )
    # Add arguments from the parameters dictionary
    for name, data in parameters.items():
        value, description = data
        parser.add_argument(
            f"-{name}", type=type(value), help=description, default=value
        )

    return parser.parse_args(args)


def main(args_main=None):
    """Evaluates the command line and starts the simulation"""
    args = parse_args(args_main)

    check = args.check
    del args.check
    N = args.N

    # Convert the element object from the string
    if "element" in args:
        vars(args)["element"] = globals()[args.element]
    grid, total_time = simulate(**vars(args))

    print(f"{N = } iterations")
    print(f"total_time [s]   = {total_time:.03f}")
    print(f"temps/ite [s/ite] = {total_time / N:.03e}")
    if check:
        check_solution(grid, args.T)

if __name__ == "__main__":
    main()