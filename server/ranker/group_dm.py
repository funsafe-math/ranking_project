import numpy as np

__all__ = ['AIJ', 'AIP']


#AIJ - używa się przed stworzeniem rankingu
#Z wykładu: use it when different decision makers use the same internal criteria
class AIJ:
    def __init__(self):
        pass

    def group_matrices(self,decisions):
        result = np.ones(decisions[0].shape)
        for i in range(decisions[0].shape[0]):
            for j in range(decisions[0].shape[1]):
                result[i][j] = np.prod([decision[i][j] for decision in decisions])
                result[i][j] = np.power(result[i][j], 1/len(decisions))
        return result

    def __call__(self, *args, **kwargs):
        return self.group_matrices(*args, **kwargs)
        pass

#AIP - używa się po stworzeniu rankingu
#Z wykładu: use it when different decision makers use different internal criteria
class AIP:
    def __init__(self):
        pass

    def group_rankings(self,decisions):
        result = np.ones(len(decisions[0]))
        for i,decision in enumerate(decisions):
            result *= decision
        result = np.power(result, (1/len(decisions)))
        return result

    def __call__(self, *args, **kwargs):
        return self.group_rankings(*args, **kwargs)
        pass
