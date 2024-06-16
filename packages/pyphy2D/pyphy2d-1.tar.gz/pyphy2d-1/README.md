# PyPhy2D

## Description
PyPhy2D is a 2D Rigid Body Physics Engine designed to simulate physical interactions of objects in a two-dimensional space. It is easy to integrate and can be used for games, simulations, and educational purposes.

## License
This project is licensed under the MIT License.

## Installation
Before installing PyPhy2D, ensure you have pygame or pygame-ce installed:

```sh
pip install pygame

```
or
```sh
pip install pygame-ce

```

## Example Project
```python
from pyphy import World, Body, Vector2
import pygame
import sys

WIDTH, HEIGHT = 900, 900
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

space = World(window=WINDOW, gravity=(0, 9.8))

clock = pygame.time.Clock()
FPS = 60

testBody = Body.CreateCircleBody(radius=25, center=Vector2(100, 100), density=1.2, restitution=0.8, static=False)
space.AddBody(testBody)

while True:
    dt = clock.tick(FPS) / 1000

    space.step(dt)

    WINDOW.fill((0, 0, 0))
    space.Render()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
```