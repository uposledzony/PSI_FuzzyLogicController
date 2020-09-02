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
        return None
    
    def GenerateFuzzyMemberships(domain, very_high, high, mid_high, mid, mid_low, low, very_low):
        return {
                    "low" : trapmf(domain, [very_low, very_low, low, mid_low]),
                    "mid_low": trimf(domain, [low, mid_low, mid]),
                    "mid" : trimf(domain, [mid_low, mid, mid_high]),
                    "mid_high" : trimf(domain, [mid, mid_high, high]),
                    "high" : trapmf(domain, [mid_high, high, very_high, very_high])
               }
    
    def GetRules(membership_functions, domain, measured_value):
        return {f"is_{k}" : interp_membership(domain, v, measured_value) for k,v in membership_functions.items()}
    
    def Conclude(antecedent, consequent):
        return Ops.And(antecedent, consequent)

    def Defuzz(domain, aggregated_conclusions, mode='Centroid'):
        return defuzz(domain, aggregated_conclusions, mode)
    
class Defaults(object):
    class Force:
        VeryHigh = 30
        High = 10
        MidHigh = 1
        Idle = 0
        MidHighNegative = -MidHigh
        HighNegative = -High
        VeryHighNegative = -VeryHigh

    class Distance:
        VeryFar = 2.5
        Far = 1
        MidFar = 0.1
        InPlace = 0
        MidFarNegative = -MidFar
        FarNegative = -Far
        VeryFarNegative = -VeryFar
        
    class Angle:
        VeryLarge = pi/2
        Large = pi/4
        MidLarge = pi/8
        Zero = 0
        MidLargeNegative = -MidLarge
        LargeNegative = -Large
        VeryLargeNegative = -VeryLarge
        
    class Velocity:
        VeryHigh = 3
        High = 1
        MidHigh = 0.3125
        Idle = 0
        MidHighNegative = -MidHigh
        HighNegative = -High
        VeryHighNegative = -VeryHigh
        

class RealDomains(object):
    def __init__(self):
        self.PendulumAngles = arange(-2 * pi, 2 * pi, pi/24)
        self.CartVelocities = arange(-3, 3, 0.0625)
        self.CartPositions = arange(-6, 6, 0.125) if IsTask_2 else None
        self.CartDeltas = arange(-6, 6, 0.125) if not IsTask_2 else None
        self.CartForces = arange(-30, 30, 0.625)
        self.PendulumVelocities = arange(-3, 3, 0.0625)