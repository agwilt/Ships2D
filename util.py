#!/usr/bin/env python3

def colour_replace(surface, old_col, new_col):
    for x in range(surface.get_size()[0]):
        for y in range(surface.get_size()[1]):
            if surface.get_at([x,y]) == old_col:
                surface.set_at([x,y], new_col)
    return surface
