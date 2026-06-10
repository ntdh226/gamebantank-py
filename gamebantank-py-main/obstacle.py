 # obstacle.py
class Obstacle:
    EMPTY  = 0
    BRICK  = 1
    STEEL  = 2
    WATER  = 3
    FOREST = 4
    BASE   = 5

PASSABLE = {
    Obstacle.EMPTY:  True,
    Obstacle.BRICK:  False,
    Obstacle.STEEL:  False,
    Obstacle.WATER:  False,
    Obstacle.FOREST: True,
    Obstacle.BASE:   False,
}

DESTRUCTIBLE = {
    Obstacle.BRICK: True,
    Obstacle.STEEL: False,
    Obstacle.BASE:  True,
}

COLORS = {
    Obstacle.EMPTY:  (0,   0,   0),
    Obstacle.BRICK:  (180, 80,  20),
    Obstacle.STEEL:  (150, 150, 150),
    Obstacle.WATER:  (0,   80,  200),
    Obstacle.FOREST: (0,   120, 0),
    Obstacle.BASE:   (255, 200, 0),
}