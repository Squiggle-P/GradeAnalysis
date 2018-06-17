
""" Dependancies """
import numpy as np, pandas as pd, matplotlib.pyplot as plt, tkinter as tk #pkgutils as pkg, timeit

# Configuration Stuff - To be red from file / GUI

CSVFileName = "PM1 KPI Determinants.csv"
# TagCoding = {'1GRADECODE':'A',
#              '1BWSCNAV':'B',
#              '1CWSCNAV':'C',
#              '1CWTGT':'D',
#              '1MACHSPD':'E',
#              '1MSTSCAV':'F',
#              '1SBFLG':'G'
#              }
# SB_RemovePrior = pd.to_timedelta('-2m')
# SB_RemoveAfter = pd.to_timedelta('15m')

# User-Defined Rules:
"""
I'd like users to be able to write their own conditionals but that's going to require a lot more effort.

    Hey buddy screw you let's do it.

"""
# Remove data that is less than 2 minutes prior to a sheet break
# Remove data that is during a sheetbreak
# Remove data that is within 15 minutes of getting back on the reel

# Split data into grades - within the base dataframe we can probably just use the existing grade code flag and conditionals.
# # This might change when lasso functionality is implemented - I'm not sure how that works at this point in time.


# Build Pandas Arrays
print("Reading BW CSV")
RawDF = pd.read_csv(CSVFileName, sep=";", header=0, index_col=0)

print("Converting DateTimes")
# OK Woah - getting the formatting right increases the speed by almost %100,000 - that's not an exaggeration.
RawDF.index = pd.to_datetime(RawDF.index, format="%m/%d/%Y %I:%M:%S %p")
print("Converted")


def ValueEquals(ser,val,inverse=False,timeshift=False,td_pre='0m',td_post='0m'):
    """
    Takes series (ideally column of DataFrame) and returns a 2xN list of date-times during which values in the series equal a single, specified value.

    :param ser:         series input to be evaluated
    :param val:         value to evaluate series true/false
    :param inverse:     boolean, if True return times ser.row <> val. Else return ser.row == val
    :param timeshift:   boolean, if True add/subtract time to final timeranges
    :param td_pre:      string to flag values earlier than event-start
    :param td_post:     string to flag values later than event-end
    :return:            TimeList of
    """

    def EqualsFlag(row,col1,col2,value):
        if row[col1] == value and row[col2] != value:
            marker = "Start"
        elif row[col1] != value and row[col2] == value:
            marker = "End"
        else:
            marker = np.nan
        return marker

    def NotEqualsFlag(row,col1,col2,value):
        if row[col1] != value and row[col2] == value:
            marker = "Start"
        elif row[col1] == value and row[col2] != value:
            marker = "End"
        else:
            marker = np.nan
        return marker


    TimeList = []
    header = ser.name
    frame = ser.to_frame()
# Identify start/end points in a row format rather than a column format
    frame[header+'shift'] = frame[header].shift(1)

# Run comparison routines
    if not inverse:
        frame[header+'flags'] = frame.apply(EqualsFlag, axis=1, args=(header,header+'shift',val))
    else:
        frame[header + 'flags'] = frame.apply(NotEqualsFlag, axis=1, args=(header, header + 'shift', val))
    StartList = frame.index[frame[header+'flags']=="Start"]
    EndList = frame.index[frame[header+'flags']=="End"]

    ## Validate lists to get pairs
    # If timestamps are uneven lengths, a condition was probably split
    # Need to chop one off.

    if not len(StartList) == len(EndList):

        if not StartList[0] < EndList[0]:
            EndList = EndList[1:]
        elif not EndList[len(EndList)-1] > StartList[len(StartList)-1]:
            for item in StartList:
                print (item)
            StartList = StartList[:len(StartList)-1]
            for item in StartList:
                print (item)
    # If timestamps were uneven but it still isn't right, two conditions were probably split.
    # How unlucky.
    else:
        if  (StartList[0] > EndList[0]) and (EndList[len(EndList)-1] < StartList[len(StartList)]-1):
            EndList = EndList[1:]
            StartList = StartList[:len(StartList)-1]

    # print(len(StartList),len(EndList))
    for index in range(len(StartList)):
        # print(index, StartList[index],EndList[index])
        TimeList.append((StartList[index], EndList[index]))

    # Apply time shifts to encapsulate more data
    if timeshift:
        ExtendedTimesList = []
        td_pre = pd.to_timedelta(td_pre)
        td_post = pd.to_timedelta(td_post)
        for index in range(len(TimeList)):
            new_start = TimeList[index][0] + td_pre
            new_end = TimeList[index][1] + td_post
            ExtendedTimesList.append([new_start, new_end])

        return ExtendedTimesList
    else:
        return TimeList

## Test Site

print ("Processing Grade")
GradeException = ValueEquals(RawDF['1GRADECODE'],5505,True,True,'-2H','30m')
print ("Grades Done")
print ("Processing SB")
SBException = ValueEquals(RawDF['1SBFLG'],1,False,True,'-2m','15m')
print ("SB Done")


plt.figure()
plt.plot(RawDF['1BWSCNAV'])
for item in SBException:
    plt.axvspan(item[0],item[1],color='red',alpha=0.3)
for item in GradeException:
    plt.axvspan(item[0],item[1],color='blue',alpha=0.3)
# plt.plot(RawDF.G)
# plt.plot(RawDF.SB_Removal)
plt.show()

#List of Run Grades:
Temp = RawDF.groupby('1GRADECODE')['1GRADECODE'].count()
GradeList = Temp[Temp>10].sort_values(ascending = False)
Temp = []
#
# def plotfunc(dataframe):
#     global ax
#     b, g, r, c, m, y, k, w
#     color = 'b' if (dataframe['A'] == 5505) else 'g'
#     ax.plot(dataframe.index, dataframe.B, c=color, linewidth=2)


# Build a GUI - storage code

root = tk.Tk()  # This is the main parent attribute for the GUI
HeaderLabel = tk.Label(root, text="Limit Calculations") # This is a label
HeaderLabel.pack()      # Size yourself w/ the given text


class App:
    def __init__(self, master):
        frame = tk.Frame(master)    # Create a container
        frame.pack(side='top')      # Put the container above(? Not above) <strike>the text earlier</strike>

        self.QuitButton = tk.Button(
            frame, text="QUIT", fg="blue", bg="red", command=frame.quit
        )
        self.QuitButton.pack(side='right')

        self.HiButton = tk.Button(
            frame, text="Hello", command=self.say_hi
        )
        self.HiButton.pack(side='bottom')

    def say_hi(self):
        print("hi there, everyone!")

app = App(root)
app2 = App(root)
root.mainloop()         # Show yourself until destroyed
root.destroy()