import tkinter as tk

def set_tile(row, col, sub_row, sub_col):
    global current_player
    button = ultimate_frame.grid_slaves(row=row+1, column=col)[0].grid_slaves(row=sub_row, column=sub_col)[0]
    if button["text"] == "":
        button["text"] = current_player
        if check_winner(row, col):
            label.config(text=f"{current_player} wins the sub-board!")
            disable_sub_board(row, col)
            display_winner(row, col, current_player)
            
            # Check for main game winner after a sub-board is won
            if check_main_winner():
                label.config(text=f"GAME OVER! {current_player} WINS THE GAME!")
                disable_all_boards()
                return
                
        elif check_draw(row, col):
            label.config(text="Sub-board is a draw!")
            disable_sub_board(row, col)
        else:
            current_player = player_o if current_player == player_x else player_x
            label.config(text=f"{current_player}'s Turn")

def check_winner(row, col):
    frame = ultimate_frame.grid_slaves(row=row+1, column=col)[0]
    for i in range(3):
        if all(frame.grid_slaves(row=i, column=j)[0]["text"] == current_player for j in range(3)):
            return True
        if all(frame.grid_slaves(row=j, column=i)[0]["text"] == current_player for j in range(3)):
            return True
    if all(frame.grid_slaves(row=i, column=i)[0]["text"] == current_player for i in range(3)):
        return True
    if all(frame.grid_slaves(row=i, column=2-i)[0]["text"] == current_player for i in range(3)):
        return True
    return False

def check_draw(row, col):
    frame = ultimate_frame.grid_slaves(row=row+1, column=col)[0]
    return all(frame.grid_slaves(row=i, column=j)[0]["text"] != "" for i in range(3) for j in range(3))

def disable_sub_board(row, col):
    frame = ultimate_frame.grid_slaves(row=row+1, column=col)[0]
    for i in range(3):
        for j in range(3):
            button = frame.grid_slaves(row=i, column=j)[0]
            button.config(background="black", state="disabled")

def reset_game():
    global current_player
    current_player = player_x
    label.config(text=f"{current_player}'s Turn")
    for row in range(3):
        for col in range(3):
            frame = ultimate_frame.grid_slaves(row=row+1, column=col)[0]
            for widget in frame.winfo_children():
                widget.destroy()
                
            for sub_row in range(3):
                for sub_col in range(3):
                    button = tk.Button(frame, text="", font=("Arial", 16), width=3, height=2,
                                     command=lambda r=row, c=col, sr=sub_row, sc=sub_col: set_tile(r, c, sr, sc))
                    button.grid(row=sub_row, column=sub_col, padx=2, pady=2)

def display_winner(row, col, winner):
    # Get the frame of the sub-board
    frame = ultimate_frame.grid_slaves(row=row+1, column=col)[0]
    
    # Hide all buttons except the center one
    for sub_row in range(3):
        for sub_col in range(3):
            button = frame.grid_slaves(row=sub_row, column=sub_col)[0]
            if sub_row == 1 and sub_col == 1:  # Center button
                button.config(text=winner, font=("Arial", 60), width=3, height=2, disabledforeground="red")

            else:
                button.grid_remove()  # Hide other buttons

def check_main_winner():
    # Check rows
    for i in range(3):
        if all(has_sub_board_winner(i, j, current_player) for j in range(3)):
            return True
    # Check columns
    for j in range(3):
        if all(has_sub_board_winner(i, j, current_player) for i in range(3)):
            return True
    # Check diagonals
    if all(has_sub_board_winner(i, i, current_player) for i in range(3)):
        return True
    if all(has_sub_board_winner(i, 2-i, current_player) for i in range(3)):
        return True
    return False

def has_sub_board_winner(row, col, player):
    frame = ultimate_frame.grid_slaves(row=row+1, column=col)[0]
    # Check if the center button (where we display the winner) has the player's symbol
    center_button = frame.grid_slaves(row=1, column=1)[0]
    return center_button["text"] == player

# Add this new function to disable all boards when game is won
def disable_all_boards():
    for row in range(3):
        for col in range(3):
            frame = ultimate_frame.grid_slaves(row=row+1, column=col)[0]
            for button in frame.winfo_children():
                if isinstance(button, tk.Button):
                    button.config(state="disabled")


player_x = "X"
player_o = "O"
current_player = player_x

game_board = tk.Tk()
game_board.title("Xtreme Tic Tac Toe")
game_board.geometry("700x750")
game_board.resizable(False, False)
game_board.configure(bg="lightblue")

ultimate_frame = tk.Frame(game_board)

label = tk.Label(ultimate_frame, text=f"{current_player}'s Turn", font=("Arial", 16), background= "gray", fg="white")
label.grid(row=0, column=0, padx=5, pady=5, columnspan=3, sticky="ew")

for row in range(3):
    for col in range(3):
        frame = tk.Frame(ultimate_frame, borderwidth=2, relief="solid", bg="darkgray")
        frame.grid(row=row+1, column=col, padx=5, pady=5)
        for sub_row in range(3):
            for sub_col in range(3):
                button = tk.Button(frame, text="", font=("Arial", 16), width=3, height=2,
                                   command=lambda r=row, c=col, sr=sub_row, sc=sub_col: set_tile(r, c, sr, sc))
                button.grid(row=sub_row, column=sub_col, padx=2, pady=2)

reset_btn = tk.Button(ultimate_frame, text="Reset Game", font=("Arial", 14), bg="gray", fg="white",
                      command=reset_game)
reset_btn.grid(row=4, column=0, padx=5, pady=10, columnspan=3, sticky="ew")



ultimate_frame.pack()

game_board.mainloop()