import fastremap
import numpy as np 

x = np.ones((1700,1700,1700), dtype=np.uint8)
uniq, cts = fastremap.unique(x, return_counts=True)
print(uniq, cts)

print(cts[0] / 2**32)


# @profile
# def run():
#   x = np.ones( (512,512,512), dtype=np.uint32, order='C')
#   x += 1
#   print(x.strides, x.flags)
#   y = np.asfortranarray(x)
#   print(x.strides, x.flags)

#   print("done.")

# run()