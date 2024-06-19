from .approximation import Approximation


def turn_type(inc: Approximation, out: Approximation) -> str:
    delta = (out.bearing - inc.bearing) - 180
    while delta < 0:
        delta += 360

    if delta >= 315 or delta <= 45:
        return "UTURN"
    elif 135 < delta < 225:
        return "THRU"
    elif 45 < delta <= 135:
        return "LEFT"
    return "RIGHT"
