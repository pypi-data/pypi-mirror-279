from .tensor import Tensor

def matmul(tensor1, tensor2):
    result = np.dot(tensor1.data, tensor2.data)
    return Tensor(result)