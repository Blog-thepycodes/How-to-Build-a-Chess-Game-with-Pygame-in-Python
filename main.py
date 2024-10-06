import pygame
import chess
import random
 
 
# Initialize Pygame
pygame.init()
 
 
# Set up display with resizable window
width, height = 800, 500  # Default size
window = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Chess - The Pycodes")
 
 
# Load images for pieces
images = {}
image_files = {
   'p': 'images/p.png',  # White pawn
   'n': 'images/n.png',  # White knight
   'b': 'images/b.png',  # White bishop
   'r': 'images/r.png',  # White rook
   'q': 'images/q.png',  # White queen
   'k': 'images/k.png',  # White king
   'P1': 'images/P1.png',  # Black pawn
   'N1': 'images/N1.png',  # Black knight
   'B1': 'images/B1.png',  # Black bishop
   'R1': 'images/R1.png',  # Black rook
   'Q1': 'images/Q1.png',  # Black queen
   'K1': 'images/K1.png'  # Black king
}
 
 
def load_images(square_size):
   """Load chess piece images into the images dictionary, scaled to the square size."""
   for symbol, file in image_files.items():
       try:
           images[symbol] = pygame.transform.scale(pygame.image.load(file), (square_size, square_size))
       except pygame.error as e:
           print(f"Error loading image for {symbol}: {e}")
 
 
def draw_text(text, font, color, x, y):
   """Helper function to draw text on the screen."""
   screen_text = font.render(text, True, color)
   window.blit(screen_text, (x, y))
 
 
def menu_screen():
   """Menu screen to choose game options."""
   font = pygame.font.Font(None, 60)
   small_font = pygame.font.Font(None, 40)
   selected_mode = None
   selected_difficulty = 'medium'
   selected_side = 'w'
 
 
   running = True
   while running:
       window.fill(pygame.Color("black"))
 
 
       draw_text("Chess Game", font, pygame.Color("white"), 280, 50)
 
 
       # Game mode options
       draw_text("1. Player vs Player", small_font, pygame.Color("white"), 250, 150)
       draw_text("2. Player vs Computer", small_font, pygame.Color("white"), 250, 200)
 
 
       # Difficulty options (Only if Player vs Computer is selected)
       if selected_mode == 'computer':
           draw_text(f"Difficulty: {selected_difficulty.capitalize()}", small_font, pygame.Color("white"), 250, 250)
           draw_text("Press D to toggle difficulty", small_font, pygame.Color("white"), 250, 300)
 
 
       # Side selection
       draw_text(f"Your side: {'White' if selected_side == 'w' else 'Black'}", small_font, pygame.Color("white"), 250, 350)
       draw_text("Press S to toggle side", small_font, pygame.Color("white"), 250, 400)
 
 
       draw_text("Press ENTER to start", small_font, pygame.Color("white"), 250, 500)
 
 
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               running = False
               pygame.quit()
               return None, None, None  # Exit the game
 
 
           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_1:
                   selected_mode = 'player'
               elif event.key == pygame.K_2:
                   selected_mode = 'computer'
               elif event.key == pygame.K_d and selected_mode == 'computer':
                   # Toggle difficulty
                   if selected_difficulty == 'easy':
                       selected_difficulty = 'medium'
                   elif selected_difficulty == 'medium':
                       selected_difficulty = 'hard'
                   else:
                       selected_difficulty = 'easy'
               elif event.key == pygame.K_s:
                   # Toggle player side
                   selected_side = 'b' if selected_side == 'w' else 'w'
               elif event.key == pygame.K_RETURN and selected_mode is not None:
                   running = False  # Exit the menu
 
 
       pygame.display.flip()
 
 
   return selected_mode, selected_difficulty, selected_side
 
 
def draw_board(board, square_size, selected_square=None, last_move=None):
   """Draw the chess board and pieces, adjusting to the current square size."""
   colors = [pygame.Color("white"), pygame.Color("gray")]
   for row in range(8):
       for col in range(8):
           color = colors[(row + col) % 2]
           pygame.draw.rect(window, color, pygame.Rect(col * square_size, row * square_size, square_size, square_size))
 
 
           # Draw pieces on the board
           piece = board.piece_at(chess.square(col, 7 - row))
           if piece:
               custom_symbol = get_custom_piece_symbol(piece)
               piece_image = images.get(custom_symbol)
               if piece_image:
                   window.blit(piece_image, (col * square_size, row * square_size))
 
 
   # Highlight the last move (from and to squares)
   if last_move:
       highlight_square(last_move.from_square, square_size, color="blue")
       highlight_square(last_move.to_square, square_size, color="blue")
 
 
   # Highlight the selected square
   if selected_square is not None:
       highlight_square(selected_square, square_size)
 
 
def highlight_square(square, square_size, color="yellow"):
   """Highlight the selected square."""
   col, row = chess.square_file(square), 7 - chess.square_rank(square)
   pygame.draw.rect(window, pygame.Color(color), pygame.Rect(col * square_size, row * square_size, square_size, square_size), 3)
 
 
