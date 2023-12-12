import numpy as np

__all__ = ['EVM', 'GMM', 'WCSM', 'SSCSM']

class EVM:                             #nie działa
    def __init__(self):
        pass

    def evaluate(self, matrix, *args, **kwargs): #todo
        w, v = np.linalg.eig(matrix)
        w = np.real(w)
        w = np.abs(w)
        max_index = np.where(w == np.max(w))[0][0]
        v = v[:,max_index]
        v = v / np.sum(v)
        return v

    def __call__(self, matrix, *args, **kwargs):
        return self.evaluate(matrix, *args, **kwargs)
        pass

class GMM:
    def __init__(self):
        pass

    def evaluate(self, matrix, *args, **kwargs):
        w = np.ndarray(matrix.shape[0])
        for i in range(matrix.shape[0]):
            w[i] = np.prod(matrix[i])
            w[i] = np.power(w[i], 1.0 / matrix.shape[0])
        w = w / np.sum(w)
        return w

    def __call__(self, matrix, *args, **kwargs):
        return self.evaluate(matrix, *args, **kwargs)
        pass

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
