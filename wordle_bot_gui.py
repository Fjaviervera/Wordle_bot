import tkinter as tk
from tkinter import messagebox
import tkinter.font as font
from time import sleep
from wordle_solver import WorldeSolver
import scraper_wordle
from utils import create_dicc_words
import webbrowser

# pyinstaller --specpath ./build --workpath ./build/build --distpath ./build/dist --onefile  --add-binary "../chromedriver_win32/chromedriver.exe;chromedriver_win32" --collect-data selenium  --add-data "../palabras_5_letras.txt;." --noconsole wordle_bot_gui.py

root= tk.Tk()
root.title("Wordle Bot")
canvas = tk.Canvas(root, width =400, height = 250)
canvas.pack()
browser = None
roboto = font.Font(family='Roboto')

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
    dicc_wordle = create_dicc_words()
    solver_wordler = WorldeSolver(dicc_wordle)

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
        dicc_wordle = create_dicc_words(avoid_letters=["ñ"], avoid_words=[
                                        "zungo", "vinto", "depto", "putre", "tunja", "tupac","jordi"])
        

        solver_wordler = WorldeSolver(dicc_wordle)

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

   
tittle = tk.Label(text="WORDLE BOT",font='Roboto 26 bold',fg="#53a4c2")
    
button_daily = tk.Button(text='Jugar Wordle Diario', command=play_daily,font=roboto)
button_custom = tk.Button(text='Jugar Wordle Personalizado', command=popup_custom,font=roboto)


canvas.create_window( 200, 70, window=tittle)
canvas.create_window(200, 140, window=button_daily)
canvas.create_window(200, 200, window=button_custom)

root.eval('tk::PlaceWindow . center')
root.protocol("WM_DELETE_WINDOW",  on_close)
root.mainloop()

