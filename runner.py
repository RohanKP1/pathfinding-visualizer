from customtkinter import *
from script import main_code

def main():
    window = CTk()
    window.title("Pathfinder Algorithm Visualizer")
    window.configure(bg="#242424")
    window.geometry("420x260") 
    window.resizable(0,0)

    label1 = CTkLabel(window, text="Pathfinder Algorithm", fg_color="transparent", font=("calibri", 15), text_color="#00FF89")
    label1.place(relx=0.5, rely=0.15, anchor=CENTER)

    choice = StringVar()
    combobox1 = CTkComboBox(window,values=["DFS Algorithm", "Dijkstra Algorithm", "A* Algorithm"],variable=choice,state="readonly", command=lambda e:print(e), button_color="#00FF89")
    combobox1.set("A* Algorithm")
    combobox1.place(relx=0.5, rely=0.30, anchor=CENTER)

    label2 = CTkLabel(window, text="Maze Algorithm", fg_color="transparent", font=("calibri", 15), text_color="#FF0099")
    label2.place(relx=0.5, rely=0.50, anchor=CENTER)

    mazeChoice = StringVar()
    combobox2 = CTkComboBox(window,values=["Empty Canvas", "DFS Algorithm", "Kruskal's algorithm", "Wilson's algorithm"],variable=mazeChoice,state="readonly", command=lambda e:print(e), button_color="#FF0099")
    combobox2.set("Empty Canvas")
    combobox2.place(relx=0.5, rely=0.65, anchor=CENTER)

    pfDict = {"DFS Algorithm":0, "Dijkstra Algorithm":1, "A* Algorithm":2}
    mazeDict = {"Empty Canvas":0, "DFS Algorithm":1, "Kruskal's algorithm":2, "Wilson's algorithm":3}
    def runner():
        main_code.main_program(pfDict.get(choice.get()),mazeDict.get(mazeChoice.get()))       
        # print(choice.get(), mazeChoice.get())
    CTkButton(window,font = ('calibri', 12, 'bold'),text="Submit",command = runner).place(relx=0.5, rely=0.85, anchor=CENTER)

    window.mainloop()

if __name__ == "__main__":
    main()    