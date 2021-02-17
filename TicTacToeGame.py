import random


class Game:
    def __init__(self, p1, p2, role):
        self.gameOver = False
        self.player1 = p1
        self.player2 = p2
        self.board = [[":white_large_square:", ":white_large_square:", ":white_large_square:"],
                      [":white_large_square:", ":white_large_square:", ":white_large_square:"],
                      [":white_large_square:", ":white_large_square:", ":white_large_square:"]]
        self.win_sequences = [[(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)],
                              [(2, 0), (2, 1), (2, 2)], [(0, 0), (1, 0), (2, 0)],
                              [(1, 0), (1, 1), (1, 2)], [(0, 0), (1, 1), (2, 2)],
                              [(0, 2), (1, 1), (2, 0)]]
        self.mark = random.randint(1, 2)
        if self.mark == 1:
            self.turn = p1
        else:
            self.turn = p2
        self.role = role

    def place(self, value1: int, value2: int):
        if self.board[value1 - 1][value2 - 1] != ":white_large_square:":
            return 0
        else:
            if self.mark == 1:
                self.board[value1 - 1][value2 - 1] = ":regional_indicator_x:"
                self.mark = 2
                self.turn = self.player2
            else:
                self.board[value1 - 1][value2 - 1] = ":zero:"
                self.mark = 1
                self.turn = self.player1

    def check_win(self):
        ok = False
        for row in self.win_sequences:
            win = 0
            for element in row:
                if self.board[element[0]][element[1]] != ":white_large_square:":
                    win += 1
            if self.board[row[0][0]][row[0][1]] == self.board[row[1][0]][row[1][1]] and self.board[row[1][0]][
                row[1][1]] == self.board[row[2][0]][row[2][1]]:
                if win == 3:
                    if self.mark == 1:
                        self.winner = self.player2
                    else:
                        self.winner = self.player1
                    self.gameOver = True
                    ok = True
                    break
        return ok

    def check_stalemate(self):
        nr = 0
        for row in self.board:
            for item in row:
                if item != ":white_large_square:":
                    nr += 1
        if nr == 9:
            self.gameOver = True
            return True
        else:
            return False

