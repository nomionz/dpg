import time
import sys
import numpy as np

from mpi4py import MPI


def estimate_pi(num_samples):
    """Monte Carlo method"""
    x = np.random.random(num_samples)
    y = np.random.random(num_samples)

    inside_circle = (x ** 2 + y ** 2 <= 1.0)

    return np.sum(inside_circle)

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        if len(sys.argv) > 1:
            try:
                input_file = sys.argv[1]
                with open(input_file, 'r') as f:
                    total_samples = int(f.readline().strip())
            except Exception as e:
                print(f"Error reading input file: {e}")
                comm.Abort(1)
        else:
            print("Error: Input file is required.")
            print("Usage: mpiexec -n <num_processes> python pi.py <input_file>")
            comm.Abort(1)

        print(f"Estimating pi using {total_samples} total samples across {size} processes")
        start_time = time.time()
    else:
        total_samples = None

    # master node broadcasts
    total_samples = comm.bcast(total_samples, root=0)

    samples_per_process = total_samples // size

    local_count = estimate_pi(samples_per_process)

    total_count = comm.reduce(local_count, op=MPI.SUM, root=0)

    # calculate final result and write to file
    if rank == 0:
        pi_estimate = 4.0 * total_count / total_samples
        end_time = time.time()
        elapsed = end_time - start_time

        print(f"pi estimate: {pi_estimate}")
        print(f"True pi value: {np.pi}")
        print(f"Error: {abs(pi_estimate - np.pi)}")
        print(f"Execution time: {elapsed:.2f} seconds")

        with open("result.txt", "w") as f:
            f.write(f"Number of processes: {size}\n")
            f.write(f"Total samples: {total_samples}\n")
            f.write(f"pi estimate: {pi_estimate}\n")
            f.write(f"True pi value: {np.pi}\n")
            f.write(f"Error: {abs(pi_estimate - np.pi)}\n")
            f.write(f"Execution time: {elapsed:.2f} seconds\n")

        print("Results written to result.txt")

if __name__ == "__main__":
    main()