import tkinter as tk

def set_tile(row, col, sub_row, sub_col):
    #getting the global variables needed
    global current_player, next_sub_board_row, next_sub_board_col

    # Enforce move to the correct sub-board if specified
    if (next_sub_board_row is not None and next_sub_board_col is not None and 
        (row != next_sub_board_row or col != next_sub_board_col)):
        return  
    # Set the button text if it's empty
    button = ultimate_frame.grid_slaves(row=row+1, column=col)[0].grid_slaves(row=sub_row, column=sub_col)[0]
    if button["text"] == "":
        button["text"] = current_player
        
        # Check for sub-board win or draw
        if check_winner(row, col):
            label.config(text=f"{current_player} wins the sub-board!")
            disable_sub_board(row, col)
            display_winner(row, col, current_player)
            # Check for main board win
            if check_main_winner():
                label.config(text=f"GAME OVER! {current_player} WINS THE GAME!")
                disable_all_boards()
                return
            elif check_main_draw(): # Check for main board draw 
                label.config(text="GAME OVER! IT'S A TIE!")
                disable_all_boards()
                return
        elif check_draw(row, col):# Check for sub-board draw
            label.config(text="Sub-board is a draw!")
            disable_sub_board(row, col)
            display_winner(row, col, "T")  
            if check_main_draw():  # Check for main board draw
                label.config(text="GAME OVER! IT'S A TIE!")
                disable_all_boards()
                return
        
        # Determine the next sub-board to play in
        if is_sub_board_complete(sub_row, sub_col):
            next_sub_board_row = None
            next_sub_board_col = None
        else:
            next_sub_board_row = sub_row
            next_sub_board_col = sub_col
        
        # Switch players
        current_player = player_o if current_player == player_x else player_x
        update_turn_label()

def check_main_draw():
    #Check if all sub-boards are complete and there's no winner
   
    all_complete = all(is_sub_board_complete(row, col) 
                      for row in range(3) 
                      for col in range(3))
    return all_complete and not check_main_winner()

def check_winner(row, col):
    # Check rows, columns, and diagonals in the specified sub-board
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
    # Check if the specified sub-board is full (draw)
    frame = ultimate_frame.grid_slaves(row=row+1, column=col)[0]
    return all(frame.grid_slaves(row=i, column=j)[0]["text"] != "" for i in range(3) for j in range(3))

def disable_sub_board(row, col):
    # Disable all buttons in the specified sub-board
    frame = ultimate_frame.grid_slaves(row=row+1, column=col)[0]
    for i in range(3):
        for j in range(3):
            button = frame.grid_slaves(row=i, column=j)[0]
            button.config(background="black", state="disabled")

def reset_game():
    # Reset the entire game state
    global current_player, next_sub_board_row, next_sub_board_col
    current_player = player_x
    next_sub_board_row = None
    next_sub_board_col = None
    reset_board_colors()
    update_turn_label()
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
    # Display the winner in the center of the sub-board
    frame = ultimate_frame.grid_slaves(row=row+1, column=col)[0]
    
    # Clear all buttons and show the winner in the center
    for sub_row in range(3):
        for sub_col in range(3):
            button = frame.grid_slaves(row=sub_row, column=sub_col)[0]
            if sub_row == 1 and sub_col == 1:  
                button.config(text=winner, font=("Arial", 60), width=3, height=2, disabledforeground="red")

            else:
                button.grid_remove()  

def check_main_winner():
    # Check rows, columns, and diagonals of sub-boards for a main board win
    for i in range(3):
        if all(has_sub_board_winner(i, j, current_player) for j in range(3)):
            return True
    
    for j in range(3):
        if all(has_sub_board_winner(i, j, current_player) for i in range(3)):
            return True

    if all(has_sub_board_winner(i, i, current_player) for i in range(3)):
        return True
    if all(has_sub_board_winner(i, 2-i, current_player) for i in range(3)):
        return True
    return False

def has_sub_board_winner(row, col, player):
    # First check if the board is complete
    if not is_sub_board_complete(row, col):
        return False
    # Then check if the center button has the player's symbol
    frame = ultimate_frame.grid_slaves(row=row+1, column=col)[0]
    center_button = frame.grid_slaves(row=1, column=1)[0]
    return center_button["text"] == player


def disable_all_boards():
    # Disable all buttons in all sub-boards
    reset_board_colors()
    for row in range(3):
        for col in range(3):
            frame = ultimate_frame.grid_slaves(row=row+1, column=col)[0]
            for button in frame.winfo_children():
                if isinstance(button, tk.Button):
                    button.config(state="disabled")


def is_sub_board_complete(row, col):
    #Check if a sub-board is won or drawn
    frame = ultimate_frame.grid_slaves(row=row+1, column=col)[0]
    center_button = frame.grid_slaves(row=1, column=1)[0]
    
    # If the center button is black, the board is won
    if center_button.cget('background') == ("black"):
        return True
        
    # If all buttons are filled, the board is drawn
    buttons = [widget for widget in frame.winfo_children() if isinstance(widget, tk.Button)]
    return all(button["text"] != "" for button in buttons)

def highlight_active_board(row, col):
    #Highlight the active board in yellow
    frame = ultimate_frame.grid_slaves(row=row+1, column=col)[0]
    frame.configure(bg="yellow")

def reset_board_colors():
    #Reset all board backgrounds to darkgray
    for row in range(3):
        for col in range(3):
            frame = ultimate_frame.grid_slaves(row=row+1, column=col)[0]
            frame.configure(bg="darkgray")


def update_turn_label():
    #Update the turn label and highlight active board
    reset_board_colors()  
    if next_sub_board_row is not None and next_sub_board_col is not None:
        label.config(text=f"{current_player}'s Turn - Must play in board ({next_sub_board_row+1}, {next_sub_board_col+1})")
        highlight_active_board(next_sub_board_row, next_sub_board_col)
    else:
        label.config(text=f"{current_player}'s Turn - Free Choice")




# Main Game Variables
player_x = "X"
player_o = "O"
current_player = player_x

# Variables to track the next sub-board to play in
next_sub_board_row = None  
next_sub_board_col = None  



# GUI Setup
game_board = tk.Tk()
game_board.title("Xtreme Tic Tac Toe")
game_board.geometry("700x750")
game_board.resizable(False, False)
game_board.configure(bg="lightblue")

# Create the ultimate frame
ultimate_frame = tk.Frame(game_board)

# Create sub-boards and buttons
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