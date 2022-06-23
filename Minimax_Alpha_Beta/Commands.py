import copy


class CMD:
    def __init__(self, b, size, d, xx, yy, ch):
        self.Board = b
        self.Depth = d    # how much depth our tree is
        self.Size = size
        self.X = xx
        self.Y = yy
        self.Choice = ch
        self.minEvalBoard = -1  # min - 1
        self.maxEvalBoard = size * size + 4 * size + 4 + 1  # max + 1

    def make_move(self, board, x, y, player):  # assuming valid move
        disk_remove = 0  # total number of opponent pieces taken
        board[y][x] = player
        for d in range(8):  # 8 directions
            ctr = 0
            for i in range(self.Size):
                dx = x + self.X[d] * (i + 1)
                dy = y + self.Y[d] * (i + 1)
                if dx < 0 or dx > self.Size - 1 or dy < 0 or dy > self.Size - 1:
                    ctr = 0
                    break
                elif board[dy][dx] == player:
                    break
                elif board[dy][dx] == '0':
                    ctr = 0
                    break
                else:
                    ctr += 1
            for i in range(ctr):
                dx = x + self.X[d] * (i + 1)
                dy = y + self.Y[d] * (i + 1)
                board[dy][dx] = player
            disk_remove += ctr
        return (board, disk_remove)

    def valid_move(self, board, x, y, player):
        if x < 0 or x > self.Size - 1 or y < 0 or y > self.Size - 1:
            return False
        if board[y][x] != '0':
            return False
        (boardTemp, disk_remove) = self.make_move(copy.deepcopy(board), x, y, player)
        if disk_remove == 0:
            return False
        return True



    def ai_best_move(self, board, player):
        max_points = 0
        mx = -1
        my = -1
        points = 0
        for y in range(self.Size):
            for x in range(self.Size):
                if self.valid_move(board, x, y, player):
                    (boardTemp, disk_remove) = self.make_move(copy.deepcopy(board), x, y, player)
                    if player == '1':
                        points = self.mini_max(boardTemp, player, self.Depth, True)
                    elif player == '2':
                        points = self.alpha_beta(board, player, self.Depth, self.minEvalBoard, self.maxEvalBoard, True)

                    if points > max_points:
                        max_points = points
                        mx = x
                        my = y
        return (mx, my)

# Evaluate all available moves using mini_max then return best move.

    def find_best_move(self, board, player):
        max_points = 0
        mx = -1
        my = -1
        points = 0
        for y in range(self.Size):
            for x in range(self.Size):
                if self.valid_move(board, x, y, player):
                    (boardTemp, disk_remove) = self.make_move(copy.deepcopy(board), x, y, player)
                    if self.Choice == 0:
                        points = self.eval_board(boardTemp, player)
                    elif self.Choice == 1:
                        points = self.mini_max(boardTemp, player, self.Depth, True)
                    elif self.Choice == 2:
                        points = self.alpha_beta(board, player, self.Depth, self.minEvalBoard, self.maxEvalBoard, True)

                    if points > max_points:
                        max_points = points
                        mx = x
                        my = y
        return (mx, my)

    def eval_board(self, board, player):
        tot = 0
        for y in range(self.Size):
            for x in range(self.Size):
                if board[y][x] == player:
                    if (x == 0 or x == self.Size - 1) and (y == 0 or y == self.Size - 1):
                        tot += 4  # corner
                    elif (x == 0 or x == self.Size - 1) or (y == 0 or y == self.Size - 1):
                        tot += 2  # side
                    else:
                        tot += 1

        return tot

    # if no valid move(s) possible then True
    def is_terminal_node(self, board, player):
        for y in range(self.Size):
            for x in range(self.Size):
                if self.valid_move(board, x, y, player):
                    return False
        return True

    def mini_max(self, board, player, depth, maximizing_player):
        if depth == 0 or self.is_terminal_node(board, player):  # we see a node if it's reach on win or lose condition or depth
            return self.eval_board(board, player)  # return the best choice up to the parent node
        if maximizing_player:   # Maximizing Player
            best_value = self.minEvalBoard
            for y in range(self.Size):
                for x in range(self.Size):
                    if self.valid_move(board, x, y, player):
                        (boardTemp, disk_remove) = self.make_move(copy.deepcopy(board), x, y, player)
                        v = self.mini_max(boardTemp, player, depth - 1, False)
                        best_value = max(best_value, v)
        else:  # Minimizing Player
            best_value = self.maxEvalBoard
            for y in range(self.Size):
                for x in range(self.Size):
                    if self.valid_move(board, x, y, player):
                        (boardTemp, disk_remove) = self.make_move(copy.deepcopy(board), x, y, player)
                        v = self.mini_max(boardTemp, player, depth - 1, True)
                        best_value = min(best_value, v)
        return best_value

    def alpha_beta(self, board, player, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.is_terminal_node(board, player):
            return self.eval_board(board, player)
        if maximizing_player:  # Maximizing Player
            v = self.minEvalBoard
            for y in range(self.Size):
                for x in range(self.Size):
                    if self.valid_move(board, x, y, player):
                        (boardTemp, disk_remove) = self.make_move(copy.deepcopy(board), x, y, player)
                        v = max(v, self.alpha_beta(boardTemp, player, depth - 1, alpha, beta, False))
                        alpha = max(alpha, v)
                        if beta <= alpha:
                            break  # Alpha Stop
            return v
        else:  # Minimizing Player
            v = self.maxEvalBoard
            for y in range(self.Size):
                for x in range(self.Size):
                    if self.valid_move(board, x, y, player):
                        (boardTemp, disk_remove) = self.make_move(copy.deepcopy(board), x, y, player)
                        v = min(v, self.alpha_beta(boardTemp, player, depth - 1, alpha, beta, True))
                        beta = min(beta, v)
                        if beta <= alpha:
                            break  # Beta Stop
            return v