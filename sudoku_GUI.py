import tkinter as tk
from turtle import bgcolor
from pygame import mixer
from sudoku_grid_generator import gen_sudoku
import random

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry('350x400')
        self.title('Pydoku')
        #self.iconbitmap('./imgs/sudoku_icon.ico')    
        self.start_page = StartPage(self, self)
        self.start_page.pack()
        
        mixer.init()
        #mixer.music.load('music.mp3')
        #mixer.music.play()
        mixer.music.set_volume(0.3)
        

class StartPage(tk.Frame):
    def __init__(self, container, master):
        tk.Frame.__init__(self, container)

        play = tk.Frame(self, pady=20)
        play.pack()
        play_btn = tk.Button(play, text = 'Let\'s play!', command = lambda: self.start_sudoku(master))
        play_btn.pack()
        
        levels = tk.Frame(self, pady = 10)
        levels.pack()
        
        select_msg = tk.Label(levels, text = 'Select a level')
        select_msg.grid(row= 0, column = 1)
        
        self.level_selected = tk.StringVar(master, 'intermediate')
        
        easy = tk.Radiobutton (levels, text = 'Easy', variable = self.level_selected, \
                                value = 'easy', indicator = 0)
        easy.grid(row = 2, column = 0)
        intermediate = tk.Radiobutton (levels, text = 'Intermediate', variable = self.level_selected,\
                                        value = 'intermediate', indicator = 0)
        intermediate.grid(row = 2, column = 1)
        hard = tk.Radiobutton (levels, text = 'Hard', variable = self.level_selected, \
                                value = 'hard', indicator = 0)
        hard.grid(row = 2, column = 2)       
        
        options = tk.Frame(self, pady = 10)
        options.pack()
        options_msg = tk.Label(options, text = 'Options')
        options_msg.pack()
        
        self.help_state = tk.IntVar()
        help_option = tk.Checkbutton(options, text = 'Play with help', variable = self.help_state)
        help_option.select()
        help_option.pack(side = 'right')

        self.music_state = tk.IntVar()
        music_option = tk.Checkbutton(options, text = 'Music', variable = self.music_state, \
                                    command = lambda: self.on_off_music(self.music_state.get()))
        music_option.select()  
        music_option.pack(side = 'left')

    def on_off_music(self, value):
        if value == 1:
            mixer.music.unpause()
            mixer.music.set_volume(0.3)
        else:
            mixer.music.pause()

    def start_sudoku(self, master):
        sudoku_game = PlaySudoku(master, master)
        self.pack_forget()
        sudoku_game.pack()

class PlaySudoku(tk.Frame):
    def __init__(self, container, master):
        tk.Frame.__init__(self, container)
        self.master = master
        # header = tk.Frame(self)
        # header.pack()

        sudoku_frame = tk.Frame(self)
        sudoku_frame.pack()
        sudoku_grid = gen_sudoku()
        taken_away = self.transform_grid(sudoku_grid, master.start_page.level_selected)
        cells = {}

        buttons_area = tk.Frame(self)
        buttons_area.pack()

        if master.start_page.help_state.get() == 1:
            btn_help = tk.Button(buttons_area, width = 10, text = 'Get help', command = \
                                lambda: self.get_help(taken_away, cells, sudoku_frame))
            btn_help.pack()
        btn_menu = tk.Button(buttons_area, width = 10, text = 'Main menu', command = \
                            self.back_menu)
        btn_menu.pack()

        self.errors_area = tk.Frame(self)
        self.errors_area.pack()

        self.reg = master.register(self.validate_number)

        self.draw_9x9_grid(sudoku_frame, sudoku_grid, master, cells)


    def back_menu(self):
        self.master.start_page.pack()
        self.destroy()

    def get_help(self, taken_away, cells, frame):      
        rand_cell = random.choice(list(taken_away))
        row = rand_cell[0]
        column = rand_cell[1]
        bg_color = cells[rand_cell]['bg']
        num = str(taken_away[rand_cell])
        cells[rand_cell].destroy()  
        cell = tk.Label(frame, text = num, \
                        width = 4, bg = bg_color, justify = 'center', \
                        borderwidth = 1, relief = 'groove')
        cell.grid(row = row, column = column, sticky = 'nsew', ipady = 5)
        cells[rand_cell] = cell

    def transform_grid(self, grid, level):
        possible_cells = []
        for row in range(9):
            for col in range(9):
                possible_cells.append((row, col))
        if level == 'easy':
            take_away = 40
        elif level == 'intermediate':
            take_away = 45    
        else:
            take_away = 50
        taken_away = {}
        for i in range(take_away):        
            row_col = random.choice(possible_cells)
            row = row_col[0]
            col = row_col[1]
            taken_away[row_col] = grid[row][col]
            grid[row][col] = 0
            possible_cells.remove(row_col)
        return taken_away

    def validate_number(self, char):
        out = (char.isdigit() or char == '') and len(char) <= 1
        if out == False:
            error_entry_msg = tk.Label(self.errors_area, text = 'Enter one number', fg = 'red')
            error_entry_msg.pack()
            self.master.after(1000, self.destroy_widget, error_entry_msg)
        return out

    def destroy_widget(self, widget):
        widget.destroy()

    def draw_3x3_grid(self, row, column, bg_color, frame, grid, master, cells):
        for ri in range(3):
            for ci in range(3):
                if grid[row + ri][column + ci] == 0:
                    e = tk.Entry(frame, width = 5, bg = bg_color, justify = 'center',\
                                validate = 'key', validatecommand = (self.reg, '%P'),
                                borderwidth = 1, relief = 'groove')
                    e.grid(row = row + ri, column = column + ci, sticky = 'nsew', ipady = 5)
                    cells[(row + ri, column + ci)] = e
                else:
                    cell = tk.Label(frame, text = str(grid[row + ri][column + ci]), \
                                    width = 4, bg = bg_color, justify = 'center', \
                                    borderwidth = 1, relief = 'groove')
                    cell.grid(row = row + ri, column = column + ci, sticky = 'nsew', ipady = 5)
                    cells[(row + ri, column + ci)] = cell

    def draw_9x9_grid(self, frame, grid, master, cells):
        color = '#D4D4D4'
        for row in range(0, 9, 3):
            for column in range(0, 9, 3):
                self.draw_3x3_grid(row, column, color, frame, grid, master, cells)
                if color == '#D4D4D4':
                    color = '#FFFFFF'
                else:
                    color = '#D4D4D4'

app = App()  
app.mainloop()


# btn_clear = tk.Button(buttons_area, command = lambda: self.clear_grid(cells),
#                             text = 'Clear grid', width = 10)
#         btn_clear.pack()

    # def clear_grid(self, cells):
    #     for row in range(0, 9):
    #         for column in range(0, 9):
    #             cell = cells[(row, column)]
    #             if type(cell) == tk.Entry:
    #                 cell.delete(0)  