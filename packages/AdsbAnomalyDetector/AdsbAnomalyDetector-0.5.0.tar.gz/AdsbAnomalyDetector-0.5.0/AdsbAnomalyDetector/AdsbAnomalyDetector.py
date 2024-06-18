from ._Utils_os_wrapper import os
from ._Utils_numpy import np, ax
from . import _Utils_geographic_maths as geo
HERE = os.path.abspath(os.path.dirname(__file__))
from ._Utils_module import module_to_dict
from .E_Trainer_TrajectorySeparator_Trainer import Trainer as TrajectorySeparator
from .E_Trainer_AircraftClassification_Trainer import Trainer as AircraftClassification
from .E_Trainer_FloodingSolver_Trainer import Trainer as FloodingSolver
from .E_Trainer_ReplaySolver_Trainer import Trainer as ReplaySolver
from . import _Utils_FeatureGetter as FG
from ._Utils_ADSB_Streamer import cast_msg

def getCTX(CTX, default_CTX=None):
    CTX = module_to_dict(CTX)
    if (default_CTX != None):
        default_CTX = module_to_dict(default_CTX)
        for param in default_CTX:
            if (param not in CTX):
                CTX[param] = default_CTX[param]
    return CTX



from .B_Model_AircraftClassification_CNN2 import Model as CNN2
from . import C_Constants_AircraftClassification_CNN as CNN2_CTX
from . import C_Constants_AircraftClassification_DefaultCTX as CNN2_DefaultCTX
CTX_AC = getCTX(CNN2_CTX, CNN2_DefaultCTX)
aircraftClassification = AircraftClassification(CTX_AC, CNN2)
aircraftClassification.load(HERE+"/AircraftClassification")


from .B_Model_TrajectorySeparator_GeoModel import Model as GEO
from . import C_Constants_TrajectorySeparator_Model as GEO_CTX
from . import C_Constants_TrajectorySeparator_DefaultCTX as GEO_DefaultCTX
from .D_DataLoader_AircraftClassification_Utils import getLabel
CTX_TS = getCTX(GEO_CTX, GEO_DefaultCTX)
trajectorySeparator = TrajectorySeparator(CTX_TS, GEO)
trajectorySeparator.load(HERE+"/TrajectorySeparator")

from .B_Model_FloodingSolver_LSTM import Model as LSTM
from . import C_Constants_FloodingSolver_LSTM as LSTM_CTX
from . import C_Constants_FloodingSolver_DefaultCTX as LSTM_DefaultCTX
CTX_FS = getCTX(LSTM_CTX, LSTM_DefaultCTX)
floodingSolver = FloodingSolver(CTX_FS, LSTM)
floodingSolver.load(HERE+"/FloodingSolver")

from .B_Model_ReplaySolver_HASH import Model as HASH
from . import C_Constants_ReplaySolver_HASH as HASH_CTX
from . import C_Constants_ReplaySolver_DefaultCTX as HASH_DefaultCTX
CTX_RS = getCTX(HASH_CTX, HASH_DefaultCTX)
replaySolver = ReplaySolver(CTX_RS, HASH)
replaySolver.load(HERE+"/ReplaySolver")



def get(lst, bool_arr) -> list:
    return [lst[i] for i in range(len(lst)) if bool_arr[i]]



def predict(messages: "list[dict[str, str]]") -> "list[dict[str, str]]":
    for i in range(len(messages)):
        messages[i] = {col:cast_msg(col,  messages[i].get(col, np.nan)) for col in messages[i]}

    FG.init(CTX_TS)
    sub_icaos = trajectorySeparator.predict(messages)
    for i in range(len(messages)):
        messages[i]["icao24"] = sub_icaos[i]

    FG.init(CTX_RS)
    matches = replaySolver.predict(messages)
    for i in range(len(messages)):
        messages[i]["replay"] = (matches[i] != "none" and matches[i] != "unknown")

    FG.init(CTX_FS)
    y_, y = floodingSolver.predict(messages)
    for i in range(len(messages)):
        d = geo.distance(y_[i][0], y_[i][1], y[i][0], y[i][1])
        messages[i]["flooding"] = (d > CTX_FS["THRESHOLD"])

    FG.init(CTX_AC)
    _, label_proba = aircraftClassification.predict(messages)
    spoofing = is_spoofing(messages, label_proba)
    for i in range(len(messages)):
        messages[i]["spoofing"] = spoofing[i]

    return messages


# |====================================================================================================================
# | UTILS
# |====================================================================================================================


def get_base_icaos(messages: "list[dict[str, str]]") -> "list[str]":
    icaos = [messages[i]["icao24"] for i in range(len(messages))]
    return [icaos[i].split("_")[0] if ("_" in icaos[i]) else icaos[i] for i in range(len(icaos))]

def get_true_aircraft_type(messages: "list[dict[str, str]]") -> "list[int]":
    icaos = get_base_icaos(messages)
    return [getLabel(CTX_AC, icaos[i]) for i in range(len(icaos))]


def get_pred_aircraft_type(proba: "np.ndarray") -> "list[int]":
    argmax = np.argmax(proba, axis=1)
    confidence = np.nan_to_num([proba[i][argmax[i]] for i in range(len(argmax))])
    return [0 if confidence[i] <= 0.5 else CTX_AC["USED_LABELS"][argmax[i]] for i in range(len(argmax))]

def is_spoofing(messages: "list[dict[str, str]]", predictions: "np.ndarray") -> "list[bool]":
    true_labels = get_true_aircraft_type(messages)
    pred_labels = get_pred_aircraft_type(predictions)

    return [pred_labels[i] != 0
        and pred_labels[i] != true_labels[i]
        for i in range(len(true_labels))]