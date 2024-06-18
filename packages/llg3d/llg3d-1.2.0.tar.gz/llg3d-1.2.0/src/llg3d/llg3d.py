"""
Solver for the stochastic Landau-Lifshitz-Gilbert equation in 3D
"""

import argparse
import json
import sys
import time
from dataclasses import dataclass

import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
status = MPI.Status()

# Parameters: default value and description
parameters = {
    "element": ("Cobalt", "Chemical element of the sample"),
    "N": (5000, "Number of time iterations"),  # default 5000
    "dt": (1.0e-14, "Time step"),  # default 1.e-14
    "Jx": (300, "Number of points in x"),
    "Jy": (21, "Number of points in y"),
    "Jz": (21, "Number of points in z"),
    "dx": (1.0e-9, "Step in x"),  # default 1.e-9
    "T": (0.0, "Temperature"),
    "H_ext": (
        0.0 / (4 * np.pi * 1.0e-7),
        "External field",
    ),  # must be constant, default 0.0
    "n_average": (4000, "Start index of time average"),  # default 4000
    "n_integral": (1, "Spatial average frequency (number of iterations)"),
    "n_profile": (0, "x-profile save frequency (number of iterations)"),
}

json_file = "run.json"


def progress_bar(rank: int, it, prefix="", size=60, out=sys.stdout):
    """
    Displays a progress bar
    (Source: https://stackoverflow.com/a/34482761/16593179)
    """

    count = len(it)

    def show(j):
        x = int(size * j / count)
        if rank == 0:
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
    if rank == 0:
        print("\n", flush=True, file=out)


@dataclass
class Grid:
    """Stores grid data"""

    # Parameter values correspond to the global grid
    Jx: int
    Jy: int
    Jz: int
    dx: float

    def __post_init__(self) -> None:
        """Compute grid characteristics"""
        self.dy = self.dz = self.dx  # Setting dx = dy = dz
        self.Lx = (self.Jx - 1) * self.dx
        self.Ly = (self.Jy - 1) * self.dy
        self.Lz = (self.Jz - 1) * self.dz
        # shape of the local array to the process
        self.dims = self.Jx // size, self.Jy, self.Jz
        # elemental volume of a cell
        self.dV = self.dx * self.dy * self.dz
        # total volume
        self.V = self.Lx * self.Ly * self.Lz
        # total number of points
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

    def get_filename(
        self, T: float, name: str = "m1_integral_space", extension="txt"
    ) -> str:
        """
        Returns the output file name for a given temperature

        >>> g = Grid(Jx=300, Jy=21, Jz=21, dx=1.e-9)
        >>> g.get_filename(1100)
        'm1_integral_space_T1100_300x21x21_np<MPI_size>.txt'
        """
        suffix = f"T{int(T)}_{self.Jx}x{self.Jy}x{self.Jz}_np{size}"
        return f"{name}_{suffix}.{extension}"

    def get_mesh(self, loc: bool = True) -> list:
        """
        Returns a list of 3D arrays with the coordinates
        of the grid points

        Args:
            loc: if True, returns the local coordinates,
                otherwise the global coordinates
        """
        xglob = np.linspace(0, self.Lx, self.Jx)  # global coordinates
        if loc:
            xloc = np.split(xglob, size)[rank]  # local coordinates
            x = xloc
        else:
            x = xglob
        return np.meshgrid(
            x,
            np.linspace(0, self.Ly, self.Jy),
            np.linspace(0, self.Lz, self.Jz),
            indexing="ij",
        )


class Element:
    """Abstract class for chemical elements"""

    A = 0.0
    K = 0.0
    gamma = 0.0
    mu_0 = 0.0
    k_B = 0.0
    lambda_G = 0.0
    M_s = 0.0
    a_eff = 0.0

    def __init__(self, T: float, H_ext: float, g: Grid, dt: float) -> None:
        self.H_ext = H_ext
        self.g = g
        self.dt = dt
        self.gamma_0 = self.gamma * self.mu_0
        self.d0 = np.sqrt(self.A / self.K)  # only if K is positive

        # --- Characteristic Scales ---
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

    def get_CFL(self):
        return self.dt * self.coeff_1 / self.g.dx**2


