"""
Lyncs, a python API for LQCD applications
"""
import lyncs_config as config

if config.mpi_enabled:
    from lyncs import mpi
    
if config.ddalphaamg_enabled:
    from lyncs import DDalphaAMG
