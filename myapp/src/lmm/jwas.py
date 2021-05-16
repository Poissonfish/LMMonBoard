# import os
# os.chdir("../../..")
# os.getcwd()
from ..lib import *
from . import path as PATH

# for anaconda interpreter
import sys
if "conda" in sys.executable:
    print("It's Conda Python")
    from julia.api import Julia
    jl = Julia(compiled_modules=False)

# import Julia packages
from julia import JWAS
from julia import DataFrames
from julia import CSV

def call_JWAS():
    # take inputs
    dt_param = pd.read_csv(PATH.param_Julia, header=None)
    ARG = dict()
    ARG["data"] =   dt_param.iloc[0].values[0]
    ARG["ped"] =    dt_param.iloc[1].values[0]
    ARG["eq"] =     dt_param.iloc[2].values[0]
    ARG["cov"] =    dt_param.iloc[3].values[0]
    ARG["rdmstr"] = dt_param.iloc[4].values[0]
    ARG["rdmiid"] = dt_param.iloc[5].values[0]
    ARG["vgstr"] =  dt_param.iloc[6].values[0]
    ARG["vgiid"] =  dt_param.iloc[7].values[0]
    ARG["vgres"] =  dt_param.iloc[8].values[0]

    PATH_OUT = "myapp/out/jwas_%s.csv"
    # read data
    julia_dt = CSV.read(ARG["data"], DataFrames.DataFrame,
                        missingstrings=["0", ""])
    ped = JWAS.get_pedigree(ARG["ped"], header=True,
                            separator=",", missingstrings=["0", ""])

    # build pedigree
    id_ped = pd.Series(ped.IDs).str.\
                replace("[a-zA-Z]", "").\
                astype(int)
    id_int = np.array([int(ID) for ID in id_ped])
    order_ped = np.argsort(id_int)
    id_order = id_int[order_ped]

    # compute inversed A
    Ai = np.array(JWAS.PedModule.AInverse(ped))
    A = np.linalg.inv(Ai).round(2)
    dt_ped = pd.DataFrame(A).iloc[order_ped, order_ped]
    dt_ped.columns = np.array(ped.IDs)[order_ped]
    dt_ped.to_csv(PATH_OUT % "A", index=False)

    # build model equation
    model = JWAS.build_model(ARG["eq"], np.array(
        pd.read_csv(ARG["vgres"]).iloc[:, 1:])[0][0])

    # factor or covariates
    if ARG['cov'] == ARG['cov']:
        # is not nan field
        JWAS.set_covariate(model, ARG["cov"])

    # fixed or random
    if ARG['rdmstr'] == ARG['rdmstr']:
        # is not nan field
        JWAS.set_random(model, ARG["rdmstr"], ped, np.array(
            pd.read_csv(ARG["vgstr"]).iloc[:, 1:]))

    if ARG['rdmiid'] == ARG['rdmiid']:
        # is not nan field
        # JWAS.set_random(model, ARG["rdmiid"], ARG["vu"])
        JWAS.set_random(model, ARG["rdmiid"], np.array(
            pd.read_csv(ARG["vgiid"]).iloc[:, 1:]))

    # solve
    out = JWAS.solve(model, julia_dt)
    LHS = out[2]
    RHS = out[3]
    sol = pd.DataFrame(dict({"terms": out[0],
                            "values": np.array(np.linalg.pinv(LHS) @ RHS).
                            reshape(-1)}))

    # organize output
    ls_terms = re.split(r"\s*=\s*", ARG["eq"])
    name_y = ls_terms[0]

    # get random index
    ls_rdm = []
    if ARG["rdmstr"] == ARG["rdmstr"]:
        ls_rdm += re.split(r"\s", ARG["rdmstr"])
    if ARG["rdmiid"] == ARG["rdmiid"]:
        ls_rdm += re.split(r"\s", ARG["rdmiid"])

    idx_rdm = []
    for term in ls_rdm:
        idx_rdm += [i for i in range(len(sol)) if term in sol.iloc[i, 0]]

    # make solution df
    def format_terms(array):
        arr = [re.sub("%s:" % name_y, "", item) for item in array]
        arr = [re.sub("intercept:intercept", "*intercept:0", item) for item in arr]
        arr = [re.sub(":", "_", item) for item in arr]
        return np.array(arr).astype(str)

    dt_fix = sol.drop(idx_rdm)
    dt_fix.iloc[:, 0] = format_terms(dt_fix.iloc[:, 0])
    if len(dt_fix) != 0:
        dt_fix.loc[:, "isFixed"] = 1

    dt_rdm = sol.loc[idx_rdm, :]
    dt_rdm.iloc[:, 0] = format_terms(dt_rdm.iloc[:, 0])
    if len(dt_rdm) != 0:
        dt_rdm.loc[:, "isFixed"] = 0

    dt_sol = pd.concat([dt_fix, dt_rdm])
    dt_sol.columns = ["terms", "effects", "isFixed"]

    # get the right order
    terms_origin = format_terms(sol.iloc[:, 0])
    dt_split = dt_sol["terms"].str.split("_", expand=True)
    dt_sol.loc[:, "terms_name"] = dt_split.iloc[:, 0]
    dt_sol.loc[:, "terms_int"] = dt_split.iloc[:, 1].\
                                    str.\
                                    replace("[a-zA-Z]", "0").\
                                    astype(int)

    dt_sol = dt_sol.sort_values(by=["isFixed", "terms_name", "terms_int"],
                                ascending=[False, True, True])
    terms_order = dt_sol.terms.values
    order = [list(terms_origin).index(term) for term in terms_order]

    # ourput solution
    dt_sol.loc[:, "terms"] = dt_sol.terms.str.replace(r".*intercept.*", "intercept")
    dt_sol.iloc[:, :3].to_csv(PATH_OUT % "sol", index=False)
    ls_isFixed = dt_sol.isFixed.values.astype(bool)

    # make incidence matrix
    dt_inc = pd.DataFrame(np.array(out[1])[:, order])
    try:
        dt_fix = dt_inc.loc[:, ls_isFixed]
        dt_fix.columns = dt_sol.terms[ls_isFixed].values
        dt_fix.to_csv(PATH_OUT % "X", index=False)
    except:
        pd.DataFrame().to_csv(PATH_OUT % "X", index=False)

    try:
        dt_rdm = dt_inc.loc[:, ~ls_isFixed]
        dt_rdm.columns = dt_sol.terms[~ls_isFixed].values
        dt_rdm.to_csv(PATH_OUT % "Z", index=False)
    except:
        pd.DataFrame().to_csv(PATH_OUT % "Z", index=False)

    # LHS, RHS
    pd.DataFrame(np.array(out[2])[order, :][:, order]).to_csv(PATH_OUT % "lhs", index=False)
    pd.DataFrame(np.array(out[3])[order, :]).to_csv(PATH_OUT % "rhs", index=False)


