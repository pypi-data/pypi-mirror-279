from pyphy.vector2 import Vector2
from pyphy.world import World
from pyphy.body import Body
import pygame as pg

pg.init()

WIDTH, HEIGHT = 1280, 720
WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Dummy File')

FONT = pg.font.SysFont(None, 50)

space = World(WINDOW, (0, 9.8))
space.CreateBounds()

t1 = Body.CreateBoxBody(500, 50, Vector2(350, 400), 1000, 0.8, True)
t1.Rotate(0.3)
space.AddBody(t1)

t2 = Body.CreateBoxBody(400, 50, Vector2(850, 200), 1000, 0.8, True)
t2.Rotate(-2.2)
space.AddBody(t2)

def DrawText(text, pos) -> None:
    text = FONT.render(text, True, 'green')
    WINDOW.blit(text, pos)

def AddShape(button, pos) -> None:
    body = None
    if button == 1:
        body = Body.CreateCircleBody(25, Vector2(*pos), 100, 0.7, False)
    elif button == 3:
        body = Body.CreateBoxBody(50, 50, Vector2(*pos), 100, 0.7, False)
    if body is not None:
        space.AddBody(body)

clock = pg.time.Clock()

while True:
    WINDOW.fill('black')
    dt = clock.tick() / 1000

    space.step(dt)
    space.Render()

    DrawText(str(round(clock.get_fps(), 2)), (10, 10))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            AddShape(event.button, event.pos)

    pg.display.update()