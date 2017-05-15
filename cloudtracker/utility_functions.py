import numpy as np

from .load_config import c

nx = c.nx
ny = c.ny
nz = c.nz

#---------------------------------

def index_to_zyx(index):
    z = np.floor_divide(index, (ny * nx))
    index = np.mod(index, (ny * nx))
    y = np.floor_divide(index, (nx))
    x = np.mod(index, nx)
    return (z, y, x)

# @numba.jit
# def index_to_zyx(index):
#     z = index // (ny*nx)
#     index = index % (ny*nx)
#     y = index // nx
#     x = index % nx
#     return (z, y, x)

def zyx_to_index(z, y, x):
    return (ny * nx * z + nx * y + x)

#---------------------------------

def jit_expand(z, y, x, nearest, expanded_cell):
    for index_3 in range(7): 
        expanded_cell[0][index_3] = np.mod((z + nearest[index_3 + 0]), nz)
        expanded_cell[1][index_3] = np.mod((y + nearest[index_3 + 1]), ny)
        expanded_cell[2][index_3] = np.mod((x + nearest[index_3 + 2]), nx)
    return expanded_cell

def expand_indexes(indexes):
    # Expand a given set of indexes to include the nearest
    # neighbour points in all directions.
    # indexes is an array of grid indexes
    # expanded_index = np.array(jit_expand(index_to_zyx(indexes)))

    K_J_I = index_to_zyx( indexes )

    expanded_length = (len(indexes) * 6 + len(indexes))
    expanded_index = np.zeros((3, expanded_length), dtype=np.int64)

    # 1 seed cell + 6 nearest cells
    expanded_cell = np.zeros((3, 7), dtype=np.int64)
    nearest = np.array( [0, 0, 0, -1, 0, 0, 1, 0, 0, 
               0, -1, 0, 0, 1, 0, 0, 0, -1, 0, 0, 1] )
    for i in range(len(indexes)):
        jit_expand(K_J_I[0][i], K_J_I[1][i], K_J_I[2][i], \
            nearest, expanded_cell)
        expanded_index[:, i*7:i*7+7] = expanded_cell

    # convert back to indexes
    expanded_index = zyx_to_index(expanded_index[0, :],
                                  expanded_index[1, :],
                                  expanded_index[2, :])

    return np.unique(expanded_index)

#---------------------------

def find_halo(indexes):
    # Expand the set of core points to include the nearest 
    # neighbour points in all directions.
    new_indexes = expand_indexes(indexes)

    # From the expanded mask, select the points outside the core
    # expand_index_list returns only unique values,
    # so we don't have to check for duplicates.
    halo = np.setdiff1d(new_indexes, indexes, assume_unique=True)

    return halo

#---------------------------

# TODO: Optimize Eulerian distance calculation (with modifications)
def calc_distance(point1, point2):
    # Calculate distances corrected for re-entrant domain
    delta_x = np.abs(point2[2][:] - point1[2][:])
    mask = delta_x >= (nx/2)
    delta_x[mask] = nx - delta_x[mask]
                    
    delta_y = np.abs(point2[1][:] - point1[1][:])
    mask = delta_y >= (ny/2)
    delta_y[mask] = ny - delta_y[mask]
                                
    delta_z = point2[0][:] - point1[0][:]
                                    
    return np.sqrt(delta_x**2 + delta_y**2 + delta_z**2)
                                        
#---------------------------

def calc_radii(data, reference):
    data_points = np.array(index_to_zyx(data))
    ref_points = np.array(index_to_zyx(reference))
    
    result = np.ones(data.shape, np.float)*(nx + ny)

    k_values = np.unique(ref_points[0][:])
    
    for k in k_values:
        data_mask = data_points[0, :] == k
        ref_mask = ref_points[0, :] == k
        
        k_data = data_points[:, data_mask]
        k_ref = ref_points[:, ref_mask]
        
        m = k_data.shape[1]
        n = k_ref.shape[1]
        
        k_data = k_data[:, :, np.newaxis] * np.ones((3, m, n))
        k_ref = k_ref[:, np.newaxis, :] * np.ones((3, m, n))
        
        distances = calc_distance(k_data, k_ref)
        
        result[data_mask] = distances.min(1)

    return result
