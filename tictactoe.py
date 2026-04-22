import tkinter as tk
import math

# ------------------ GAME STATE ------------------ #
board = [" " for _ in range(9)]
buttons = []

# ------------------ LOGIC ------------------ #
def check_winner(b, player):
    win = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    return any(all(b[i] == player for i in combo) for combo in win)

def is_draw(b):
    return " " not in b

def minimax(b, is_max):
    if check_winner(b, "O"):
        return 1
    if check_winner(b, "X"):
        return -1
    if is_draw(b):
        return 0

    if is_max:
        best = -math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = "O"
                score = minimax(b, False)
                b[i] = " "
                best = max(best, score)
        return best
    else:
        best = math.inf
        for i in range(9):
            if b[i] == " ":
                b[i] = "X"
                score = minimax(b, True)
                b[i] = " "
                best = min(best, score)
        return best

def best_move():
    best_score = -math.inf
    move = -1
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    return move

# ------------------ UI ACTIONS ------------------ #
def on_click(i):
    if board[i] != " ":
        return

    # Player move
    board[i] = "X"
    buttons[i].config(text="X", state="disabled")

    if check_winner(board, "X"):
        status_label.config(text="You Win! 🎉")
        disable_all()
        return

    if is_draw(board):
        status_label.config(text="Draw!")
        return

    # AI move
    ai = best_move()
    board[ai] = "O"
    buttons[ai].config(text="O", state="disabled")

    if check_winner(board, "O"):
        status_label.config(text="AI Wins! 🤖")
        disable_all()
        return

    if is_draw(board):
        status_label.config(text="Draw!")

def disable_all():
    for btn in buttons:
        btn.config(state="disabled")

def reset_game():
    global board
    board = [" " for _ in range(9)]
    for btn in buttons:
        btn.config(text="", state="normal")
    status_label.config(text="Your Turn (X)")

# ------------------ UI SETUP ------------------ #
root = tk.Tk()
root.title("Tic-Tac-Toe AI")

frame = tk.Frame(root)
frame.pack()

for i in range(9):
    btn = tk.Button(frame, text="", font=("Arial", 20), width=5, height=2,
                    command=lambda i=i: on_click(i))
    btn.grid(row=i//3, column=i%3)
    buttons.append(btn)

status_label = tk.Label(root, text="Your Turn (X)", font=("Arial", 14))
status_label.pack()

reset_btn = tk.Button(root, text="Restart", command=reset_game)
reset_btn.pack()

root.mainloop()
