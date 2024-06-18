[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

qtealeaves
==========

The qtealeaves library of Quantum TEA contains tensor network representation as
python classes, e.g., MPS, TTN, LPTN, and TTO. qtealeaves is the API for building
quantum models in Quantum TEA and has for example a single-tensor update ground state
search for TTNs. Moreover, qtealeaves is backbone for running quantum circuits via
Quantum matcha TEA and the frontend for the fortran backend running Quantum Green TEA,
i.e., solving the Schrödinger equation.


Documentation
=============

[Here](https://quantum_tea_leaves.baltig-pages.infn.it/py_api_quantum_tea_leaves/)
is the documentation. The documentation can also be built locally via sphinx.


License
=======

The project ``qtealeaves`` is hosted at the repository
``https://baltig.infn.it/quantum_tea_leaves/py_api_quantum_tea_leaves.git``,
and is licensed under the following license:

[Apache License 2.0](LICENSE)

The license applies to the files of this project as indicated
in the header of each file, but not its dependencies.


Installation
============

Independent of the use-case, you have to install the dependencies. Then,
there are the options using it as a stand-alone package, within [quantum
matcha TEA](https://baltig.infn.it/quantum_matcha_tea), or for quantum green TEA.

Local installation via pip
--------------------------

The package is available via PyPi and `pip install qtealeaves`.
After cloning the repository, an local installation via pip is
also possible via `pip install .`.

Dependencies
------------

The python dependencies can be found in the [``requirements.txt``](requirements.txt)
and are required independently of the following use-cases.

Stand-alone package
-------------------

If you are looking to explore small exact diagonalization examples,
want to run a single-tensor update ground state search with TTNs,
or have TN-states on files to be post-processed, you are ready to
go.

qmatchatea simulations
----------------------

Quantum circuit simulations via qmatchatea have qtealeaves as a
dependency. Follow the instructions to install qmatchatea to get
the right version of qtealeaves.

qgreentea simulations
---------------------

If you want to use the qgreentea toolchain with TTNs and aTTNS, you need to
install qtealeaves under a matching version. qgreentea provides instructions
which version is compatible; see installation instructions there. qgreentea
is not yet public, but it will be made public step-by-step.
