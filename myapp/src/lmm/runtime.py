from ..lib import *
from .__main__ import *
from .func import *
from . import path as PATH


def set_runtime(SRC, GUI, PARAM, DT, HT):
    if PARAM["enable_JWAS"]:
        from .jwas import call_JWAS

    def run_JWAS_wrapper(event):
        GUI["bt_JWAS"].disabled = True

        print("JWAS is running", flush=True)
        curdoc().add_next_tick_callback(run_JWAS)

    def run_JWAS():
        # output customized data
        pd.DataFrame(SRC["data"].data).iloc[:, 1:].to_csv(
            PATH.CUS.DATA.value, index=False)
        pd.DataFrame(SRC["ped"].data).iloc[:, 1:].to_csv(
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
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout

        try:
            if PARAM["enable_JWAS"]:
                call_JWAS()
            plot_results(PARAM, DT, SRC, HT)
        except Exception as e:
            print(e, flush=True)
            GUI["bt_JWAS"].disabled = False
        finally:
            # print("LMM is computed successfully!", flush=True)
            GUI["bt_JWAS"].disabled = False

        GUI["logger"].text = new_stdout.getvalue()
        sys.stdout = old_stdout

    # interactive functions
    def update_terms(attr, old, new):
        # analyze equation
        ls_eq_right = re.split("\s*=\s*", GUI["txt_eq"].value)[1]
        ls_eq_right = re.sub("\s", "", ls_eq_right)
        ls_options_catcon = re.split("[^0-9a-zA-Z]+", ls_eq_right)
        ls_options_catcon = list(np.unique(ls_options_catcon))
        ls_options_fixrdm = re.split("[^0-9a-zA-Z*]+", ls_eq_right)
        ls_options_fixrdm = list(np.unique(ls_options_fixrdm))

        # categorical and continous: options
        GUI["mc_cat"].options   = ls_options_catcon
        GUI["mc_con"].options   = ls_options_catcon
        # fixed, random: options
        GUI["mc_fix"].options   = ls_options_fixrdm
        GUI["mc_rdms"].options  = ls_options_fixrdm
        GUI["mc_rdmns"].options = ls_options_fixrdm
        # Values
        GUI["mc_cat"].value     = ls_options_catcon
        GUI["mc_con"].value     = []
        GUI["mc_fix"].value     = ls_options_fixrdm
        GUI["mc_rdms"].value    = []
        GUI["mc_rdmns"].value   = []

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

    def set_options(options, subsets="all"):
        if subsets == "all":
            GUI["mc_con"].options = options
            GUI["mc_cat"].options = options
            GUI["mc_fix"].options = options
            GUI["mc_rdms"].options = options
            GUI["mc_rdmns"].options = options

        elif subsets == "concat":
            GUI["mc_con"].options = options
            GUI["mc_cat"].options = options

        elif subsets == "fixrdm":
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

        path_ped = str.replace(path_dt, ".csv", "_PED.csv")
        dt_ped = pd.read_csv(path_ped)

        SRC["ped"].data = dt_ped
        DT["ped"].columns = [TableColumn(field="Animal"),
                             TableColumn(field="Sire"),
                             TableColumn(field="Dam")]

        # preload items
        if enum_dt == PATH.DATA.DEMO_1:
            set_options(["Sex", "Animal"])
            GUI["txt_eq"].value = "WWG = Sex + Animal"

            GUI["mc_con"].value = []
            GUI["mc_cat"].value = ["Sex", "Animal"]

            GUI["mc_fix"].value = ["Sex"]
            GUI["mc_rdms"].value = ["Animal"]

            # update variance
            dt = pd.DataFrame(SRC["Gstr"].data)
            dt.iloc[0, 2] = 20
            SRC["Gstr"].data = dt.iloc[:, 1:]
            dt = pd.DataFrame(SRC["Gres"].data)
            dt.iloc[0, 2] = 40
            SRC["Gres"].data = dt.iloc[:, 1:]

        elif enum_dt == PATH.DATA.DEMO_2:
            set_options(["Parity", "Animal", "PE"])
            GUI["txt_eq"].value = "Fat_yield = Parity + Animal + PE"

            GUI["mc_con"].value = []
            GUI["mc_cat"].value = ["Parity", "Animal", "PE"]

            GUI["mc_fix"].value = ["Parity"]
            GUI["mc_rdms"].value = ["Animal"]
            GUI["mc_rdmns"].value = ["PE"]

            # update variance
            dt = pd.DataFrame(SRC["Gstr"].data)
            dt.iloc[0, 2] = 20
            SRC["Gstr"].data = dt.iloc[:, 1:]
            dt = pd.DataFrame(SRC["Giid"].data)
            dt.iloc[0, 2] = 12
            SRC["Giid"].data = dt.iloc[:, 1:]
            dt = pd.DataFrame(SRC["Gres"].data)
            dt.iloc[0, 2] = 28
            SRC["Gres"].data = dt.iloc[:, 1:]

        elif enum_dt == PATH.DATA.DEMO_3:
            set_options(["Animal", "Dam", "Sex"])
            GUI["txt_eq"].value = "Weight = Sex + Animal + Dam"

            GUI["mc_con"].value = []
            GUI["mc_cat"].value = ["Sex", "Animal", "Dam"]

            GUI["mc_fix"].value = ["Sex"]
            GUI["mc_rdms"].value = ["Animal"]
            GUI["mc_rdmns"].value = ["Dam"]

            # update variance
            dt = pd.DataFrame(SRC["Gstr"].data)
            dt.iloc[0, 2] = 20
            SRC["Gstr"].data = dt.iloc[:, 1:]
            dt = pd.DataFrame(SRC["Giid"].data)
            dt.iloc[0, 2] = 15
            SRC["Giid"].data = dt.iloc[:, 1:]
            dt = pd.DataFrame(SRC["Gres"].data)
            dt.iloc[0, 2] = 65
            SRC["Gres"].data = dt.iloc[:, 1:]

        elif enum_dt == PATH.DATA.DEMO_4:
            set_options(["Parity", "Animal", "PE"])
            GUI["txt_eq"].value = "Birth_weight = Herds + Pen + Animal + Dam + PE"

            GUI["mc_con"].value = []
            GUI["mc_cat"].value = ["Herds", "Pen", "Animal", "Dam", "PE"]

            GUI["mc_fix"].value = ["Herds", "Pen"]
            GUI["mc_rdms"].value = ["Animal", "Dam"]
            GUI["mc_rdmns"].value = ["PE"]

            # update variance
            dt = pd.DataFrame(SRC["Gstr"].data)
            dt.iloc[0, 2] = 150
            dt.iloc[0, 3] = -40
            dt.iloc[1, 2] = -40
            dt.iloc[1, 3] = 90
            SRC["Gstr"].data = dt.iloc[:, 1:]
            dt = pd.DataFrame(SRC["Giid"].data)
            dt.iloc[0, 2] = 40
            SRC["Giid"].data = dt.iloc[:, 1:]
            dt = pd.DataFrame(SRC["Gres"].data)
            dt.iloc[0, 2] = 350
            SRC["Gres"].data = dt.iloc[:, 1:]

        elif enum_dt == PATH.DATA.DEMO_5:
            set_options(["X0", "X1", "X2"], subsets="concat")
            set_options(["X0*Animal", "X1*Animal", "X2*Animal"], subsets="fixrdm")

            GUI["txt_eq"].value = "Y = X0*Animal + X1*Animal + X2*Animal"

            GUI["mc_con"].value = ["X0", "X1", "X2"]
            GUI["mc_cat"].value = ["Animal"]

            GUI["mc_fix"].value = []
            GUI["mc_rdms"].value = ["X0*Animal", "X1*Animal", "X2*Animal"]
            GUI["mc_rdmns"].value = []

            # update variance
            dt = pd.DataFrame(SRC["Gstr"].data)
            dt.iloc[0, 2] = 50
            dt.iloc[0, 3] = 0
            dt.iloc[0, 4] = 0
            dt.iloc[1, 2] = 0
            dt.iloc[1, 3] = 50
            dt.iloc[1, 4] = 0
            dt.iloc[2, 2] = 0
            dt.iloc[2, 3] = 0
            dt.iloc[2, 4] = 50
            SRC["Gstr"].data = dt.iloc[:, 1:]
            dt = pd.DataFrame(SRC["Gres"].data)
            dt.iloc[0, 2] = 50
            SRC["Gres"].data = dt.iloc[:, 1:]

        elif enum_dt == PATH.DATA.DEMO_6:
            set_options(["X1", "X2", "X3", "X4", "X5"])
            GUI["txt_eq"].value = "Y1 = Animal + X1 + X2 + X5"

            GUI["mc_con"].value = ["X5"]
            GUI["mc_cat"].value = ["Animal", "X1", "X2"]

            GUI["mc_fix"].value = ["X2", "X5"]
            GUI["mc_rdms"].value = ["Animal"]
            GUI["mc_rdmns"].value = ["X1"]

            # update variance
            dt = pd.DataFrame(SRC["Gstr"].data)
            dt.iloc[0, 2] = 50
            SRC["Gstr"].data = dt.iloc[:, 1:]
            dt = pd.DataFrame(SRC["Giid"].data)
            dt.iloc[0, 2] = 50
            SRC["Giid"].data = dt.iloc[:, 1:]
            dt = pd.DataFrame(SRC["Gres"].data)
            dt.iloc[0, 2] = 50
            SRC["Gres"].data = dt.iloc[:, 1:]

        run_JWAS()


    # interactive actions
    GUI["txt_eq"].on_change("value", update_terms)
    GUI["bt_JWAS"].on_click(run_JWAS_wrapper)
    GUI["mc_con"].on_change("value", choose_con)
    GUI["mc_cat"].on_change("value", choose_cat)
    GUI["mc_fix"].on_change("value", choose_fix)
    GUI["mc_rdms"].on_change("value", choose_rdms)
    GUI["mc_rdmns"].on_change("value", choose_rdmns)
    GUI["sel_data"].on_change("value", choose_data)
