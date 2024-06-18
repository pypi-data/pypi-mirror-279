import pycuda.autoinit
import pycuda.driver as drv
from pycuda.compiler import SourceModule
import numpy as np

def vector_add(a, b, n):
    mod = SourceModule("""
    __global__ void vector_add(float *a, float *b, float *c, int n) {
        int index = threadIdx.x + blockIdx.x * blockDim.x;
        if (index < n) {
            c[index] = a[index] + b[index];
        }
    }
    """)
    
    vector_add = mod.get_function("vector_add")
    a_gpu = drv.mem_alloc(a.nbytes)
    b_gpu = drv.mem_alloc(b.nbytes)
    c_gpu = drv.mem_alloc(a.nbytes)
    drv.memcpy_htod(a_gpu, a)
    drv.memcpy_htod(b_gpu, b)
    
    vector_add(a_gpu, b_gpu, c_gpu, np.int32(n), block=(256,1,1), grid=(n//256+1,1))
    
    c = np.empty_like(a)
    drv.memcpy_dtoh(c, c_gpu)
    return c