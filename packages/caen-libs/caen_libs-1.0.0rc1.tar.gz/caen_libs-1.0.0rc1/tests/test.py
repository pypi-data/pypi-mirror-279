import timeit
repeat = 100
setup="from struct import pack; from random import random; import numpy;  from array import array; import ctypes; t = [random() for _ in range(2* 1000)];"
print(timeit.timeit(stmt="v = array('f',t); addr, count = v.buffer_info();x = ctypes.cast(addr,ctypes.POINTER(ctypes.c_float))",setup=setup,number=repeat))
print(timeit.timeit(stmt="v = array('f',t);a = (ctypes.c_float * len(v)).from_buffer(v)",setup=setup,number=repeat))
print(timeit.timeit(stmt='x = (ctypes.c_float * len(t))(*t)',setup=setup,number=repeat))
print(timeit.timeit(stmt="x = pack('f'*len(t), *t);",setup=setup,number=repeat))
print(timeit.timeit(stmt='x = (ctypes.c_float * len(t))(); x[:] = t',setup=setup,number=repeat))
print(timeit.timeit(stmt='x = numpy.array(t,numpy.float32).data',setup=setup,number=repeat))