class Cobalt(Element):
    A = 30.0e-12
    K = 520.0e3
    gamma = 1.76e11
    mu_0 = 1.26e-6
    k_B = 1.38e-23
    lambda_G = 0.5  # 0.5 par defaut
    M_s = 1400.0e3
    a_eff = 0.25e-9
    anisotropy = "uniaxial"


class Iron(Element):
    A = 21.0e-12
    K = 48.0e3
    gamma = 1.76e11
    mu_0 = 1.26e-6
    gamma_0 = gamma * mu_0
    k_B = 1.38e-23
    lambda_G = 0.5  # 0.5 par defaut
    M_s = 1700.0e3
    a_eff = 0.286e-9
    anisotropy = "cubic"


class Nickel(Element):
    A = 9.0e-12
    K = -5.7e3
    gamma = 1.76e11
    mu_0 = 1.26e-6
    gamma_0 = gamma * mu_0
    k_B = 1.38e-23
    lambda_G = 0.5  # 0.5 par defaut
    M_s = 490.0e3
    a_eff = 0.345e-9
    anisotropy = "cubic"


def get_boundaries_x(
    g: Grid, m, blocking: bool = False
) -> tuple[np.ndarray, np.ndarray, MPI.Request, MPI.Request]:
    """
    Returns the boundaries asynchronously:
    allows overlapping communication time of boundaries
    with calculations
    """

    # Extract slices for Neumann boundary conditions

    m_start_x = np.empty((1, g.Jy, g.Jz))
    m_end_x = np.empty_like(m_start_x)

    # Prepare ring communication:
    # Even if procs 0 and size - 1 shouldn't receive anything from left
    # and right respectively, it's simpler to express it like this
    right = (rank + 1) % size
    left = (rank - 1 + size) % size

    if blocking:
        # Wait for boundaries to be available
        comm.Sendrecv(m[:1, :, :], dest=left, sendtag=0, recvbuf=m_end_x, source=right)
        comm.Sendrecv(
            m[-1:, :, :], dest=right, sendtag=1, recvbuf=m_start_x, source=left
        )
        return m_start_x, m_end_x, None, None
    else:
        request_start = comm.Irecv(m_start_x, source=left, tag=201)
        request_end = comm.Irecv(m_end_x, source=right, tag=202)
        comm.Isend(m[-1:, :, :], dest=right, tag=201)
        comm.Isend(m[:1, :, :], dest=left, tag=202)

        return m_start_x, m_end_x, request_start, request_end


def calculate_laplacian(
    e: Element,
    g: Grid,
    m: np.ndarray,
    m_start_x: np.ndarray,
    m_end_x: np.ndarray,
    request_end: MPI.Request,
    request_start: MPI.Request,
) -> np.ndarray:
    """
    Returns the Laplacian of m (* coeff_1) in 3D.
    We start by calculating contributions in y and z, to wait
    for the end of communications in x.
    """

    # Extract slices for Neumann boundary conditions
    m_start_y = m[:, 1:2, :]
    m_end_y = m[:, -2:-1, :]

    m_start_z = m[:, :, 1:2]
    m_end_z = m[:, :, -2:-1]

    m_y_plus = np.concatenate((m[:, 1:, :], m_end_y), axis=1)
    m_y_minus = np.concatenate((m_start_y, m[:, :-1, :]), axis=1)
    m_z_plus = np.concatenate((m[:, :, 1:], m_end_z), axis=2)
    m_z_minus = np.concatenate((m_start_z, m[:, :, :-1]), axis=2)

    laplacian = (
        (m_y_plus + m_y_minus) / g.dy**2
        + (m_z_plus + m_z_minus) / g.dz**2
        - 2 * (1 / g.dx**2 + 1 / g.dy**2 + 1 / g.dz**2) * m
    )

    # Wait for x-boundaries to be available (communications completed)
    try:
        request_end.Wait(status)
        request_start.Wait(status)
    except AttributeError:
        pass

    # For extreme procs, apply Neumann boundary conditions in x
    if rank == size - 1:
        m_end_x = m[-2:-1, :, :]
    if rank == 0:
        m_start_x = m[1:2, :, :]

    m_x_plus = np.concatenate((m[1:, :, :], m_end_x), axis=0)
    m_x_minus = np.concatenate((m_start_x, m[:-1, :, :]), axis=0)

    laplacian += (m_x_plus + m_x_minus) / g.dx**2

    return e.coeff_1 * laplacian


