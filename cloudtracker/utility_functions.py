import numpy as np

import numba, code

#---------------------------------

@numba.jit(nopython=True)
def index_to_zyx(index, nz, ny, nx):
    z = index // (ny*nx)
    index = index % (ny*nx)
    y = index // nx
    x = index % nx
    return (z, y, x)

@numba.jit(nopython=True)
def zyx_to_index(z, y, x, nz, ny, nx):
    return (ny*nx*z + nx*y + x)

#---------------------------------

@numba.jit
def jit_expand(K_J_I):
    neighbour_cells = [ [-1, 0, 0], [1, 0, 0], 
                        [0, -1, 0], [0, 1, 0], 
                        [0, 0, -1], [0, 0, 1] ]
    z_expand = []
    y_expand = []
    x_expand = []
    for item in neighbour_cells:
        # List comprehension not supported in non-python mode (yet)
        # z_expand += [z + item[0] for z in K_J_I[0]]
        # y_expand += [y + item[1] for y in K_J_I[1]]
        # x_expand += [x + item[2] for x in K_J_I[2]]

        for i in range(len(K_J_I[0])):
            z_expand += [item[0] + K_J_I[0][i]]
            y_expand += [item[1] + K_J_I[1][i]]
            x_expand += [item[2] + K_J_I[2][i]]
    return [z_expand, y_expand, x_expand]

# FIXME: make nearest into a 1D array and run Numba
# @numba.jit(nopython=True)
def expand_generator(nearest, z, y, x):
    for i in nearest:
        z_exp = z + i[2]
        y_exp = y + i[1]
        x_exp = x + i[0]
        yield (x_exp, y_exp, z_exp)

# TODO (LOH): Parallelize 
# @numba.jit
# @profile
def expand_indexes(indexes, nz, ny, nx):
    # Expand a given set of indexes to include the nearest
    # neighbour points in all directions.
    # indexes is an array of grid indexes
    # expanded_index = np.array(jit_expand(index_to_zyx(indexes, nz, ny, nx)))

    K_J_I = index_to_zyx( indexes, nz, ny, nx )
    # expanded_length = (len(indexes) * 6 + len(indexes))
    # expanded_index = np.zeros((3, expanded_length), dtype=np.int)

    # nearest = np.array([ [-1, 0, 0], [1, 0, 0], 
    #             [0, -1, 0], [0, 1, 0], 
    #             [0, 0, -1], [0, 0, 1] ])

    # exp_i = 0
    # for item in range(len(indexes)):
    #     stack_list = ((K_J_I[0][item], K_J_I[1][item], K_J_I[2][item]))
    #     expanded_index[:, exp_i] = stack_list
    #     exp_i += 1

    #     for index in expand_generator(nearest, stack_list[2], stack_list[1], stack_list[0]):
    #         # expanded_index[2][exp_i] = index[2]
    #         # expanded_index[1][exp_i] = index[1]
    #         # expanded_index[0][exp_i] = index[0]
    #         expanded_index[:, exp_i] = index
    #         exp_i += 1

    stack_list = [K_J_I, ]
    nearest = np.array([[[-1], [0], [0]], [[1], [0], [0]],
                 [[0], [-1], [0]], [[0], [1], [0]], 
                 [[0], [0], [-1]], [[0], [0], [1]]])
    for item in nearest:
        stack_list.append(K_J_I + item)
        
    expanded_index = np.hstack(stack_list)

    # re-entrant domain
    expanded_index[0, expanded_index[0, :] == nz] = nz-1
    expanded_index[0, expanded_index[0, :] < 0] = 0
    expanded_index[1, :] = expanded_index[1, :]%ny
    expanded_index[2, :] = expanded_index[2, :]%nx

    # convert back to indexes
    expanded_index = zyx_to_index(expanded_index[0, :],
                                  expanded_index[1, :],
                                  expanded_index[2, :],
                                  nz, ny, nx)

    return np.unique(expanded_index)

#---------------------------

def find_halo(indexes, MC):
    # Expand the set of core points to include the nearest 
    # neighbour points in all directions.
    new_indexes = expand_indexes(indexes, MC)

    # From the expanded mask, select the points outside the core
    # expand_index_list returns only unique values,
    # so we don't have to check for duplicates.
    halo = np.setdiff1d(new_indexes, indexes, assume_unique=True)

    return halo

#---------------------------

def calc_distance(point1, point2, MC):
    # Calculate distances corrected for reentrant domain
    ny, nx = MC['ny'], MC['nx']
        
    delta_x = np.abs(point2[2, :] - point1[2, :])
    mask = delta_x >= (nx/2)
    delta_x[mask] = nx - delta_x[mask]
                    
    delta_y = np.abs(point2[1, :] - point1[1, :])
    mask = delta_y >= (ny/2)
    delta_y[mask] = ny - delta_y[mask]
                                
    delta_z = point2[0, :] - point1[0, :]
                                    
    return np.sqrt(delta_x**2 + delta_y**2 + delta_z**2)
                                        
#---------------------------

def calc_radii(data, reference, MC):
    ny, nx = MC['ny'], MC['nx']
    data_points = index_to_zyx(data, MC)
    ref_points = index_to_zyx(reference, MC)
    
    result = np.ones(data.shape, np.float)*(nx + ny)

    k_values = np.unique(ref_points[0,:])
    
    for k in k_values:
        data_mask = data_points[0, :] == k
        ref_mask = ref_points[0, :] == k
        
        k_data = data_points[:, data_mask]
        k_ref = ref_points[:, ref_mask]
        
        m = k_data.shape[1]
        n = k_ref.shape[1]
        
        k_data = k_data[:, :, np.newaxis] * np.ones((3, m, n))
        k_ref = k_ref[:, np.newaxis, :] * np.ones((3, m, n))
        
        distances = calc_distance(k_data, k_ref, MC)
        
        result[data_mask] = distances.min(1)

    return result
