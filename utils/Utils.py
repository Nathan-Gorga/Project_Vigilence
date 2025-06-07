from include import TOLERANCE


def isSameEvent(x1 :int,x2 :int):
    return (x1 - TOLERANCE) <= x2 <= (x1 + TOLERANCE)


def findLocalMaximum(buffer :list[int]):
    return max(buffer)