from tkinter import Tk, Toplevel, messagebox

class Menu(Tk):

    def __init__(self, root):
        self.root = root
        self.root.title('Menu')
        self.root.geometry('300x300')
        self.openWindows = []
        self.initButtons()
        self.breeds_Window = None
        self.breeds_Window = None

    def initButtons(self):

        from tkinter import Button

        self.breeds = Button(self.root, text='Breeds', command=self.open_breeds)
        self.breeds.pack()

        self.breed_finder = Button(self.root, text='Breed Finder', command=self.open_breed_finder)
        self.breed_finder.pack()

        self.debug = Button(self.root, text='Debug', command=self.debug)
        self.debug.pack()

    def open_breeds(self):
        if self.breeds_Window in self.openWindows:
            messagebox.showinfo("Warning", "You already have a breeds window open. Please close it first.")
            print(self.breeds_Window)
            return
        
        print(self.breeds_Window)
        
        self.breeds_Window: Breeds_Window = Breeds_Window(Toplevel(self.root))
        self.openWindows.append(self.breeds_Window)
        self.breeds_Window.run()
        self.breed_finder = self.breed_finder_Window.run()
        
    def open_breed_finder(self):
        if self.breed_finder_Window != None:
            messagebox.showinfo("Warning", "You already have a breed_finder window open. Please close it first.")
            return
        print("opening breed finder window")

        self.breed_finder_Window: Breed_finder_Window = Breed_finder_Window(Toplevel(self.root))
        self.breed_finder = self.breed_finder_Window.run()

    def debug(self):
        print(self.root.winfo_children())

    def run(self):
        self.root.mainloop()

class Breeds_Window(Tk):

    def __init__(self, root):
        self.root = root
        self.root.title('Breeds')
        self.root.geometry('300x300')
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()

class Breed_finder_Window(Tk):

    def __init__(self, root):
        self.root = root
        self.root.title('Breed Finder')
        self.root.geometry('300x300')
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    root = Tk()
    menu = Menu(root)
    menu.run()
