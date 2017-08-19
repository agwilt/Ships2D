#!/usr/bin/env python3

import util
from classes import *
import turrets

class Dreadnought(Ship):

    class_name = "Dreadnought"
    _image_name = "images/ships/HMS Dreadnought.bmp"

    armour_deck = 20 # [mm]
    armour_belt = 250 # [mm]

    fuel_type = Fuel.Coal
    fuel_cap = 3000 # [t]
    fuel_cons = 9.5 # v * capacity / range [t/h]

    max_speed = 39 # [km/h]
    turn_rad = 700 # [m]

    dim_length = 160
    dim_beam = 25
    dim_draught = 9

    def __init__(self, name):
        super().__init__(name)

        self.turret_names = {'A':turrets.Gun_12inch_dual(self, 57, 0), 'X':turrets.Gun_12inch_dual(self, 0, 0, base_angle=180), 'Y':turrets.Gun_12inch_dual(self, 0, 0, base_angle=180), 'L':turrets.Gun_12inch_dual(self, 43, -4, max_langle=180, max_rangle=0), 'R':turrets.Gun_12inch_dual(self, 43, 4, max_langle=0, max_rangle=180)}
        for tur_name in self.turret_names:
            self.turrets.add(self.turret_names[tur_name])
        self.weapon_groups = [pygame.sprite.Group() for i in range(9)]

        self.res_fuel = self.fuel_cap
        self.res_water = 0
