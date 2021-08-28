import tkinter as tk
import random
import time


win=tk.Tk()
win.title("RockPaperScissors")
win.geometry("300x200")

choices=["ROCK", "PAPER", "SCISSORS"]

def close_window():
    win.destroy()   #closes the window
    print("You quitted the game")

button_quit=tk.Button(text="QUIT", bg="red", command=close_window)
button_quit.grid(row=3, column=2)

#ROCK
def rock():
    computer_choice_rock = random.choice(choices)

    print("Your choice is: "+"ROCK")
    print("Computer's choice is: " + computer_choice_rock)
    if(computer_choice_rock=="PAPER"):
        print("YOU LOSS")
    elif(computer_choice_rock=="SCISSORS"):
        print("YOU WON")
    elif(computer_choice_rock=="ROCK"):
        print("DRAW")
    
    def goAhead():  
        time.sleep(0.5)
        win.withdraw() #closes the main window

        computer_choice_rock=random.choice(choices)#changes the "choice" of computer
        win.deiconify() #re-opens the window

        print("Your choice is: "+ "ROCK")
        print("Computer's choice is"+ computer_choice_rock)

        if(computer_choice_rock == "SCISSORS"):
            print("YOU WON")
        elif(computer_choice_rock == "ROCK"):
            print("DRAW")
        elif(computer_choice_rock == "PAPER"):
            print("YOU LOSS")   
        
    win2 = tk.Toplevel(win)
    win2.geometry("100x40")

    btn_continue = tk.Button(win2, text="continue", bg="green", command=goAhead)#se nn metto questo mi da 2 giocate
    btn_continue.grid(row=0, column=0)

    win2.destroy()

btn_rock = tk.Button(text="ROCK", bg="grey", width="10", height="2", command=rock)
btn_rock.grid(row=1, column=1)

#PAPER
def paper():
    computer_choice_paper = random.choice(choices)

    print("Your choice is: "+"PAPER")
    print("Computer's choice is: "+ computer_choice_paper)

    if(computer_choice_paper=="SCISSORS"):
        print("YOU LOSS")
    elif(computer_choice_paper=="ROCK"):
        print("YOU WON")
    elif(computer_choice_paper=="PAPER"):
        print("DRAW")

    def goAhead():
        time.sleep(0.5)
        win.withdraw() #closes the window 
        computer_choice_paper=random.choice(choices)
        win.deiconify() #re_opens the window

        print("Your choice is: PAPER")
        print("Computer's choice is: " + computer_choice_paper)

        if(computer_choice_paper=="PAPER"):
            print("DRAW")
        elif(computer_choice_paper=="SCISSORS"):
            print("YOU LOSS")
        elif(computer_choice_paper=="ROCK"):
            print("YOU WON")

        win2 = tk.Toplevel(win)
        win2.geometry("100x40")

        btn_continue=tk.Button(win2, text="continue", bg="green", command=goAhead)
        btn_continue.grid(row=0, column=0)

        win2.destroy()

btn_paper = tk.Button(text="PAPER", bg="white", width="10", height="2", command=paper)
btn_paper.grid(row=1, column=2)

#SCISSORS
def scissors():
    computer_choice_scissors = random.choice(choices)
    print("Your choice is: "+"SCISSORS")
    print("Computer's choice is: "+ computer_choice_scissors)
    if(computer_choice_scissors=="ROCK"):
        print("YOU LOSS")
    elif(computer_choice_scissors=="PAPER"):
        print("YOU WON")
    elif(computer_choice_scissors=="SCISSORS"):
        print("DRAW")
    
    def goAhead():
        time.sleep(0.5)
        win.withdraw() #closes the window 
        computer_choice_scissors=random.choice(choices)
        win.deiconify() #re-opens the window

        print("Your choice is: SCISSORS")
        print("Computer's choice is: "+ computer_choice_scissors)

        if(computer_choice_scissors=="SCISSORS"):
            print("DRAW")
        elif(computer_choice_scissors=="ROCK"):
            print("YOU LOSS")
        elif(computer_choice_scissors=="PAPER"):
            print("YOU WON")

        win2 = tk.Toplevel(win)
        win2.geometry("100x40")

        btn_continue=tk.Button(win2, text="continue", bg="green", command=goAhead)
        btn_continue.grid(row=0, column=0)

        win2.destroy() #don't shows the second window(win2)

btn_scissors = tk.Button(text="SCISSORS", bg="yellow", width="10", height="2", command=scissors)
btn_scissors.grid(row=1, column=3)


win.mainloop()

