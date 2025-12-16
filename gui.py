import pygame
import sys
from search.bfs import solve as bfs_solve
from search.dfs import solve as dfs_solve
from search.astar import solve as astar_solve
from search.greedy import solve as greedy_solve

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("River Crossing Problem Solver")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLUE = (100, 150, 255)      # River
GREEN = (100, 200, 100)     # Banks
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Font
font = pygame.font.SysFont(None, 28)

# State & Animation
current_path = []
current_step = 0
is_playing = False
is_paused = False # New variable for pause/resume
speed = 1000  # ms per step
last_move_time = 0

# Game states
MENU = 0
SIMULATION = 1
game_state = MENU

# Algorithm mapping
ALGORITHMS = {
    "BFS": bfs_solve,
    "DFS": dfs_solve,
    "A*": astar_solve,
    "Greedy": greedy_solve,
}
selected_algo = "BFS"
metrics = {"path_len": "--", "nodes": "--", "time": "--"}
algo_names = list(ALGORITHMS.keys())
current_algo_index = 0

def draw_scene(current_state, previous_state=None, animation_progress=0.0):
    M_L, C_L, B = current_state
    screen.fill(WHITE)

    # Draw banks
    pygame.draw.rect(screen, GREEN, (0, 0, WIDTH//3, HEIGHT))
    pygame.draw.rect(screen, GREEN, (2*WIDTH//3, 0, WIDTH//3, HEIGHT))

    # Draw river
    pygame.draw.rect(screen, BLUE, (WIDTH//3, 0, WIDTH//3, HEIGHT))

    # Draw state text
    state_text = font.render(f"State: ({M_L}, {C_L}, {'L' if B == 1 else 'R'})", True, BLACK)
    screen.blit(state_text, (10, 10))

    # Calculate right bank counts
    M_R = 3 - M_L
    C_R = 3 - C_L

    # Determine boat position
    boat_start_x = WIDTH // 3 + 50 if B == 1 else 2 * WIDTH // 3 - 100
    boat_end_x = WIDTH // 3 + 50 if B == 0 else 2 * WIDTH // 3 - 100

    if previous_state and current_state[2] != previous_state[2]: # Boat is moving
        # Interpolate boat position
        if current_state[2] == 0: # Moving from Left to Right
            boat_pos_x = boat_start_x + (boat_end_x - boat_start_x) * animation_progress
        else: # Moving from Right to Left
            boat_pos_x = boat_start_x - (boat_start_x - boat_end_x) * animation_progress
    else:
        boat_pos_x = boat_start_x

    # Draw boat
    boat_rect = pygame.Rect(boat_pos_x, HEIGHT - 100, 100, 30)
    pygame.draw.rect(screen, (139, 69, 19), boat_rect) # Brown boat

    # Positions for characters
    left_bank_positions_m = [(50 + i * 30, HEIGHT - 120) for i in range(3)]
    left_bank_positions_c = [(50 + i * 30, HEIGHT - 150) for i in range(3)]
    right_bank_positions_m = [(WIDTH - 80 - i * 30, HEIGHT - 120) for i in range(3)]
    right_bank_positions_c = [(WIDTH - 80 - i * 30, HEIGHT - 150) for i in range(3)]

    boat_positions_m = [(boat_pos_x + 10 + i * 30, HEIGHT - 80) for i in range(2)]
    boat_positions_c = [(boat_pos_x + 10 + i * 30, HEIGHT - 50) for i in range(2)]

    # Determine who is on the boat for animation
    m_on_boat = 0
    c_on_boat = 0
    if previous_state:
        prev_M_L, prev_C_L, prev_B = previous_state
        if B != prev_B: # Boat moved
            if B == 0: # Boat moved from Left to Right
                m_on_boat = prev_M_L - M_L
                c_on_boat = prev_C_L - C_L
            else: # Boat moved from Right to Left
                m_on_boat = M_L - prev_M_L
                c_on_boat = C_L - prev_C_L

    # Draw missionaries and cannibals on left bank
    m_left_bank_count = M_L
    c_left_bank_count = C_L

    if previous_state and current_state[2] != previous_state[2]: # Boat is moving
        if current_state[2] == 0: # Boat moving from Left to Right
            # Characters that were on the left bank but are now on the boat
            m_left_bank_count = M_L + m_on_boat
            c_left_bank_count = C_L + c_on_boat
        else: # Boat moving from Right to Left
            # Characters that are moving to the left bank from the boat
            pass # M_L and C_L already reflect the final state on the left bank

    for i in range(m_left_bank_count):
        pygame.draw.circle(screen, (255, 0, 0), left_bank_positions_m[i], 10) # Red for missionaries
    for i in range(c_left_bank_count):
        pygame.draw.circle(screen, (0, 0, 255), left_bank_positions_c[i], 10) # Blue for cannibals

    # Draw missionaries and cannibals on right bank
    m_right_bank_count = M_R
    c_right_bank_count = C_R

    if previous_state and current_state[2] != previous_state[2]: # Boat is moving
        if current_state[2] == 1: # Boat moving from Right to Left
            # Characters that were on the right bank but are now on the boat
            m_right_bank_count = M_R + m_on_boat
            c_right_bank_count = C_R + c_on_boat
        else: # Boat moving from Left to Right
            # Characters that are moving to the right bank from the boat
            pass # M_R and C_R already reflect the final state on the right bank

    for i in range(m_right_bank_count):
        pygame.draw.circle(screen, (255, 0, 0), right_bank_positions_m[i], 10)
    for i in range(c_right_bank_count):
        pygame.draw.circle(screen, (0, 0, 255), right_bank_positions_c[i], 10)

    # Draw missionaries and cannibals on the boat
    for i in range(m_on_boat):
        pygame.draw.circle(screen, (255, 0, 0), boat_positions_m[i], 10)
    for i in range(c_on_boat):
        pygame.draw.circle(screen, (0, 0, 255), boat_positions_c[i], 10)

def run_algorithm():
    global current_path, current_step, is_playing, metrics, selected_algo
    solver = ALGORITHMS[selected_algo]
    path, nodes, time_ms = solver()
    current_path = path
    current_step = 0
    is_playing = True

    # Update metrics
    if path:
        metrics["path_len"] = str(len(path) - 1)
        metrics["nodes"] = str(nodes)
        metrics["time"] = f"{time_ms:.2f}"
    else:
        metrics = {"path_len": "No sol", "nodes": str(nodes), "time": f"{time_ms:.2f}"}

# Main loop
running = True
while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_state == MENU:
                # Handle menu key presses
                if event.key == pygame.K_1:
                    selected_algo = algo_names[0]
                    run_algorithm()
                    game_state = SIMULATION
                elif event.key == pygame.K_2:
                    selected_algo = algo_names[1]
                    run_algorithm()
                    game_state = SIMULATION
                elif event.key == pygame.K_3:
                    selected_algo = algo_names[2]
                    run_algorithm()
                    game_state = SIMULATION
                elif event.key == pygame.K_4:
                    selected_algo = algo_names[3]
                    run_algorithm()
                    game_state = SIMULATION
            elif game_state == SIMULATION:
                # Handle simulation key presses
                if event.key == pygame.K_SPACE and current_path:
                    if current_step < len(current_path) - 1:
                        current_step += 1
                elif event.key == pygame.K_r:
                    run_algorithm()
                elif event.key == pygame.K_LEFT:
                    current_algo_index = (current_algo_index - 1) % len(algo_names)
                    selected_algo = algo_names[current_algo_index]
                    run_algorithm() # Rerun with new algorithm
                elif event.key == pygame.K_RIGHT:
                    current_algo_index = (current_algo_index + 1) % len(algo_names)
                    selected_algo = algo_names[current_algo_index]
                    run_algorithm() # Rerun with new algorithm
                elif event.key == pygame.K_p:
                    is_paused = not is_paused # Toggle pause state
                elif event.key == pygame.K_ESCAPE:
                    running = False

    if game_state == SIMULATION:
        # Auto-advance if playing
        if is_playing and not is_paused and current_path and current_step < len(current_path) - 1:
            # Draw
            if current_path and current_step < len(current_path):
                current_s = current_path[current_step]
                previous_s = current_path[current_step - 1] if current_step > 0 else None

                # Update step for next frame if playing and not paused
                if is_playing and not is_paused and current_time - last_move_time > speed:
                    current_step += 1
                    last_move_time = current_time

            # Calculate animation progress for boat movement
            animation_progress = 0.0
            if previous_s and current_s[2] != previous_s[2]: # If boat is moving
                elapsed_time = current_time - last_move_time
                animation_progress = min(1.0, elapsed_time / speed)

            draw_scene(current_s, previous_s, animation_progress)
        else:
            screen.fill(WHITE)
            draw_scene((3, 3, 1))  # default start

        # Draw metrics dashboard (right side)
        pygame.draw.rect(screen, GRAY, (WIDTH - 250, 0, 250, HEIGHT))
        
        # Display selected algorithm
        algo_text = font.render(f"Algorithm: {selected_algo}", True, BLACK)
        screen.blit(algo_text, (WIDTH - 240, 20))

        y = 50
        for label, value in [("Path Length", metrics["path_len"]), 
                             ("Nodes Explored", metrics["nodes"]), 
                             ("Time (ms)", metrics["time"])]:
            text = font.render(f"{label}: {value}", True, BLACK)
            screen.blit(text, (WIDTH - 240, y))
            y += 40
    else: # MENU state
        screen.fill(WHITE)
        title_text = font.render("Select an Algorithm", True, BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

        y_offset = HEIGHT // 2
        for i, algo_name in enumerate(algo_names):
            menu_text = font.render(f"{i+1}. {algo_name}", True, BLACK)
            screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, y_offset + i * 40))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()