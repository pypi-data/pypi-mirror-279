# This code is part of qtealeaves.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Generic base class for operators.
"""

import os

# pylint: disable-next=no-name-in-module
import os.path
from collections import OrderedDict
from copy import deepcopy
import numpy as np

from qtealeaves.tooling import _ParameterizedClass
from qtealeaves import write_tensor, write_symtensor
from qtealeaves import StrBuffer


__all__ = ["TNOperators"]


class TNOperators(_ParameterizedClass):
    """
    Generic class to write operators. This class contains no pre-defined
    operators. It allows you to start from scratch if no other operator
    class fulfills your needs.

    **Arguments**

    folder_operators : str
        The name of the subfolder inside the input folder, where
        we store operators.
    """

    def __init__(self, folder_operators="SPIN12"):
        self.folder_operators = folder_operators
        self.ops = OrderedDict()

    def keys(self):
        """Return the keys of the underlying dictionary."""
        return self.ops.keys()

    def __getitem__(self, key):
        if isinstance(key, str) and isinstance(self.ops, list):
            raise Exception("Operators are site-dependent.")

        if isinstance(key, str):
            return self.ops[key]

        site_key, key = key

        if isinstance(self.ops, list):
            return self.ops[site_key][key]

        return self.ops[key]

    def write_operator(
        self, folder_dst, operator_name, params, tensor_backend, **kwargs
    ):
        """
        Write operator to file. Format depends on the tensor backend.

        **Arguments**

        folder_dst : str or filehandle
            If filehandle, write there. If string, it defines the folder.

        operator_name : str
            Name of the operator.

        params : dictionary
            Contains the simulation parameters.

        kwargs : passed to write_symtensor

        """
        if operator_name not in self.ops:
            raise Exception("Operator `%s` not defined." % (operator_name))

        if tensor_backend == 1:
            return self.write_operator_abeliansym(
                folder_dst, operator_name, params, **kwargs
            )
        elif tensor_backend == 2:
            self.write_operator_dense(folder_dst, operator_name, params)
            return None
        else:
            raise Exception("Unknown tensor backend %d." % (tensor_backend))

    def write_operator_dense(self, folder_dst, operator_name, params):
        """
        Write dense tensor based on the numpy array.

        **Arguments**

        see write_operator
        """
        if hasattr(folder_dst, "write"):
            # filehandle
            full_filename = folder_dst
        else:
            # pylint: disable-next=no-member
            full_filename = os.path.join(folder_dst, operator_name + ".dat")

        op_mat = self.get_operator(operator_name, params)

        write_tensor(op_mat, full_filename)

        return operator_name + ".dat"

    def write_operator_abeliansym(self, folder_dst, operator_name, params, **kwargs):
        """
        Write an abelian symmetry tensor based on the parameter dictionary,
        which has to provide the definitions of the symmetry, i.e., generators
        and symmetry type.

        **Arguments**

        see write_operator
        """
        if hasattr(folder_dst, "write"):
            # filehandle
            dst = folder_dst
        else:
            # pylint: disable-next=no-member
            dst = os.path.join(folder_dst, operator_name + ".dat")

        op_mat = self.get_operator(operator_name, params)

        sector = params.get("SymmetrySectors", None)
        generators = params.get("SymmetryGenerators", None)
        gen_types = params.get("SymmetryTypes", None)

        if (sector is None) and (generators is None) and (gen_types is None):
            sector = []
            generators = [0 * op_mat]
            gen_types = "U"
        elif (
            (sector is not None)
            and (generators is not None)
            and (gen_types is not None)
        ):
            length_sectors = len(sector)
            length_generators = len(generators)
            length_symmetry_types = len(gen_types)

            if (length_sectors != length_generators) or (
                length_generators != length_symmetry_types
            ):
                raise Exception("Symmetry specifications must be of equal length.")
        else:
            raise NotImplementedError("Incomplete definition of symmetry.")

        generator_matrices = []
        for elem in generators:
            if isinstance(elem, str):
                op_ii = self.get_operator(elem, params)
            elif isinstance(elem, np.ndarray):
                op_ii = elem
            else:
                raise Exception("Unknown data type for generator.")

            generator_matrices.append(op_ii)

        op_info = write_symtensor(op_mat, dst, generator_matrices, gen_types, **kwargs)
        # if(hasattr(folder_dst, 'write')):
        #    tmp = 'check_op_' + operator_name + '.dat'
        #    write_symtensor(op, tmp, generator_matrices, gen_types, **kwargs)

        # Check if argument is set (v3 onwards)
        if kwargs.get("op_info", False):
            return op_info

        # legacy version: return filename (v1 and v2)
        return operator_name + ".dat"

    def get_operator(self, operator_name, params):
        """
        Provide a method to return any operator, either defined via
        a callable or directly as a matrix.

        **Arguments**

        operator_name : str
            Tag/identifier of the operator.

        params : dict
            Simulation parameters as a dictionary; dict is passed
            to callable.
        """
        if hasattr(self.ops[operator_name], "__call__"):
            op_mat = self.ops[operator_name](params)
        else:
            op_mat = self.ops[operator_name]

        return op_mat

    def write_input(self, folder_name, params, tensor_backend, required_operators):
        """
        Write the input for each operator.

        **Arguments**

        folder_name : str
            Folder name with all the input files; will be extended
            by the subfolder with the operators.

        params : dict
            Dictionary with the simulation parameters.

        tensor_backend : integer
            The integer flag indicates if ``AbelianSymTensors`` or
            ``Tensors`` should be written to the input files.

        required_operators : list
            List of operators keys which is needed for AbelianSymTensors,
            where we distinguish between left, right, center, and independent
            operators.
        """
        # pylint: disable-next=no-member
        full_path = os.path.join(folder_name, self.folder_operators)
        # pylint: disable-next=no-member
        if not os.path.isdir(full_path):
            # pylint: disable-next=no-member
            os.makedirs(full_path)

        # pylint: disable-next=no-member
        relative_file = os.path.join(full_path, "operators.dat")
        buffer_str = StrBuffer()

        operator_id_mapping = {}

        ii = 0
        for operator_ii in self.ops.keys():
            ii += 1
            op_info = self.write_operator(
                buffer_str, operator_ii, params, tensor_backend, op_info=True
            )

            operator_id_mapping[(operator_ii, op_info)] = ii

        if tensor_backend == 1:
            # Need to provide all operators
            required_operators_ = deepcopy(required_operators)
            required_operators_.sort(key=lambda xx: str(xx))

            for elem in operator_id_mapping:
                if elem not in required_operators_:
                    continue

                required_operators_.remove(elem)

            for elem in required_operators_:
                ii += 1
                op_info = self.write_operator(
                    buffer_str, elem[0], params, tensor_backend, add_links=elem[1]
                )

                operator_id_mapping[elem] = ii

            # Aposterio length because added operator are written
            nn = len(operator_id_mapping)
        else:
            # Provide keys for 'l', 'r' (tensor unchanged without symmetry)

            # Apriori length because operators are not written
            nn = len(operator_id_mapping)

            for key in list(operator_id_mapping.keys()):
                idx = operator_id_mapping[key]

                operator_id_mapping[(key[0], "l")] = idx
                operator_id_mapping[(key[0], "r")] = idx

        with open(relative_file, "w+") as fh:
            fh.write(str(nn) + "\n")
            fh.write(buffer_str())

        return relative_file, operator_id_mapping
