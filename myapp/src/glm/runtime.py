from .__main__ import *
from .func import *

def refresh_slider(attr, old, new):
    run(n=ARG["n"], n_dis=ARG["n_dis"], m=ARG["m"], nqtn=GUI["sli_nqtn"].value,
        eff_mu=GUI["sli_effmu"].value, eff_sd=GUI["sli_effsd"].value,
        h2=GUI["sli_h2"].value)

def refresh_button(event):
    run(n=ARG["n"], n_dis=ARG["n_dis"], m=ARG["m"], nqtn=GUI["sli_nqtn"].value,
        eff_mu=GUI["sli_effmu"].value, eff_sd=GUI["sli_effsd"].value,
        h2=GUI["sli_h2"].value)

def run(n, n_dis, m, nqtn, eff_mu, eff_sd, h2):
    # solve equation
    eff_background = get_glm_eff(
        size=n, nqtn=n, mu=eff_mu, sd=eff_sd)
    eff_samples = get_glm_eff(
        size=m, nqtn=nqtn, mu=eff_mu, sd=eff_sd)
    mat_X = get_glm_x(n=n, m=m)
    y_obs, y_m = get_glm_y(mat_X=mat_X, ls_eff=eff_samples, h2=h2)
    eff_estimated, residuals, y_bv, mse = solve_eq(
        mat_y=y_obs[:n_dis], mat_X=mat_X[:n_dis])

    # sources
    digits = 4
    SRC["y"].data = pd.DataFrame(
        dict({
            "p": y_obs,
            "g": y_m
        })
    ).round(digits)
    SRC["y_s"].data = pd.DataFrame(
        dict({
            "obs": y_obs[:ARG["n_dis"]],
            "bv": y_bv,
            "res": residuals,
            "err": str("MSE: %.3f" % mse)
        })
    ).round(digits)

    SRC["eff"].data = pd.DataFrame(
        dict({
            "eff": eff_background
        })
    ).round(digits)

    SRC["eff_s"].data = pd.DataFrame(
        dict({
            "sample": eff_samples,
            "estimate": eff_estimated
        })
    ).round(digits)

    SRC["X"].data = mat_to_pd(mat_X, col_prefix="X").round(digits)

    nbins = 50
    # hist for y
    hist_yp, edges_yp = np.histogram(
        SRC["y"].data["p"], bins=nbins, density=True)
    hist_yg, edges_yg = np.histogram(
        SRC["y"].data["g"], bins=nbins, density=True)
    SRC["h_y"].data = pd.DataFrame(
        dict({
            "yp_hist": hist_yp, "yp_edL": edges_yp[:-1], "yp_edR": edges_yp[1:],
            "yg_hist": hist_yg, "yg_edL": edges_yg[:-1], "yg_edR": edges_yg[1:]
        })
    )

    # hist for M
    hist_m, edges_m = np.histogram(
        SRC["eff"].data["eff"], bins=nbins, density=False)
    hist_ms, edges_ms = np.histogram(
        SRC["eff_s"].data["sample"], bins=nbins, density=True)
    SRC["h_m"].data = pd.DataFrame(
        dict({
            "m_hist": hist_m, "m_edL": edges_m[:-1], "m_edR": edges_m[1:],
            "ms_hist": hist_ms, "ms_edL": edges_ms[:-1], "ms_edR": edges_ms[1:]
        })
    )

#===== interactive functions
SRC["X"].selected.on_change('indices', refresh_slider)
GUI["sli_h2"].on_change("value", refresh_slider)
GUI["sli_nqtn"].on_change("value", refresh_slider)
GUI["sli_effmu"].on_change("value", refresh_slider)
GUI["sli_effsd"].on_change("value", refresh_slider)
GUI["bt_shuffle"].on_click(refresh_button)
