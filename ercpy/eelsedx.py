import ercpy.utils as ut
import numpy as np
import scipy as sc

__all__ = ['Nbr_compotokeep', 'VCA_decomposition']

from scipy.sparse.linalg import svds

def Nbr_compotokeep(hyperspy_signal, Prcent_to_keep):
    """
    Calculate the number of components you should use for the decomposition to keep more than "Prcent-to-keep"% of the original data
    Should be use AFTER decomposition has been performed
    """
    i = 0
    sum_up_to=hyperspy_signal.get_explained_variance_ratio().data[i]

    if (Prcent_to_keep<100):
	while (sum_up_to<Prcent_to_keep/100):
		i+=1
		sum_up_to+=hyperspy_signal.get_explained_variance_ratio().data[i]
    	if i==0:
		print "Use larger 'Prcent_to_keep' value to perform the decomposition"

    else:
	print "Keep less than 100% for the decomposition"

    return i

def VCA_decomposition(hyperspy_signal, nbr_compo, centering, normalization, whitening):
    """
    Perform the VCA decomposition of the dataset

    Transformation of the data can be performed (using fct_whitening in utils)

    Inputs:
	Data taken from hyperspy_signal.data
	nbr_compo: Number of dimensions on which you want to decompose your data (integer)
	Centering (default True): subtract the mean of the vectors along the signal direction
	Normalization (default True): Normalize the vectors to 1 along the signal direction
	whitening (default True)

    Outputs:
	Factors: 2D numpy array
        Loadings: 2D numpy array
    """

    T_data = ut.hspy_to_2Dnp(hyperspy_signal)

    if (centering==True):
	k=0
	while k < T_data.shape[0]:
		T_data[k,:]=(T_data[k,:]-np.mean(T_data[k,:]))
		k +=1

    if (normalization==True):
	k=0
	while k < T_data.shape[0]:
		T_data[k,:]=T_data[k,:]/sum(T_data[k,:])
		k +=1

    #Calculate the covariance matrix of T_data
    sigma = np.dot(T_data,np.transpose(T_data))/T_data[:,1].size

    U, S, V = svds(sigma, k=nbr_compo, which='LM', return_singular_vectors=True)

    del(sigma)
    del(V)
    U[:,:nbr_compo] = U[:, nbr_compo-1::-1]
    S = S[::-1]

    #Projection of the data matrix to the sub-space composed of nbr_compo dimensions
    xRot = np.dot(np.transpose(U),T_data)

    if (whitening==True):
	epsilon = 0.1
    	S_diag = np.empty([S.size,S.size],dtype="float64")
    	S_diag [:,:] = 0
    	i=0
	while i < S.size:
		S_diag[i,i] = 1/np.sqrt(S[i]+epsilon)
		i += 1
	xRot = np.dot(S_diag, xRot)

    del(S)
    del(S_diag)

    #Perform the VCA decomposition
    A = np.empty([nbr_compo,nbr_compo],dtype="float64")
    A[nbr_compo-1,0]=1

    indice = np.empty([nbr_compo],dtype="int")
    indice[:]=0

    w = np.empty([nbr_compo,1],dtype="float64")
    w[:,:]=0

    i=0
    while (i<nbr_compo):
	w = np.random.randn(nbr_compo,1)
	w= abs(w)
	#f = w-np.dot(np.dot(A,np.linalg.pinv(A)),w) #changed MD 23 oct 2015
	f = w-np.dot(np.dot(A,sc.linalg.pinv(A)),w)
	f = f / sc.linalg.norm(f)
	v = np.dot(np.transpose(f),xRot)
	indice[i] =  np.argmax(abs(v))
	A[:,i] = xRot[:,indice[i]]
	i += 1

    return np.dot(U,xRot[:,indice])
