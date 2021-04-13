from ..lib import *
from .main import *
from .func import *
from . import path as PATH
from .jwas import call_JWAS

def run_JWAS_wrapper(event):
    GUI["bt_JWAS"].disabled = True
    print("JWAS is running", flush=True)
    curdoc().add_next_tick_callback(run_JWAS)


def run_JWAS():
    # output customized data
    pd.DataFrame(SRC["data"].data).iloc[:, 1:].to_csv(
        PATH.CUS.DATA.value, index=False)
    pd.DataFrame(SRC["data"].data).loc[:, ["Animal", "Sire", "Dam"]].to_csv(
        PATH.CUS.PED.value, index=False)
    # output customized covariance matrix
    pd.DataFrame(SRC["Gstr"].data).iloc[:, 1:].to_csv(
        PATH.CUS.Gstr.value, index=False)
    pd.DataFrame(SRC["Giid"].data).iloc[:, 1:].to_csv(
        PATH.CUS.Giid.value, index=False)
    pd.DataFrame(SRC["Gres"].data).iloc[:, 1:].to_csv(
        PATH.CUS.Gres.value, index=False)

    # export inputs
    ARG = [
           # path to data
           PATH.CUS.DATA.value,
           PATH.CUS.PED.value,
           # equation
           GUI["txt_eq"].value,
           # continuous terms
           GUI["mc_con"].value,
           # random terms
           GUI["mc_rdms"].value, GUI["mc_rdmns"].value,
           # variance
           PATH.CUS.Gstr.value, PATH.CUS.Giid.value, PATH.CUS.Gres.value]
    ARG = [re.sub(r'[\[\]\',]', '', str(a)) for a in ARG]
    pd.DataFrame(ARG).to_csv(
        PATH.param_Julia, index=False, header=None)

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

    # multi-trait
    trait = re.split("\s*=\s*", GUI["txt_eq"].value)[0]
    update_var_matrix("Gres", [trait])

# covariates
def choose_con(attr, old, new):
    GUI["mc_cat"].value = list(set(GUI["mc_cat"].options) - set(new))

def choose_cat(attr, old, new):
    GUI["mc_con"].value = list(set(GUI["mc_con"].options) - set(new))

# terms
def update_var_matrix(item, new, default_var=50):
    n_terms = len(new)
    var = default_var
    dt_tmp = pd.DataFrame(np.identity(n_terms)*var, columns=new, index=new)
    dt_tmp = dt_tmp.reset_index()
    dt_tmp.columns = ["Terms"] + new
    SRC[item].data = dt_tmp
    DT[item].columns = [TableColumn(field=f) for f in dt_tmp.columns]


def choose_fix(attr, old, new):
    GUI["mc_rdms"].value = list(set(GUI["mc_rdms"].value) - set(new))
    GUI["mc_rdmns"].value = list(set(GUI["mc_rdmns"].value) - set(new))

def choose_rdms(attr, old, new):
    GUI["mc_fix"].value = list(set(GUI["mc_fix"].value) - set(new))
    GUI["mc_rdmns"].value = list(set(GUI["mc_rdmns"].value) - set(new))
    update_var_matrix("Gstr", new)

def choose_rdmns(attr, old, new):
    GUI["mc_rdms"].value = list(set(GUI["mc_rdms"].value) - set(new))
    GUI["mc_fix"].value = list(set(GUI["mc_fix"].value) - set(new))
    update_var_matrix("Giid", new)

def set_options(options):
    GUI["mc_con"].options = options
    GUI["mc_cat"].options = options
    GUI["mc_fix"].options = options
    GUI["mc_rdms"].options = options
    GUI["mc_rdmns"].options = options

def choose_data(attr, old, new):
    # find data path
    value = GUI["sel_data"].value
    path_dt = PATH.DATA.get_path_by_name(name=value)
    enum_dt = PATH.DATA.get_enum_by_name(name=value)

    # load data
    dt = pd.read_csv(path_dt)
    SRC["data"].data = dt
    DT["data"].columns = [TableColumn(field=str(s))
                          for s in dt.columns]

    # preload items
    if enum_dt == PATH.DATA.DEMO_1:
        set_options(["intercept", "Animal", "Sire", "Dam", "Herd"])
        GUI["txt_eq"].value = "Observation = Herd + Animal"

        GUI["mc_con"].value = ["intercept"]
        GUI["mc_cat"].value = ["Herd", "Animal"]

        GUI["mc_fix"].value = ["intercept", "Herd"]
        GUI["mc_rdms"].value = ["Animal"]

    elif enum_dt == PATH.DATA.DEMO_2:
        set_options(["intercept", "Animal", "Dam", "Sex"])
        GUI["txt_eq"].value = "Weight = intercept + Sex + Animal + Dam"

        GUI["mc_con"].value = ["intercept"]
        GUI["mc_cat"].value = ["Sex", "Animal", "Dam"]

        GUI["mc_fix"].value = ["intercept", "Sex"]
        GUI["mc_rdms"].value = ["Animal"]
        GUI["mc_rdmns"].value = ["Dam"]

    elif enum_dt == PATH.DATA.DEMO_3:
        set_options(["intercept", "Animal", "Sire", "CG"])
        GUI["txt_eq"].value = "Weight = intercept + Animal + Sire + CG"

        GUI["mc_con"].value = ["intercept"]
        GUI["mc_cat"].value = ["Animal", "Sire", "CG"]

        GUI["mc_fix"].value = ["intercept", "CG"]
        GUI["mc_rdms"].value = ["Animal", "Sire"]


# interactive actions
GUI["txt_eq"].on_change("value", update_terms)
GUI["bt_JWAS"].on_click(run_JWAS_wrapper)
GUI["mc_con"].on_change("value", choose_con)
GUI["mc_cat"].on_change("value", choose_cat)
GUI["mc_fix"].on_change("value", choose_fix)
GUI["mc_rdms"].on_change("value", choose_rdms)
GUI["mc_rdmns"].on_change("value", choose_rdmns)
GUI["sel_data"].on_change("value", choose_data)
