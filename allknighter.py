#Position goes like [0,1,2,3] [2,2 for [b,2], empty=0 pawn=1, knight=3 bishop=4 queen=9 rook=5 king=10, Black=-1 or white=1 or empty=0
#board[i,j] has color 1,-1 and empty 0
last_move=[]
PIECE_SYMBOLS = {
    1: {
        1: "P", 3: "N", 4: "B", 5: "R", 9: "Q", 10: "K"
    },
    -1: {
        1: "p", 3: "n", 4: "b", 5: "r", 9: "q", 10: "k"
    }
}

def print_board(board, pieces):

    display = [["." for _ in range(8)] for _ in range(8)]

    for x, y, p, c in pieces:
        display[y][x] = PIECE_SYMBOLS[c][p]

    for y in range(7, -1, -1):
        print(f"{y+1}  ", end="")
        print(" ".join(display[y]))

    print("\n   a b c d e f g h\n")

def promotion(board, position):
    x=int(input("PROMOTE"))
    position[2]=x

def make_board(pieces):
    board = [[0 for _ in range(8)] for _ in range(8)]
    for x, y, _, color in pieces:
        board[x][y] = color
    return board

def score(pieces):
    white_score = 0
    black_score = 0
    for i in pieces:
        if i[3]==1:
            if i[2]==4:
                white_score+=3
            elif i[2]==10:
                white_score+=1000
            else:
                white_score+=i[2]
        else:
            if i[2]==4:
                black_score+=3
            elif i[2]==10:
                black_score+=1000
            else:
                black_score+=i[2]
    return white_score-black_score


def pawn(board, position):
    possible_valid_pawn_moves = []
    if (position[1] == 1 and position[3] == 1) or (position[1] == 6 and position[3] == -1):
        if board[position[0]][position[1] + position[3]] == 0:
            possible_valid_pawn_moves.append([position[0], position[1] + position[3]])
            if board[position[0]][position[1] + position[3] * 2] == 0:
                possible_valid_pawn_moves.append([position[0], position[1] + position[3] * 2])

    if (position[1] < 7 and position[3] == 1) or (position[1] > 0 and position[3] == -1):  # Adjusted bound
        if board[position[0]][position[1] + position[3]] == 0:
            possible_valid_pawn_moves.append([position[0], position[1] + position[3]])

    if 0<=position[0] + 1 < 8 and 0<=position[1]+position[3] < 8:
        if board[position[0] + 1][position[1] + position[3]] == -1 * position[3]:
            possible_valid_pawn_moves.append([position[0] + 1, position[1] + position[3]])
    if 8>position[0] - 1 >= 0 and 0<=position[1]+position[3] < 8 :
        if board[position[0] - 1][position[1] + position[3]] == -1 * position[3]:
            possible_valid_pawn_moves.append([position[0] - 1, position[1] + position[3]])

    if (position[1] == 6 and position[3] == 1) or (position[1] == 1 and position[3] == -1):
        if board[position[0]][position[1] + position[3]] == 0:
            possible_valid_pawn_moves.append([position[0], position[1] + position[3]])
    #if moves_yet[-1][0]== "Pawn" and moves_yet[-1][1]==

    valid_moves = []
    for x, y in possible_valid_pawn_moves:
        if 0 <= x < 8 and 0 <= y < 8 and (board[x][y] == 0 or board[x][y] == -position[3]):
            valid_moves.append([x, y])
    return [list(move) for move in set(tuple(move) for move in valid_moves)]

def knight(board, position):
    x, y, _, color = position

    moves = [
        [x+2, y+1], [x+1, y+2],
        [x-1, y+2], [x-2, y+1],
        [x-2, y-1], [x-1, y-2],
        [x+1, y-2], [x+2, y-1]
    ]

    valid_moves = []
    for nx, ny in moves:
        if 0 <= nx < 8 and 0 <= ny < 8:
            if board[nx][ny] == 0 or board[nx][ny] == -color:
                valid_moves.append([nx, ny])

    return [list(move) for move in set(tuple(move) for move in valid_moves)]


