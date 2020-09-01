#
# Kod pomocniczy
#

from typing import Union
from numpy import fmax, fmin

class CartForce:
    UNIT_LEFT = -1 # jednostkowe pchnięcie wzóka w lewo [N]
    UNIT_RIGHT = 1 # jednostkowe pchnięcie wózka w prawo [N]
    IDLE_FORCE = 0


class HumanControl(object):
    UserForce = None # type: Union [int, None] # siła, którą użytkownik chce pchnąć wózek
    WantReset = False
    WantPause = False
    WantExit = False


class Keys(object):
    LEFT = 0xFF51
    RIGHT = 0xFF53
    ESCAPE = 0xFF1B
    P = 112
    Q = 113
    R = 114

class Ops(object):
    
    def Or(cond1, cond2):
        return fmax(cond1, cond2)
    
    def And(cond1, cond2):
        return fmin(cond1, cond2)
    
    def Aggregate(*conditions):
        l = len(conditions)
        if l > 1:
            cond = conditions[0]
            for i in range(1, l):
                cond = Ops.Or(cond, conditions[i])
                
            return cond
        return None
    
        