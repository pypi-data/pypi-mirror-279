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
Observable to measure the probabilities of the final state of the MPS
"""

from .tnobase import _TNObsBase

__all__ = ["TNObsProbabilities"]


class TNObsProbabilities(_TNObsBase):
    r"""
    Observable to measure the probabilities of the state configurations
    at the end of an evolution. The probabilities are computed following
    a probability tree, where each node is a site, and has a number of
    childs equal to the local dimension :math:`d` of the site. We keep
    track of the probabilities of the paths from the root to the leaves.
    The leaves identify the final state. For example, a state written as

    .. math::
        |\psi\rangle = \sqrt{N}\left(|00\rangle + |01\rangle
        + 2|11\rangle\right)

    with :math:`N=\frac{1}{6}` will have the following
    probability tree. Branches going left measures :math:`0` while
    branches on the right measures :math:`1`. The ordering here is
    the right-most site being the index-0 site.

    .. code-block::

                   ----o----             # No measure, state s2,s1
            p=1/6/            \p=5/6     # First measure, states s2,0 or s2,1
                o              o
         p=1/6/   \p=0  p=1/6/   \p=4/6  # Second measure, states 0,0 or 0,1 or 1,1
             00   10        01   11

    There are three possible ways of computing the probability:

    - Going down **evenly** on the tree, which means following ALL possible paths
      at the same time, and discarding paths which probability is below an input
      threshold :math:`\epsilon`. You might have no outputs, if all the branches
      has a probability :math:`p<\epsilon`.
    - Going down **greedily** on the tree, which means following each time the path
      with highest probability, until the total probability measured is more then
      a threshold :math:`\mathcal{E}`. This procedure is dangerous, since it can
      take an exponentially-long time if :math:`\mathcal{E}` is too high.
    - Going down **unbiasedly** on the tree, which means drawing a ``num_sumples``
      uniformly distributed random numbers :math:`u\sim U(0,1)` and ending in the
      leaf which probability interval :math:`[p_{\mathrm{low}}, p_{\mathrm{high}}]`
      is such that :math:`u\in [p_{\mathrm{low}}, p_{\mathrm{high}}]`. This is the
      suggested method. See http://arxiv.org/abs/2401.10330 for additional details.

    The result of the observable will be a dictionary where:

    - the keys are the measured state on a given basis
    - the values are the probabilities of measuring the key for the **even** and
      **greedy** approach, while they are the probability intervals for the
      **unbiased** approach.

    Parameters
    ----------
    prob_type: str, optional
        The type of probability measure. Default to 'U'. Available:
        - 'U', unbiased
        - 'G', greedy
        - 'E', even. Also implemented in Fortran backend
    num_samples: int, optional
        Number of samples for the unbiased prob_type. Default to 100.
        If a list is passed, the function is called multiple times with that list of
        parameters.
    prob_threshold: float, optional
        probability treshold for `prob_type=('G', 'E')`. Default to 0.9.
    qiskit_convention : bool, optional
        If you should use the qiskit convention when measuring, i.e. least significant qubit
        on the right. Default to False.
    """

    def __init__(
        self,
        prob_type="U",
        num_samples=100,
        prob_threshold=0.9,
        qiskit_convention=False,
    ):
        self.prob_type = [prob_type.upper()]
        self.qiskit_convention = [qiskit_convention]

        if prob_type == "U":
            self.prob_param = [num_samples]
            name = ["unbiased_probability"]
        elif prob_type == "E":
            self.prob_param = [prob_threshold]
            name = ["even_probability"]
        elif prob_type == "G":
            self.prob_param = [prob_threshold]
            name = ["greedy_probability"]
        else:
            raise ValueError(
                f"Probability types can only be U, G or E. Not {prob_type}"
            )

        _TNObsBase.__init__(self, name)

    def __len__(self):
        """
        Provide appropriate length method
        """
        return len(self.prob_type)

    def __iadd__(self, other):
        """
        Documentation see :func:`_TNObsBase.__iadd__`.
        """
        if isinstance(other, TNObsProbabilities):
            self.prob_type += other.prob_type
            self.prob_param += other.prob_param
            self.name += other.name
            self.qiskit_convention += other.qiskit_convention
        else:
            raise Exception("__iadd__ not defined for this type.")

        return self

    @classmethod
    def empty(cls):
        """
        Documentation see :func:`_TNObsBase.empty`.
        """
        obj = cls()
        obj.prob_type = []
        obj.prob_param = []
        obj.name = []
        obj.qiskit_convention = []

        return obj

    def read(self, fh, **kwargs):
        """
        Read the measurements of the projective measurement
        observable from fortran.

        Parameters
        ----------

        fh : filehandle
            Read the information about the measurements from this filehandle.
        """
        fh.readline()  # separator
        is_meas = fh.readline().replace("\n", "").replace(" ", "")
        self.is_measured = is_meas == "T"

        for ii, name in enumerate(self.name):
            if self.is_measured:
                num_lines = int(fh.readline().replace("\n", ""))
                measures = {}
                for _ in range(num_lines):
                    line = fh.readline().replace("\n", "")
                    words = line.replace(" ", "").split("|")
                    if self.prob_type[ii] == "U":
                        bounds = words[1].replace("(", "").replace(")", "")
                        bounds = bounds.split(",")
                        measures[words[0]] = [float(bounds[0]), float(bounds[1])]
                    else:
                        measures[words[0]] = float(words[1])
                yield name, measures
            else:
                yield name, None

    def write(self, fh, **kwargs):
        """
        Write fortran compatible definition of observable to file.

        Parameters
        ----------

        fh : filehandle
            Write the information about the measurements to this filehandle.
        """

        str_buffer = "------------------- tnobsprobabilities\n"

        str_buffer += "%d\n" % (len(self.prob_type))
        for ii, prob_type in enumerate(self.prob_type):
            str_buffer += prob_type + "\n"
            str_buffer += "%d\n" % (self.prob_param[ii])

        fh.write(str_buffer)

        return

    def write_results(self, fh, is_measured, **kwargs):
        """
        Documentation see :func:`_TNObsBase.write_results`.
        """
        # Write separator first
        fh.write("-" * 20 + "tnobsprobabilities\n")
        # Assignment for the linter
        _ = fh.write("T \n") if is_measured else fh.write("F \n")

        if is_measured:
            for name_ii in self.name:
                fh.write(str(len(self.results_buffer[name_ii])) + "\n")
                for key, value in self.results_buffer[name_ii].items():
                    fh.write(f"{key} | {value} \n")