def rook(board, position):
    possible_valid_rook_moves = []
    a, b, c, d = 1, 1, 1, 1
    for y in range(1, 8):
        if 0 <= position[1] + y < 8 and a != 0:
            if board[position[0]][position[1] + y] == 0:
                possible_valid_rook_moves.append([position[0], position[1] + y])
            elif board[position[0]][position[1] + y] == position[3]:
                a = 0
            else:
                possible_valid_rook_moves.append([position[0], position[1] + y])
                a = 0
        if 0 <= position[1] - y < 8 and b != 0:
            if board[position[0]][position[1] - y] == 0:
                possible_valid_rook_moves.append([position[0], position[1] - y])
            elif board[position[0]][position[1] - y] == position[3]:
                b = 0
            else:
                possible_valid_rook_moves.append([position[0], position[1] - y])
                b = 0
        if 0 <= position[0] + y < 8 and c != 0:
            if board[position[0] + y][position[1]] == 0:
                possible_valid_rook_moves.append([position[0] + y, position[1]])
            elif board[position[0] + y][position[1]] == position[3]:
                c = 0
            else:
                possible_valid_rook_moves.append([position[0] + y, position[1]])
                c = 0
        if 0 <= position[0] - y < 8 and d != 0:
            if board[position[0] - y][position[1]] == 0:
                possible_valid_rook_moves.append([position[0] - y, position[1]])
            elif board[position[0] - y][position[1]] == position[3]:
                d = 0
            else:
                possible_valid_rook_moves.append([position[0] - y, position[1]])
                d = 0
    return [list(move) for move in set(tuple(move) for move in possible_valid_rook_moves)]


def bishop(board, position):
    possible_valid_bishop_moves = []
    a, b, c, d = 1, 1, 1, 1
    for y in range(1, 8):
        if 0 <= position[1] + y < 8 and 0 <= position[0] + y < 8 and a != 0:
            if board[position[0] + y][position[1] + y] == 0:
                possible_valid_bishop_moves.append([position[0] + y, position[1] + y])
            elif board[position[0] + y][position[1] + y] == position[3]:
                a = 0
            else:
                possible_valid_bishop_moves.append([position[0] + y, position[1] + y])
                a = 0
        if 0 <= position[1] - y < 8 and 0 <= position[0] + y < 8 and b != 0:
            if board[position[0] + y][position[1] - y] == 0:
                possible_valid_bishop_moves.append([position[0] + y, position[1] - y])
            elif board[position[0] + y][position[1] - y] == position[3]:
                b = 0
            else:
                possible_valid_bishop_moves.append([position[0] + y, position[1] - y])
                b = 0
        if 0 <= position[0] - y < 8 and 0 <= position[1] + y < 8 and d != 0:
            if board[position[0] - y][position[1] + y] == 0:
                possible_valid_bishop_moves.append([position[0] - y, position[1] + y])
            elif board[position[0] - y][position[1] + y] == position[3]:
                d = 0
            else:
                possible_valid_bishop_moves.append([position[0] - y, position[1] + y])
                d = 0
        if 0 <= position[0] - y < 8 and 0 <= position[1] - y < 8 and c != 0:
            if board[position[0] - y][position[1] - y] == 0:
                possible_valid_bishop_moves.append([position[0] - y, position[1] - y])
            elif board[position[0] - y][position[1] - y] == position[3]:
                c = 0
            else:
                possible_valid_bishop_moves.append([position[0] - y, position[1] - y])
                c = 0
    return [list(move) for move in set(tuple(move) for move in possible_valid_bishop_moves)]

def queen(board, position):
    possible_valid_queen_moves = rook(board, position)+bishop(board, position)
    return [list(move) for move in set(tuple(move) for move in possible_valid_queen_moves)]

def king(board, position):
    possible_valid_king_moves = [[position[0] + 1, position[1]], [position[0] - 1, position[1]],
                                 [position[0], position[1] + 1], [position[0], position[1] - 1],
                                 [position[0] + 1, position[1] + 1], [position[0] + 1, position[1] - 1],
                                 [position[0] - 1, position[1] + 1], [position[0] - 1, position[1] - 1]]
    valid_moves = []
    for x, y in possible_valid_king_moves:
        if 0 <= x < 8 and 0 <= y < 8 and (board[x][y] == 0 or board[x][y] == -position[3]):
            valid_moves.append([x, y])
    possible_valid_king_moves = valid_moves
    return [list(move) for move in set(tuple(move) for move in valid_moves)]

