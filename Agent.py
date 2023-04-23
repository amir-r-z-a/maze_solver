import math
import colors
from Environment import Board


def check_block(tile):
    if not tile.isBlocked:
        return True
    return False
    pass


def check_visited(tile):
    if tile.get_color() != colors.red:
        return True
    return False


def check_validation(tile):
    if check_block(tile) and check_visited(tile):
        return True
    return False


def distance_calculator(x1, x2, y1, y2):
    return int(math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2)))


def tile_actions(tile, father, x1, y1):
    tile.set_parent(father)
    x2 = tile.x
    y2 = tile.y
    distance = distance_calculator(x1, x2, y1, y2)
    tile.set_distance(distance)


class Agent:
    def __init__(self, board, start, end):
        self.complexity = 0
        self.end_point = end
        self.bb = board
        self.position = board.get_agent_pos()
        self.current_state = board.get_current_state()
        self.open_list = []
        self.close_list = []
        starting_tile = board.boardArray[start["x"]][start["y"]]
        self.close_list.append(starting_tile)
        self.reach_goal = False
        self.last_tile = None
        self.finish = False
        distance = int(math.sqrt(((end["x"] - starting_tile.x) ** 2) + ((end["y"] - starting_tile.y) ** 2)))
        starting_tile.set_distance(distance)

    def get_position(self):
        return self.position

    def set_position(self, position, board):
        self.position = position
        board.set_agent_pos(position)
        board.update_board(self.current_state)

    def get_actions(self, board):
        end = self.end_point
        actions = []
        self.position = board.get_agent_pos()
        father = board.boardArray[self.position[0]][self.position[1]]
        x1 = end["x"]
        y1 = end["y"]

        if self.position[1] + 1 < 13:
            bot_tile = self.current_state[self.position[0]][self.position[1] + 1]
            if check_validation(bot_tile):
                actions.append(bot_tile)
                tile_actions(bot_tile, father, x1, y1)

        if self.position[1] - 1 >= 0:
            top_tile = self.current_state[self.position[0]][self.position[1] - 1]
            if check_validation(top_tile):
                actions.append(top_tile)
                tile_actions(top_tile, father, x1, y1)

        if self.position[0] + 1 < 13:
            right_tile = self.current_state[self.position[0] + 1][self.position[1]]
            if check_validation(right_tile):
                actions.append(right_tile)
                tile_actions(right_tile, father, x1, y1)

        if self.position[0] - 1 >= 0:
            left_tile = self.current_state[self.position[0] - 1][self.position[1]]
            if check_validation(left_tile):
                actions.append(left_tile)
                tile_actions(left_tile, father, x1, y1)
        return actions

    def greener(self):
        self.last_tile.set_color(colors.green)
        self.last_tile = self.last_tile.parent
        if self.last_tile.isStart:
            self.last_tile.set_color(colors.green)
            self.finish = True
            print(f'time complexity for this algorithm :  {self.complexity}')
        return

    # BFS ...................................................................
    def bfs(self, bb: Board):
        self.complexity += 1
        if self.finish:
            return
        if self.reach_goal:
            self.greener()
            return
        self.open_list.extend(self.get_actions(bb))
        selected_tile = self.open_list[0]
        if selected_tile not in self.close_list:
            if selected_tile.isGoal:
                self.reach_goal = True
                self.last_tile = selected_tile
            else:
                self.close_list.append(selected_tile)
                bb.set_agent_pos({'x': selected_tile.x, 'y': selected_tile.y})
                self.open_list.remove(selected_tile)
                self.open_list.extend(self.get_actions(bb))
        else:
            self.open_list.remove(selected_tile)
        pass

    # DFS .........................................................

    def dfs(self, bb):
        self.complexity += 1
        if self.finish:
            return
        if self.reach_goal:
            self.greener()
            return
        self.open_list.extend(self.get_actions(bb))
        selected_tile = self.open_list.pop()
        if selected_tile not in self.close_list:
            if selected_tile.isGoal:
                self.reach_goal = True
                self.last_tile = selected_tile
            else:
                self.close_list.append(selected_tile)
                bb.set_agent_pos({'x': selected_tile.x, 'y': selected_tile.y})
                self.open_list.extend(self.get_actions(bb))
        pass

    # A_STAR..........................................................................

    def a_star(self, bb):
        self.complexity += 1
        if self.finish:
            return
        if self.reach_goal:
            self.greener()
            return
        self.open_list.extend(self.get_actions(bb))
        self.open_list = sorted(self.open_list, key=lambda x: x.distance)
        selected_tile = self.open_list[0]
        if selected_tile not in self.close_list:
            if selected_tile.isGoal:
                self.reach_goal = True
                self.last_tile = selected_tile
            else:
                self.close_list.append(selected_tile)
                bb.set_agent_pos({'x': selected_tile.x, 'y': selected_tile.y})
                self.open_list.remove(selected_tile)
                self.open_list.extend(self.get_actions(bb))
                self.open_list = sorted(self.open_list, key=lambda x: x.distance)
        else:
            self.open_list.remove(selected_tile)
        pass
