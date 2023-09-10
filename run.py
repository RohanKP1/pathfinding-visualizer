from customtkinter import *
from script import main_program

def main():
    window = CTk()
    window.title("PAV Runner")
    window.configure(bg="#1E1E1E")
    window.geometry("240x200") 
    window.resizable(0,0)

    choice = StringVar()
    combobox = CTkComboBox(window,values=["DFS Algorithm", "Dijkstra Algorithm", "A* Algorithm"],variable=choice,state="readonly")
    combobox.set("A* Algorithm")
    combobox.grid(row=0, column=0,padx=(50,50),pady=(50,10))

    def runner():
        choice_str = choice.get()
        if choice_str == "DFS Algorithm":
            main_program(0)
        elif choice_str == "Dijkstra Algorithm":
            main_program(1)
        elif choice_str == "A* Algorithm":
            main_program(2)        

    CTkButton(window,font = ('calibri', 12, 'bold'),text="Submit",command = runner).grid(row=2,column=0,padx=(50,50),pady=(10,50))

    window.mainloop()

if __name__ == "__main__":
    main()    