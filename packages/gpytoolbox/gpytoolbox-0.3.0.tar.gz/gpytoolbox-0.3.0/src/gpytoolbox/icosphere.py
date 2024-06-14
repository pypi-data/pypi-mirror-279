import numpy as np
from .subdivide import subdivide

def icosphere(n=0):
    """Returns an icosahedral sphere with a given subdivision level.

    Parameters
    ----------
    n : int, optional (default 0)
        the subdivision level

    Returns
    -------
    V : (n,3) numpy array
        vertex positions of the icosphere
    F : (m,3) numpy array
        face positions of the icosphere

    Examples
    --------
    ```python
    >>> import gpytoolbox as gpy
    >>> V,F = gpy.icosphere()
    >>> V
    array([[ 4.62592927e-18, -8.32667268e-17,  1.00000000e+00],
           [ 7.23606798e-01, -5.25731112e-01,  4.47213595e-01],
           [ 7.23606798e-01,  5.25731112e-01,  4.47213595e-01],
           [-2.76393202e-01,  8.50650808e-01,  4.47213595e-01],
           [-8.94427191e-01, -8.32667268e-17,  4.47213595e-01],
           [-2.76393202e-01, -8.50650808e-01,  4.47213595e-01],
           [ 8.94427191e-01, -8.32667268e-17, -4.47213595e-01],
           [ 2.76393202e-01,  8.50650808e-01, -4.47213595e-01],
           [-7.23606798e-01,  5.25731112e-01, -4.47213595e-01],
           [-7.23606798e-01, -5.25731112e-01, -4.47213595e-01],
           [ 2.76393202e-01, -8.50650808e-01, -4.47213595e-01],
           [ 4.62592927e-18, -8.32667268e-17, -1.00000000e+00]])
    >>> F
    array([[ 0,  1,  2],
           [ 0,  2,  3],
           [ 0,  3,  4],
           [ 0,  4,  5],
           [ 0,  5,  1],
           [ 1,  6,  2],
           [ 2,  7,  3],
           [ 3,  8,  4],
           [ 4,  9,  5],
           [ 5, 10,  1],
           [ 6,  7,  2],
           [ 7,  8,  3],
           [ 8,  9,  4],
           [ 9, 10,  5],
           [10,  6,  1],
           [ 6, 11,  7],
           [ 7, 11,  8],
           [ 8, 11,  9],
           [ 9, 11, 10],
           [10, 11,  6]])
    ```
    
    """

    # This function is similar to gptoolbox's subdivided_sphere.m by Alec
    # Jacobson:
    # https://github.com/alecjacobson/gptoolbox/blob/master/mesh/subdivided_sphere.m
    assert n>=0

    V = np.array([[0.,                          0.,                        1.],
        [0.723606797749979,        -0.525731112119134,         0.447213595499958],
         [0.723606797749979,         0.525731112119134,         0.447213595499958],
        [-0.276393202250021,          0.85065080835204,         0.447213595499958],
        [-0.894427190999916,                          0.,        0.447213595499958],
        [-0.276393202250021,         -0.85065080835204,         0.447213595499958],
        [ 0.894427190999916,                         0.,       -0.447213595499958],
        [ 0.276393202250021,          0.85065080835204,        -0.447213595499958],
        [-0.723606797749979,         0.525731112119134,        -0.447213595499958],
        [-0.723606797749979,        -0.525731112119133,        -0.447213595499958],
        [ 0.276393202250021,         -0.85065080835204,        -0.447213595499958],
        [                 0.,                         0.,                      -1]])
    V -= np.mean(V, axis=0)[None,:]
    V /= np.linalg.norm(V, axis=-1)[:,None]

    F = np.array([[0,     1,     2],
     [0,     2,     3],
     [0,     3,     4],
     [0,     4,     5],
     [0,     5,     1],
     [1,     6,     2],
     [2,     7,     3],
     [3,     8,     4],
     [4,     9,     5],
     [5,    10,     1],
     [6,     7,     2],
     [7,     8,     3],
     [8,     9,     4],
     [9,    10,     5],
    [10,     6,     1],
     [6,    11,     7],
     [7,    11,     8],
     [8,    11,     9],
     [9,    11,    10],
    [10,    11,     6]])

    for i in range(n):
        V,F = subdivide(V,F)
        V /= np.linalg.norm(V, axis=-1)[:,None]

    return V,F

