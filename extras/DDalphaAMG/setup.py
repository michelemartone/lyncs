try:
    from lyncs_setuptools import setup, CMakeExtension
    from lyncs_clime import __path__ as lime_path
except:
    print(
        """
    
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    Install first the requirements:
    pip install -r requirements.txt
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    """
    )

setup(
    "lyncs_DDalphaAMG",
    exclude=["*.config"],
    ext_modules=[
        CMakeExtension("lyncs_DDalphaAMG.lib", ".", ["-DLIME_PATH=%s" % lime_path[0]])
    ],
    data_files=[(".", ["config.py.in"])],
    install_requires=["lyncs-mpi", "lyncs-cppyy", "lyncs-clime",],
    keywords=[
        "Lyncs",
        "DDalphaAMG",
        "Lattice QCD",
        "Multigrid",
        "Wilson",
        "Twisted-mass",
        "Clover",
        "Fermions",
    ],
)