def highlight_check(board, square_size):
   """Highlight the king if in check."""
   if board.is_check():
       king_square = board.king(board.turn)
       highlight_square(king_square, square_size, color="red")
 
 
def highlight_legal_moves(board, selected_square, square_size):
   """Highlight legal moves for the selected piece."""
   legal_moves = board.legal_moves
   for move in legal_moves:
       if move.from_square == selected_square:
           row = 7 - chess.square_rank(move.to_square)
           col = chess.square_file(move.to_square)
           pygame.draw.circle(window, pygame.Color("blue"), (col * square_size + square_size // 2, row * square_size + square_size // 2), square_size // 6)
 
 
 
 
def get_custom_piece_symbol(piece):
   """Map python-chess piece symbols to custom notation."""
   symbol = piece.symbol()
   if piece.color == chess.WHITE:
       return symbol.lower()
   else:
       return symbol.upper() + '1'
 
 
def piece_value(piece):
   """Assign a value to each piece type."""
   piece_values = {
       chess.PAWN: 1,
       chess.KNIGHT: 3,
       chess.BISHOP: 3,
       chess.ROOK: 5,
       chess.QUEEN: 9,
       chess.KING: 1000  # King has an artificially high value to avoid danger
   }
   return piece_values.get(piece.piece_type, 0)
 
 
def evaluate_board(board):
   """A simple evaluation function that sums up the values of pieces on the board."""
   piece_values = {
       chess.PAWN: 1,
       chess.KNIGHT: 3,
       chess.BISHOP: 3,
       chess.ROOK: 5,
       chess.QUEEN: 9,
       chess.KING: 1000
   }
   score = 0
   for square in chess.SQUARES:
       piece = board.piece_at(square)
       if piece:
           value = piece_values.get(piece.piece_type, 0)
           if piece.color == chess.WHITE:
               score += value  # Add value for White pieces
           else:
               score -= value  # Subtract value for Black pieces
   return score
 
 
def is_piece_threatened(board, square):
   """Check if a piece on a given square is attacked by the opponent."""
   attackers = board.attackers(not board.piece_at(square).color, square)
   return bool(attackers)
 
 
 
 
def evaluate_move(board, move):
   """Evaluate the value of a move based on material gain/loss and board state."""
   board.push(move)
 
 
   # Basic evaluation by counting material (more complex evaluation can be added)
   score = evaluate_board(board)
 
 
   # Adjust score for different piece values
   piece_values = {
       chess.PAWN: 1,
       chess.KNIGHT: 3,
       chess.BISHOP: 3,
       chess.ROOK: 5,
       chess.QUEEN: 9,
       chess.KING: 1000  # King is invaluable
   }
 
 
   # Prioritize capturing opponent pieces
   captured_piece = board.piece_at(move.to_square)
   if captured_piece:
       score += piece_values.get(captured_piece.piece_type, 0)  # Gain value from capture
 
 
   # Penalize if moving a piece to a threatened square, but first ensure the piece exists
   moving_piece = board.piece_at(move.from_square)
   if moving_piece and board.is_attacked_by(not board.turn, move.to_square):
       score -= piece_values.get(moving_piece.piece_type, 0)
 
 
   board.pop()  # Undo the move
   return score
 
 
def computer_move(board, difficulty):
   """Generate the best move for the computer, ensuring proper evaluation for both White and Black."""
   legal_moves = list(board.legal_moves)
 
 
   if board.is_game_over():
       return None  # No move if the game is over
 
 
   best_move = None
   if board.turn == chess.WHITE:
       best_value = -float('inf')  # White aims to maximize
   else:
       best_value = float('inf')  # Black aims to minimize
 
 
   for move in legal_moves:
       move_value = evaluate_move(board, move)
 
 
       if board.turn == chess.WHITE:
           if move_value > best_value:
               best_value = move_value
               best_move = move
       else:
           if move_value < best_value:
               best_value = move_value
               best_move = move
 
 
   # Fallback to a random move if no best move found
   if not best_move:
       best_move = random.choice(legal_moves)
 
 
   return best_move
 
 
def promote_pawn(board, move):
  """Promote a pawn if it reaches the opposite end of the board."""
  piece = board.piece_at(move.from_square)
 
 
 
  # Check if the move is a pawn reaching the promotion rank
  if piece and piece.piece_type == chess.PAWN:
      promotion_rank_white = chess.square_rank(move.to_square) == 7
      promotion_rank_black = chess.square_rank(move.to_square) == 0
 
 
 
 
      if (piece.color == chess.WHITE and promotion_rank_white) or (
              piece.color == chess.BLACK and promotion_rank_black):
          return choose_promotion()  # Prompt player for promotion choice
  return None
 
 
def choose_promotion():
  """Prompt the player to choose the promotion piece."""
  font = pygame.font.Font(None, 40)
  prompt = True
  promotion_choice = None
 
 
 
 
  while prompt:
      window.fill(pygame.Color("black"))
      draw_text("Choose Promotion Piece", font, pygame.Color("white"), 200, 200)
      draw_text("Q: Queen, R: Rook, B: Bishop, N: Knight", font, pygame.Color("white"), 150, 300)
      pygame.display.flip()
 
 
 
 
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              pygame.quit()
              return chess.QUEEN  # Default promotion to Queen if the game is quit
 
 
 
 
          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_q:
                  promotion_choice = chess.QUEEN
              elif event.key == pygame.K_r:
                  promotion_choice = chess.ROOK
              elif event.key == pygame.K_b:
                  promotion_choice = chess.BISHOP
              elif event.key == pygame.K_n:
                  promotion_choice = chess.KNIGHT
 
 
 
 
      if promotion_choice:
          prompt = False
 
 
 
 
  return promotion_choice
 
 
def checkmate_screen(winner):
   """Display a screen when checkmate or stalemate occurs, showing the winner."""
   font = pygame.font.Font(None, 80)
   small_font = pygame.font.Font(None, 40)
   running = True
 
 
   while running:
       window.fill(pygame.Color("black"))
 
 
       if winner == 'draw':
           draw_text("Stalemate! It's a Draw!", font, pygame.Color("white"), 130, 200)
       else:
           draw_text(f"Checkmate! {winner} Wins!", font, pygame.Color("white"), 130, 200)
 
 
       draw_text("Press R to Restart", small_font, pygame.Color("white"), 150, 400)
       draw_text("Press Q to Quit", small_font, pygame.Color("white"), 150, 440)
 
 
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               running = False
               pygame.quit()
 
 
           if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_r:
                   return True  # Restart game
               elif event.key == pygame.K_q:
                   return False  # Quit game
 
 
       pygame.display.flip()
 
 
   return False
 
 
 
 
def main():
 
 
   # Get initial window size
   # Initialize the window
   DEFAULT_WIDTH, DEFAULT_HEIGHT = 800, 800  # Default size
   window = pygame.display.set_mode((DEFAULT_WIDTH, DEFAULT_HEIGHT), pygame.RESIZABLE)
   pygame.display.set_caption("Chess - The Pycodes")
   width, height = window.get_size()
   square_size = width // 8
 
 
   # Load images based on square size
   load_images(square_size)
 
 
   # Show menu screen to choose game options
   game_mode, difficulty, player_side = menu_screen()
 
 
   board = chess.Board()
   selected_square = None
   last_move = None
   running = True
 
 
   if game_mode is None:  # If the game is exited from the menu
       return
 
 
   # Set up the clock to manage frame rate
   clock = pygame.time.Clock()
 
 
   while running:
       # Adjust square size dynamically based on current window dimensions
       width, height = window.get_size()
       square_size = min(width, height) // 8  # Ensure the board fits in the window
 
 
       # Draw the board and update highlights
       draw_board(board, square_size, selected_square, last_move)
       highlight_check(board, square_size)
 
 
       if selected_square:
           highlight_legal_moves(board, selected_square, square_size)
 
 
       pygame.display.flip()
 
 
       # Event handling
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               running = False
           elif event.type == pygame.VIDEORESIZE:  # Handle window resizing
               window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
           elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse click
               col, row = event.pos[0] // square_size, event.pos[1] // square_size
               clicked_square = chess.square(col, 7 - row)
 
 
               if selected_square is None:
                   # If no square is selected, select this square
                   if board.piece_at(clicked_square) and board.piece_at(clicked_square).color == board.turn:
                       selected_square = clicked_square
                       highlight_legal_moves(board, selected_square, square_size)
               else:
                   # Try to move to the clicked square
                   move = chess.Move(selected_square, clicked_square, promotion=promote_pawn(board, chess.Move(selected_square, clicked_square)))
                   if move in board.legal_moves:
                       last_move = move
                       board.push(move)
                       selected_square = None
 
 
                       # Check for game end (checkmate or stalemate)
                       if board.is_checkmate():
                           winner = "White" if board.turn == chess.BLACK else "Black"
                           if not checkmate_screen(winner):  # If player quits, exit loop
                               running = False
                           else:
                               return main()  # Restart game
 
 
                       elif board.is_stalemate():
                           if not checkmate_screen("draw"):  # If player quits, exit loop
                               running = False
                           else:
                               return main()  # Restart game
                   else:
                       # If move is illegal, deselect the square
                       selected_square = None
 
 
       # Computer move (for Player vs Computer mode)
       if game_mode == 'computer' and board.turn != (player_side == 'w'):
           pygame.time.delay(1000)  # Add delay to simulate thinking
           move = computer_move(board, difficulty)
           if move:
               last_move = move
               board.push(move)
 
 
               # Check for game end (checkmate or stalemate)
               if board.is_checkmate():
                   winner = "White" if board.turn == chess.BLACK else "Black"
                   if not checkmate_screen(winner):  # If player quits, exit loop
                       running = False
                   else:
                       return main()  # Restart game
 
 
               elif board.is_stalemate():
                   if not checkmate_screen("draw"):  # If player quits, exit loop
                       running = False
                   else:
                       return main()  # Restart game
 
 
       # Cap frame rate at 60 FPS
       clock.tick(60)
 
 
   pygame.quit()
 
 
if __name__ == "__main__":
   main()