def calculate_si(
    e: Element,
    g: Grid,
    m1: np.ndarray,
    m2: np.ndarray,
    m3: np.ndarray,
    R_alea: np.ndarray,
    boundaries,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Returns the s_i = a_i + b_i"""

    # Precalculate terms used multiple times

    l_G_m1m2 = e.lambda_G * m1 * m2
    l_G_m1m3 = e.lambda_G * m1 * m3
    l_G_m2m3 = e.lambda_G * m2 * m3

    m1m1 = m1 * m1
    m2m2 = m2 * m2
    m3m3 = m3 * m3

    laplacian_m1 = calculate_laplacian(e, g, m1, *boundaries[0])
    laplacian_m2 = calculate_laplacian(e, g, m2, *boundaries[1])
    laplacian_m3 = calculate_laplacian(e, g, m3, *boundaries[2])

    if e.anisotropy == "uniaxial":
        aniso_1 = m1
        aniso_2 = np.zeros(np.shape(m1))
        aniso_3 = np.zeros(np.shape(m1))

    if e.anisotropy == "cubic":
        aniso_1 = -(1 - m1m1 + m2m2 * m3m3) * m1
        aniso_2 = -(1 - m2m2 + m1m1 * m3m3) * m2
        aniso_3 = -(1 - m3m3 + m1m1 * m2m2) * m3

    R_1 = laplacian_m1 + e.coeff_2 * aniso_1 + e.coeff_3 + e.coeff_4 * R_alea[0]
    R_2 = laplacian_m2 + e.coeff_2 * aniso_2 + e.coeff_4 * R_alea[1]
    R_3 = laplacian_m3 + e.coeff_2 * aniso_3 + e.coeff_4 * R_alea[2]

    s1 = (
        (-m2 - l_G_m1m3) * R_3
        + (m3 - l_G_m1m2) * R_2
        + e.lambda_G * (m2m2 + m3m3) * R_1
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
    Returns the spatial average of m of shape (g.dims)
    using the midpoint method on each process
    """

    # Make a copy of m to avoid modifying its value
    mm = m.copy()

    # On y and z edges, divide the contribution by 2
    mm[:, 0, :] /= 2
    mm[:, -1, :] /= 2
    mm[:, :, 0] /= 2
    mm[:, :, -1] /= 2

    # On x edges (only on extreme procs), divide the contribution by 2
    if rank == 0:
        mm[0] /= 2
    if rank == size - 1:
        mm[-1] /= 2
    local_sum = mm.sum()

    # Sum across all processes gathered by process 0
    global_sum = comm.reduce(local_sum)

    # Spatial average is the global sum divided by the number of cells
    return global_sum / g.ncell if rank == 0 else 0.0


def integral_yz(m: np.ndarray) -> np.ndarray:
    """
    Returns the spatial average of shape (g.dims[0],)
    in y and z of m of shape (g.dims) using the midpoint method
    """

    # Make a copy of m to avoid modifying its value
    mm = m.copy()

    # On y and z edges, divide the contribution by 2
    mm[:, 0, :] /= 2
    mm[:, -1, :] /= 2
    mm[:, :, 0] /= 2
    mm[:, :, -1] /= 2

    n_cell_yz = (mm.shape[1] - 1) * (mm.shape[2] - 1)
    return mm.sum(axis=(1, 2)) / n_cell_yz


def profile(m: np.ndarray, m_xprof: np.ndarray):
    """
    Retrieves the x profile of the average of m in y and z
    """

    # Gather m in mglob
    m_mean_yz = integral_yz(m)
    comm.Gather(m_mean_yz, m_xprof)


def theta_init(t: float, g: Grid) -> np.ndarray:
    """Initialization of theta"""
    x, y, z = g.get_mesh()
    # return 2.*np.arctan(np.exp(-(x-g.Lx/2+e.d0*e.coeff_3*e.lambda_G*t)/e.d0))
    return np.zeros(g.dims)


def phi_init(t: float, g: Grid, e: Element) -> np.ndarray:
    """Initialization of phi"""
    # return np.zeros(shape) + e.coeff_3 * t
    return np.zeros(g.dims) + e.gamma_0 * e.H_ext * t


def simulate(
    N: int,
    Jx: int,
    Jy: int,
    Jz: int,
    dx: float,
    T: float,
    H_ext: float,
    dt: float,
    n_average: int,
    n_integral: int,
    n_profile: int,
    element: Element = Cobalt,
    blocking: bool = False,
):
    """
    Simulates the system for N iterations
    Returns the computation time, output filename
    and the temporal average
    """

    if Jx % size != 0:
        if rank == 0:
            print(
                f"Error: Jx must be divisible by the number of processes"
                f"({Jx = }, np = {size})"
            )
        comm.barrier()
        MPI.Finalize()
        exit(2)

    # Initialize a sequence of random seeds
    # See: https://numpy.org/doc/stable/reference/random/parallel.html
    ss = np.random.SeedSequence(12345)

    # Deploy size x SeedSequence to pass to child processes
    child_seeds = ss.spawn(size)
    streams = [np.random.default_rng(s) for s in child_seeds]
    rng = streams[rank]

    # Create the grid
    g = Grid(Jx=Jx, Jy=Jy, Jz=Jz, dx=dx)

    if rank == 0:
        print(g)

    e = element(T, H_ext, g, dt)
    if rank == 0:
        print(f"CFL = {e.get_CFL()}")

    m1 = np.zeros((2,) + g.dims)
    m2 = np.zeros_like(m1)
    m3 = np.zeros_like(m1)

    theta = theta_init(0, g)
    phi = phi_init(0, g, e)

    m1[0] = np.cos(theta)
    m2[0] = np.sin(theta) * np.cos(phi)
    m3[0] = np.sin(theta) * np.sin(phi)

    m_xprof = np.zeros(g.Jx)  # global coordinates

    output_filenames = []
    if n_integral != 0:
        output_filenames.append(g.get_filename(T, extension="txt"))
    if n_profile != 0:
        output_filenames.extend(
            [g.get_filename(T, name=f"m{i+1}", extension="npy") for i in range(3)]
        )
    if rank == 0:
        if n_integral != 0:
            f_integral = open(output_filenames[0], "w")  # integral of m1
        if n_profile != 0:
            f_profiles = [
                open(output_filename, "wb") for output_filename in output_filenames[1:]
            ]  # x profiles of m_i

    t = 0.0
    m1_average = 0.0

    start_time = time.perf_counter()

    for n in progress_bar(rank, range(1, N + 1), "Iteration: ", 40):
        t += dt

        x_boundaries = [
            get_boundaries_x(g, m[0], blocking=blocking) for m in (m1, m2, m3)
        ]

        # adding randomness: effect of temperature
        R_random = rng.standard_normal((3, *g.dims))

        # prediction phase
        s1_pre, s2_pre, s3_pre = calculate_si(
            e, g, m1[0], m2[0], m3[0], R_random, x_boundaries
        )

        # update
        m1[1] = m1[0] + dt * s1_pre
        m2[1] = m2[0] + dt * s2_pre
        m3[1] = m3[0] + dt * s3_pre

        # correction phase
        x_boundaries = [
            get_boundaries_x(g, m[0], blocking=blocking) for m in (m1, m2, m3)
        ]

        s1_cor, s2_cor, s3_cor = calculate_si(
            e, g, m1[1], m2[1], m3[1], R_random, x_boundaries
        )

        # update
        m1[1] = m1[0] + dt * 0.5 * (s1_pre + s1_cor)
        m2[1] = m2[0] + dt * 0.5 * (s2_pre + s2_cor)
        m3[1] = m3[0] + dt * 0.5 * (s3_pre + s3_cor)

        # renormalize to verify the constraint of being on the sphere
        norm = np.sqrt(m1[1] ** 2 + m2[1] ** 2 + m3[1] ** 2)
        m1[1] /= norm
        m2[1] /= norm
        m3[1] /= norm

        m1[0] = m1[1]
        m2[0] = m2[1]
        m3[0] = m3[1]

        # Export the average of m1 to a file
        if n_integral != 0 and n % n_integral == 0:
            m1_integral_global = integral(g, m1[0])
            if rank == 0:
                if n >= n_average:
                    m1_average += m1_integral_global * n_integral
                f_integral.write(f"{t:10.8e} {m1_integral_global:10.8e}\n")
        # Export the x profiles of the averaged m_i in y and z
        if n_profile != 0 and n % n_profile == 0:
            for i, m in enumerate((m1[0], m2[0], m3[0])):
                profile(m, m_xprof)
                if rank == 0:
                    # add an x profile to the file
                    np.save(f_profiles[i], m_xprof)

    total_time = time.perf_counter() - start_time

    if rank == 0:
        if n_integral != 0:
            f_integral.close()
        if n_profile != 0:
            for i in range(3):
                f_profiles[i].close()

        if n > n_average:
            m1_average /= N - n_average
            print(f"{m1_average = :e}")

    return total_time, output_filenames, m1_average


class ArgumentParser(argparse.ArgumentParser):
    """An argument parser compatible with MPI"""

    def _print_message(self, message, file=None):
        if rank == 0 and message:
            if file is None:
                file = sys.stderr
            file.write(message)

    def exit(self, status=0, message=None):
        if message:
            self._print_message(message, sys.stderr)
        comm.barrier()
        MPI.Finalize()
        exit(status)


def get_element_class(element_name: str):
    """Returns the chemical element class from its name"""
    for cls in Element.__subclasses__():
        if cls.__name__ == element_name:
            return cls


def simulate_temperature(params: dict) -> dict:
    """
    Runs a simulation for a given parameter set.
    Returns a dictionary of the run.
    """
    # Backup copy as run['element'] will be modified
    run = {"params": params.copy(), "results": {}}
    run["params"]["np"] = size
    # Referencing the element class from the string
    params["element"] = globals()[run["params"]["element"]]

    # Run the simulation
    total_time, filenames, m1_mean = simulate(**params)

    if rank == 0:
        N = run["params"]["N"]
        run["results"] = {
            params["T"]: {"total_time": total_time}
        }
        # Export the integral of m1
        if len(filenames) > 0:
            run["results"][params["T"]]["integral_file"] = filenames[0]
            print(f"Integral of m1 in {filenames[0]}")
        # Export the x-profiles of m1, m2 and m3
        if len(filenames) > 1:
            for i in range(1, 4):
                run["results"][params["T"]][f"xprofile_m{i}"] = filenames[i]
                print(f"x-profile of m{i} in {filenames[i]}")

        print(f"N iterations      = {N}")
        print(f"total_time [s]    = {total_time:.03f}")
        print(f"time/ite [s/iter] = {total_time / N:.03e}")
        if N > run["params"]["n_average"]:
            print(f"m1_mean           = {m1_mean:e}")
            run["results"][params["T"]]["m1_mean"] = m1_mean

    return run


def temperature_variation(params: dict):
    """Sweeps an array of temperature"""

    # Initialize the run dictionary
    run = {"params": params.copy(), "results": {}}
    for T in params["T"]:
        if rank == 0:
            print("-------------")
            print(f"T[K] = {T}")
            print("-------------")
        params_T = params.copy()
        params_T["T"] = T  # replace the list with the element
        run_T = simulate_temperature(params_T)
        # Update the results dictionary
        if rank == 0:
            run["results"][T] = run_T["results"][T]
    return run


def parameter_list(d: dict) -> str:
    """Returns parameter values as a string"""
    width = max([len(s) for s in d])
    s = ""
    for k, v in d.items():
        sep = ":" if isinstance(v, str) else "="
        s += "{0:<{1}} {2} {3}\n".format(k, width, sep, v)
    return s


def write_json(run: dict):
    """Writes the run dictionary to a JSON file"""
    if rank == 0:
        with open(json_file, "w") as f:
            json.dump(run, f, indent=4)
        print(f"Summary in {json_file}")


def parse_args(args) -> argparse.Namespace:
    """Argument parser for llg3d"""
    parser = ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    # Automatically add arguments from the parameter dictionary
    for name, data in parameters.items():
        value, description = data
        nargs = "*" if name == "T" else None  # T may be a list
        parser.add_argument(
            f"-{name}", type=type(value), nargs=nargs, default=value, help=description
        )
    # Add an argument to handle the type of communications
    parser.add_argument(
        "-b",
        "--blocking",
        action="store_true",
        help="Use blocking communications",
    )
    return parser.parse_args(args)


def main(args_main=None):
    """Evaluates the command line and runs the simulation"""

    args = parse_args(args_main)
    if rank == 0:
        # Display parameters as a list
        print(parameter_list(vars(args)))

    if isinstance(args.T, float) or len(args.T) == 1:
        if isinstance(args.T, list):
            vars(args)["T"] = vars(args)["T"][0]
        run = simulate_temperature(vars(args))
        write_json(run)
    else:
        run = temperature_variation(vars(args))
        write_json(run)


if __name__ == "__main__":
    main()
