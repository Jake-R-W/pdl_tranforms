import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import astropy.units as units
from abc import ABC, abstractmethod
from scipy.spatial.transform import Rotation as R

class Transforms(ABC):

    def __init__(self, name: str, input_coord: np.array, input_unit: units,
                 output_coord: np.array, output_unit: units, parameters: dict,
                 inverted_flag: bool, reverse_flag: bool, input_dim: int=None,
                 output_dim: int=None):
        """
        :type name: str
        :type input_coord: np.array
        :type input_unit: astropy.units
        :type output_coord: np.array
        :type output_unit: astropy.units
        :type parameters: dict
        :type inverted_flag: bool
        :type reverse_flag: bool
        :type input_dim: int
        :type output_dim: int
        """
        self.name = name
        self.input_coord = input_coord
        self.input_unit = input_unit
        self.output_coord = output_coord
        self.output_unit = output_unit
        self.parameters = parameters
        self.inverted_flag = inverted_flag
        self.reverse_flag = reverse_flag
        self.input_dim = input_dim
        self.output_dim = output_dim

    def composition(self):
        pass

    def inverse(self):
        pass

    @abstractmethod
    def apply(self, data, backward=0):
        pass

    def invert(self, data):
        return self.apply(data, backward=1)

    def map(self, data=None, template=None, pdl=None, opts=None):
        pass

    def match(self, pdl, opts=None):
        return self.map(pdl=pdl, opts=opts)

    def __parse(self, defaults, uopts=None):
        return_dict = defaults.copy()
        if uopts is None:
            return return_dict
        for k in defaults.keys():
            for r in uopts.keys():
                if k == r and uopts[r] is not None:
                    return_dict[k] = uopts[r]

        return return_dict


class t_identity(Transforms):
    """
    Return Copy of OG data with apply
    """

    def __init__(self, input_coord=None, input_unit=None, output_coord=None,
                         output_unit=None, parameters=None, inverted_flag=None,
                         reverse_flag=None, input_dim=0, output_dim=0):
        super().__init__("identity", input_coord=input_coord, input_unit=input_unit, output_coord=output_coord,
                         output_unit=output_unit, parameters=parameters, inverted_flag=inverted_flag,
                         reverse_flag=reverse_flag, input_dim=input_dim, output_dim=output_dim)

    def apply(self, data, backward=0):
        pass


class t_linear(Transforms):
    """
    parameter is a dict with the keys:

    matrix: a numpy.array. The transformation matrix. It does not even have to be square, if you want to change
        the dimensionality of your input. If it is invertible (note: must be square for that), then you automagically
        get an inverse transform too.

    rot: a rotation angle in degrees, another numpy.array. If it is one value, it is a scalar.

    scale: A scaling matrix, or a scalar. another numpy.array or a scalar

    pre: The vector to be added to the data before they get multiplied by the matrix
        (equivalent of CRVAL in FITS, if you are converting from scientific to pixel units).

    post: The vector to be added to the data after it gets multiplied by the matrix (equivalent of CRPIX-1 in FITS,
        if youre converting from scientific to pixel units).

    dims:Most of the time it is obvious how many dimensions you want to deal with: if you supply a matrix, it defines
        the transformation; if you input offset vectors in the pre and post options, those define the number of
        dimensions. But if you only supply scalars, there is no way to tell and the default number of dimensions is 2.
        This provides a way to do, e.g., 3-D scaling: just set {s=<scale-factor>, dims=>3}> and you are on your way.

    """

    def __init__(self, input_coord: np.array, input_unit: units,
                 output_coord: np.array, output_unit: units, parameters: dict,
                 inverted_flag: bool, reverse_flag: bool, input_dim: int,
                 output_dim: int):
        # this basic implementation doesn't deal with all the cases you see in PDL. They will be implemented later
        # params = {"matrix": None, "scale": None, "rot": 0, "pre": None, "post": None, "dims": None}



        super().__init__("t_linear", input_coord, input_unit, output_coord,
                         output_unit, parameters, inverted_flag,
                         reverse_flag, input_dim, output_dim)

        # Figuring out the number of dimensions to transform, and, if necessary, generate a new matrix
        if self.parameters['matrix'] is not None:
            self.input_dim = self.parameters['matrix'].shape[0]
            self.output_dim = self.parameters['matrix'].shape[1]
        else:
            if self.parameters['rot'] is not None and type(self.parameters['rot']) is np.ndarray:
                if self.parameters['rot'].size == 1:
                    self.input_dim = self.output_dim = 2
                elif self.parameters['rot'].size == 3:
                    self.input_dim = self.output_dim == 3

            if self.parameters['scale'] is not None and type(self.parameters['scale']) is np.ndarray:
                self.input_dim = self.output_dim = self.parameters['scale'].shape[0]
                # look at craig's response to email about this
            elif self.parameters['pre'] is not None and type(self.parameters['pre']) is np.ndarray:
                self.input_dim = self.output_dim = self.parameters['pre'].shape[0]
            elif self.parameters['post'] is not None and type(self.parameters['post']) is np.ndarray:
                self.input_dim = self.output_dim = self.parameters['post'].shape[0]
            elif self.parameters['dims'] is not None:
                self.input_dim = self.output_dim = self.parameters['dims']
            else:
                print("Assuming 2-D transform(set dims options)")
                self.input_dim = self.output_dim = 2;

            self.parameters['matrix'] = np.zeros([self.input_dim, self.output_dim])
            np.fill_diagonal(self.parameters['matrix'], 1)


        # Handle rotation option
        rot = self.parameters['rot']
        if rot is not None:



        # applying scaling
        if self.parameters['scale'] is not None and type((self.parameters['scale']) is not np.ndarray):

            for j in range(self.parameters['matrix'].shape[0]):
                self.parameters['matrix'][j][j] *= self.parameters['scale']

        elif type(self.parameters['scale']) is np.ndarray:
            if np.ndim(self.parameters['scale']) > 1:




    def apply(self, data, backwards=0):
        pass
