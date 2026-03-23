from code.entities.coin import Coin
from code.entities.obstacle import Obstacle
from code.entities.player import Player


class EntityFactory:
    @staticmethod
    def create(entity_name: str):
        match entity_name:
            case 'Player':
                return Player()
            case 'Obstacle':
                return Obstacle()
            case 'Coin':
                return Coin()
            case _:
                raise ValueError(f'Entidade desconhecida: {entity_name}')
