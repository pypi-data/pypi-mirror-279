# This code is part of qtealeaves.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

import os
import os.path
import unittest
from io import StringIO
import pylint.lint
from pylint.reporters.text import ParseableTextReporter


class TestPylint(unittest.TestCase):
    """
    Run pylint to check syntax in source files.

    **Details**

    We disable globally:

    * C0325: superfluous parenthesis
    * C0209: consider using fstring
    * C3001: Lambda expression assigned to a variable
    * W1514: unspecified encoding
    * R1711: useless returns (for allowing empty iterators with
      return-yield)
    * Skip Unused argument errors when args
    * Skip Unused argument errors when kargs
    """

    def setUp(self):
        """
        Provide the test setup.
        """
        good_names = "ii,jj,kk,ll,nn,mm"
        good_names += ",i1,i2,i3,n1,n2,n3,ix,iy,iz,jx,jy,jz"
        good_names += ",dx,dy,dz,dt"
        good_names += ",fh,op,xp"
        self.pylint_args = {
            "good-names": good_names,
            "disable": "C0325,C0209,W1514,R1711,C3001",
        }

    def run_pylint(self, filename, local_settings={}):
        """
        Run linter test with our unit test settings for one specific
        filename.
        """
        args = []

        ignore_in_line = []
        if "ignore_in_line" in local_settings:
            ignore_in_line = local_settings["ignore_in_line"]
            del local_settings["ignore_in_line"]

        for elem in self.pylint_args.keys():
            args += ["--" + elem + "=" + self.pylint_args[elem]]

            if elem in local_settings:
                args[-1] = args[-1] + "," + local_settings[elem]
                del local_settings[elem]

        for elem in local_settings.keys():
            args += ["--" + elem + "=" + local_settings[elem]]

        args += [filename]

        obj = StringIO()
        reporter = pylint.reporters.text.ParseableTextReporter(obj)
        pylint.lint.Run(args, reporter=reporter, exit=False)

        error_list = []
        for elem in obj.getvalue().split("\n"):
            tmp = elem.replace("\n", "")

            if len(tmp) == 0:
                continue
            if tmp.startswith("***"):
                continue
            if tmp.startswith("---"):
                continue
            if tmp.startswith("Your code"):
                continue
            if "Unused argument 'args'" in tmp:
                continue
            if "Unused argument 'kwargs'" in tmp:
                continue

            do_continue = False
            for pattern in ignore_in_line:
                if pattern in tmp:
                    do_continue = True

            if do_continue:
                continue

            error_list.append(tmp)

        return error_list

    def test_folders_recursively(self):
        """
        Recursively run python linter test on all .py files of
        specified folders.
        """
        parent_folders = ["Examples", "qtealeaves"]
        skip_files = []
        error_list = []

        for elem in parent_folders:
            for root, dirnames, filenames in os.walk(elem):
                for filename in filenames:
                    if not filename.endswith(".py"):
                        continue

                    if filename in skip_files:
                        continue

                    target_file = os.path.join(root, filename)

                    target_attr = "get_settings_" + filename.replace(".py", "")
                    if hasattr(self, target_attr):
                        target_setting = self.__getattribute__(target_attr)()
                    else:
                        target_setting = {}

                    error_list_ii = self.run_pylint(
                        target_file, local_settings=target_setting
                    )

                    error_list += error_list_ii

        self.assertEqual(len(error_list), 0, "\n".join(error_list))

    # --------------------------------------------------------------------------
    #                          Settings for qtealeaves
    # --------------------------------------------------------------------------

    def get_settings_fortran_interfaces(self):
        """
        Linter for module ``fortran_interface.py``.

        **Details**

        We locally ignore:

        * R0912: too many branches
        * R0913: too many arguments
        * R0914: too many locals
        * R0915: too many statements
        * R1728: consider using generator
        * R1732: consider using with
        """
        local_settings = {
            "disable": "R0912,R0913,R0914,R0915,R1728,R1732",
            "good-names": "fh, dl, ii",
        }
        return local_settings

    def get_settings_simulation_setup(self):
        """
        Linter for module ``simulation_setup.py``

        **Details**

        We locally ignore:

        * C0302: too many lines
        * R0902: too many instance attributes
        * R0913: too many arguments
        * R0914: too many locals
        * R0915: too many statements
        * W0108: unnecesarry lambda
        * R1705: no else return
        * R1732: consider using with
        * R0912: too many branches
        * R1702: too many nested blocks
        """
        local_settings = {
            "disable": "C0302,R0902,R0912,R0913,R0914,R0915,R1702,R1705,R1732,W0108"
        }
        return local_settings

    def get_settings_hilbert_curvature(self):
        """
        Linter for module ``hilbert_curvature.py``

        **Details**

        We locally ignore:

        * C0302: too many lines
        * R0912: too many branches
        * R0913: too many arguments
        * R0914: too many local variables
        * R0915: too many statements
        * R1705: no else return
        * R1720: no else raise
        * W0612: redefined outer name
        * W1114: arguments out of order
        """
        local_settings = {
            "disable": "C0302,R0912,R0913,R0914,R0915,R1705,R1720,W0621,W1114",
            "good-names": "nx,ny,nz,xs,ys,zs,i1,i2,i3,j1,j2,j3",
        }
        return local_settings

    def get_settings_baseterm(self):
        """
        Linter for module ``baseterm.py``

        **Details**

        We locally ignore:

        * E1101: no member
        * R0913: too many arguments.
        """
        pattern_1 = (
            "W0223(abstract-method), _ModelTerm1D] Method "
            + "'get_interactions' is abstract in class '_ModelTerm' but "
            + "is not overridden"
        )
        local_settings = {
            "disable": "E1101,R0913",
            "good-names": "ll",
            "ignore_in_line": [pattern_1],
        }
        return local_settings

    def get_settings_localterm(self):
        """
        Linter for module ``localterm.py``

        **Details**

        We locally ignore:

        * R0912: too many branches.
        * R0913: too many arguments.
        """
        local_settings = {"disable": "R0912,R0913", "good-names": "ll"}
        return local_settings

    def get_settings_sparsematrixoperator(self):
        """
        Linter for module ``sparsematrixoperator.py``

        **Details**

        We locally ignore:

        * E1307: bad string format type
        * R0902: too many instance attributes
        """
        local_settings = {
            "disable": "E1307,R0902",
            "good-names": "ll,n1,n2,m1,m2,l1,l2",
        }
        return local_settings

    def get_settings_sparsematrixproductoperator(self):
        """
        Linter for module ``sparsematrixproductoperator.py``

        **Details**

        We locally ignore:

        * R0914: too many locals.
        """
        local_settings = {"disable": "R0914", "good-names": "ll"}
        return local_settings

    def get_settings_conv_params(self):
        """
        Linter for module ``conv_params.py``

        **Details**

        We locally ignore:

        * R0902: too many instance arguments.
        * R0913: too many arguments
        * R0914: too many locals
        """
        local_settings = {"disable": "R0902,R0913,R0914", "good-names": "ll"}
        return local_settings

    def get_settings_twobodyterm1d(self):
        """
        Linter for module ``twobodyterm1d.py``

        **Details**

        We locally ignore:

        * R0913: too many arguments
        * R0914: too many locals
        """
        pattern_1 = "Unused argument 'params'"
        local_settings = {
            "disable": "R0913,R0914",
            "good-names": "ix,jx,ll,bc",
            "ignore_in_line": [pattern_1],
        }
        return local_settings

    def get_settings_twobodyterm2d(self):
        """
        Linter for module ``twobodyterm2d.py``

        **Details**

        We locally ignore:

        * R0902: too many instance attributes
        * R0912: too many branches
        * R0913: too many arguments
        * R0914: too many locals
        """
        pattern_1 = "Unused argument 'params'"
        local_settings = {
            "disable": "R0902,R0912,R0913,R0914",
            "good-names": "ix,iy,jx,jy,ll,bc",
            "ignore_in_line": [pattern_1],
        }
        return local_settings

    def get_settings_plaquetteterm2d(self):
        """
        Linter for module ``plaquetteterm2d.py``

        **Details**

        We locally ignore:

        * R0902: too many instance attributes
        * R0912: too many branches
        * R0913: too many arguments
        * R0914: too many locals
        """
        pattern_1 = "Unused argument 'params'"
        local_settings = {
            "disable": "R0902,R0912,R0913,R0914",
            "good-names": "ll,x1,y1,x2,x3,x4,y2,y3,y4",
            "ignore_in_line": [pattern_1],
        }
        return local_settings

    def get_settings_blockterm2d(self):
        """
        Linter for module ``blockterm2d.py``

        **Details**

        We locally ignore:

        * R0913: too many arguments
        * R0914 : too many locals
        """

        pattern_1 = "Unused argument 'params'"
        local_settings = {
            "disable": "R0913,R0914",
            "good-names": "ll,ii",
            "ignore_in_line": [pattern_1],
        }
        return local_settings

    def get_settings_quantummodel(self):
        """
        Linter for module ``quantummodel.py``

        **Details**

        We locally ignore:

        * R0902: too many instance attributes
        * R0912: too many branches
        * R0913: too many arguments
        * R0914: too many locals
        * R0915: too many statements
        """
        local_settings = {
            "disable": "R0902,R0912,R0913,R0914,R0915",
            "good-names": "nx,ll",
        }
        return local_settings

    def get_settings_tensorproductoperator(self):
        """
        Linter for module ``tensorproductoperator.py``

        **Details**

        We locally ignore:

        * C0302: too many lines
        * R0902: too many instance attributes
        * R0912 : too many branches
        * R0913: too many arguments
        * R0914 : too many locals
        * R0915 : too many statements
        * W0212: protected access
        """
        local_settings = {
            "disable": "C0302,R0902,R0912,R0913,R0914,R0915,W0212",
        }
        return local_settings

    def get_settings_rydberg_model(self):
        """
        Linter for module ``rydberg_model.py``

        **Details**

        We locally ignore:

        * C0302: too many lines
        * E1101: no member
        * R0902: too many instance attributes
        * R0912: too many branches
        * R0913: too many arguments
        * R0914: too many locals
        * R1705: no else return
        * R1720: no else raise
        * R1732: consider using with
        * W0223: abstract method not overwritten, only for _ModelTerm1D
        * W0613: unused arguments
        * E1102, only for self.strength: if case checks explicitly
          if callable attribute is available.
        """
        pattern_1 = (
            "[E1102(not-callable), _ModelTerm.eval_strength] "
            + "self.strength is not callable"
        )
        pattern_2 = (
            "W0223(abstract-method), _ModelTerm1D] Method "
            + "'get_interactions' is abstract in class '_ModelTerm' but "
            + "is not overridden"
        )

        local_settings = {
            "disable": "C0302,E1101,R0902,R0912,R0913,R0914,R1705,R1720,R1732,W0613",
            "good-names": "ix,iy,iz,jx,jy,jz,ll,nx,bc",
            "ignore_in_line": [pattern_1, pattern_2],
        }
        return local_settings

    def get_settings_tnobservables(self):
        """
        Linter for module ``tnobservables.py``

        **Details**

        We locally ignore:

        * R0914: too many locals
        """
        local_settings = {"disable": "R0914"}
        return local_settings

    def get_settings_tnoperators(self):
        """
        Linter for module ``tnoperators.py``

        **Details**

        We locally ignore:

        * R0914: too many locals
        * W0108: unnecesarry lambda
        * R1705: no else return
        """
        pattern_1 = "Unused argument 'params'"
        local_settings = {"disable": "R0914,W0108,R1705"}
        return local_settings

    def get_settings_lattice_layout(self):
        """
        Linter for module ``lattice_layout.py``

        **Details**

        We locally ignore:

        * None
        """
        local_settings = {"good-names": "ix,iy,jx,jy"}
        return local_settings

    @staticmethod
    def get_settings___init__():
        """
        Linter for module ``__init__.py``

        **Details**

        We locally ignore:

        * C0411: wrong import order
        """
        local_settings = {"disable": "C0411"}
        return local_settings

    def get_settings_correlation(self):
        """
        Linter for module ``correlation.py``

        **Details**

        We locally ignore:

        * R0914: too many locals
        """
        local_settings = {"good-names": "j2,j3,j4", "disable": "R0914"}
        return local_settings

    def get_settings_custom_correlation(self):
        """
        Linter for module ``custom_correlation.py``

        **Details**

        We locally ignore:

        * R0913: too many arguments
        """
        local_settings = {"disable": "R0913"}
        return local_settings

    # --------------------------------------------------------------------------
    #                          Settings for examples
    # --------------------------------------------------------------------------

    @staticmethod
    def get_settings_BoseHubbard_1d_groundstate():
        """
        Linter settings for BoseHubbard_1d_groundstate example.

        **Details**

        We locally ignore:

        * R0914: too many locals
        * C0103: invalid name (module name only)
        """
        return {
            "disable": "R0914",
            "ignore_in_line": ["[C0103(invalid-name), ] Module name"],
        }

    @staticmethod
    def get_settings_BoseHubbard_2d_quench():
        """
        Linter settings for BoseHubbard_1d_groundstate example.

        **Details**

        We locally ignore:

        * R0914: too many locals
        * C0103: invalid name (module name only)
        """
        return {
            "disable": "R0914",
            "ignore_in_line": ["[C0103(invalid-name), ] Module name"],
        }

    @staticmethod
    def get_settings_QED_2d_groundstate():
        """
        Linter settings for QED_2d_groundstate example.

        **Details**

        We locally ignore:

        * R0914: too many locals
        * C0103: invalid name (module name only)
        """
        pattern_1 = "[C0103(invalid-name), ] Module name"
        return {"disable": "R0914", "good-names": "ll", "ignore_in_line": [pattern_1]}

    @staticmethod
    def get_settings_QuantumIsing_1d_groundstate():
        """
        Linter settings for QuantumIsing_1d_groundstate example.

        **Details**

        We locally ignore:

        * R0914: too many locals
        * C0103: invalid name (module name only)
        """
        return {
            "disable": "R0914",
            "ignore_in_line": ["[C0103(invalid-name), ] Module name"],
        }

    @staticmethod
    def get_settings_QuantumIsing_1d_quench():
        """
        Linter settings for QuantumIsing_1d_quench example.

        **Details**

        We locally ignore:

        * R0914: too many locals
        * C0103: invalid name (module name only)
        """
        return {
            "disable": "R0914",
            "ignore_in_line": ["[C0103(invalid-name), ] Module name"],
        }

    @staticmethod
    def get_settings_QuantumIsing_2d_groundstate():
        """
        Linter settings for QuantumIsing_2d_groundstate example.

        **Details**

        We locally ignore:

        * R0914: too many locals
        * C0103: invalid name (module name only)
        """
        return {
            "disable": "R0914",
            "ignore_in_line": ["[C0103(invalid-name), ] Module name"],
        }

    @staticmethod
    def get_settings_QuantumIsing_2d_groundstate_threaded():
        """
        Linter settings for QuantumIsing_2d_groundstate example.

        **Details**

        We locally ignore:

        * R0914: too many locals
        * C0103: invalid name (module name only)
        """
        return {
            "disable": "R0914",
            "ignore_in_line": ["[C0103(invalid-name), ] Module name"],
        }

    @staticmethod
    def get_settings_QuantumIsing_2d_quench():
        """
        Linter settings for QuantumIsing_2d_quench example.

        **Details**

        We locally ignore:

        * R0914: too many locals
        * C0103: invalid name (module name only)
        """
        return {
            "disable": "R0914",
            "ignore_in_line": ["[C0103(invalid-name), ] Module name"],
        }

    @staticmethod
    def get_settings_RydbergRb87_3d_groundstate():
        """
        Linter settings for 3d Rydberg statics example with
        long-range interactions.

        **Details**

        We locally ignore:

        * C0103: invalid name (module name only)
        """
        return {"ignore_in_line": ["[C0103(invalid-name), ] Module name"]}

    @staticmethod
    def get_settings_SpinGlass_1d_groundstate():
        """
        Linter settings for QuantumIsing_2d_quench example.

        **Details**

        We locally ignore:

        * R0914: too many locals
        * C0103: invalid name (module name only)
        """
        return {
            "disable": "R0914",
            "ignore_in_line": ["[C0103(invalid-name), ] Module name"],
        }

    @staticmethod
    def get_settings_XXZModel_1d_oqs():
        """
        Linter settings for XXZModel_1d_oqs example.

        **Details**

        We locally ignore:

        * R0914: too many locals
        * C0103: invalid name (module name only)
        """
        return {
            "disable": "R0914",
            "good-names": "ll",
            "ignore_in_line": ["[C0103(invalid-name), ] Module name"],
        }

    @staticmethod
    def get_settings_Simple_classification():
        """
        Linter settings for Simple_classification example.

        **Details**

        We locally ignore:

        * R0914: too many locals
        * C0103: invalid name
        * E1121: too-many-function-args
        """
        return {
            "disable": "C0103, R0914, E1121",
        }

    # --------------------------------------------------------------------------
    #                          Settings for emulator
    # --------------------------------------------------------------------------

    @staticmethod
    def get_settings_abstract_tn():
        """
        Linter settings for the abstract tensor network class.

        **Details**

        We locally ignore:

        * C0302: too many lines
        * R0902: too many instance attributes
        * R0903: too few public methods (class needs at least 2)
        * R0912: too many branches
        * R0913: too many arguments
        * R0914: too many locals
        * R0914: too many statements
        * R0904: too many public methods
        * R1705: no-else-return
        * I1101: c-extension-no-member
        * W0102: dangerous default value
        * W0108: unnecessary lambda
        """
        return {
            "disable": "C0302,R0902,R0903,R0912,R0913,R0914,R0915,R1705,R0904,I1101,W0108,W0102",
            "good-names": "tSVD,tEQR,ss,QR,sc",
        }

    @staticmethod
    def get_settings_mps_simulator():
        """
        Linter settings for mps simulator.

        **Details**

        We locally ignore:

        * R0902: too many instance attributes
        * R0904: too many public methods
        * R0912: too maby branhces
        * R0913: too many arguments
        * R0914: too many locals
        * R1720: no-else-raise
        * R1705: no-else-return
        * C0302: too-many-lines
        * W0212: protected-access
        """
        p1 = """Variable name "addMPS" doesn't conform to snake_case naming style"""
        p2 = """Access to a protected member _cut_ratio of a client class"""
        p3 = """Access to a protected member _singvals of a client class"""
        return {
            "disable": "R0902,R0904,R0912,R0913,R0914,R1720,R1705,C0302,W0212",
            "ignore_in_line": [p1, p2, p3],
            "good-names": "ii, jj, kk, ss, fh, op",
        }

    @staticmethod
    def get_settings_mpi_mps_simulator():
        """
        Linter settings for mpimps simulator.

        **Details**

        We locally ignore:

        * R0902: too many instance attributes
        * R0913: too many arguments
        * I1101: c-extension-no-member
        """
        return {
            "disable": "R0902,R0913,I1101",
            "good-names": "ii, jj, kk, cp, op",
        }

    @staticmethod
    def get_settings_ed_simulation():
        """
        Linter settings for ed simulations.

        **Details**

        We locally ignore:

        * R0913: too many arguments
        * R0914: too many locals
        """
        return {
            "disable": "R0913,R0914",
            "good-names": "ii,jj,kk,fh",
        }

    @staticmethod
    def get_settings_ttn_simulator():
        """
        Linter settings for TTN simulator.

        **Details**

        We locally ignore:

        * C0200: consider-using-enumerate
        * R0902: too many instance attributes
        * R0904: too many public methods
        * R0912: too many branches
        * R0913: too many arguments
        * R0914: too many locals
        * R0915: too many statements
        * C0302: too-many-lines
        * W0102 : dangerous default value
        * W0212: protected-access (needed to avoid duplicate code)
        """
        return {
            "disable": "C0200,C0302,R0902,R0904,R0912,R0913,R0914,R0915,W0102,W0212",
            "good-names": "ii, jj, kk,ll,i0,i1,i2,d0,d1,d2,p0,p1,sc",
        }

    @staticmethod
    def get_settings_attn_simulator():
        """
        Linter settings for TTN simulator.

        **Details**

        We locally ignore:

        * R0913: too many arguments
        * W0102 : dangerous default value
        -
        """
        return {
            "disable": "R0913,W0102",
            "good-names": "ii, jj, kk",
        }

    @staticmethod
    def get_settings_tto_simulator():
        """
        Linter settings for TTO simulator.

        **Details**

        We locally ignore:

        * C0302: too many lines
        * R0912: too many branches
        * R0913: too many arguments
        * R0914: too many locals
        * R0915: too many statements
        * W0105: pointless string statement (raises warning when using triple
          quotes for multiline comments)
        * R0904: too many public methods
        """
        return {
            "disable": "C0302,R0912,R0913,R0914,R0915,W0105,R0904",
            "good-names": "ii,jj,kk",
        }

    @staticmethod
    def get_settings_symmetrygroups():
        """
        Linter settings for symmetry groups

        **Details**

        We locally ignore:

        """
        return {
            "disable": "",
            "good-names": "ii,jj,kk,n1,n2,i1,i2",
        }

    @staticmethod
    def get_settings_abstracttensor():
        """
        Linter settings for abstract tensors.

        **Details**

        We locally ignore:

        * R0904 : too many public methods
        * R0913 : too many arguments
        * W0102 : dangerous default value
        """
        return {
            "disable": "R0904,R0913,W0102",
            "good-names": "ii,jj,kk,sc",
        }

    @staticmethod
    def get_settings_tensor():
        """
        Linter settings for tensors.

        **Details**

        We locally ignore:

        * C0302 : too many lines
        * R0904 : too many public methods
        * R0913 : too many arguments
        * R0914 : too many locals
        * W0102 : dangereous default values
        * W0212 : protected access
        """
        return {
            "disable": "C0302,R0904,R0913,R0914,W0102,W0212",
            "good-names": "ii,jj,kk,i1,i2,i3,j1,j2,k1,k2,d1,d2,d3,d4,r1,r2,c1,c2,sc",
        }

    @staticmethod
    def get_settings_abeliantensor():
        """
        Linter settings for Abelian tensors.

        **Details**

        We locally ignore:

        * C0302: too many lines
        * R0904 : too many public methods
        * R0912 : too many branches
        * R0913 : too many arguments
        * R0914 : too many locals
        * R0915 : too many statements
        * W0102 : dangereous default values
        * W0212 : protected access
        """
        return {
            "disable": "C0302,R0904,R0912,R0913,R0914,R0915,W0102,W0212",
            "good-names": "ii,jj,kk,j1,j2,k1,k2,cs,sc",
        }

    @staticmethod
    def get_settings_abelianlinks():
        """
        Linter settings for ....

        **Details**

        We locally ignore:

        * R0914 : too many locals

        """
        return {
            "disable": "R0914",
            "good-names": "ii,jj,kk,k1,k2,cs",
        }

    @staticmethod
    def get_settings_ibarrays():
        """
        Linter settings for ibarrays

        **Details**

        We locally ignore:

        """
        return {
            "disable": "",
            "good-names": "ii,jj,kk",
        }

    @staticmethod
    def get_settings_couplingsectors():
        """
        Linter settings for ....

        **Details**

        We locally ignore:

        * W0102 : dangerous default value
        """
        return {
            "disable": "W0102",
            "good-names": "d1,d2",
        }

    @staticmethod
    def get_settings_irreplistings():
        """
        Linter settings for irrep listing

        **Details**

        We locally ignore:

        * R0913: too many arguments
        """
        return {
            "disable": "R0913",
            "good-names": "ii,jj,kk,n2",
        }
