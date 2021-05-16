from enum import Enum

class DATA(Enum):
    DEMO_1 = dict({"name": "Animal Model",
                   "path": "myapp/data/D_AnimalModel.csv"})
    DEMO_2 = dict({"name": "Repeatability Model",
                   "path": "myapp/data/D_Repeat.csv"})
    DEMO_3 = dict({"name": "Common Environmental Effects",
                   "path": "myapp/data/D_CommonEnv.csv"})
    DEMO_4 = dict({"name": "Maternal Genetic Effects",
                   "path": "myapp/data/D_Maternal.csv"})

    def get_members():
        return DATA._member_names_

    def get_names():
        return [DATA[name].value["name"] for name in DATA._member_names_]

    def get_paths():
        return [DATA[name].value["path"] for name in DATA._member_names_]

    def get_path_by_name(name):
        idx = DATA.get_index(name)
        return DATA.get_paths()[idx]

    def get_enum_by_name(name):
        idx = DATA.get_index(name)
        return DATA.get_enum_by_index(idx)

    def get_enum_by_index(index):
        return DATA[DATA.get_members()[index]]

    def get_index(name):
        idx = [DATA[name].value["name"]
               for name in DATA.__members__].index(name)
        return idx


class IMG(Enum):
    EQ = "myapp/static/img_eq3.png"
    X =  "myapp/static/img_x.png"
    Z =  "myapp/static/img_z.png"


class CUS(Enum):
    DATA = "myapp/data/customized.csv"
    PED  = "myapp/data/customized.ped"
    Gstr = "myapp/data/Gstr.csv"
    Giid = "myapp/data/Giid.csv"
    Gres = "myapp/data/Gres.csv"


exec_Julia = "/usr/local/bin/julia"
param_Julia = "myapp/out/param.csv"

