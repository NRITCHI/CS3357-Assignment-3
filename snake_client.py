import pygame
import socket

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 500, 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

# Global variables
client_number = 0

# Connect to the server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 5555))

# draw the game state
def draw_game_state(game_state):
    # Reset screen to black before drawing
    win.fill((0, 0, 0))





     # When game states are concatonated split them
    if ')(' in game_state:
        # Find the last occurrence of ')(' which is likely where the split should occur
        split_index = game_state.rfind(')(')
        # Add a split character '|' to separate the two game states
        game_state = game_state[:split_index+1] + '|' + game_state[split_index+1:]


    print('gamestate: ' + game_state)

    # Split game state into snake positions and snack positions and discard the previously concatonated game state
    if '|' in game_state:
        snake_pos_str, snacks_pos_str = game_state.split('|', 2)[slice(2)]
        
        #snake_pos_str, snacks_pos_str = game_state.split('|')
        #snake_pos_str, snacks_pos_str = game_state.split('|', 1)
        snake_positions = snake_pos_str.split('**')
        #print("test" + snacks_pos_str)

        # Draw each snake
        for snake_str in snake_positions:
            snake_body = snake_str.split('*')
            for pos_str in snake_body:
                if pos_str:  # Ensure the position is not empty
                    x, y = map(int, pos_str.strip('()').split(','))
                    pygame.draw.rect(win, (255, 0, 0), (x * 20, y * 20, 20, 20))

        # Draw the snacks
        snack_positions = snacks_pos_str.split('**')
        for snack_pos_str in snack_positions:
            if snack_pos_str:  # Ensure the position is not empty
                print("post split:" + snack_pos_str)
                x, y = map(int, snack_pos_str.strip('()').split(','))
                pygame.draw.rect(win, (0, 255, 0), (x * 20, y * 20, 20, 20))

    # Update display
    pygame.display.update()

# Main loop
run = True
while run:
    pygame.time.delay(50)
    #send quit command if needed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
        # Send movement commands to the server
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                sock.send("left".encode())
            if event.key == pygame.K_RIGHT:
                sock.send("right".encode())
            if event.key == pygame.K_UP:
                sock.send("up".encode())
            if event.key == pygame.K_DOWN:
                sock.send("down".encode())

    # Send command to get the game state
    sock.send("get".encode())
    game_state = sock.recv(2048).decode()

    # Draw the game state
    draw_game_state(game_state)

sock.close()

