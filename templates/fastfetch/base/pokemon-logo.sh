#!/usr/bin/env python3
"""Wrapper for fastfetch that shows a random Pokémon sprite from local files.
Outputs a fixed-height canvas with the sprite centered vertically."""

import os
import random
import re
import sys

CANVAS_HEIGHT = 13

SPRITES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sprites')

ANSI_RE = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]|\x1b\([B0-9]')

def strip_ansi(s):
    return ANSI_RE.sub('', s)

# Get all sprite files
sprites = [f for f in os.listdir(SPRITES_DIR) if f.endswith('.txt')]
if not sprites:
    sys.stdout.write('\n' * CANVAS_HEIGHT)
    sys.exit(0)

# Pick random sprite
sprite_file = os.path.join(SPRITES_DIR, random.choice(sprites))
with open(sprite_file, 'r') as f:
    sprite = f.read().rstrip('\n')

lines = sprite.split('\n')

# Strip leading/trailing whitespace-only lines
while lines and not strip_ansi(lines[0]).strip():
    lines.pop(0)
while lines and not strip_ansi(lines[-1]).strip():
    lines.pop()

if not lines:
    sys.stdout.write('\n' * CANVAS_HEIGHT)
    sys.exit(0)

sprite_height = len(lines)

# Crop or pad to exactly CANVAS_HEIGHT, centered vertically
if sprite_height > CANVAS_HEIGHT:
    start = (sprite_height - CANVAS_HEIGHT) // 2
    display_lines = lines[start:start + CANVAS_HEIGHT]
else:
    top_pad = (CANVAS_HEIGHT - sprite_height) // 2
    bottom_pad = CANVAS_HEIGHT - sprite_height - top_pad
    display_lines = [''] * top_pad + lines + [''] * bottom_pad

sys.stdout.write('\n'.join(display_lines) + '\n')
