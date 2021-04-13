from enum import Enum

class DATA(Enum):
    DEMO_1 = dict({"name": "Animal Model",
                   "path": "myapp/data/demo_1.csv"})
    DEMO_2 = dict({"name": "Common Environmental Effects",
                   "path": "myapp/data/demo_2.csv"})
    DEMO_3 = dict({"name": "Maternal Genetics Effects",
                   "path": "myapp/data/demo_3.csv"})

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
    EQ = "myapp/static/img_eq2.png"
    X =  "myapp/static/img_X.png"
    Z =  "myapp/static/img_Z.png"


class CUS(Enum):
    DATA = "myapp/data/customized.csv"
    PED  = "myapp/data/customized.ped"
    Gstr = "myapp/data/Gstr.csv"
    Giid = "myapp/data/Giid.csv"
    Gres = "myapp/data/Gres.csv"


exec_Julia = "/usr/local/bin/julia"
param_Julia = "myapp/out/param.csv"

