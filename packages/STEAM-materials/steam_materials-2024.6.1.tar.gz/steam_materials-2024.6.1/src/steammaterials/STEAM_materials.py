import ctypes as ct
import os
import platform
import numpy as np
from pathlib import Path
from numpy.ctypeslib import ndpointer
#import matlab.engine


class STEAM_materials:

    def __init__(self, func_name, n_arg, n_points, material_objects_path: os.PathLike=None):
        """
        :param func_name: string with function name corresponding to dll file name (without the .dll in the string)
        :param n_arg:	number of arguments of the func_name function. This corresponds to number of columns in 2D numpy array, numpy2d, to be used in the method. Use numpy2d.shape[1] to get the number.
        :param n_points: number of points to evaluate. This corresponds to number of rows in 2D numpy array, numpy2d, to be used in the eval method. Use numpy2d.shape[0] to get the number.
        :param material_objects_path: If not specified, the code assumes the .dll files are in a folder called CFUN in the same directory as this script. Otherwise a full path to a folder needs to be given.
        """
        if material_objects_path is not None:
            dll_path: Path = Path(material_objects_path)  # allows user to specify full path to folder with .dlls
        else:
            dll_path: Path = Path(__file__).parent / 'CFUN'  # Assumes .dlls are in a folder called CFUN in the same directory as this script

        if platform.system() == 'Windows':
            self._dll_name = f'{func_name}.dll'
        elif platform.system() == 'Linux':
            self._dll_name = f'lib{func_name}.so'
        else:
            raise NotImplementedError(f'Platform "{platform.system()}" is not supported!')

        _dll = ct.CDLL(str(dll_path / self._dll_name))
        self.func_name = func_name.encode('ascii')
        self.n_points = n_points
        self.n_arg = n_arg
        array_type = ct.c_double * self.n_points
        self.RealPtr = array_type()
        self.Int_Ptr = array_type()
        _doublepp = ndpointer(dtype=np.uintp, ndim=1, flags='C')
        f_name = ct.c_char_p
        n_arg = ct.c_int
        b_size = ct.c_int
        ifail = ct.c_long
        _dll.init.argtypes = []
        _dll.init.restype = ct.c_long
        self.eval = _dll.eval
        self.eval.argtypes = [f_name, n_arg, _doublepp, _doublepp, b_size, array_type, array_type]
        self.eval.restype = ifail

    def evaluate(self, numpy2d):
        """
        DLL funcion call. It can take a tuple with arguments or numpy array where each row is a set of arguments
        :param numpy2d: Numpy array with number of columns corresponding to number of function arguments and points to evaluate in rows
        :return: Numpy array with values calculated by .dll function
        """
        inReal = (numpy2d.__array_interface__['data'][0] + np.arange(numpy2d.shape[0]) * numpy2d.strides[0]).astype(np.uintp)
        error_out = self.eval(self.func_name, self.n_arg, inReal, inReal, self.n_points, self.RealPtr, self.Int_Ptr)
        if error_out == 1:
            pass
        else:
            raise ValueError(f"There was a problem with calling {self._dll_name} with arguments {numpy2d}. Check if library file exists or if number of arguments is correct.")
        return np.array(self.RealPtr)

class STEAM_materials_Matlab:
    def __init__(self,func_name:str,arg_list:str):
        self.arguments=arg_list
        self.func=func_name


    def evaluate(self):
        eng = matlab.engine.start_matlab()
        result=eng.eval(self.func+self.arguments)
        print(result)

if __name__ == "__main__":
   # STEAM_materials_Matlab("rhoCu_nist","(1.8,1,120.0,5)").evaluate()



    func_4d = 'CFUN_rhoCuNIST'  # function name, this one takes 4 arguments as input and returns a single float for resistivity
    T_min = 1.8
    T_max = 300
    B = 1.
    RRR = 120.0
    T_ref_RRR = 273.
    num_elem = 1000
    T = np.linspace(T_min, T_max, num_elem)

    # make numpy array
    numpy2d = np.vstack((T, np.ones(num_elem) * B, np.ones(num_elem) * RRR, np.ones(num_elem) * T_ref_RRR))

    # make dll func object
    sm = STEAM_materials(func_4d, numpy2d.shape[0], numpy2d.shape[1], r'G:\Projects\lhccm\STEAM\MaterialsLibrary\V0.1')

    # call with 2D numpy array and get results back
    result_numpy = sm.evaluate(numpy2d)
    print(result_numpy)
