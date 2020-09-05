#
# Kod pomocniczy
#

from typing import Union
from numpy import fmax, fmin, arange, pi
from skfuzzy import trapmf, trimf, interp_membership, defuzz

IsTask_2 = True

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
        return conditions[0]
    
    def GenerateFuzzyMemberships(domain, **kwargs):
        return {k : (trapmf(domain, v) if len(v) == 4 else trimf(domain, v)) for k, v in kwargs.items() }
    
    def GetRules(membership_functions, domain, measured_value):
        return {f"is_{k}" : interp_membership(domain, v, measured_value) for k,v in membership_functions.items()}
    
    def Conclude(antecedent, consequent):
        return Ops.And(antecedent, consequent)

    def Defuzz(domain, aggregated_conclusions, mode='Centroid'):
        return defuzz(domain, aggregated_conclusions, mode)
    
            
class RealDomains(object):
    def __init__(self):
        self.PendulumAngles = arange(-2 * pi, 2 * pi, pi/96)
        self.CartVelocities = arange(-3, 3, 0.01)
        self.CartPositions = arange(-2.5, 2.5, 0.01) if IsTask_2 else None
        self.CartDeltas = arange(-2.5, 2.5, 0.01) if not IsTask_2 else None
        self.CartForces = arange(-30, 30, 0.01)
        self.PendulumVelocities = arange(-1.5, 1.5, 0.01)