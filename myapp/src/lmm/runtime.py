from ..lib import *
from .main import *
from .func import *
from .jwas import call_JWAS

def run_JWAS_wrapper(event):
    GUI["bt_JWAS"].disabled = True
    print("JWAS is running", flush=True)
    curdoc().add_next_tick_callback(run_JWAS)


def run_JWAS():
    # output customized data
    pd.DataFrame(SRC["data"].data).iloc[:, 1:].to_csv(
        PARAM["path_cusdata"], index=False)
    pd.DataFrame(SRC["data"].data).loc[:, ["Animal", "Sire", "Dam"]].to_csv(
        PARAM["path_cusped"], index=False)
    # output customized covariance matrix
    pd.DataFrame(SRC["Gstr"].data).iloc[:, 1:].to_csv(
        PARAM["path_Gstr"], index=False)
    pd.DataFrame(SRC["Giid"].data).iloc[:, 1:].to_csv(
        PARAM["path_Giid"], index=False)

    # export inputs
    ARG = [
           # path to data
           PARAM["path_cusdata"],
           PARAM["path_cusped"],
           # equation
           GUI["txt_eq"].value,
           # continuous terms
           GUI["mc_con"].value,
           # random terms
           GUI["mc_rdms"].value, GUI["mc_rdmns"].value,
           # variance
           GUI["sp_vare"].value, PARAM["path_Gstr"], PARAM["path_Giid"]]
    ARG = [re.sub(r'[\[\]\',]', '', str(a)) for a in ARG]
    pd.DataFrame(ARG).to_csv(
        PARAM["path_JWAS_param"], index=False, header=None)

    # run JWAS
    try:
        call_JWAS()
        plot_results()
    except Exception as e:
        print(e)
        GUI["bt_JWAS"].disabled = False
    finally:
        print("JWAS Done")
        GUI["bt_JWAS"].disabled = False


# interactive functions
def update_terms(attr, old, new):
    # analyze equation
    ls_options = re.split(
        "[^0-9a-zA-Z*]+", re.split("\s*=\s*", GUI["txt_eq"].value)[1])
    # categorical and continous
    GUI["mc_cat"].options = ls_options
    GUI["mc_con"].options = ls_options
    # fixed, random: options
    GUI["mc_fix"].options = ls_options
    GUI["mc_rdms"].options = ls_options
    GUI["mc_rdmns"].options = ls_options
    # fixed, random: values
    GUI["mc_cat"].value = ls_options
    GUI["mc_con"].value = []
    GUI["mc_fix"].value = []
    GUI["mc_rdms"].value = ls_options
    GUI["mc_rdmns"].value = []

# covariates
def choose_con(attr, old, new):
    GUI["mc_cat"].value = list(set(GUI["mc_cat"].value) - set(new))

def choose_cat(attr, old, new):
    GUI["mc_con"].value = list(set(GUI["mc_con"].value) - set(new))

# terms
def choose_fix(attr, old, new):
    GUI["mc_rdms"].value = list(set(GUI["mc_rdms"].value) - set(new))
    GUI["mc_rdmns"].value = list(set(GUI["mc_rdmns"].value) - set(new))


def update_var_matrix(item, new, default_var=4):
    n_terms = len(new)
    var = default_var
    dt_tmp = pd.DataFrame(np.identity(n_terms)*var, columns=new, index=new)
    dt_tmp = dt_tmp.reset_index()
    dt_tmp.columns = ["Terms"] + new
    SRC[item].data = dt_tmp
    DT[item].columns = [TableColumn(field=f) for f in dt_tmp.columns]


def choose_rdms(attr, old, new):
    GUI["mc_fix"].value = list(set(GUI["mc_fix"].value) - set(new))
    GUI["mc_rdmns"].value = list(set(GUI["mc_rdmns"].value) - set(new))
    update_var_matrix("Gstr", new)

def choose_rdmns(attr, old, new):
    GUI["mc_rdms"].value = list(set(GUI["mc_rdms"].value) - set(new))
    GUI["mc_fix"].value = list(set(GUI["mc_fix"].value) - set(new))
    update_var_matrix("Giid", new)


# interactive actions
GUI["txt_eq"].on_change("value", update_terms)
GUI["bt_JWAS"].on_click(run_JWAS_wrapper)
GUI["mc_con"].on_change("value", choose_con)
GUI["mc_cat"].on_change("value", choose_cat)
GUI["mc_fix"].on_change("value", choose_fix)
GUI["mc_rdms"].on_change("value", choose_rdms)
GUI["mc_rdmns"].on_change("value", choose_rdmns)


GUI["mc_fix"].value = ["intercept", "CG"]
GUI["mc_rdms"].value = ["Animal", "Sire"]
