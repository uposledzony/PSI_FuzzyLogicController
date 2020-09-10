# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 18:13:09 2020

@author: Kamil Chrustowski
"""
from numpy import pi

class Force:
    VeryHigh = 30
    High = 10
    MidHigh = 8
    Mid = 5
    MidLight = 1.3
    Light = 0.3
    Idle = 0.0
    HighVec = [MidHigh, High, VeryHigh, VeryHigh]
    MidHighVec = [Mid, MidHigh, High]
    MidVec = [MidLight, Mid, MidHigh]
    MidLightVec = [Light, MidLight, Mid]
    LightVec = [Idle, Light, MidLight]
    IdleVec = [-Light, Idle, Light]

class Distance:
    VeryFar = 2.5
    Far = 1.7
    MidFar = 1.3
    Mid = 0.5
    Close = 0.01
    InPlace = 0
    FarVec=[MidFar, Far, VeryFar, VeryFar]
    MidFarVec=[Mid, MidFar, Far]
    MidVec=[Close, Mid, MidFar]
    CloseVec=[InPlace, Close, Mid]
    InPlaceVec=[-Close, InPlace, Close]
    
class Angle:
    VeryLarge = pi
    Large = pi/4
    MidLarge = pi/8
    Mid = pi/64
    Small = pi/512
    Zero = 0
    LargeVec=[MidLarge, Large, VeryLarge, VeryLarge]
    MidLargeVec=[Mid, MidLarge, Large]
    MidVec=[Small, Mid, MidLarge]
    SmallVec=[Zero, Small, Mid]
    ZeroVec=[-Small, Zero, Small]
    
class Velocity:
    VeryHigh = 3
    High = 1.5
    Mid = 0.4
    Small = 0.016125
    Idle = 0
    HighVec=[Mid, High, VeryHigh]
    MidVec=[Small, Mid, High]
    SmallVec=[Idle, Small, Mid]
    IdleVec=[-Small, Idle, Small]
    
class AngleVelocity:
    VeryHigh = 1.5
    High = 0.625
    Mid = 0.2825
    Small = 0.18
    Idle = 0
    HighVec=[Mid, High, VeryHigh]
    MidVec=[Small, Mid, High]
    SmallVec=[Idle, Small, Mid]
    IdleVec=[-Small, Idle, Small]