from board.move import move
from pieces.nullpiece import nullpiece
from pieces.queen import queen
import random

class AI:

    global tp
    tp=[]


    def __init__(self):
        pass


    def evaluate(self,gametiles):
        min=100000
        count=0
        count2=0
        chuk=[]
        movex=move()
        tp.clear()
        xp=self.minimax(gametiles,3,-1000000000,1000000000,False)

        for zoom in tp:
            if zoom[4]<min:
                chuk.clear()
                chuk.append(zoom)
                min=zoom[4]
            if zoom[4]==min:
                chuk.append(zoom)
        fx=random.randrange(len(chuk))
        print(tp)
        return chuk[fx][0],chuk[fx][1],chuk[fx][2],chuk[fx][3]


    def reset(self,gametiles):
        for x in range(8):
            for y in range(8):
                if gametiles[x][y].pieceonTile.tostring()=='k' or gametiles[x][y].pieceonTile.tostring()=='r':
                    gametiles[x][y].pieceonTile.moved=False


    def updateposition(self,x,y):
        a=x*8
        b=a+y
        return b

    def checkmate(self,gametiles):
        movex=move()
        if movex.checkw(gametiles)[0]=='checked':
            array=movex.movesifcheckedw(gametiles)
            if len(array)==0:
                return True

        if movex.checkb(gametiles)[0]=='checked' :
            array=movex.movesifcheckedb(gametiles)
            if len(array)==0:
                return True

    def stalemate(self,gametiles,player):
        movex=move()
        if player==False:
            if movex.checkb(gametiles)[0]=='notchecked':
                check=False
                for x in range(8):
                    for y in range(8):
                        if gametiles[y][x].pieceonTile.alliance=='Black':
                            moves1=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                            lx1=movex.pinnedb(gametiles,moves1,y,x)
                            if len(lx1)==0:
                                continue
                            else:
                                check=True
                            if check==True:
                                break
                    if check==True:
                        break

                if check==False:
                    return True

        if player==True:
                if movex.checkw(gametiles)[0]=='notchecked':
                    check=False
                    for x in range(8):
                        for y in range(8):
                            if gametiles[y][x].pieceonTile.alliance=='White':
                                moves1=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                                lx1=movex.pinnedw(gametiles,moves1,y,x)
                                if len(lx1)==0:
                                    continue
                                else:
                                    check=True
                                if check==True:
                                    break
                        if check==True:
                            break

                    if check==False:
                        return True






    def minimax(self,gametiles, depth,alpha , beta ,player):
        if depth==0 or self.checkmate(gametiles)==True or self.stalemate(gametiles,player)==True:
            return self.calculateb(gametiles)
        if not player:
            minEval=100000000
            kp,ks=self.eva(gametiles,player)
            for lk in kp:
                for move in lk:
                    mts=gametiles[move[2]][move[3]].pieceonTile
                    gametiles=self.move(gametiles,move[0],move[1],move[2],move[3])
                    evalk=self.minimax(gametiles,depth-1,alpha,beta,True)
                    if evalk<minEval and depth==3:
                        tp.clear()
                        tp.append(move)
                    if evalk==minEval and depth==3:
                        tp.append(move)
                    minEval=min(minEval,evalk)
                    beta=min(beta,evalk)
                    gametiles=self.revmove(gametiles,move[2],move[3],move[0],move[1],mts)
                    if beta<=alpha:
                        break

                if beta<=alpha:
                    break
            return minEval

        else:
            maxEval=-100000000
            kp,ks=self.eva(gametiles,player)
            for lk in ks:
                for move in lk:
                    mts=gametiles[move[2]][move[3]].pieceonTile
                    gametiles=self.movew(gametiles,move[0],move[1],move[2],move[3])
                    evalk=self.minimax(gametiles,depth-1,alpha,beta,False)
                    maxEval=max(maxEval,evalk)
                    alpha=max(alpha,evalk)
                    gametiles=self.revmove(gametiles,move[2],move[3],move[0],move[1],mts)
                    if beta<=alpha:
                        break
                if beta<=alpha:
                    break

            return maxEval



    def printboard(self,gametilles):
        count = 0
        for rows in range(8):
            for column in range(8):
                print('|', end=gametilles[rows][column].pieceonTile.tostring())
            print("|",end='\n')


    def checkeva(self,gametiles,moves):
        arr=[]
        for move in moves:
            lk=[[move[2],move[3]]]
            arr.append(self.calci(gametiles,move[0],move[1],lk))

        return arr



    def eva(self,gametiles,player):
        lx=[]
        moves=[]
        kp=[]
        ks=[]
        movex=move()
        for x in range(8):
            for y in range(8):
                    if gametiles[y][x].pieceonTile.alliance=='Black' and player==False:
                        if movex.checkb(gametiles)[0]=='checked':
                            moves=movex.movesifcheckedb(gametiles)
                            arr=self.checkeva(gametiles,moves)
                            kp=arr
                            return kp,ks
                        moves=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                        if len(moves)==0:
                            continue
                        else:
                            if(gametiles[y][x].pieceonTile.tostring()=='K'):
                                ax=movex.castlingb(gametiles)
                                if not len(ax)==0:
                                    for l in ax:
                                        if l=='ks':
                                            moves.append([0,6])
                                        if l=='qs':
                                            moves.append([0,2])
                        if gametiles[y][x].pieceonTile.alliance=='Black':
                            lx=movex.pinnedb(gametiles,moves,y,x)
                        moves=lx
                        if len(moves)==0:
                            continue
                        kp.append(self.calci(gametiles,y,x,moves))


                    if gametiles[y][x].pieceonTile.alliance=='White' and player==True:
                        if movex.checkw(gametiles)[0]=='checked':
                            moves=movex.movesifcheckedw(gametiles)
                            arr=self.checkeva(gametiles,moves)
                            ks=arr
                            return kp,ks
                        moves=gametiles[y][x].pieceonTile.legalmoveb(gametiles)
                        if moves==None:
                            print(y)
                            print(x)
                            print(gametiles[y][x].pieceonTile.position)
                        if len(moves)==0:
                            continue
                        else:
                            if(gametiles[y][x].pieceonTile.tostring()=='k'):
                                ax=movex.castlingw(gametiles)
                                if not len(ax)==0:
                                    for l in ax:
                                        if l=='ks':
                                            moves.append([7,6])
                                        if l=='qs':
                                            moves.append([7,2])
                        if gametiles[y][x].pieceonTile.alliance=='White':
                            lx=movex.pinnedw(gametiles,moves,y,x)
                        moves=lx
                        if len(moves)==0:
                            continue
                        ks.append(self.calci(gametiles,y,x,moves))

        return kp,ks



    def calci(self,gametiles,y,x,moves):
        arr=[]
        jk=object
        for move in moves:
            jk=gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            mk=self.calculateb(gametiles)
            gametiles[y][x].pieceonTile=gametiles[move[0]][move[1]].pieceonTile
            gametiles[move[0]][move[1]].pieceonTile=jk
            arr.append([y,x,move[0],move[1],mk])
        return arr


    def calculateb(self,gametiles):
        # Sets the values of each piece type dduring the "early game" stage
        early_game_piece_values = {
            'p': 82,
            'n': 337,
            'b': 365,
            'r': 477,
            'q': 1025,
            'k': 20000
        }

        # Sets the values of each piece type dduring the "end game" stage
        end_game_piece_values = {
            'p': 94,
            'n': 281,
            'b': 297,
            'r': 512,
            'q': 936,
            'k': 20000
        }

        # A piece square table to weight certain positions higher than others for each piece type. This one targets the "early game" stage
        early_game_piece_square_table = {
            'p': [
                [      20000,   20000,   20000,   20000,   20000,   20000,  20000,   20000,],
                [     98, 134,  61,  95,  68, 126, 34, -11,],
                [     -6,   7,  26,  31,  65,  56, 25, -20,],
                [    -14,  13,   6,  21,  23,  12, 17, -23,],
                [    -27,  -2,  -5,  12,  17,   6, 10, -25,],
                [    -26,  -4,  -4, -10,   3,   3, 33, -12,],
                [    -35,  -1, -20, -23, -15,  24, 38, -22,],
                [      0,   0,   0,   0,   0,   0,  0,   0,],
            ],
            'n': [
                [    -167, -89, -34, -49,  61, -97, -15, -107,],
                [     -73, -41,  72,  36,  23,  62,   7,  -17,],
                [     -47,  60,  37,  65,  84, 129,  73,   44,],
                [      -9,  17,  19,  53,  37,  69,  18,   22,],
                [     -13,   4,  16,  13,  28,  19,  21,   -8,],
                [     -23,  -9,  12,  10,  19,  16,  25,  -16,],
                [     -29, -53, -12,  -3,  -1,  18, -14,  -19,],
                [    -105, -21, -58, -33, -17, -28, -19,  -23,],
            ],
            'b': [
                [    -29,   4, -82, -37, -25, -42,   7,  -8,],
                [    -26,  16, -18, -13,  30,  59,  18, -47,],
                [    -16,  37,  43,  40,  35,  50,  37,  -2,],
                [     -4,   5,  19,  50,  37,  37,   7,  -2,],
                [     -6,  13,  13,  26,  34,  12,  10,   4,],
                [      0,  15,  15,  15,  14,  27,  18,  10,],
                [      4,  15,  16,   0,   7,  21,  33,   1,],
                [    -33,  -3, -14, -21, -13, -12, -39, -21,],
            ],
            'r': [
                [     32,  42,  32,  51, 63,  9,  31,  43,],
                [     27,  32,  58,  62, 80, 67,  26,  44,],
                [     -5,  19,  26,  36, 17, 45,  61,  16,],
                [    -24, -11,   7,  26, 24, 35,  -8, -20,],
                [    -36, -26, -12,  -1,  9, -7,   6, -23,],
                [    -45, -25, -16, -17,  3,  0,  -5, -33,],
                [    -44, -16, -20,  -9, -1, 11,  -6, -71,],
                [    -19, -13,   1,  17, 16,  7, -37, -26,],
            ],
            'q': [
                [    -28,   0,  29,  12,  59,  44,  43,  45,],
                [    -24, -39,  -5,   1, -16,  57,  28,  54,],
                [    -13, -17,   7,   8,  29,  56,  47,  57,],
                [    -27, -27, -16, -16,  -1,  17,  -2,   1,],
                [     -9, -26,  -9, -10,  -2,  -4,   3,  -3,],
                [    -14,   2, -11,  -2,  -5,   2,  14,   5,],
                [    -35,  -8,  11,   2,   8,  15,  -3,   1,],
                [     -1, -18,  -9,  10, -15, -25, -31, -50,],
            ],
            'k': [
                [    -65,  23,  16, -15, -56, -34,   2,  13,],
                [     29,  -1, -20,  -7,  -8,  -4, -38, -29,],
                [     -9,  24,   2, -16, -20,   6,  22, -22,],
                [    -17, -20, -12, -27, -30, -25, -14, -36,],
                [    -49,  -1, -27, -39, -46, -44, -33, -51,],
                [    -14, -14, -22, -46, -44, -30, -15, -27,],
                [      1,   7,  -8, -64, -43, -16,   9,   8,],
                [    -15,  36,  12, -54,   8, -28,  24,  14,],
            ]
        }

        # A piece square table to weight certain positions higher than others for each piece type. This one targets the "end game" stage
        end_game_piece_square_table = {
            'p': [
                [      20000,   20000,   20000,   20000,   20000,   20000,   20000,   20000,],
                [    178, 173, 158, 134, 147, 132, 165, 187,],
                [     94, 100,  85,  67,  56,  53,  82,  84,],
                [     32,  24,  13,   5,  -2,   4,  17,  17,],
                [     13,   9,  -3,  -7,  -7,  -8,   3,  -1,],
                [      4,   7,  -6,   1,   0,  -5,  -1,  -8,],
                [     13,   8,   8,  10,  13,   0,   2,  -7,],
                [      0,   0,   0,   0,   0,   0,   0,   0,],
            ],
            'n': [
                [    -58, -38, -13, -28, -31, -27, -63, -99,],
                [    -25,  -8, -25,  -2,  -9, -25, -24, -52,],
                [    -24, -20,  10,   9,  -1,  -9, -19, -41,],
                [    -17,   3,  22,  22,  22,  11,   8, -18,],
                [    -18,  -6,  16,  25,  16,  17,   4, -18,],
                [    -23,  -3,  -1,  15,  10,  -3, -20, -22,],
                [    -42, -20, -10,  -5,  -2, -20, -23, -44,],
                [    -29, -51, -23, -15, -22, -18, -50, -64,],
            ],
            'b': [
                [    -14, -21, -11,  -8, -7,  -9, -17, -24,],
                [     -8,  -4,   7, -12, -3, -13,  -4, -14,],
                [      2,  -8,   0,  -1, -2,   6,   0,   4,],
                [     -3,   9,  12,   9, 14,  10,   3,   2,],
                [     -6,   3,  13,  19,  7,  10,  -3,  -9,],
                [    -12,  -3,   8,  10, 13,   3,  -7, -15,],
                [    -14, -18,  -7,  -1,  4,  -9, -15, -27,],
                [    -23,  -9, -23,  -5, -9, -16,  -5, -17,],
            ],
            'r': [
                [    13, 10, 18, 15, 12,  12,   8,   5,],
                [    11, 13, 13, 11, -3,   3,   8,   3,],
                [     7,  7,  7,  5,  4,  -3,  -5,  -3,],
                [     4,  3, 13,  1,  2,   1,  -1,   2,],
                [     3,  5,  8,  4, -5,  -6,  -8, -11,],
                [    -4,  0, -5, -1, -7, -12,  -8, -16,],
                [    -6, -6,  0,  2, -9,  -9, -11,  -3,],
                [    -9,  2,  3, -1, -5, -13,   4, -20,],
            ],
            'q': [
                [     -9,  22,  22,  27,  27,  19,  10,  20,],
                [    -17,  20,  32,  41,  58,  25,  30,   0,],
                [    -20,   6,   9,  49,  47,  35,  19,   9,],
                [      3,  22,  24,  45,  57,  40,  57,  36,],
                [    -18,  28,  19,  47,  31,  34,  39,  23,],
                [    -16, -27,  15,   6,   9,  17,  10,   5,],
                [    -22, -23, -30, -16, -16, -23, -36, -32,],
                [    -33, -28, -22, -43,  -5, -32, -20, -41,],
            ],
            'k': [
                [    -74, -35, -18, -18, -11,  15,   4, -17,],
                [    -12,  17,  14,  17,  17,  38,  23,  11,],
                [     10,  17,  23,  15,  20,  45,  44,  13,],
                [     -8,  22,  24,  27,  26,  33,  26,   3,],
                [    -18,  -4,  21,  24,  27,  23,   9, -11,],
                [    -19,  -3,  11,  21,  23,  16,   7,  -9,],
                [    -27, -11,   4,  13,  14,   4,  -5, -17,],
                [    -53, -34, -21, -11, -28, -14, -24, -43],
            ]
        }

        # How much to incremenet the game "phase" if a certain piece type is removed
        piece_gamephase_inc = {
            'p': 0,
            'n': 1,
            'b': 1,
            'r': 2,
            'q': 4,
            'k': 0
        }

        # We calculate the values for both the early game piece square table as well as the late game piece square table
        early_game_value = 0
        end_game_value = 0
        gamephase = 0
        for y in range(8):
            for x in range(8):
                piece = gametiles[y][x].pieceonTile.tostring() # Get piece
                if piece == '-': # Skip blanks
                    continue
                if piece.islower(): # If it's our piece, increment both early and end game values by their respective piece_value and square table values
                    early_game_value = early_game_value + early_game_piece_values[piece] + early_game_piece_square_table[piece][y][x]
                    end_game_value   = end_game_value   + end_game_piece_values[piece]   + end_game_piece_square_table[piece][y][x]
                else: # If it's the opponent's piece, decrement the values instead
                    early_game_value = early_game_value - early_game_piece_values[piece.lower()] - early_game_piece_square_table[piece.lower()][7-y][7-x]
                    end_game_value   = end_game_value   - end_game_piece_values[piece.lower()]   - end_game_piece_square_table[piece.lower()][7-y][7-x]
                gamephase = gamephase + piece_gamephase_inc[piece.lower()]

        # We interpolate between the early_game_value and end_game_value based on the game phase, with higher values prioritizing the former.
        early_game_phase = gamephase
        if early_game_phase > 24:
            early_game_phase = 24
        end_game_phase = 24 - early_game_phase
        return (early_game_value * early_game_phase + end_game_value * end_game_phase) / 24.0


    def move(self,gametiles,y,x,n,m):
        promotion=False
        if gametiles[y][x].pieceonTile.tostring()=='K' or gametiles[y][x].pieceonTile.tostring()=='R':
            gametiles[y][x].pieceonTile.moved=True

        if gametiles[y][x].pieceonTile.tostring()=='K' and m==x+2:
            gametiles[y][x+1].pieceonTile=gametiles[y][x+3].pieceonTile
            s=self.updateposition(y,x+1)
            gametiles[y][x+1].pieceonTile.position=s
            gametiles[y][x+3].pieceonTile=nullpiece()
        if gametiles[y][x].pieceonTile.tostring()=='K' and m==x-2:
            gametiles[y][x-1].pieceonTile=gametiles[y][0].pieceonTile
            s=self.updateposition(y,x-1)
            gametiles[y][x-1].pieceonTile.position=s
            gametiles[y][0].pieceonTile=nullpiece()



        if gametiles[y][x].pieceonTile.tostring()=='P' and y+1==n and y==6:
            promotion=True


        if promotion==False:

            gametiles[n][m].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            s=self.updateposition(n,m)
            gametiles[n][m].pieceonTile.position=s

        if promotion==True:

            if gametiles[y][x].pieceonTile.tostring()=='P':
                gametiles[y][x].pieceonTile=nullpiece()
                gametiles[n][m].pieceonTile=queen('Black',self.updateposition(n,m))
                promotion=False

        return gametiles



    def revmove(self,gametiles,x,y,n,m,mts):
        if gametiles[x][y].pieceonTile.tostring()=='K':
            if m==y-2:
                gametiles[x][y].pieceonTile.moved=False
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][7].pieceonTile=gametiles[x][y-1].pieceonTile
                s=self.updateposition(n,7)
                gametiles[n][7].pieceonTile.position=s
                gametiles[n][7].pieceonTile.moved=False

                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()

            elif m==y+2:
                gametiles[x][y].pieceonTile.moved=False
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][0].pieceonTile=gametiles[x][y+1].pieceonTile
                s=self.updateposition(m,0)
                gametiles[n][0].pieceonTile.position=s
                gametiles[n][0].pieceonTile.moved=False
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()

            else:
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[x][y].pieceonTile=mts

            return gametiles

        if gametiles[x][y].pieceonTile.tostring()=='k':
            if m==y-2:

                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][7].pieceonTile=gametiles[x][y-1].pieceonTile
                s=self.updateposition(n,7)
                gametiles[n][7].pieceonTile.position=s
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()


            elif m==y+2:

                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[n][0].pieceonTile=gametiles[x][y+1].pieceonTile
                s=self.updateposition(n,0)
                gametiles[n][0].pieceonTile.position=s
                gametiles[x][y].pieceonTile=nullpiece()
                gametiles[x][y-1].pieceonTile=nullpiece()


            else:
                gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
                s=self.updateposition(n,m)
                gametiles[n][m].pieceonTile.position=s
                gametiles[x][y].pieceonTile=mts


            return gametiles

        gametiles[n][m].pieceonTile=gametiles[x][y].pieceonTile
        s=self.updateposition(n,m)
        gametiles[n][m].pieceonTile.position=s
        gametiles[x][y].pieceonTile=mts

        return gametiles



    def movew(self,gametiles,y,x,n,m):
        promotion=False
        if gametiles[y][x].pieceonTile.tostring()=='k' or gametiles[y][x].pieceonTile.tostring()=='r':
            pass

        if gametiles[y][x].pieceonTile.tostring()=='k' and m==x+2:
            gametiles[y][x+1].pieceonTile=gametiles[y][x+3].pieceonTile
            s=self.updateposition(y,x+1)
            gametiles[y][x+1].pieceonTile.position=s
            gametiles[y][x+3].pieceonTile=nullpiece()
        if gametiles[y][x].pieceonTile.tostring()=='k' and m==x-2:
            gametiles[y][x-1].pieceonTile=gametiles[y][0].pieceonTile
            s=self.updateposition(y,x-1)
            gametiles[y][x-1].pieceonTile.position=s
            gametiles[y][0].pieceonTile=nullpiece()



        if gametiles[y][x].pieceonTile.tostring()=='p' and y-1==n and y==1:
            promotion=True


        if promotion==False:

            gametiles[n][m].pieceonTile=gametiles[y][x].pieceonTile
            gametiles[y][x].pieceonTile=nullpiece()
            s=self.updateposition(n,m)
            gametiles[n][m].pieceonTile.position=s

        if promotion==True:

            if gametiles[y][x].pieceonTile.tostring()=='p':
                gametiles[y][x].pieceonTile=nullpiece()
                gametiles[n][m].pieceonTile=queen('White',self.updateposition(n,m))
                promotion=False

        return gametiles
























                        
