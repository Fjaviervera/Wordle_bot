import tkinter as tk
from tkinter import messagebox
import tkinter.font as font
from time import sleep
from wordle_solver import WordleSolver
import scraper_wordle
from utils import create_words_list_from_txt
import webbrowser


def on_close():

     close = messagebox.askokcancel("Cerrar", "¿Cerrar Wordle Bot?")
     if close:
        if browser is not None:
            browser.quit()
        root.destroy()




def mywordle_callback(url):
    webbrowser.open_new(url)


def play_daily():
    print("running daily")
    global browser
    if browser is not None:
        browser.quit()
    
    browser = scraper_wordle.open_game("https://wordle.danielfrg.com/")
    sleep(0.5)
    scraper_wordle.start(browser)
    sleep(0.5)
    words_wordle= create_words_list_from_txt("palabras_5_letras.txt")
    solver_wordler = WordleSolver(words_wordle, parallel_sim=False)

    for _ in range(6):


        game_state = scraper_wordle.read_game_daily(browser)

        if solver_wordler.check_correct_word(game_state):
            break

        word = solver_wordler.guess_word(game_state, debug=True)


        scraper_wordle.send_word_using_screen_board(word, browser)



def play_custom(entry):
    global browser
    if browser is not None:
        browser.quit()
    print("running custom")

    if "mywordle.strivemath.com/?word=" not in entry.get() or "&lang=sp" not in entry.get():

        
        messagebox.showerror("Link erroneo", "Copia el link de un juego de mywordle.strivemath.com en castellano")

    else:

        
        browser = scraper_wordle.open_game(entry.get())
        sleep(0.5)

        words_list = create_words_list_from_txt("palabras_5_letras.txt",avoid_letters = ["ñ"],avoid_words = ["zungo", "vinto", "depto", "putre", "tunja", "tupac","gomez","hazte","gafez"])

        solver_wordler = WordleSolver(words_list,parallel_sim=False)

        for _ in range(6):

            
            game_state = scraper_wordle.read_game_custom(browser)


            if solver_wordler.check_correct_word(game_state):
                break

            word = solver_wordler.guess_word(game_state, debug=True)

            
            scraper_wordle.send_word(word, browser)
            sleep(0.1)


def insert_val(e):
    e.delete(0,"end")
    e.insert(0, root.clipboard_get())
    
def popup_custom():

   roboto = font.Font(family='Roboto')
   top= tk.Toplevel(canvas)

   x =root.winfo_x()
   y = root.winfo_y()
   top.geometry("+%d+%d" %(x,y+50))
   top.geometry("400x150")

   entry= tk.Entry(top, width= 100,font=roboto)
   entry.pack()


   tk.Button(top,text= "Pegar", command= lambda:insert_val(entry),font=roboto).pack(pady= 5,side=tk.TOP)
   
   button= tk.Button(top, text="Jugar", command=lambda:play_custom(entry),font=roboto)
   button.pack(pady=5, side= tk.TOP)


   link = tk.Label(top, text="mywordle.strivemath.com", fg="blue", cursor="hand2",font=roboto)
   link.pack(pady=5,side= tk.BOTTOM)
   link.bind("<Button-1>", lambda e: mywordle_callback("https://mywordle.strivemath.com/"))

   


if __name__ == '__main__':

    root= tk.Tk()
    root.title("Wordle Bot")
    canvas = tk.Canvas(root, width =400, height = 250)
    canvas.pack()
    browser = None

    tittle = tk.Label(text="WORDLE BOT",font='Roboto 26 bold',fg="#53a4c2")
    roboto = font.Font(family='Roboto')
    button_daily = tk.Button(text='Jugar Wordle Diario', command=play_daily,font=roboto)
    button_custom = tk.Button(text='Jugar Wordle Personalizado', command=popup_custom,font=roboto)

    canvas.create_window( 200, 70, window=tittle)
    canvas.create_window(200, 140, window=button_daily)
    canvas.create_window(200, 200, window=button_custom)

    root.eval('tk::PlaceWindow . center')
    root.protocol("WM_DELETE_WINDOW",  on_close)
    root.mainloop()

