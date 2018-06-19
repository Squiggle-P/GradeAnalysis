"""
This is mostly a testbed for the GUI functionality


"""


import tkinter as tk


class App:
    def __init__(self, master):
        self.headerframe = tk.Frame(master)    # Create a container
        self.headerframe.pack(side='top')      # Put the container above(? Not above) <strike>the text earlier</strike>
        HeaderLabel = tk.Label(self.headerframe, text="Limits Calculator (1)")
        HeaderLabel.pack(side="left")

        CSV_Filename = tk.StringVar

        self.QuitButton = tk.Button(
            self.headerframe, text="QUIT", fg="blue", bg="red", command=self.headerframe.quit
        )
        self.QuitButton.pack(side='right')

        self.HiButton = tk.Button(
            self.headerframe, text="Hello", command=self.say_hi
        )
        self.HiButton.pack(side='bottom')



        self.UpperBodyFrame = tk.Frame(master, bg="grey", height=400, width=1000)
        self.UpperBodyFrame.pack(side="bottom")

        self.GeneratorFrame = tk.Frame(self.UpperBodyFrame, bg="white", height=400, width=600, padx=20)
        self.GeneratorFrame.pack(side="left")

        self.CsvFrame = tk.Frame(self.GeneratorFrame, bg="blue", height=50, width = 400)
        self.CsvFrame.pack(side="left")

        self.RulesFrame = tk.Frame(self.UpperBodyFrame, bg="black", height = 400, width=380, padx=20)
        self.RulesFrame.pack(side="right")

        self.CSVField = tk.Entry(self.CsvFrame, textvariable=CSV_Filename, width=40)
        self.CSVBrowse = tk.Button(self.CsvFrame, text="Browse",command=self.BrowseCSV)
        self.CSVField.pack(side='left')
        self.CSVBrowse.pack(side='right')

    def say_hi(self):
        print("hi there, everyone!")

    def add_rule(self):
        print("I add da rule")

    def BrowseCSV(self):
        print ("Browse for CSV")

root = tk.Tk()  # This is the main parent attribute for the GUI
# HeaderLabel = tk.Label(root, text="Limit Calculations") # This is a label
# HeaderLabel.pack()      # Size yourself w/ the given text

app = App(root)
root.mainloop()         # Show yourself until destroyed
root.destroy()