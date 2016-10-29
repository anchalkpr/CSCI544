class Board:
    def __init__(self, player, opponent, size):
        self.player = player
        self.opponent = opponent
        self.size = size
        self.empty = "."
        self.fields = [[[0, 0] for i in range(self.size)] for i in range(self.size)]
        
    def add_field(self, i, j, value):
        self.fields[i][j] = value
                    
    def make_move(self, player, opponent, move, move_type):
        moved_pieces = []
        self.fields[move[0]][move[1]][0] = player
        if move_type == 'Raid':
            neighbours = self.neighbours(move)
            for n in neighbours[opponent]:
                    self.fields[n[0]][n[1]][0] = player
                    moved_pieces.append(n)
        return moved_pieces
    
    def remove_move(self, move, moved_pieces, turn):
        self.fields[move[0]][move[1]][0] = self.empty
        for m in moved_pieces:
            self.fields[m[0]][m[1]][0] = turn
    
    def possible_moves_game_over(self):
        poss_moves = []
        for i in range(self.size):
            for j in range(self.size):
                if self.fields[i][j][0] == self.empty:
                    poss_moves.append((i,j))
        return poss_moves
    
    def possible_moves(self, player, opponent):
        poss_moves = []
        raids = []
        for i in range(self.size):
            for j in range(self.size):
                currentField = self.fields[i][j][0]
                if currentField == self.empty:
                    poss_moves.append(((i,j), 'Stake'))
                    if self.raidOrStake((i, j), player, opponent) =='Raid':
                        raids.append(((i,j), 'Raid'))
        poss_moves = poss_moves + raids
        return poss_moves
    
    def game_over(self):
        if len(self.possible_moves_game_over()) == 0:
            return True
        return False
    
    def score(self):
        playerScore = 0
        opponentScore = 0
        for i in range(self.size):
            for j in range(self.size):
                currentField = self.fields[i][j]
                if currentField[0] == self.player:
                    playerScore += currentField[1]
                elif currentField[0] == self.opponent:
                    opponentScore += currentField[1]
        return playerScore - opponentScore
    
    def neighbours(self, move):
        i = move[0]
        j = move[1]
        n = {'X':[], 'O':[], '.':[]}
        x = [0, 1, 0, -1]
        y = [1, 0, -1, 0]
        for k in range(4):
            xval = i + x[k]
            yval = j + y[k]
            if xval >= 0 and xval < self.size and yval >= 0 and yval < self.size:
                n[self.fields[xval][yval][0]].append((xval, yval))
        return n
    
    def raidOrStake(self, move, player, opponent):
        neighbours = self.neighbours(move)
        move_type = None
        if len(neighbours[opponent]) == 0 or (len(neighbours[opponent]) > 0 and len(neighbours[player]) == 0):
            move_type = 'Stake'
        elif len(neighbours[opponent]) > 0 and len(neighbours[player]) > 0:
            move_type = 'Raid'
        return move_type
    
    def returnBoardState(self):
        final_board = [[0 for i in range(self.size)] for i in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                final_board[i][j] = self.fields[i][j][0]
        return final_board