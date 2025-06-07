from numpy import max

from include import TOLERANCE


def isSameEvent(x1 :int,x2 :int):
    return (x1 - TOLERANCE) <= x2 <= (x1 + TOLERANCE)


def findLocalMaximum(buffer :list[int]):
    if buffer == []: raise ValueError("Provided buffer is empty")
    return max(buffer)

def localMaximumIndex(buffer :list[int], offset : int = 0):
    return offset + buffer.index(findLocalMaximum(buffer))