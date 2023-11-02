import pygame


def gui():
    # Initialize pygame and create a window
    pygame.init()
    screen = pygame.display.set_mode((500, 500))

    # Create a 5x5 grid of blue squares
    for i in range(5):
        for j in range(5):
            pygame.draw.rect(screen, (220, 220, 220), (i * 100, j * 100, 100, 100))

    # draw borders
    # horizontal
    for i in range(6):
        pygame.draw.rect(screen, (0, 0, 0), (i * 100 - 6, 0, 12, 500))
    # vertical
    for i in range(6):
        pygame.draw.rect(screen, (0, 0, 0), (0, i * 100 - 6, 500, 12))

    # Create the pieces for each player
    player1_pieces = []
    player2_pieces = []

    # Create 5 pieces for player 1 and place them on the bottom row
    for i in range(5):
        player1_pieces.append(pygame.Surface((70, 70)))
        player1_pieces[i].fill((255, 0, 0))  # red color
        screen.blit(player1_pieces[i], (i * 100 + 15, 415))

    # Create 5 pieces for player 2 and place them on the top row
    for i in range(5):
        player2_pieces.append(pygame.Surface((70, 70)))
        player2_pieces[i].fill((0, 255, 0))  # green color
        screen.blit(player2_pieces[i], (i * 100 + 15, 15))

    # Update the display
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    # cleanup and exit
    pygame.quit()
