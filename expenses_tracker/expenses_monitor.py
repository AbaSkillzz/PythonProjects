from os import write
from PySimpleGUI.PySimpleGUI import WIN_CLOSED
import matplotlib.pyplot as plt
import numpy as np
import csv
import PySimpleGUI as sg
import os


#FUNCTIONS
def add_expense():
    layout =[[sg.Text("Fill each input to save a new expense.", text_color="red", font=("Arial", 14))],
             [sg.Text("(Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec)")],
             [sg.Text("Month(write it like above)"),sg.Input(pad=(20,0), size=(60,10), key="month")],
             [sg.HorizontalSeparator(color="black", pad=(None, 10))],
             [sg.Text("(Health, Personal, Useless, Investments)")],
             [sg.Text("Category(write it like above)"), sg.Input(size=(50,10), key="category")],
             [sg.Text("Expense",pad=(55,None)), sg.Input(pad=(15,None), size=(90,10), key="expense")],
             [sg.Button("Add Expense"), sg.Text("Click Done to return to the main interface.",font=("Arial", 8),text_color="yellow",pad=(10,None)), sg.Button("Done")] ]

    window = sg.Window(title="Expenses Tracker", layout=layout, size=(450, 260))
    while True:
        event, value = window.read()
        
        if (event == WIN_CLOSED) or (event == "Done"):
            window.close()
            break

        elif event == "Add Expense":
            adding_permission = True

            months_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            month = value["month"]
            if not month in months_list:
                adding_permission = False
                sg.popup_error("MONTH NOT IN LIST, CHANGE IT!")

            category_list = ["Health", "Personal", "Useless", "Investments"]
            category = value["category"]
            if not category in category_list:
                adding_permission = False
                sg.popup_error("CATEGORY NOT IN LIST, CHANGE IT!")

            expense = value["expense"]
            if not expense.isdigit():
                adding_permission = False
                sg.popup_error("CANNOT HAVE AN EXPENSE THAT IS NOT A NUMBER! WRITE A NUMBER.")

            if adding_permission:
                try:
                    with open(path_to_csv, "a") as csv_file:
                        fieldnames = ["month","category","expense"]
                        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                        
                        new_line = {
                            "month": month,
                            "category": category,
                            "expense": expense
                        }
                        writer.writerow(new_line)
                        print("SUCCESSFULLY ADDED NEW EXPENSE!")

                except Exception as err:
                    print(err)
            
def show_graph():
    #initialize graph
    x = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"] 
    health_y = np.zeros(12)
    personal_y = np.zeros(12)
    useless_y = np.zeros(12)
    investments_y = np.zeros(12)

    #processing available data
    with open(path_to_csv, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for line in csv_reader:
            month_position = x.index(str(line["month"]))  #getting the month(month index in x) at every loop

            #sorting by each category
            if line["category"] == "Health":
                health_y[month_position] = float(line["expense"])
            
            elif line["category"] == "Personal":
                personal_y[month_position] = float(line["expense"])
            
            elif line["category"] == "Useless":
                useless_y[month_position] = float(line["expense"])
            
            elif line["category"] == "Investments":
                investments_y[month_position] = float(line["expense"])

    #output the total expenses of each category
    total_health = 0
    total_personal = 0
    total_useless = 0
    total_investments = 0
    for val in health_y:
        total_health += val
    for val in personal_y:
        total_personal += val
    for val in useless_y:
        total_useless += val
    for val in investments_y:
        total_investments += val
    print(f"Total spent money in:\nHealth: {total_health}\nPersonal: {total_personal}\nUseless: {total_useless}\nInvestments: {total_investments}")
    print(f"Total spent money in the year: {total_health + total_personal + total_useless + total_investments}")

    #create and store graph with latest data
    plt.plot(x, health_y, marker="o", color="blue", label="health")
    plt.plot(x, personal_y, marker="o", color="violet", label="personal")
    plt.plot(x, useless_y, marker="o", color="red", label="useless")
    plt.plot(x, investments_y, marker="o", color="green", label="investments")

    plt.xlabel("Timeline")
    plt.ylabel("Spent Money")
    plt.legend()
    plt.grid()
    plt.tight_layout()

    plt.savefig("last_plot.png", dpi=72)
    plt.show()

def month_expenses(month):
    x = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"] 
    if not month in x:
        return("MONTH NOT IN THE MONTH LIST!")
    total = 0
    with open(path_to_csv, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for line in csv_reader:
            if line["month"] == month:
                category = line["category"]
                expense = line["expense"]
                total += float(line["expense"])
                print(f"Category: {category} | Expense: {expense}")
        return f"Total expenses for this month: {total}"

def category_expenses(category):
    category_list = ["Health", "Personal", "Useless", "Investments"]
    if not category in category_list:
        return("CATEGORY NOT IN THE CATEGORY LIST!")
    total = 0
    with open(path_to_csv, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for line in csv_reader:
            if line["category"] == category:
                total += float(line["expense"])
        return f"Total expenses for this category: {total}"

#USER INTERFACE
path_to_csv = str(input("INSERT THE PATH TO A CSV FILE TO LET THIS PROGRAM TO STORE DATA FOR YOUR EXPENSES TRACKER(INSERT AS HEADER: month,category,expense)\n>>> "))
if os.path.isfile(path_to_csv):
    try:
        print('Write "h" to list all available commands\nWrite "q" to quit the program\nWrite "a" to add expenses of derterminated months\nWrite "s" to get a graph of given(current available) expenses\nWrite "i" to get the info of expenses of a month or a certain category' )
        while True:
            user_inp = str(input("\nWhat do you want to do?\n>>> "))
            if user_inp == "q":
                print("QUITTING.")
                break

            elif user_inp == "h":
                print('Write "h" to list all available commands\nWrite "q" to quit the program\nWrite "a" to add expenses of derterminated months\nWrite "s" to get a graph of given(current available) expenses\nWrite "i" to get the info of expenses of a year, month or of a certain category' )
            
            elif user_inp == "a":
                print("REMEMBER: If you add a new expense on a month that already has an expense in a certain category, the new value will replace the old value!")
                add_expense()
            
            elif user_inp == "s":
                print("SHOWING EXPENSES GRAPH WITH THE LATEST GIVEN VALUES, THE GRAPH WILL BE STORED AS A .png FILE IN THE CURRENT DIRECTORY")
                print(show_graph())
            
            elif user_inp == "i":
                info_of = str(input('You can get expenses informations about a "month" or a "category"\n>>> '))
                if info_of == "month":
                    print("(Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec)")
                    month = str(input("Insert the month you want to know about(write it like above)\n>>> "))
                    print(month_expenses(month))
                elif info_of == "category":
                    print("(Health, Personal, Useless, Investments)")
                    category = str(input("Choose one of the category(write it like above)\n>>> "))
                    print(category_expenses(category))
                else:
                    print("YOU MUST CHOOSE TO GET EXPENSES INFORMATION ABOUT A MONTH OR A CATEGORY!")
            
            else:
                print("INVALID INPUT!")

    except Exception as err:
        print(err)

else:
    print("ERROR WITH THE GIVEN FILE! MAKE SURE TO GIVE AS INPUT A VALID CSV FILE!")
