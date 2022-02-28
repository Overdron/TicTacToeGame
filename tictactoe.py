from tkinter import *
from tkinter import messagebox
import time
import numpy as np


class Game:
    __instance = None

    @staticmethod
    def inst(player2=None):
        if Game.__instance == None:
            Game.__instance = Game(player2)
        return Game.__instance
    
    def __init__(self, player2=None):
        print('init called')
        self.__tk = Tk()
        self.__app_running = True
        self.__size_canvas_x = 512
        self.__size_canvas_y = 512

        self.__tk.protocol("WM_DELETE_WINDOW", self.__on_closing)
        self.__tk.title("TicTacToe game")
        self.__tk.resizable(0, 0)
        self.__tk.wm_attributes("-topmost", 1)
        self.__canvas = Canvas(self.__tk, width=self.__size_canvas_x, height=self.__size_canvas_y, bd=0, highlightthickness=0)
        self.__canvas.create_rectangle(0, 0, self.__size_canvas_x, self.__size_canvas_y, fill="white")
        self.__canvas.pack()
        self.__tk.update()

        self.__s_x = 3
        self.__s_y = self.__s_x
        self.__step_x = self.__size_canvas_x // self.__s_x
        self.__step_y = self.__size_canvas_y // self.__s_y

        self.__draw_table()
        self.__reinit_table()
        self.__canvas.bind_all("<Button-1>", self.__make_turn)  # ЛКМ
        self.__canvas.bind_all("<space>", self.__restart)  # Пробел

        self.player2 = player2  # AI player / red played
        self.winner = -1  # -1 - game is in progress, 0 - blue won, 1 - red won, 2 - draw
        self.whose_turn = 0  # player1 / blue player does first step
        self.episode_counter = 0
        self.episodes_score = np.array([])

    def __draw_table(self):
        for i in range(0, self.__s_x + 1):
            self.__canvas.create_line(0, i * self.__step_y, self.__size_canvas_x, i * self.__step_y)
        for i in range(0, self.__s_y + 1):
            self.__canvas.create_line(i * self.__step_y, 0, i * self.__step_y, self.__size_canvas_y)

    def __on_closing(self):
        """closing window"""
        if messagebox.askokcancel("Exit", "Exit game?"):
            self.__app_running = False
            self.__tk.destroy()

    def __reinit_table(self):
        self.grid = np.array([-1 for _ in range(self.__s_x * self.__s_y)])
        self.__list_ids = []
        self.turn_counter = 0
        self.winner = -1

    def __block_table(self):
        """make whole board unavailable. only way to continue is by pressing keyboard space button"""
        self.grid = [10 for i in range(self.__s_x * self.__s_y)]

    def play(self):
        """main loop of the game. Ends only on window closing"""
        while self.__app_running:
            self.whose_turn = self.__decide_whose_turn()
            # step into when AI is moving, otherwise wait for player1 action
            if self.player2 is not None and self.whose_turn == 1:
                point = self.player2.policy(self)  # AI's decision how to turn
                self.__make_turn(point)
            self.__tk.update_idletasks()
            self.__tk.update()
            time.sleep(0.01)

    def __make_turn(self, event):
        """main action method"""
        if isinstance(event, Event):
            cell_idx = self.__event_to_cell_index(event)  # if event is mouse1 click
        else:
            cell_idx = event  # if event is cell, chosen by ai_player
        try:
            # make turn if there are available cells
            if self.grid[cell_idx] == -1:
                self.grid[cell_idx] = self.whose_turn  # write player_id in cell
                self.__draw_symbol(cell_idx, self.whose_turn)
                # check winner
                if self.__check_winner(self.grid, self.whose_turn):
                    self.__block_table()  # block grid
                    self.episode_counter += 1 # collect statistics
                    self.episodes_score = np.append(self.episodes_score, self.winner) # collect statistics
                    self.__winning_window(self.winner)
                self.turn_counter += 1
        except IndexError:  # in case of clicking out of bounds
            pass
        except TypeError:  # in case of no empty cells
            pass

    def __draw_symbol(self, cell_id, type):
        color = 'blue' if type == 0 else 'red'
        symbol = 'X' if type == 0 else 'O'
        row = cell_id // self.__s_x
        col = cell_id % self.__s_y
        symbol_id = self.__canvas.create_text(col * self.__step_x + self.__step_x / 2, row * self.__step_y + self.__step_y / 2,
                                            text=symbol,
                                            fill=color, font="Verdana 100")
        self.__list_ids.append(symbol_id)

    def simulate_move(self, cell_idx, whose_turn):
        """isolated way to evaluate next turn for minmax algorithm"""
        if self.grid[cell_idx] == -1:  # check if it is blank
            self.grid[cell_idx] = whose_turn
            if self.__check_winner(self.grid, whose_turn):
                self.winner = whose_turn
            return True
        return False

    def __event_to_cell_index(self, event):
        """Obtain cell id from mouse click"""
        raw_idx = event.y // self.__step_y
        col_idx = event.x // self.__step_x
        cell_idx = 3 * raw_idx + col_idx
        return cell_idx

    def __decide_whose_turn(self):
        """odd turn for X (blue), even for O (red)"""
        return 1 if self.turn_counter % 2 > 0 else 0

    def __restart(self, event):
        """reinit table and delete current symbols"""
        for i in self.__list_ids:
            self.__canvas.delete(i)
        self.__reinit_table()

    def __check_winner(self, grid, player):
        """check if there is a winner or a draw"""
        if grid[0] == grid[1] == grid[2] == player:  # 1 row
            self.winner = player
            return True
        if grid[3] == grid[4] == grid[5] == player:  # 2 row
            self.winner = player
            return True
        if grid[6] == grid[7] == grid[8] == player:  # 3 row
            self.winner = player
            return True

        if grid[0] == grid[3] == grid[6] == player:  # 1 col
            self.winner = player
            return True
        if grid[1] == grid[4] == grid[7] == player:  # 2 col
            self.winner = player
            return True
        if grid[2] == grid[5] == grid[8] == player:  # 3 col
            self.winner = player
            return True

        if grid[0] == grid[4] == grid[8] == player:  # 1 diagonal
            self.winner = player
            return True
        if grid[2] == grid[4] == grid[6] == player:  # 2 diagonal
            self.winner = player
            return True

        _, num_available = self.determine_available_cells()
        if num_available == 0:
            self.winner = 2
            return True

        self.winner = -1
        return False

    def __winning_window(self, winner):
        label_text = f'{"Blue player won!" if winner == 0 else "Red player won!" if winner == 1 else "Draw!"}'
        message_text = f"""
        Press space to restart
        episodes played: {self.episode_counter}
        blue won times: {sum(self.episodes_score == 0)}
        red won times: {sum(self.episodes_score == 1)}
        draws: {sum(self.episodes_score == 2)}"""
        win = Tk()
        win.geometry("300x200")
        win.title('GameResult')
        win.wm_attributes("-topmost", 1)
        w = Label(win, text=label_text, font="90", fg="Navy")
        w.pack()
        msg = Message(win, text=message_text, font="90")
        msg.pack()

    def determine_available_cells(self):
        available_indices = np.where(self.grid == -1)[0]
        num_available = available_indices.shape[0]
        return available_indices, num_available
