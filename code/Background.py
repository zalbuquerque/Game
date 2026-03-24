from code.Const import WIN_WIDTH
from code.Entity import Entity


BACKGROUND_SPEED = {
    "Level1Bg0": 0,
    "Level1Bg1": 1,
    "Level1Bg2": 2,
    "Level1Bg3": 3,
    "Level1Bg4": 4,
    "Level1Bg5": 5,
    "Level1Bg6": 2,
}


class Background(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)

    def move(self):
        self.rect.centerx -= BACKGROUND_SPEED.get(self.name, 0)
        if self.rect.right <= 0:
            self.rect.left = WIN_WIDTH
