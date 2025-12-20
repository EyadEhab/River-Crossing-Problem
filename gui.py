import tkinter as tk
from tkinter import messagebox
import os
import pygame
from tkinter import messagebox
import time
import math
from typing import List, Tuple

# Import solvers
from search.bfs import solve as bfs_solve
from search.dfs import solve as dfs_solve
from search.astar import solve as astar_solve
from search.greedy import solve as greedy_solve

from core.river_crossing import GOAL_STATE, INITIAL_STATE

# Colors
COLOR_SKY = "#87CEEB"
COLOR_RIVER = "#4682B4"
COLOR_LAND = "#228B22"
COLOR_BOAT = "#8B4513"
COLOR_MISSIONARY = "#FFD700"  # Gold
COLOR_CANNIBAL = "#FF4500"    # OrangeRed
COLOR_TEXT = "#FFFFFF"

class RiverCrossingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("River Crossing Problem Solver")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=800, height=600, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.solvers = {
            "BFS": bfs_solve,
            "DFS": dfs_solve,
            "A*": astar_solve,
            "Greedy": greedy_solve
        }

        self.current_state = INITIAL_STATE
        self.animation_speed = 0.02  # seconds per frame
        self.is_animating = False
        
        # Metrics
        self.metrics = None
        self.metrics_visible = False
        self.metrics_btn_id = None

        # Controls
        self.is_paused = False
        self.control_ids = []


        # Audio System
        self.init_audio()

        # Volume Control Slider (Persistent)
        self.create_volume_slider()

        self.show_start_menu()

    def show_start_menu(self):
        self.canvas.delete("all")
        self.draw_background()
        
        # Title
        self.canvas.create_text(400, 150, text="River Crossing Problem", font=("Helvetica", 36, "bold"), fill="white", tags="menu")
        self.canvas.create_text(400, 200, text="Choose an Algorithm to Solve", font=("Helvetica", 18), fill="white", tags="menu")

        # Buttons
        y_start = 250
        for i, (name, solver) in enumerate(self.solvers.items()):
            btn_y = y_start + i * 60
            self.create_button(400, btn_y, name, lambda s=name: self.run_simulation(s))
            
        # Run All Algorithms Button
        self.create_button(400, y_start + 4 * 60, "Compare All Algorithms", self.run_all_algorithms, bg_color="#2F4F4F")

    def create_button(self, x, y, text, command, bg_color="#333"):
        # Simple custom button on canvas
        btn_width = 300
        btn_height = 40
        x1, y1 = x - btn_width // 2, y - btn_height // 2
        x2, y2 = x + btn_width // 2, y + btn_height // 2
        
        btn_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=bg_color, outline="white", width=2, tags="menu_btn")
        txt_id = self.canvas.create_text(x, y, text=text, font=("Helvetica", 14, "bold"), fill="white", tags="menu_btn")
        
        # Bind events
        self.canvas.tag_bind(btn_id, "<Button-1>", lambda e: command())
        self.canvas.tag_bind(txt_id, "<Button-1>", lambda e: command())
        
        # Hover effect
        self.canvas.tag_bind(btn_id, "<Enter>", lambda e: self.canvas.itemconfig(btn_id, fill="#555"))
        self.canvas.tag_bind(btn_id, "<Leave>", lambda e: self.canvas.itemconfig(btn_id, fill=bg_color))

    def draw_background(self):
        # Sky
        self.canvas.create_rectangle(0, 0, 800, 300, fill=COLOR_SKY, outline="")
        # River
        self.canvas.create_rectangle(0, 300, 800, 600, fill=COLOR_RIVER, outline="")
        # Left Bank
        self.canvas.create_rectangle(0, 300, 250, 600, fill=COLOR_LAND, outline="")
        # Right Bank
        self.canvas.create_rectangle(550, 300, 800, 600, fill=COLOR_LAND, outline="")
        
        # Sun
        self.canvas.create_oval(650, 50, 750, 150, fill="#FFD700", outline="#FFA500", width=2)
        
        # Clouds
        self.draw_cloud(100, 80)
        self.draw_cloud(250, 50)
        self.draw_cloud(450, 90)
        self.draw_cloud(50, 150)

    def draw_cloud(self, x, y):
        # Draw a fluffy cloud using overlapping ovals
        self.canvas.create_oval(x, y, x+40, y+30, fill="white", outline="", tags="background")
        self.canvas.create_oval(x+20, y-10, x+60, y+30, fill="white", outline="", tags="background")
        self.canvas.create_oval(x+40, y, x+80, y+30, fill="white", outline="", tags="background")

    def run_all_algorithms(self):
        self.canvas.delete("all")
        self.draw_background()
        
        # Loading
        self.canvas.create_text(400, 300, text="Running all algorithms...", font=("Helvetica", 24), fill="white", tags="loading")
        self.root.update()
        
        results = []
        for name, solver in self.solvers.items():
            try:
                path, nodes, time_taken = solver()
                # path length = moves = len(path) - 1 if path else "N/A"
                pl = len(path) - 1 if path else "Fail"
                results.append((name, pl, nodes, time_taken * 1000))
            except Exception as e:
                results.append((name, "Error", 0, 0.0))
        
        self.canvas.delete("loading")
        self.show_comparison_view(results)

    def show_comparison_view(self, results):
        self.canvas.delete("all")
        self.draw_background()
        
        self.canvas.create_text(400, 50, text="Algorithm Comparison", font=("Helvetica", 32, "bold"), fill="black")
        
        # Headers
        headers = ["Algorithm", "Path Length", "Nodes Explored", "Time (ms)"]
        y_start = 120
        x_offsets = [150, 300, 480, 650]
        
        for i, h in enumerate(headers):
            self.canvas.create_text(x_offsets[i], y_start, text=h, font=("Arial", 14, "bold"), fill="#FFD700")
            
        self.canvas.create_line(50, y_start + 20, 750, y_start + 20, fill="black", width=2)
        
        # Rows
        row_y = y_start + 50
        for res in results:
            name, pl, nodes, time_ms = res
            
            # Format time
            t_str = f"{time_ms:.2f}"
            
            self.canvas.create_text(x_offsets[0], row_y, text=name, font=("Arial", 12), fill="black")
            self.canvas.create_text(x_offsets[1], row_y, text=str(pl), font=("Arial", 12), fill="black")
            self.canvas.create_text(x_offsets[2], row_y, text=str(nodes), font=("Arial", 12), fill="black")
            self.canvas.create_text(x_offsets[3], row_y, text=t_str, font=("Arial", 12), fill="black")
            
            row_y += 40
            
        # Back Button
        self.create_button(400, 500, "Main Menu", self.show_start_menu)

    def run_simulation(self, algo_name):
        print(f"Running {algo_name}...")
        self.canvas.delete("menu")
        self.canvas.delete("menu_btn")
        
        # Show loading or preparing info
        self.canvas.create_text(400, 300, text=f"Solving with {algo_name}...", font=("Helvetica", 24), fill="white", tags="loading")
        self.root.update()

        solver_func = self.solvers[algo_name]
        try:
            path, nodes, time_taken = solver_func()
        except Exception as e:
            messagebox.showerror("Error", f"Algorithm failed: {e}")
            self.show_start_menu()
            return

        self.canvas.delete("loading")
        
        if not path:
            messagebox.showinfo("Result", "No solution found.")
            self.show_start_menu()
            return
            
        print(f"Solution found: {len(path)} steps")
        
        # Store metrics
        self.metrics = {
            "Algo": algo_name,
            "Path Length": len(path) - 1,
            "Nodes Explored": nodes,
            "Time": f"{time_taken * 1000:.2f} ms"
        }
        
        self.create_metrics_button()
        self.create_control_buttons()
        
        # Display Algorithm Title
        self.canvas.create_text(400, 30, text=f"Algorithm: {algo_name}", font=("Helvetica", 20, "bold"), fill="white", tags="ui")
        
        self.is_paused = False
        self.animate_solution(path)

    def create_metrics_button(self):
        # Top-left button
        x, y = 60, 30
        self.metrics_btn_id = self.canvas.create_rectangle(x-50, y-15, x+50, y+15, fill="#555", outline="white", tags="ui")
        txt_id = self.canvas.create_text(x, y, text="Metrics", fill="white", font=("Arial", 10, "bold"), tags="ui")
        
        self.canvas.tag_bind(self.metrics_btn_id, "<Button-1>", lambda e: self.toggle_metrics())
        self.canvas.tag_bind(txt_id, "<Button-1>", lambda e: self.toggle_metrics())

    def create_control_buttons(self):
        # Bottom area controls
        y_pos = 570
        
        # Pause/Resume
        self.create_mini_button(300, y_pos, "Pause/Resume", self.toggle_pause)
        # Reset
        self.create_mini_button(400, y_pos, "Reset", self.reset_simulation)
        # Exit
        self.create_mini_button(500, y_pos, "End Game", self.exit_app, color="#8B0000")

    def create_mini_button(self, x, y, text, command, color="#444"):
        w, h = 90, 30
        bid = self.canvas.create_rectangle(x-w//2, y-h//2, x+w//2, y+h//2, fill=color, outline="white", tags="controls")
        tid = self.canvas.create_text(x, y, text=text, fill="white", font=("Arial", 10), tags="controls")
        
        self.canvas.tag_bind(bid, "<Button-1>", lambda e: command())
        self.canvas.tag_bind(tid, "<Button-1>", lambda e: command())
        self.canvas.tag_bind(bid, "<Enter>", lambda e: self.canvas.itemconfig(bid, fill="#666"))
        self.canvas.tag_bind(bid, "<Leave>", lambda e: self.canvas.itemconfig(bid, fill=color))

    def toggle_pause(self):
        self.is_paused = not self.is_paused

    def reset_simulation(self):
        self.is_animating = False
        self.canvas.delete("ui")
        self.canvas.delete("controls")
        self.canvas.delete("metrics_overlay")
        self.show_start_menu()

    def exit_app(self):
        pygame.mixer.quit()
        self.root.destroy()
    
    def init_audio(self):
        try:
            pygame.mixer.init()
            sound_path = os.path.join("sound", "test.mpeg")
            if os.path.exists(sound_path):
                pygame.mixer.music.load(sound_path)
                pygame.mixer.music.play(-1)  # Loop indefinitely
                pygame.mixer.music.set_volume(0.5)
            else:
                print(f"Warning: Sound file not found at {sound_path}")
        except Exception as e:
            print(f"Audio init error: {e}")

    def create_volume_slider(self):
        # Create a "Volume" button
        self.vol_btn = tk.Button(self.root, text="Volume", command=self.toggle_volume_slider,
                                 bg="#444", fg="white", font=("Arial", 10, "bold"), bd=1)
        self.vol_btn.place(x=720, y=10)
        
        # Create the slider but don't place it yet (hidden)
        self.vol_scale = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, 
                                  command=self.set_volume, length=150, 
                                  bg="#87CEEB", fg="white", 
                                  troughcolor="#FFFFFF", highlightthickness=0, bd=0,
                                  width=10, showvalue=1)
        self.vol_scale.set(50)
        self.vol_visible = False

    def toggle_volume_slider(self):
        if self.vol_visible:
            self.vol_scale.place_forget()
            self.vol_visible = False
        else:
            # Place above the sun (Sun is at ~50+ y)
            # We'll place it to the left of the button, slightly down or just aligned
            # Button is at x=720. Slider length=150.
            # Let's put it at x=560, y=15.
            self.vol_scale.place(x=560, y=10)
            self.vol_visible = True

    def set_volume(self, val):
        try:
            # Convert 0-100 to 0.0-1.0
            volume = float(val) / 100.0
            pygame.mixer.music.set_volume(volume)
        except Exception:
            pass



    def toggle_metrics(self):
        self.metrics_visible = not self.metrics_visible
        if self.metrics_visible:
            self.draw_metrics_overlay()
        else:
            self.canvas.delete("metrics_overlay")

    def draw_metrics_overlay(self):
        self.canvas.delete("metrics_overlay")
        if not self.metrics:
            return
            
        # Draw semi-transparent box
        x1, y1 = 10, 60
        x2, y2 = 250, 180
        
        # Canvas doesn't support alpha directly for shapes easily without images or extra windows.
        # We'll simulate it with stipple or just solid color.
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#222", outline="white", width=2, tags="metrics_overlay")
        
        y_text = y1 + 20
        for key, value in self.metrics.items():
            text = f"{key}: {value}"
            self.canvas.create_text(x1 + 10, y_text, text=text, anchor="w", fill="white", font=("Courier", 12), tags="metrics_overlay")
            y_text += 25


    def draw_entities(self, state):
        # Static draw for start/end
        # Use draw_scene_phase with empty movers to just draw the state static
        self.draw_scene_phase("cross", state, [], "LtoR", 0.0)

    def draw_character(self, x, y, char_type, color):
        if char_type == "M":
            self.draw_missionary(x, y)
        else:
            self.draw_cannibal(x, y)

    def draw_missionary(self, x, y):
        # Draw Missionary (Robe style)
        # Head
        self.canvas.create_oval(x-8, y-35, x+8, y-19, fill="#FFCCAA", outline="black", tags="entity") # Skin head
        
        # Body (Robe)
        # Triangle/Trapezoid shape
        points = [x, y-20, x-12, y+10, x+12, y+10]
        self.canvas.create_polygon(points, fill=COLOR_MISSIONARY, outline="black", tags="entity")
        
        # Cross on chest
        self.canvas.create_line(x, y-15, x, y, fill="black", width=1, tags="entity")
        self.canvas.create_line(x-5, y-10, x+5, y-10, fill="black", width=1, tags="entity")

    def draw_cannibal(self, x, y):
        # Draw Cannibal (Tribal style)
        # Head
        self.canvas.create_oval(x-8, y-35, x+8, y-19, fill="#D2691E", outline="black", tags="entity") # Darker skin head
        
        # Body (Torso)
        self.canvas.create_oval(x-10, y-20, x+10, y+5, fill="#8B4513", outline="black", tags="entity") # Body
        
        # Skirt/Loincloth
        skirt_points = [x-10, y, x+10, y, x+8, y+10, x-8, y+10]
        self.canvas.create_polygon(skirt_points, fill=COLOR_CANNIBAL, outline="black", tags="entity")
        
        # Spear (held in hand)
        self.canvas.create_line(x+10, y+10, x+15, y-25, fill="brown", width=2, tags="entity") # Shaft
        self.canvas.create_polygon(x+14, y-25, x+16, y-25, x+15, y-30, fill="silver", outline="black", tags="entity") # Tip


    def animate_solution(self, path):
        self.is_animating = True
        self.animate_sequence(path, 0)
        
    def animate_sequence(self, path, index):
        if not self.is_animating:
            return

        if index >= len(path) - 1:
            self.draw_entities(path[-1])
            self.show_success()
            return
            
        current_state = path[index]
        next_state = path[index+1]
        
        self.start_transition(current_state, next_state, path, index)

    def start_transition(self, curr_state, next_state, path, index):
        # Determine movement details
        c_m, c_c, c_b = curr_state
        n_m, n_c, n_b = next_state
        
        m_moved_count = abs(c_m - n_m)
        c_moved_count = abs(c_c - n_c)
        direction = "LtoR" if c_b == 1 else "RtoL"
        
        passengers = []
        # Identify who moves (simplification: take from end of lists)
        # We need (type, from_pos, to_pos)
        
        # Boat seats (indices)
        seat_indices = []
        if m_moved_count + c_moved_count == 1:
            seat_indices = [0] # Center-ish? Or use 0 (left seat)
        elif m_moved_count + c_moved_count == 2:
            seat_indices = [0, 1]
            
        # Assign seats
        seat_idx = 0
        
        # Source Bank Counts (for coordinate calculation)
        if direction == "LtoR":
            # Leaving Left Bank
            # Missionaries taking last spots
            src_m_start_idx = c_m - m_moved_count
            src_c_start_idx = c_c - c_moved_count
            bank_side = "left"
        else:
            # Leaving Right Bank
            src_m_start_idx = (3-c_m) - m_moved_count # Right bank M count = 3 - c_m
            src_c_start_idx = (3-c_c) - c_moved_count
            bank_side = "right"

        # Build movement list
        # Each item: {"type": "M" or "C", "bank_idx": int, "seat_idx": int}
        movers = []
        
        for i in range(m_moved_count):
            movers.append({"type": "M", "bank_idx": src_m_start_idx + i, "seat_idx": seat_indices[seat_idx]})
            seat_idx += 1
            
        for i in range(c_moved_count):
            movers.append({"type": "C", "bank_idx": src_c_start_idx + i, "seat_idx": seat_indices[seat_idx]})
            seat_idx += 1

        # Move Description
        parts = []
        if m_moved_count > 0:
            parts.append(f"{m_moved_count} Missionary" if m_moved_count == 1 else f"{m_moved_count} Missionaries")
        if c_moved_count > 0:
            parts.append(f"{c_moved_count} Cannibal" if c_moved_count == 1 else f"{c_moved_count} Cannibals")
            
        move_text_content = ", ".join(parts)
        if direction == "LtoR":
            move_text = f"{move_text_content} -> Right"
        else:
            move_text = f"Left <- {move_text_content}"

        # Phase 1: Embark
        self.run_embark(curr_state, next_state, movers, direction, 0.0, path, index, move_text)

    def run_embark(self, curr_state, next_state, movers, direction, progress, path, index, move_text):
        if not self.is_animating: return
        if self.is_paused:
            self.root.after(100, lambda: self.run_embark(curr_state, next_state, movers, direction, progress, path, index, move_text))
            return

        if progress > 1.0: progress = 1.0
        
        # Draw Embarking
        self.draw_scene_phase("embark", curr_state, movers, direction, progress, move_text)
        
        if progress < 1.0:
            self.root.after(20, lambda: self.run_embark(curr_state, next_state, movers, direction, progress + 0.05, path, index, move_text))
        else:
            # Done, start Crossing
            self.run_cross(curr_state, next_state, movers, direction, 0.0, path, index, move_text)

    def run_cross(self, curr_state, next_state, movers, direction, progress, path, index, move_text):
        if not self.is_animating: return
        if self.is_paused:
            self.root.after(100, lambda: self.run_cross(curr_state, next_state, movers, direction, progress, path, index, move_text))
            return

        if progress > 1.0: progress = 1.0
        
        self.draw_scene_phase("cross", curr_state, movers, direction, progress, move_text)
        
        if progress < 1.0:
            self.root.after(20, lambda: self.run_cross(curr_state, next_state, movers, direction, progress + 0.02, path, index, move_text))
        else:
            self.run_disembark(curr_state, next_state, movers, direction, 0.0, path, index, move_text)

    def run_disembark(self, curr_state, next_state, movers, direction, progress, path, index, move_text):
        if not self.is_animating: return
        if self.is_paused:
            self.root.after(100, lambda: self.run_disembark(curr_state, next_state, movers, direction, progress, path, index, move_text))
            return

        if progress > 1.0: progress = 1.0
        
        self.draw_scene_phase("disembark", curr_state, movers, direction, progress, move_text)
        
        if progress < 1.0:
            self.root.after(20, lambda: self.run_disembark(curr_state, next_state, movers, direction, progress + 0.05, path, index, move_text))
        else:
            # Finished full step
            self.animate_sequence(path, index + 1)

    def draw_scene_phase(self, phase, state, movers, direction, progress, move_text=""):
        self.canvas.delete("entity")
        
        # Draw Move Text in Sky
        if move_text:
            self.canvas.create_text(400, 280, text=move_text, font=("Helvetica", 16, "bold"), fill="black", tags="entity")
        
        m_left, c_left, boat_pos = state
        
        # Static counts (What remains on bank throughout)
        # Assuming movers are "removed" from state for drawing
        # If phase is embark, they are moving from bank to boat.
        # So static = original - moving
        
        num_m_moving = len([x for x in movers if x["type"] == "M"])
        num_c_moving = len([x for x in movers if x["type"] == "C"])
        
        # Calculate Static Entities on Banks
        if direction == "LtoR":
            static_m_l = m_left - num_m_moving
            static_c_l = c_left - num_c_moving
            static_m_r = 3 - m_left
            static_c_r = 3 - c_left
            boat_start_x = 260
            boat_end_x = 540
            bank_side = "left" # source
        else:
            # RtoL
            static_m_l = m_left
            static_c_l = c_left
            static_m_r = (3 - m_left) - num_m_moving # Right bank has total 3-m_left. 
            static_c_r = (3 - c_left) - num_c_moving
            boat_start_x = 540
            boat_end_x = 260
            bank_side = "right" # source

        # 1. Draw Static Groups
        self.draw_group(100, 350, static_m_l, static_c_l)
        self.draw_group(700, 350, static_m_r, static_c_r)
        
        # 2. Draw Boat
        boat_y = 500
        if phase == "embark":
            boat_x = boat_start_x
        elif phase == "disembark":
            boat_x = boat_end_x
        else: # cross
            boat_x = boat_start_x + (boat_end_x - boat_start_x) * progress

        self.draw_boat(boat_x, boat_y)
        
        # 3. Draw Movers
        for mover in movers:
            char_type = mover["type"]
            bank_idx = mover["bank_idx"]
            seat_idx = mover["seat_idx"]
            
            # Get Coordinates
            # Boat Seat Coords (Relative to boat center)
            offsets = [-20, 20] 
            offset = offsets[seat_idx] if seat_idx < len(offsets) else 0
            seat_x = boat_x + offset
            seat_y = boat_y - 20
            
            # Bank Coords
            bx, by = self.get_bank_coords(bank_side if phase != "disembark" else ("right" if bank_side=="left" else "left"), 
                                          char_type, bank_idx)
            
            # If Disembarking, destination is opposite bank
            # Logic check:
            # Embark: Source Bank -> Boat (Boat Static)
            # Cross: Boat -> Boat (Passenger Fixed on Boat)
            # Disembark: Boat -> Dest Bank (Boat Static)
            
            draw_x, draw_y = 0, 0
            
            if phase == "embark":
                # Interp Bank -> Seat
                bx, by = self.get_bank_coords(bank_side, char_type, bank_idx)
                
                # Ease out
                t = progress
                draw_x = bx + (seat_x - bx) * t
                draw_y = by + (seat_y - by) * t
                
            elif phase == "cross":
                # Fixed values on boat
                draw_x = seat_x
                draw_y = seat_y
                
            elif phase == "disembark":
                # Interp Left Seat -> Right Bank
                dest_side = "right" if direction == "LtoR" else "left"
                
                # We need destination index.
                # If LtoR, moving to Right Bank. existing right bank has static_m_r.
                # So new items append after static_m_r.
                # Actually, simplistic view: just append to end of existing list on dest.
                
                # We need to map *which* mover goes to *which* dest index.
                # Simple stack: if type M, index = static_m_dest + (0, 1..)
                # But we are iterating movers. We need to know order.
                # Let's recalculate dest index on fly or precalc.
                
                # Hacky: Assume calculate dest_idx based on current static + order in movers
                # But movers mixed M/C.
                # Let's count seen Ms and Cs in this loop? No, that resets every frame.
                # Use mover list index?
                pass
                
                # Better: calculate dest_idx dynamically
                if char_type == "M":
                    # How many Ms before me in movers?
                    my_m_order = len([m for m in movers[:movers.index(mover)] if m["type"]=="M"])
                    
                    if dest_side == "right": dest_start = static_m_r
                    else: dest_start = static_m_l
                    
                    dest_idx = dest_start + my_m_order
                else:
                    my_c_order = len([m for m in movers[:movers.index(mover)] if m["type"]=="C"])
                    if dest_side == "right": dest_start = static_c_r
                    else: dest_start = static_c_l
                    dest_idx = dest_start + my_c_order
                
                bx, by = self.get_bank_coords(dest_side, char_type, dest_idx)
                
                t = progress
                draw_x = seat_x + (bx - seat_x) * t
                draw_y = seat_y + (by - seat_y) * t
            
            self.draw_character(draw_x, draw_y, char_type, COLOR_MISSIONARY if char_type=="M" else COLOR_CANNIBAL)

    def get_bank_coords(self, side, char_type, index):
        # 100, 350
        if side == "left":
            base_x = 100
        else:
            base_x = 700
            
        spacing = 30
        
        # M: start_y = 350
        # C: start_y = 450
        
        start_y = 350 if char_type == "M" else 450
        
        x = base_x - 50 + (index % 3) * spacing
        y = start_y + (index // 3) * 60
        
        return x, y

    def draw_boat(self, x, y):
        # Draw realistic boat (Wooden Trapezoid)
        # Hull
        hull_points = [x-60, y-10, x+60, y-10, x+40, y+20, x-40, y+20]
        self.canvas.create_polygon(hull_points, fill=COLOR_BOAT, outline="black", width=2, tags="entity")
        
        # Wood planks details
        self.canvas.create_line(x-55, y, x+55, y, fill="#5C3317", width=1, tags="entity")
        self.canvas.create_line(x-48, y+10, x+48, y+10, fill="#5C3317", width=1, tags="entity")
        
        # Label
        self.canvas.create_text(x, y+5, text="BOAT", fill="white", font=("Arial", 8, "bold"), tags="entity")


    def draw_group(self, bank_x, start_y, m_count, c_count):
        spacing = 30
        # Draw Ms
        for i in range(m_count):
            x = bank_x - 50 + (i % 3) * spacing
            y = start_y + (i // 3) * 60
            self.draw_character(x, y, "M", COLOR_MISSIONARY)
            
        # Draw Cs
        for i in range(c_count):
            x = bank_x - 50 + (i % 3) * spacing
            y = start_y + 100 + (i // 3) * 60
            self.draw_character(x, y, "C", COLOR_CANNIBAL)

    def show_success(self):
        self.is_animating = False
        self.canvas.create_text(400, 200, text="Goal Reached!", font=("Helvetica", 32, "bold"), fill="lightgreen", tags="overlay")
        # Reuse reset logic for "Main Menu" button or just leave controls
        self.create_button(400, 350, "Main Menu", lambda: self.reset_simulation())

if __name__ == "__main__":
    root = tk.Tk()
    app = RiverCrossingApp(root)
    root.mainloop()
