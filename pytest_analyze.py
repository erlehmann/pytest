#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PyTest Analyze
# ⓒ 2012  Nils Dagsson Moskopp

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Dieses Programm hat das Ziel, die Medienkompetenz der Leser zu
# steigern. Gelegentlich packe ich sogar einen handfesten Buffer
# Overflow oder eine Format String Vulnerability zwischen die anderen
# Codezeilen und schreibe das auch nicht dran.

from codecs import getreader, getwriter
from math import sqrt
from sys import argv, stdin, stdout
stdin = getreader('utf8')(stdin)
stdout = getwriter('utf8')(stdout)

FRAMERATE = 60

reaction_times = []
positives = []
false_positives = []
false_negatives = []

currentsymbol = ''
lastsymbol = ''
keypressed = False
currentsymbol_timestamp = 0

for row in stdin:
    rowparts = row.strip().split('\t')
    timestamp = int(rowparts[0])
    event_type = rowparts[1]
    text = rowparts[2]

    if event_type == 'EVENT' and text == 'KEYDOWN':
        if currentsymbol_timestamp == 0:
            continue
        reaction_times.append(timestamp - currentsymbol_timestamp)
        if (lastsymbol == currentsymbol):  # positive
            positives.append(timestamp)
        if (lastsymbol != currentsymbol):  # false positive
            false_positives.append(timestamp)
        keypressed = True

    if event_type == 'SYMBOL':
        if (currentsymbol_timestamp > 0) and \
            (lastsymbol == currentsymbol) and \
            not keypressed:  # false negative
            false_negatives.append(timestamp)
        lastsymbol = currentsymbol
        currentsymbol = text
        currentsymbol_timestamp = timestamp
        keypressed = False

def average(l):
    return sum(l)/len(l)

def variance(l):
    return [(e - average(l))**2 for e in l]

def standard_deviation(l):
    return sqrt(average(variance(l)))


stdout.write('Reaction time average (ms):\n\t%i\n' % average(reaction_times))
stdout.write('Reaction time standard deviation (ms):\n\t%i\n' % standard_deviation(reaction_times))
stdout.write('Positives:\n\t%i\n' % len(positives))
stdout.write('False positives:\n\t%i\n' % len(false_positives))
stdout.write('False negatives:\n\t%i\n' % len(false_negatives))
stdout.write('Reaction times (ms):\n\t%s\n' % reaction_times)
stdout.write('Reaction times variance (ms²):\n\t%s\n'.decode('utf8') % variance(reaction_times))
stdout.write('Positives list:\n\t%s\n' % positives)
stdout.write('False positives list:\n\t%s\n' % false_positives)
stdout.write('False negatives list:\n\t%s\n' % false_negatives)
