#!/usr/bin/env python3

from classes import *

class Gun_12inch_dual(Turret):
    max_ammo = 80
    _image_name = "images/turrets/double_turret.bmp"

    def __init__(self, parent, pos_fore, pos_centre, base_angle=0, max_langle=100, max_rangle=100):
        super().__init__(parent, pos_fore, pos_centre, base_angle, max_langle, max_rangle)
