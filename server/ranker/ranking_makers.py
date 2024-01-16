import numpy as np
from .group_dm import *

__all__ = ['EVM', 'GMM', 'WCSM', 'SSCSM']

class EVM:
    def __init__(self):
        pass

    def evaluate_multiple(self, matrices, group_method = None):
        if len(matrices.shape) != 3:
            raise TypeError("Wrong usage! The function expects table of matrices: [list of matrices][1st dimension][2nd dimension]. If you want to evaluate single matrix, use EVM.evaluate()")
        if group_method is None:
            raise ValueError("Group method not provided. Use \"AIJ\" or \"AIP\"")
        if group_method == "AIJ":
            aij = AIJ()
            return self.evaluate(aij(matrices))
        if group_method == "AIP":
            results = []
            for i in matrices:
                results.append(self.evaluate(i))
            aip = AIP()
            return aip(results)
        raise ValueError("Unsupported or nonexistant grouping method: " + group_method)

    def evaluate(self, matrix, group_method = None):
        if len(matrix.shape) == 3:
            return self.evaluate_multiple(matrix, group_method)
        if len(matrix.shape) != 2:
            raise TypeError("Wrong usage! The function expects a matrix: [1st dimension][2nd dimension]")
        w, v = np.linalg.eig(matrix)
        w = np.real(w)
        w = np.abs(w)
        max_index = np.where(w == np.max(w))[0][0]
        v = v[:,max_index]
        v = v / np.sum(v)
        v = np.real(v)
        return v

    def __call__(self, matrix, *args, **kwargs):
        return self.evaluate(matrix, *args, **kwargs)
        pass

class GMM:
    def __init__(self):
        pass

    def evaluate_multiple(self, matrices, group_method = None):
        if len(matrices.shape) != 3:
            raise TypeError("Wrong usage! The function expects table of matrices: [list of matrices][1st dimension][2nd dimension]. If you want to evaluate single matrix, use EVM.evaluate()")
        if group_method is None:
            raise ValueError("Group method not provided. Use \"AIJ\" or \"AIP\"")
        if group_method == "AIJ":
            aij = AIJ()
            return self.evaluate(aij(matrices))
        if group_method == "AIP":
            results = []
            for i in matrices:
                results.append(self.evaluate(i))
            aip = AIP()
            return aip(results)
        raise ValueError("Unsupported or nonexistant grouping method: " + group_method)

    def evaluate(self, matrix, group_method = None):
        if len(matrix.shape) == 3:
            return self.evaluate_multiple(matrix, group_method)
        if len(matrix.shape) != 2:
            raise TypeError("Wrong usage! The function expects a matrix: [1st dimension][2nd dimension]")
        w = np.ndarray(matrix.shape[0])
        for i in range(matrix.shape[0]):
            w[i] = np.prod(matrix[i])
            w[i] = np.power(w[i], 1.0 / matrix.shape[0])
        w = w / np.sum(w)
        w = np.real(w)
        return w

    def __call__(self, matrix, *args, **kwargs):
        return self.evaluate(matrix, *args, **kwargs)
        pass

# dalej eksperymentalne - nie mają automatycznego grupowania

class WCSM:
    def __init__(self):
        pass

    def evaluate(self, matrix, *args, **kwargs):
        w = np.ndarray(matrix.shape[0])
        for i in range(matrix.shape[0]):
            w[i] = np.sum(matrix[i])
            w[i] /= matrix.shape[0]
        w = w / np.sum(w)
        return w

    def __call__(self, matrix, *args, **kwargs):
        return self.evaluate(matrix, *args, **kwargs)
        pass

class SSCSM:
    def __init__(self):
        pass

    def evaluate(self, matrix, *args, **kwargs):
        w = np.ndarray(matrix.shape[0])
        for i in range(matrix.shape[0]):
            w[i] = np.sum([matrix[i][j]/np.sum([matrix[k][j] for k in range(matrix.shape[0])]) for j in range(matrix.shape[0])])
            w[i] /= matrix.shape[0]
        w = w / np.sum(w)
        return w

    def __call__(self, matrix, *args, **kwargs):
        return self.evaluate(matrix, *args, **kwargs)
        pass
