from numpy import max,min

from include import TOLERANCE, BASICALLY_ZERO


def isSameEvent(x1 :int,x2 :int):
    return (x1 - TOLERANCE) <= x2 <= (x1 + TOLERANCE)


def findLocalMaximum(buffer :list[int]):
    if buffer == []: raise ValueError("Provided buffer is empty")
    return max(buffer)

def localMaximumIndex(buffer :list[int], offset : int = 0):
    return offset + buffer.index(findLocalMaximum(buffer))

def isBaseline(buffer):
    top = BASICALLY_ZERO
    bottom = -BASICALLY_ZERO
    
    bMax = max(buffer)
    bMin = min(buffer)
    
    return bMax <= top and bMin >= bottom 