def compile(board, pieces, piece, colour):
    l=[]
    for i in pieces:
        if i[2]==piece:
            if piece==1 and board[i[0]][i[1]]==colour:
                l.append(pawn(board, i))
            elif piece==3 and board[i[0]][i[1]]==colour:
                l.append(knight(board, i))
            elif piece==4 and board[i[0]][i[1]]==colour:
                l.append(bishop(board, i))
            elif piece==5 and board[i[0]][i[1]]==colour:
                l.append(rook(board, i))
            elif piece and board[i[0]][i[1]]==colour:
                l.append(queen(board, i))
            else:
                l.append(king(board, i))
    return [move for pair in l for move in pair]


pieces = [
    [0,0,5,1], [1,0,3,1], [2,0,4,1], [3,0,9,1],
    [4,0,10,1],[5,0,4,1], [6,0,3,1], [7,0,5,1],
    *[[x,1,1,1] for x in range(8)],

    [0,7,5,-1], [1,7,3,-1], [2,7,4,-1], [3,7,9,-1],
    [4,7,10,-1],[5,7,4,-1], [6,7,3,-1], [7,7,5,-1],
    *[[x,6,1,-1] for x in range(8)]
]
if __name__=="__main__":
    color=1
    moves_yet=[]
    while True:
        x=make_board(pieces)
        print_board(x,pieces)
        move=list(input("PIECE_NAME INITIAL FINAL").split(" "))
        a=int(move[1][1])
        b=int(move[1][3])
        c=int(move[2][1])
        d=int(move[2][3])
        pieces[:] = [
            p for p in pieces
            if not (p[0] == c and p[1] == d and p[3] == -color)
        ]

        if move[0]=='Pawn':
            if [c,d] in pawn(x,[a,b,1,color]):
                for j in pieces:
                    if j[0] == a and j[1] == b and j[2] == 1 and j[3] == color:
                        j[0] = c
                        j[1] = d
                        if (d==7 and color==1) or (d==0 and color==-1):
                            promotion(x,j)
                color*=-1
                moves_yet.append(move)
            else:
                print("INVALID MOVE")
        elif move[0]=='Rook':
            if [c,d] in rook(x,[a,b,5,color]):
                for j in pieces:
                    if j[0] == a and j[1] == b and j[2] == 5 and j[3] == color:
                        j[0] = c
                        j[1] = d
                color*=-1
                moves_yet.append(move)
            else:
                print("INVALID MOVE")
        elif move[0]=='Bishop':
            if [c,d] in bishop(x,[a,b,4,color]):
                for j in pieces:
                    if j[0] == a and j[1] == b and j[2] == 4 and j[3] == color:
                        j[0] = c
                        j[1] = d
                color*=-1
                moves_yet.append(move)
            else:
                print("INVALID MOVE")
        elif move[0]=='Knight':
            if [c,d] in knight(x,[a,b,3,color]):
                for j in pieces:
                    if j[0] == a and j[1] == b and j[2] == 3 and j[3] == color:

                        j[0] = c
                        j[1] = d
                color*=-1
            else:
                print("INVALID MOVE")
        elif move[0]=='Queen':
            if [c,d] in queen(x,[a,b,9,color]):
                for j in pieces:
                    if j[0] == a and j[1] == b and j[2] == 9 and j[3] == color:
                        j[0] = c
                        j[1] = d
                color*=-1
                moves_yet.append(move)
            else:
                print("INVALID MOVE")
        elif move[0]=='King':
            if [c,d] in king(x,[a,b,10,color]):
                for j in pieces:
                    if j[0] == a and j[1] == b and j[2] == 10 and j[3] == color:
                        j[0] = c
                        j[1] = d
                color*=-1
                moves_yet.append(move)
            else:
                print("INVALID MOVE")
        else:
            print("INVALID PIECE")

        if color==-1:
            print(moves_yet)
        print(f"EVAL BAR:{score(pieces)}" '\n')

