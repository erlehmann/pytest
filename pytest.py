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

from random import choice
from sys import argv, stdout

FRAMERATE = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Game(object):

    def __init__(self, time, symbols, colors):
        self.frames = time * FRAMERATE
        self.symbols = symbols
        self.colors = colors

        pygame.init()
        pygame.display.set_caption('PyTest')

        self.size = self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode(self.size)

        self.font = pygame.font.SysFont("sans", 120)

        self.clock = pygame.time.Clock()

    def render_text(self, text, color):
        surface = self.font.render(text, 1, color)
        self.screen.fill(BLACK)
        self.screen.blit(
            surface,
                (
                    self.width/2-(surface.get_height()/2),
                    self.height/2-(surface.get_height()/2)
                )
            )
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.log("EVENT", "KEYDOWN")

    def log(self, event_type, text):
        stdout.write(
            "%s\t%s\t%s\n" % (
                pygame.time.get_ticks(),
                event_type,
                text
            )
        )
        stdout.flush()

    def intro(self):
        frames = 99
        for i in range(frames):
            self.clock.tick(FRAMERATE)
            self.render_text('%i' % (frames-i), WHITE)

    def run(self):
        self.log("EVENT", "START")
        for i in range(self.frames):
            self.clock.tick(FRAMERATE)
            for event in pygame.event.get():
                self.handle_event(event)
            if (i%FRAMERATE == 0):
                symbol = choice(self.symbols)
                color = colors[i/FRAMERATE%len(colors)]
                self.render_text(symbol, color)
                self.log("SYMBOL", symbol)

        self.log("EVENT", "END")

if __name__ == '__main__':
    time = int(argv[1])
    symbols = [u'■', u'▲', u'●', u'◆']
    colors = [
        (115, 210, 22),  # tango green 2
        (79, 152, 247),  # tango blue 2
        (204, 0, 0),  # tango red 2
        (237, 212, 0)  # tango orange 2
    ]

    game = Game(time=time, symbols=symbols, colors=colors)
    game.intro()
    game.run()
