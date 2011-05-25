'''
    Rule module.
'''
from itertools import repeat
import widget


def empty_or_enemy(curr, newp, board_pieces):
    curr_piece = board_pieces[curr]
    new_piece = board_pieces.get(newp)
    if not new_piece:
        return True
    return curr_piece.is_enemy(new_piece)

def is_enemy(curr, newp, board_pieces):
    curr_piece = board_pieces[curr]
    new_piece = board_pieces.get(newp)
    if not new_piece:
        return False
    return curr_piece.is_enemy(new_piece)

def near(curr_pos):
    x,y = curr_pos
    nears = [(x+1,y),
             (x-1,y),
             (x,y+1),
             (x,y-1)]
    return nears


def general(curr_pos, board_pieces):
    candidates = near(curr_pos)
    candidates = [c for c in candidates if empty_or_enemy(curr_pos, c, board_pieces)]
    candidates = [c for c in candidates if 0 <= c[0] <= int(widget.Board.gx) ]
    candidates = [c for c in candidates if 0 <= c[1] <= int(widget.Board.gy) ]
    possible_moves = candidates

    return possible_moves

def advisor(curr_pos, board_pieces):
    x,y = curr_pos
    candidates = []
    for nx in (-1,0,1):
        for ny in (-1,0,1):
            candidates.append( (x+nx,y+ny) )

    candidates = [c for c in candidates if empty_or_enemy(curr_pos, c, board_pieces)]
    candidates = [c for c in candidates if 3 <= c[0] <= 5 ]
    candidates = [c for c in candidates if int(widget.Board.gy)-2 <= c[1] <= int(widget.Board.gy) 
            or 0 <= c[1] <= 2]

    possible_moves = candidates

    return possible_moves

def elephant(curr_pos, board_pieces):
    x,y = curr_pos
    candidates = []
    for nx in (-2,2):
        for ny in (-2,2):
            candidates.append( (x+nx, y+ny) )

    candidates = [c for c in candidates if empty_or_enemy(curr_pos, c, board_pieces)]
    candidates = [c for c in candidates if 0 <= c[0] <= int(widget.Board.gx) ]
    candidates = [c for c in candidates if 0 <= c[1] <= int(widget.Board.gy) ]
    possible_moves = []
    for c in candidates:
        nx, ny = c
        middle = (x+(nx-x)/2, y+(ny-y)/2)
        print middle
        if not board_pieces.get(middle):
            possible_moves.append(c)
    return possible_moves

def horse(curr_pos, board_pieces):
    # TODO: implement the block rule
    x,y = curr_pos
    candidates = []
    for px in (+1, -1):
        for py in (+1, -1):
            for nx, ny in ((1,2),(2,1)):
                candidates.append( (x+px*nx, y+py*ny) )

    candidates = [c for c in candidates if empty_or_enemy(curr_pos, c, board_pieces)]
    candidates = [c for c in candidates if 0 <= c[0] <= int(widget.Board.gx) ]
    candidates = [c for c in candidates if 0 <= c[1] <= int(widget.Board.gy) ]

    return candidates

def chariot(curr_pos, board_pieces):
    x,y = curr_pos
    candidates = []
    cy = y+1
    for cy in range(y+1, int(widget.Board.gy)+1):
        if board_pieces.get((x,cy)):
            break
        candidates.append((x, cy))
    if is_enemy(curr_pos, (x,cy), board_pieces):
        candidates.append((x, cy))

    cy = y-1
    for cy in range(y-1, -1, -1):
        if board_pieces.get((x,cy)):
            break
        candidates.append((x, cy))
    if is_enemy(curr_pos, (x,cy), board_pieces):
        candidates.append((x, cy))

    cx = x+1
    for cx in range(x+1, int(widget.Board.gx)+1):
        if board_pieces.get((cx,y)):
            break
        candidates.append((cx, y))
    if is_enemy(curr_pos, (x,cy), board_pieces):
        candidates.append((x, cy))

    cx = x-1
    for cx in range(x-1, -1, -1):
        if board_pieces.get((cx,y)):
            break
        candidates.append((cx, y))
    if is_enemy(curr_pos, (x,cy), board_pieces):
        candidates.append((x, cy))

    return candidates

def cannon(curr_pos, board_pieces):
    x,y = curr_pos
    candidates = []
    cy = y+1
    for cy in range(y+1, int(widget.Board.gy)+1):
        if board_pieces.get((x,cy)):
            break
        candidates.append((x, cy))
    cy += 1
    while cy <= int(widget.Board.gy):
        if is_enemy(curr_pos, (x,cy), board_pieces):
            candidates.append((x,cy))
            break
        cy += 1

    cy = y-1
    for cy in range(y-1, -1, -1):
        if board_pieces.get((x,cy)):
            break
        candidates.append((x, cy))
    cy -= 1
    while cy >= 0:
        if is_enemy(curr_pos, (x,cy), board_pieces):
            candidates.append((x,cy))
            break
        cy -= 1

    cx = x+1
    for cx in range(x+1, int(widget.Board.gx)+1):
        if board_pieces.get((cx,y)):
            break
        candidates.append((cx, y))
    cx += 1
    while cx <= int(widget.Board.gx):
        if is_enemy(curr_pos, (cx,y), board_pieces):
            candidates.append((cx,y))
            break
        cx += 1

    cx = x-1
    for cx in range(x-1, -1, -1):
        if board_pieces.get((cx,y)):
            break
        candidates.append((cx, y))
    cx -= 1
    while cx >= 0:
        if is_enemy(curr_pos, (cx,y), board_pieces):
            candidates.append((cx,y))
            break
        cx -= 1

    return candidates

def soldier(curr_pos, board_pieces):
    # TODO: real implementation
    return near(curr_pos)
