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

def down_line(curr_pos):
  ''' Return points starting from current posistion to the downer boarder. '''
  x, y = curr_pos
  for cy in xrange(y+1, int(widget.Board.gy)+1):
    yield x, cy

def up_line(curr_pos):
  ''' Return points starting from current posistion to the upper boarder. '''
  x, y = curr_pos
  for cy in range(y-1, -1, -1):
    yield x, cy

def is_general_territory(curr_pos):
  ''' A predicate to determine if the current position is within "General's territory" '''
  x, y = curr_pos
  return 3 <= x <= 5 and (int(widget.Board.gy)-2 <= y <= int(widget.Board.gy) or 0 <= y <= 2)

def general(curr_pos, board_pieces):
  ''' Rule for general. '''
  candidates = near(curr_pos)
  candidates = (c for c in candidates if empty_or_enemy(curr_pos, c, board_pieces))
  candidates = (c for c in candidates if is_general_territory(c))
  possible_moves = list(candidates)

  # flying general rule
  x, y = curr_pos
  if get_forward(curr_pos, board_pieces) > 0:
    line = down_line(curr_pos)
  else:
    line = up_line(curr_pos)

  for cx, cy in line:
    piece = board_pieces.get((cx,cy))
    print cx, cy
    if piece:
      if piece.is_general():
        possible_moves.append((cx,cy))
      break

  return possible_moves

def advisor(curr_pos, board_pieces):
  x,y = curr_pos
  candidates = []
  for nx in (-1,0,1):
    for ny in (-1,0,1):
      candidates.append( (x+nx,y+ny) )

  candidates = (c for c in candidates if empty_or_enemy(curr_pos, c, board_pieces))
  candidates = (c for c in candidates if is_general_territory(c))
  
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
  x,y = curr_pos
  candidates = []
  for px in (+1, -1):
    for py in (+1, -1):
      for nx, ny in ((1,2),(2,1)):
        candidates.append( (x+px*nx, y+py*ny) )

  candidates = [c for c in candidates if empty_or_enemy(curr_pos, c, board_pieces)]
  candidates = [c for c in candidates if 0 <= c[0] <= int(widget.Board.gx) ]
  candidates = [c for c in candidates if 0 <= c[1] <= int(widget.Board.gy) ]
  # filtering out the 'blocking rules' of a horse.
  possible_moves = []
  for c in candidates:
    dx = c[0] - curr_pos[0]
    dy = c[1] - curr_pos[1]
    for sign in (+1,-1):
      if (dx == sign*2 and board_pieces.get((curr_pos[0]+sign,
        curr_pos[1]))) or \
         (dy == sign*2 and board_pieces.get((curr_pos[0],
        curr_pos[1]+sign))):
        break
    else:
      possible_moves.append(c)

  return possible_moves

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

def in_enemy_territory(curr_pos, board_pieces):
  # TODO: any better implementation?
  piece = board_pieces.get(curr_pos)
  if piece.color == 'red' and 0 <= curr_pos[1] <= 4:
    return True
  if piece.color == 'black' and 5 <= curr_pos[1] <= 9:
    return True
  return False

def get_forward(curr_pos, board_pieces):
  piece = board_pieces.get(curr_pos)
  if piece.color == 'red':
    return -1
  else:
    return 1

def soldier(curr_pos, board_pieces):
  x,y = curr_pos
  forward = get_forward(curr_pos, board_pieces)
  if in_enemy_territory(curr_pos, board_pieces):
    candidates = [(x+1,y),
       (x-1,y),
       (x,y+forward),]
  else:
    candidates = [(x,y+forward)]
  candidates = [c for c in candidates if empty_or_enemy(curr_pos, c, board_pieces)]
  candidates = [c for c in candidates if 0 <= c[0] <= int(widget.Board.gx) ]
  candidates = [c for c in candidates if 0 <= c[1] <= int(widget.Board.gy) ]
  return candidates


if __name__=='__main__':
  print list(up_line((0,1)))