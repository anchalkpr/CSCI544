from Board import Board
from AlphaBeta import alpha_beta_search
from Minimax import minimax_decision
import time

alphabet = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H', 8:'I', 9:'J', 10:'K', 11:'L', 12:'M', 13:'N', 14:'O', 15:'P',
            16:'Q', 17:'R', 18:'S', 19:'T', 20:'U', 21:'V', 22:'W', 23:'X', 24:'Y', 25:'Z'}

def play_game():
    inputFile = open("input.txt", 'r')
    lines = inputFile.readlines()
    inputFile.close()
    size = int(lines[0].strip())
    algorithm = lines[1].strip()
    player = lines[2].strip()
    if player == 'X':
        opponent = 'O'
    else:
        opponent = 'X'
    depth = int(lines[3].strip())
    boardValues = []
    for line in lines[4:4+size]:
        line = line.strip().split(" ")
        line = map(int, line)
        boardValues.append(line) 
    
    boardState = []
    for line in lines[4+size:4+size+size]:
        line = line.strip()
        boardState.append(list(line))
    
    board = Board(player, opponent, size)
    for i in range(size):
        for j in range(size):
            value = [boardState[i][j], boardValues[i][j]]
            board.add_field(i, j, value)
    if algorithm == 'MINIMAX':
        output, finalBoard = minimax_decision(board, depth)
    elif algorithm == 'ALPHABETA':
        output, finalBoard = alpha_beta_search(board, depth)
        
    outputFile = open("output.txt", 'w')
    index = output[0]
    move_type = output[1]
    move = '%s%s %s' %(alphabet[index[1]], index[0] + 1, move_type)
    print move
    render_output = [move] + map(''.join, finalBoard)
    outputFile.write("\n".join(render_output))
    outputFile.close() 
        
start_time = time.time()
play_game()
print("--- %s seconds ---" % (time.time() - start_time))