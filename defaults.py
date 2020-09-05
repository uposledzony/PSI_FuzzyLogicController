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
        Mid = 3
        MidLight = 1.5
        Light = 0.7
        Idle = 0
        HighVec = [MidHigh, High, VeryHigh, VeryHigh]
        MidHighVec = [Mid, MidHigh, High]
        MidVec = [MidLight, Mid, MidHigh]
        MidLightVec = [Light, MidLight, Mid]
        LightVec = [Idle, Light, MidLight]
        IdleVec = [-Light, Idle, Light]

class Distance:
        VeryFar = 2.5
        Far = 1.7
        MidFar = 1
        Mid =0.7
        Close = 0.1
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
        Mid = pi/32
        Small = pi/64
        Zero = 0
        LargeVec=[MidLarge, Large, VeryLarge, VeryLarge]
        MidLargeVec=[Mid, MidLarge, Large]
        MidVec=[Small, Mid, MidLarge]
        SmallVec=[Zero, Small, Mid]
        ZeroVec=[-Small, Zero, Small]
        
class Velocity:
        VeryHigh = 3
        High = 2
        Mid = 1.5
        Small = 0.3125
        Idle = 0
        HighVec=[Mid, High, VeryHigh]
        MidVec=[Small, Mid, High]
        SmallVec=[Idle, Small, Mid]
        IdleVec=[-Small, Idle, Small]
        
class AngleVelocity:
        VeryHigh = 1.5
        High = 0.625
        Mid = 0.2125
        Small = 0.07
        Idle = 0
        HighVec=[Mid, High, VeryHigh]
        MidVec=[Small, Mid, High]
        SmallVec=[Idle, Small, Mid]
        IdleVec=[-Small, Idle, Small]