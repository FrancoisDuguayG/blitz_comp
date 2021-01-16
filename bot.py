from typing import List
from game_message import GameMessage, Position, Crew, TileType
from game_command import Action, UnitAction, UnitActionType, ActionType, UnitType, BuyAction
import random




class Bot:

    def get_next_move(self, game_message: GameMessage) -> List[Action]:
        """
        Here is where the magic happens, for now the moves are random. I bet you can do better ;)

        No path finding is required, you can simply send a destination per unit and the game will move your unit towards
        it in the next turns.
        """
        my_crew: Crew = game_message.get_crews_by_id()[game_message.crewId]

        mines = []
        for y in range(0, game_message.map.get_map_size()):
            for x in range(0, game_message.map.get_map_size()):
                if game_message.map.tiles[x][y] == "MINE":
                    mines.append(Position(x, y))

        print(mines)

        for mine in mines:
            for i in get_adj(mine):
                if



        # drop_out = mines[0]
        # drop_out.x -= 1
        # drop_out.y -= 1


        actions: List[UnitAction] = []
        # UnitAction(UnitActionType.MOVE,
        #                                     unit.id,
        #                                     mines[0]) for unit in my_crew.units]

        for unit in my_crew.units:
            if unit.type == UnitType.MINER:
                print(unit.id, unit.position, unit.blitzium)
                # path = self.get_closer_rock(game_message.map, unit.position, mines[0])
                if adj(unit.position, mines[0]) or unit.blitzium == 5:
                    if unit.blitzium < 5:
                        print(unit.position)
                        actions.append(UnitAction(UnitActionType.MINE, unit.id, mines[0]))
                    else:
                        if adj(unit.position, my_crew.homeBase):
                            actions.append(UnitAction(UnitActionType.DROP, unit.id, my_crew.homeBase))
                        else:
                            target = Position(my_crew.homeBase.x - 1, my_crew.homeBase.y)
                            actions.append(UnitAction(UnitActionType.MOVE, unit.id, target))
                else:
                    target = Position(mines[0].x - 1, mines[0].y)
                    actions.append(UnitAction(UnitActionType.MOVE, unit.id, target))

        print(my_crew.blitzium, len(my_crew.units))

        # if my_crew.prices.CART <= my_crew.blitzium and len(my_crew.units) < 2:
        #     actions.append(BuyAction(UnitType.CART))

        print(game_message.map.tiles)

        return actions

    def get_random_position(self, map_size: int) -> Position:
        return Position(random.randint(0, map_size - 1), random.randint(0, map_size - 1))

    def get_closer_rock(self, map, position, mine_position):
        list_tiles = map.tiles
        start_x, start_y = position.x, position.y
        list_tiles[start_y][start_x] = 0

        initial = (start_x, start_y)
        visited = []
        queue = [initial]
        distance = 0

        while queue:
            pos = queue.pop(0)
            if pos not in visited:
                start_x, start_y = pos
                distance = list_tiles[start_y][start_x]
                visited.append(pos)
                neighbours = [(start_x + 1, start_y), (start_x - 1, start_y), (start_x, start_y + 1),
                              (start_x, start_y - 1)]
                for neighbour in neighbours:
                    start_x, start_y = neighbour
                    if list_tiles[start_y][start_x] == 'EMPTY':
                        queue.append(neighbour)
                        list_tiles[start_y][start_x] = distance + 1

        x, y = mine_position.x, mine_position.y
        path = []
        while x != position.x and y != position.y:
            neighbours = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            min = 1000
            next = ()
            for neighbour in neighbours:
                val = list_tiles[neighbour[1]][neighbour[0]]
                if isinstance(val, int) and val < min:
                    min = val
                    next = (neighbour[0], neighbour[1])

            path.append(next)
            x, y = next
        path.reverse()
        return path


def adj(pos1, pos2):
    return abs((pos1.x - pos2.x) + (pos1.y - pos2.y)) == 1

def get_adj(pos):
    x, y = pos.x, pos.y
    return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
