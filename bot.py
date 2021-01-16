from typing import List
from game_message import GameMessage, Position, Crew, TileType, Map
from game_command import Action, UnitAction, UnitActionType, ActionType, UnitType, BuyAction
import random


class Bot:
    def __init__(self):
        self.initialisation = True
        self.mines = []
        self.target_mine = None
        self.miner_target = None
        self.car_target = None
        self.car_base = None

    def init(self, game_message: GameMessage):
        my_crew: Crew = game_message.get_crews_by_id()[game_message.crewId]
        map = game_message.map
        for y in range(0, map.get_map_size()):
            for x in range(0, map.get_map_size()):
                if map.tiles[x][y] == "MINE":
                    self.mines.append(Position(x, y))
        self.target_mine = min(self.mines, key=lambda k: distance(k, my_crew.homeBase))
        self.miner_target = min(map.get_adj(self.target_mine), key=lambda k: distance(k, my_crew.homeBase))
        self.miner_target = min(map.get_adj(self.target_mine), key=lambda k: distance(k, my_crew.homeBase))
        self.car_target = min(map.get_adj(self.miner_target), key=lambda k: distance(k, my_crew.homeBase))
        self.car_base = min(map.get_adj(my_crew.homeBase), key=lambda k: distance(k, self.car_target))

    def get_next_move(self, game_message: GameMessage) -> List[Action]:
        if self.initialisation:
            self.init(game_message)
            self.initialisation = False

        my_crew: Crew = game_message.get_crews_by_id()[game_message.crewId]

        actions: List[UnitAction] = []

        unit = my_crew.units[0]

        for unit in my_crew.units:
            if unit.type == UnitType.MINER:
                print(unit.id, unit.position, unit.blitzium)
                if not unit.position == self.miner_target:
                    actions.append(UnitAction(UnitActionType.MOVE, unit.id, self.miner_target))
                else:
                    actions.append(UnitAction(UnitActionType.MINE, unit.id, self.target_mine))

                #     if unit.blitzium < 5:
                #         mine = [i for i in mines if adj(i, unit.position)][0]
                #         actions.append(UnitAction(UnitActionType.MINE, unit.id, mine))
                #     else:
                #         if adj(unit.position, my_crew.homeBase):
                #             actions.append(UnitAction(UnitActionType.DROP, unit.id, my_crew.homeBase))
                #         else:
                #             adj_home = Position(*(get_adj(my_crew.homeBase)[0]))
                #             target = Position(adj_home.x, adj_home.y)
                #             actions.append(UnitAction(UnitActionType.MOVE, unit.id, target))
                # else:
                #     actions.append(UnitAction(UnitActionType.MOVE, unit.id, target))
            if unit.type == UnitType.CART:
                if unit.blitzium < 25:
                    if not unit.position == self.car_target:
                        actions.append(UnitAction(UnitActionType.MOVE, unit.id, self.car_target))
                    else:
                        actions.append(UnitAction(UnitActionType.PICKUP, unit.id, self.miner_target))
                else:
                    if not unit.position == self.car_base:
                        actions.append(UnitAction(UnitActionType.MOVE, unit.id, self.car_base))
                    else:
                        actions.append(UnitAction(UnitActionType.DROP, unit.id, my_crew.homeBase))

        print(my_crew.blitzium, len(my_crew.units))

        if my_crew.prices.CART <= my_crew.blitzium and len(my_crew.units) < 2:
            actions.append(BuyAction(UnitType.CART))

        return actions

    def get_closer_rock(self, map, position, mine_position):
        list_tiles = map.tiles
        start_x, start_y = position.x, position.y
        list_tiles[start_x][start_y] = 0

        initial = (start_x, start_y)
        visited = []
        queue = [initial]
        distance = 0

        while queue:
            pos = queue.pop(0)
            if pos not in visited:
                start_x, start_y = pos
                distance = list_tiles[start_x][start_y]
                visited.append(pos)
                neighbours = [(start_x + 1, start_y), (start_x - 1, start_y), (start_x, start_y + 1),
                              (start_x, start_y - 1)]
                for neighbour in neighbours:
                    start_x, start_y = neighbour
                    if list_tiles[start_x][start_y] == 'EMPTY':
                        queue.append(neighbour)
                        list_tiles[start_x][start_y] = distance + 1

        print(list_tiles)

        x, y = mine_position.x, mine_position.y
        path = []
        while x != position.x and y != position.y:
            neighbours = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            min = 1000
            next = ()
            for neighbour in neighbours:
                val = list_tiles[neighbour[0]][neighbour[1]]
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


def distance(pos1, pos2):
    return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y)
