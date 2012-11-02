#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PyTest
# ⓒ 2012  Nils Dagsson Moskopp

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Dieses Programm hat das Ziel, die Medienkompetenz der Leser zu
# steigern. Gelegentlich packe ich sogar einen handfesten Buffer
# Overflow oder eine Format String Vulnerability zwischen die anderen
# Codezeilen und schreibe das auch nicht dran.

import pygame

from pprint import PrettyPrinter
from random import choice

FRAMERATE = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Game(object):

    def __init__(self, symbols, colors):
        self.symbols = symbols
        self.colors = colors

        pygame.init()
        pygame.display.set_caption('PyTest')

        self.size = self.width, self.height = 640, 480
        self.screen = pygame.display.set_mode(self.size)

        self.font = pygame.font.SysFont("monospace", 120)

        self.clock = pygame.time.Clock()

        self.lastsymbol = ''
        self.currentsymbol = ''
        self.keypressed = False

        self.events = {}

    def draw_symbol(self, symbol, color):
        surface = self.font.render(symbol, 1, color)
        s_width, s_height = surface.get_width(), surface.get_height()
        self.screen.blit(
            surface,
                (
                    self.width/2-(s_width/2),
                    self.height/2-(s_height/2)
                )
            )

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if (self.lastsymbol == self.currentsymbol):
                if self.keypressed:
                    self.store('duplicate positive')
                else:
                    self.store('positive')
            else:
                if self.keypressed:
                    self.store('duplicate false positive')
                else:
                    self.store('false positive')
            self.keypressed = True

    def store(self, name):
        self.events[pygame.time.get_ticks()]=name

    def run(self):
        pygame.time.wait(1000)
        for i in range(1200):
            self.clock.tick(FRAMERATE)
            for event in pygame.event.get():
                self.handle_event(event)
            if (i%FRAMERATE == 0):
                if (self.keypressed == False) and \
                    (self.lastsymbol == self.currentsymbol):
                    self.store('false negative')
                self.keypressed = False
                self.screen.fill(BLACK)
                self.lastsymbol = self.currentsymbol
                self.currentsymbol = choice(self.symbols)
                symbolcolor = colors[i/FRAMERATE%len(colors)]
                self.draw_symbol(self.currentsymbol, symbolcolor)
                pygame.display.flip()
                self.store('new symbol')

    def stats(self):
        pp = PrettyPrinter(indent=4)
        pp.pprint(self.events)

if __name__ == '__main__':
    symbols = [u'■', u'▲', u'●', u'◆']
    colors = [
        (115, 210, 22),  # tango green 2
        (79, 152, 247),  # tango blue 2
        (204, 0, 0),  # tango red 2
        (237, 212, 0)  # tango orange 2
    ]

    game = Game(symbols=symbols, colors=colors)
    game.run()
    game.stats()
