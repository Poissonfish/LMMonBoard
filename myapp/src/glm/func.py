from ..lib import *

def solve_eq(mat_y, mat_X):
    mat_b = np.linalg.inv(np.transpose(mat_X) @
                          mat_X) @ np.transpose(mat_X) @ mat_y
    fit_y = mat_X @ mat_b
    mat_e = mat_y - fit_y
    mse = np.mean((fit_y - mat_y)**2)

    return mat_b, mat_e, fit_y, mse


def mat_to_pd(mat, col_prefix=None, col_name=None):
    """convert np matrix to valid pandas data frame"""
    mat = np.array(mat)
    try:
        n, m = mat.shape
    except Exception as e:
        # if mat is a vector
        m = 1

    if col_prefix is not None:
        return pd.DataFrame(mat, columns=["%s%d" % (col_prefix, i) for i in range(m)])
    elif col_name is not None:
        return pd.DataFrame(mat, columns=col_name)


def src_to_mat(source):
    """extract numpy matrix from source"""
    ls_data = source.data
    return np.transpose([ls_data[k] for k in ls_data.keys()][1:])


def get_glm_y(mat_X, ls_eff, h2):
    n = len(mat_X)

    # breeding values
    y_g = mat_X @ ls_eff

    # define residual by h2
    var_g = np.var(y_g)
    var_e = (var_g * (1 - h2)) / h2
    y_e = np.random.normal(0, var_e**.5, n)

    y_p = y_g + y_e
    return y_p, y_g


def get_glm_eff(size, nqtn, mu, sd):
    # compute marker effects
    ls_eff = np.random.normal(
        loc=mu, scale=sd, size=size)

    # silent some QTNs
    ls_eff[nqtn:] = 0
    np.random.shuffle(ls_eff)

    return ls_eff


def get_glm_x(n, m):
    mat_X = np.random.randint(0, 3, n * m).reshape((n, m))
    return mat_X
