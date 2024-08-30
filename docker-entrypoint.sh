#!/bin/bash
service ssh restart
exec "$@"
exec mpirun 
exec mpiexec 
