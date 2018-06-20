"""
This is mostly a testbed for the GUI functionality


"""


import tkinter as tk


class App:
    def __init__(self, master):
        self.headerframe = tk.Frame(master)    # Create a container
        # self.headerframe.pack(side='top')      # Put the container above(? Not above) <strike>the text earlier</strike>
        self.headerframe.grid(row=0,column=0,columnspan=7)
        self.HeaderLabel = tk.Label(self.headerframe, text="Limits Calculator (1)")
        # HeaderLabel.pack(side="left")
        self.HeaderLabel.grid(row=0,column=1,sticky='n,e,s,w')

        CSV_Filename = tk.StringVar

        self.QuitButton = tk.Button(
            self.headerframe, text="QUIT", fg="blue", bg="red", command=self.headerframe.quit
        )
        # self.QuitButton.pack(side='right')
        self.QuitButton.grid(row=0,column=2)
        self.HiButton = tk.Button(
            self.headerframe, text="Hello", command=self.say_hi
        )
        self.HiButton.grid(row=0,column=3, padx=5, pady=5)
        # self.HiButton.pack(side='bottom')
        #
        #
        #
        # self.UpperBodyFrame = tk.Frame(master, bg="grey", height=400, width=1000)
        # self.UpperBodyFrame.pack(side="bottom")
        #
        # self.GeneratorFrame = tk.Frame(self.UpperBodyFrame, bg="white", height=400, width=600, padx=20)
        # self.GeneratorFrame.pack(side="left")
        #
        # self.CsvFrame = tk.Frame(self.GeneratorFrame, bg="blue", height=50, width = 400)
        # self.CsvFrame.pack(side="left")
        #
        # self.RulesFrame = tk.Frame(self.UpperBodyFrame, bg="black", height = 400, width=380, padx=20)
        # self.RulesFrame.pack(side="right")
        #
        # self.CSVField = tk.Entry(self.CsvFrame, textvariable=CSV_Filename, width=40)
        # self.CSVBrowse = tk.Button(self.CsvFrame, text="Browse",command=self.BrowseCSV)
        # self.CSVField.pack(side='left')
        # self.CSVBrowse.pack(side='right')
        self.GeneratorFrame = tk.Frame(master, height=400, width=600)
        self.GeneratorFrame.grid(row=2,column=0,rowspan=5, columnspan=5,sticky="n,s,e,w",padx=5,pady=5)
        self.CSVField = tk.Entry(self.GeneratorFrame,textvariable = CSV_Filename, width=40)
        self.CSVField.grid(row=0, column=0,columnspan=3,rowspan=1,sticky='w,e')
        self.BrowseButton = tk.Button(self.GeneratorFrame,text="bws",width="2",height="1")
        self.BrowseButton.grid(row=0,column=3,sticky='w,e',padx=0,pady=0)
        self.ConfirmButton = tk.Button(self.GeneratorFrame,text="chk",width=2,height=1)
        self.ConfirmButton.grid(row=0,column=4,sticky="w,e",padx=0,pady=0)

        self.ListboxFrame = tk.Frame(self.GeneratorFrame)
        self.ListboxFrame.grid(row=1,column=0,rowspan=4,columnspan=1,sticky="w",pady=0,padx=0)
        self.TagList = tk.Listbox(self.ListboxFrame,width=20,height=8)
        self.TagList.grid(row=0,column=0,sticky="n,s,e,w",pady=0)
        self.TagListScroll = tk.Scrollbar(self.ListboxFrame,width=15)
        self.TagListScroll.grid(row=0,column=1,sticky="n,s",padx=0)
        self.TagList.config(yscrollcommand=self.TagListScroll.set)
        self.TagListScroll.config(command=self.TagList.yview)
        for i in range(100):
            self.TagList.insert(i,"Tag"+str(i+1))
        self.conditionlist = {'=','!=','<','>','=<','>='}
        self.conditionselected = tk.StringVar(master)
        self.conditionselected.set('=')
        self.evallist = {'Tag':"t",'Static':"s",'Grade':"g"}
        self.evalselected = tk.StringVar(master)
        self.ConditionCombo = tk.OptionMenu(self.GeneratorFrame,self.conditionselected,*self.conditionlist)
        self.ConditionCombo.grid(row=1,column=1,columnspan=2,sticky="w,e,n,s",padx=0,pady=0)
        self.EvalCombo = tk.OptionMenu(self.GeneratorFrame,self.evalselected,*self.evallist)
        self.EvalCombo.grid(row=2,column=1,columnspan=2,sticky="w,e,n,s",padx=0,pady=0)

        self.GenerateButton = tk.Button(self.GeneratorFrame,text="Generate!",width=10)
        self.EvaluationBox = tk.Entry(self.GeneratorFrame,text="stuff")
        self.GenerateButton.grid(row=1,column=3,columnspan=2)
        self.EvaluationBox.grid(row=2,column=3,columnspan=2)

        self.timelist = ['days','hours','minutes','seconds']
        self.pretimeselected = tk.StringVar(master)
        self.posttimeselected = tk.StringVar(master)
        self.PreTimeLabel = tk.Label(self.GeneratorFrame,text="PreTime:")
        self.PreTimeLabel.grid(row=3,column=1,sticky="w,e")
        self.PostTimeLabel = tk.Label(self.GeneratorFrame,text="PostTime:")
        self.PostTimeLabel.grid(row=4,column=1,sticky="e,w")
        self.PreTimeValue = tk.StringVar(master)
        self.PostTimeValue = tk.StringVar(master)
        self.PreTimeField = tk.Entry(self.GeneratorFrame,textvariable=self.PreTimeValue,width=3)
        self.PostTimeField = tk.Entry(self.GeneratorFrame,textvariable=self.PostTimeValue,width=3)
        self.PreTimeField.grid(row=3,column=2,sticky="w,e")
        self.PostTimeField.grid(row=4,column=2,sticky="w,e")
        self.PreTimeCombo = tk.OptionMenu(self.GeneratorFrame,self.pretimeselected,*self.timelist)
        self.PostTimeCombo = tk.OptionMenu(self.GeneratorFrame,self.posttimeselected,*self.timelist)
        self.PreTimeCombo.grid(row=3,column=3,columnspan=2,sticky="w,e")
        self.PostTimeCombo.grid(row=4,column=3,columnspan=2,sticky="w,e")

        self.RulesFrame = tk.Frame(master,height=400,width=400)
        self.RulesFrame.grid(row=2,column=5,rowspan=8,columnspan=3)
        self.RulesLabel = tk.Label(self.RulesFrame,text="RulesList")
        self.RulesLabel.grid(row=0,column=0,columnspan=2)
        self.RulesList = tk.Listbox(self.RulesFrame,width=30,height=9)
        self.RulesList.grid(row=1,column=0,columnspan=2,rowspan=5)
        self.RulesScroll = tk.Scrollbar(self.RulesFrame,width=15)
        self.RulesScroll.grid(row=1,column=2,sticky="n,s,w",rowspan=5)
        self.RulesList.config(yscrollcommand=self.RulesScroll.set)
        self.RulesScroll.config(command=self.RulesList.yview)
        for i in range(15):
            self.RulesList.insert(i,"Rule"+str(i+1))
        self.RuleOrderUpButton = tk.Button(self.RulesFrame,text="^",width=1)
        self.RuleOrderDownButton = tk.Button(self.RulesFrame,text="V",width=1)
        self.RuleDeleteButton = tk.Button(self.RulesFrame,text="X",width=1)
        self.RuleOrderUpButton.grid(row=1, column=3, sticky="n,s,e,w")
        self.RuleOrderDownButton.grid(row=2, column=3, sticky="n,s,e,w")
        self.RuleDeleteButton.grid(row=3, column=3, sticky="n,s,e,w")

        self.GradeCheck = tk.Checkbutton(self.RulesFrame)
        self.GradeCheck.grid(row=6,column=0,sticky="w")
        self.GradeLabel = tk.Label(self.RulesFrame,text="Grade Based?")
        self.GradeLabel.grid(row=6,column=1,columnspan=2,sticky="w")
        self.gradeselected = tk.StringVar
        self.gradeslist = self.TagList.cget('listvariable')
        # print (self.getvar(self.gradeslist))
        self.GradeCombo = tk.OptionMenu(self.RulesFrame,self.gradeselected,*self.TagList.keys())
        self.GradeCombo.grid(row=7,column=0,columnspan=2,sticky="w,n,e")

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