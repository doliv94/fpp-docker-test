# CODIGO DO EXERCICIO ANTERIOR /////////////////////////////////////////////

# Aluna: Brunna Dalzini
# Matéria FPPD, Ifes Serra 2024/1

# Usando o PyCharm

# Passos: Download e execução do mpi4py do site da Microsoft:
# https://www.microsoft.com/en-us/download/details.aspx?id=105289
# Depois foi instalado também com o comando: python -m pip install mpi4py
# Instalado o numpy

# Teste inicial com 4 processadores conforme exemplos
# Usando comando: mpiexec -n 4 python mpipy.py
# Também foram testados com 6 processadores, 15 e 100

# Depois alterado para o total de processadores do meu computador, 12:
# mpiexec -n 12 python mpipy.py

from mpi4py import MPI
import numpy as np
import time
import math

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
nprocs = comm.Get_size()

# BASICS
"""
print('Hello from process {} out of {}'.format(rank, size))
"""

# POINT TO POINT COMMUNICATION (using blocking communication)
"""
# master process
if rank == 0:
    data = {'x': 1, 'y': 2.0}
    # master process sends data to worker processes by
    # going through the ranks of all worker processes
    for i in range(1, size):
        comm.send(data, dest=i, tag=i)
        print('Process {} sent data:'.format(rank), data)

# worker processes
else:
    # each worker process receives data from master process
    data = comm.recv(source=0, tag=rank)
    print('Process {} received data:'.format(rank), data)
"""

# POINT TO POINT COMMUNICATION (not using blocking communication)
"""
if rank == 0:
    data = {'x': 1, 'y': 2.0}
    for i in range(1, size):
        req = comm.isend(data, dest=i, tag=i)
        req.wait()
        print('Process {} sent data:'.format(rank), data)

else:
    req = comm.irecv(source=0, tag=rank)
    data = req.wait()
    print('Process {} received data:'.format(rank), data)
"""

# COLLECTIVE COMMUNICATION
"""
#
# Broadcasting numpy array

if rank == 0:
    data = np.arange(4.0)
else:
    data = None

data = comm.bcast(data, root=0)

if rank == 0:
    print('Process {} broadcast data:'.format(rank), data)
else:
    print('Process {} received data:'.format(rank), data)


#
# Scattering numpy array

# Como divide as tasks nos processadores, se tiver mais processadores que tasks, alguns não farão nada
# Se tiver menos processadores que tasks, as primeiras pegarão mais tarefas
if rank == 0:
    data = np.arange(15.0) 

    # determine the size of each sub-task
    ave, res = divmod(data.size, nprocs)
    counts = [ave + 1 if p < res else ave for p in range(nprocs)]

    # determine the starting and ending indices of each sub-task
    starts = [sum(counts[:p]) for p in range(nprocs)]
    ends = [sum(counts[:p+1]) for p in range(nprocs)]

    # converts data into a list of arrays
    data = [data[starts[p]:ends[p]] for p in range(nprocs)]
else:
    data = None

data = comm.scatter(data, root=0)

print('Process {} has data:'.format(rank), data)
"""

#
# Gathering and scattering to compute PI

# Usando os 12 processadores do computador o código é executado no menor tempo

t0 = time.time()

# number of integration steps
nsteps = 10000000
# step size
dx = 1.0 / nsteps

if rank == 0:
    # determine the size of each sub-task
    ave, res = divmod(nsteps, nprocs)
    counts = [ave + 1 if p < res else ave for p in range(nprocs)]

    # determine the starting and ending indices of each sub-task
    starts = [sum(counts[:p]) for p in range(nprocs)]
    ends = [sum(counts[:p+1]) for p in range(nprocs)]

    # save the starting and ending indices in data
    data = [(starts[p], ends[p]) for p in range(nprocs)]
else:
    data = None

data = comm.scatter(data, root=0)

# compute partial contribution to pi on each process
partial_pi = 0.0
for i in range(data[0], data[1]):
    x = (i + 0.5) * dx
    partial_pi += 4.0 / (1.0 + x * x)
partial_pi *= dx

partial_pi = comm.gather(partial_pi, root=0)

if rank == 0:
    print('pi computed in {:.3f} sec'.format(time.time() - t0))
    print('error is {}'.format(abs(sum(partial_pi) - math.pi)))



