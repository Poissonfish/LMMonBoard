from ..lib import *
from .__main__ import *
from .figures import *

def get_std_dt(dt):
    dt2 = dt.copy()
    np_dt = np.array(dt2)
    if np_dt.std() == 0:
        dt2.iloc[:] = 0
    else:
        dt2.iloc[:] = (np_dt - np_dt.mean()) / (np_dt.std())
    return dt2


def wide_to_long(dt_org):
    dt = dt_org.copy()
    try:
        n, m = dt.shape
        dt.columns = range(1, m + 1)
    except:
        # when the dt with only one column
        dt = dt.rename(1)
    dt_heat = pd.melt(dt.reset_index(), id_vars="index")
    dt_heat.columns = ["y", "x", "value"]
    dt_heat["x"].astype(int)
    dt_heat["y"] += 1
    return dt_heat


def plot_results():
    # update matrix
    for item in ["X", "Z", "sol", "lhs", "rhs", "A"]:
        try:
            DT[item] = pd.read_csv("myapp/out/jwas_%s.csv" % item).round(2)
        except:
            # when either X or Z has empty DT
            PARAM["p%s" % item] = 0
            SRC[item].data = pd.DataFrame({"x": [0], "y": [0], "tmp": [0]})
            continue
        if item in ["X", "Z"]:
            # std
            dt_raw = wide_to_long(DT[item])
            dt_std = wide_to_long(get_std_dt(DT[item]))
            dt_raw["value_std"] = dt_std["value"]

            # change tickers
            specify_tickers(
                HT[item], DT[item], xticks=DT[item].columns)

            # get number of fix/random terms
            try:
                PARAM["p%s" % item] = DT[item].shape[1]
            except:
                # when the dt with only one column
                PARAM["p%s" % item] = 1
        elif item == "sol":
            # change separator position
            HT[item].select(name="hline").location = PARAM["pX"] + \
                PARAM["sep_offset"]

            # std
            dt_raw = wide_to_long(DT[item].iloc[:, 1])
            dtw_tmp = DT[item].iloc[:, 1].copy()
            dtw_tmp = pd.concat([get_std_dt(dtw_tmp[:PARAM["pX"]]),
                                 get_std_dt(dtw_tmp[PARAM["pX"]:])],
                                axis=0)
            dt_std = wide_to_long(dtw_tmp)
            dt_raw["value_std"] = dt_std["value"]

            # change tickers
            specify_tickers(HT[item], DT[item],
                            yticks=DT[item].terms.values)
        elif item == "lhs":
            # change separator position
            HT[item].select(name="vline").location = PARAM["pX"] + \
                PARAM["sep_offset"]
            HT[item].select(name="hline").location = PARAM["pX"] + \
                PARAM["sep_offset"]

            # std
            dt_raw = wide_to_long(DT[item])
            dtw_tmp = DT[item].copy()
            dtw_tmp.iloc[:PARAM["pX"], :PARAM["pX"]] = get_std_dt(
                dtw_tmp.iloc[:PARAM["pX"], :PARAM["pX"]])
            dtw_tmp.iloc[PARAM["pX"]:, :PARAM["pX"]] = get_std_dt(
                dtw_tmp.iloc[PARAM["pX"]:, :PARAM["pX"]])
            dtw_tmp.iloc[:PARAM["pX"], PARAM["pX"]:] = get_std_dt(
                dtw_tmp.iloc[:PARAM["pX"], PARAM["pX"]:])
            dtw_tmp.iloc[PARAM["pX"]:, PARAM["pX"]:] = get_std_dt(
                dtw_tmp.iloc[PARAM["pX"]:, PARAM["pX"]:])
            dt_std = wide_to_long(dtw_tmp)
            dt_raw["value_std"] = dt_std["value"]

            # change tickers
            specify_tickers(
                HT[item], DT[item], yticks=DT["sol"]["terms"].values)
        elif item == "rhs":
            # change separator position
            HT[item].select(name="hline").location = PARAM["pX"] + \
                PARAM["sep_offset"]

           # std
            dt_raw = wide_to_long(DT[item])
            dtw_tmp = DT[item].copy()
            dtw_tmp = pd.concat([get_std_dt(dtw_tmp[:PARAM["pX"]]),
                                 get_std_dt(dtw_tmp[PARAM["pX"]:])],
                                axis=0)
            dt_std = wide_to_long(dtw_tmp)
            dt_raw["value_std"] = dt_std["value"]

            # change tickers
            specify_tickers(
                HT[item], DT[item], yticks=DT["sol"]["terms"].values)
        elif item == "A":
            # update ped heatmap
            dt_raw = wide_to_long(DT[item])
            dt_raw["value_std"] = dt_raw["value"]

            # change tickers
            specify_tickers(
                HT[item], DT[item],
                xticks=DT[item].columns,
                yticks=DT[item].columns)

        # update source
        dt_raw.loc[dt_raw.value == 0, "value_std"] = -5
        SRC[item].data = dt_raw
