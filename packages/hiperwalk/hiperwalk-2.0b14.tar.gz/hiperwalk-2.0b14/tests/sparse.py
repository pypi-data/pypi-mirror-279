import numpy as np
import scipy.sparse as ss

M = ss.random(2000, 2000, format='csr')

A = ss.lil_matrix(np.zeros((2000, 2000)))

row = 0
next_row_ind = M.indptr[1]
for i in range(len(M.data)):
    while i == next_row_ind:
        row += 1
        next_row_ind = M.indptr[row + 1]
        
    col = M.indices[i]
    A[row, col] = M[row, col].real +1j*M[row, col].imag

A = A.tocsr()

print((A - M).nnz)
