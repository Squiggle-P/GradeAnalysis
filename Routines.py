
""" Dependancies """
import numpy as np, pandas as pd, matplotlib.pyplot as plt, tkinter as tk #pkgutils as pkg, timeit

# Configuration Stuff - To be read from file / GUI

CSVFileName = "PM1 KPI Determinants.csv"
GradeLimits = {5505:56,
               6900:70,
               4266:44,
               5511:55}
gradetag = '1GRADECODE'
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

def ValueInequality(ser,val, comparison,
                    timeshift=False,td_pre='0m',td_post='0m',
                    grade_series=pd.DataFrame()):
    """
    Takes series (ideally a column of a DataFrame) and returns a 2xN list of date-times during which values in the
    series evaluate True against the comparison condition (comparison) and the value (val) or grade-based values ([val])
    Option exists to time-shift the start/end times by pandas.time_deltas td_pre and td_post.

    :param ser:         series input to be evaluated
    :param val:         value OR dict of values {'Grade':val} to be used as a comparison
    :param comparison:  string description of inequality intended. Accepts '>', '>=', '==', '<=', '<', and '!='
    :param timeshift:   boolean, if True add/subtract time to final timeranges.
    :param td_pre:      string to flag values earlier than event-start. Negative delays time INTO the event
    :param td_post:     string to flag vlaues later than event-end. Negative delays time INTO the event
    :param grade_series:dataframe with grades in raw format - strings or integers or floats - associated to the same timespan as

    :return:            TimeList (2xN array of [start/end] of timeperiods which evaluate the inequality as True.
    """

    def EqualsFlag(row,col1,col2,value):
        if row[col1] == row[value] and row[col2] != row[value]:
            marker = "Start"
        elif row[col1] != row[value] and row[col2] == row[value]:
            marker = "End"
        else:
            marker = np.nan
        return marker

    def NotEqualsFlag(row,col1,col2,value):
        if row[col1] != row[value] and row[col2] == row[value]:
            marker = "Start"
        elif row[col1] == row[value] and row[col2] != row[value]:
            marker = "End"
        else:
            marker = np.nan
        return marker

    def GreaterFlag(row,col1,col2,value):
        if np.isnan(row[col1]) or np.isnan(row[col2]):
            return np.nan
        if row[col1] > row[value] and row[col2] <= row[value]:
            marker = "Start"
        elif row[col1] <= row[value] and row[col2] > row[value]:
            marker = "End"
        else:
            marker = np.nan
        return marker

    def GreaterEqualFlag(row,col1,col2,value):
        if row[col1] >= row[value] and row[col2] < row[value]:
            marker = "Start"
        elif row[col1] < row[value] and row[col2] >= row[value]:
            marker = "End"
        else:
            marker = np.nan
        return marker

    def LesserFlag(row,col1,col2,value):
        if row[col1] < row[value] and row[col2] >= row[value]:
            marker = "Start"
        elif row[col1] >= row[value] and row[col2] < row[value]:
            marker = "End"
        else:
            marker = np.nan
        return marker

    def LesserEqualFlag(row,col1,col2,value):
        if row[col1] <= row[value] and row[col2] > row[value]:
            marker = "Start"
        elif row[col1] > row[value] and row[col2] <= row[value]:
            marker = "End"
        else:
            marker = np.nan
        return marker

    global count
    count = 0
    timelist = []
    header = ser.name
    frame = ser.to_frame()
    # Identify start/end points in a row format rather than a column format
    frame[header+'shift'] = frame[header].shift(1)

    # Do we need grade dependant limits?
    if(isinstance(val,dict) and len(grade_series) == len(ser)): # Grades have been spec'd
        print("Grades Needed")
        frame[header+'limit'] = grade_series.map(val)

    elif(isinstance(val,dict) and len(grade_series)!= len(ser)):
        raise ValueError('Grade time-series was not delivered or does not match full data set')
    elif(not isinstance(val,dict) and len(grade_series)==len(ser)):
        raise ValueError('Grade was provided but grade-based-limits were not.')
    else:
        print("Grades NOT needed, proceed as static")
        frame[header+'limit'] = val

    # Run inequality routines - if check for correct mechanisms

    if(comparison == '<'):
        frame[header+'flags'] = frame.apply(LesserFlag,axis=1,args=(header,header+'shift',header+'limit'))
    elif(comparison == '<='):
        frame[header+'flags'] = frame.apply(LesserEqualFlag,axis=1,args=(header,header+'shift',header+'limit'))
    elif(comparison == '>'):
        frame[header+'flags'] = frame.apply(GreaterFlag,axis=1,args=(header,header+'shift',header+'limit'))
    elif(comparison == '>='):
        frame[header+'flags'] = frame.apply(GreaterEqualFlag,axis=1,args=(header,header+'shift',header+'limit'))
    elif(comparison == '=='):
        frame[header+'flags'] = frame.apply(EqualsFlag,axis=1,args=(header,header+'shift',header+'limit'))
    elif(comparison == '!='):
        frame[header+'flags'] = frame.apply(NotEqualsFlag,axis=1,args=(header,header+'shift',header+'limit'))
    else:
        raise ValueError('Comparison chosen does not exist in program. How did you do that?')

    startlist = frame.index[frame[header+'flags']=="Start"]
    endlist = frame.index[frame[header+'flags']=="End"]

    ## Validate lists to get pairs
    # If timestamps are uneven lengths, a condition was probably split
    # Need to chop one off.

    if not len(startlist) == len(endlist):

        if not startlist[0] < endlist[0]:
            EndList = endlist[1:]
        elif not endlist[len(endlist)-1] > startlist[len(startlist)-1]:
            # for item in startlist:
                # print (item)
            startlist = startlist[:len(startlist)-1]
            # for item in startlist:
            #     print (item)
    # If timestamps were uneven but it still isn't right, two conditions were probably split.
    # How unlucky.
    else:
        if  (startlist[0] > endlist[0]) and (endlist[len(endlist)-1] < startlist[len(startlist)]-1):
            endlist = endlist[1:]
            startlist = startlist[:len(startlist)-1]

    # print(len(StartList),len(EndList))
    for index in range(len(startlist)):
        # print(index, StartList[index],EndList[index])
        timelist.append((startlist[index], endlist[index]))

    if timeshift:
        extendedtimelist = []
        td_pre = pd.to_timedelta(td_pre)
        td_post = pd.to_timedelta(td_post)
        for index in range(len(timelist)):
            new_start = timelist[index][0] + td_pre
            new_end = timelist[index][1] + td_post
            extendedtimelist.append([new_start, new_end])

        return extendedtimelist
    else:
        return timelist

def ValueEquals(ser,val,inverse=False,timeshift=False,td_pre='0m',td_post='0m'):
    """
    Note:   Depreciated in version 1.3 of Routines.py, future use migrated to ValueInequality with a '==' or '!='
            comparison value.

    Takes series (ideally column of DataFrame) and returns a 2xN list of date-times during which values in the series equal a single, specified value.
    Does NOT support grade- or list-based equalities.

    :param ser:         series input to be evaluated
    :param val:         value to evaluate series true/false
    :param inverse:     boolean, if True return times ser.row <> val. Else return ser.row == val
    :param timeshift:   boolean, if True add/subtract time to final timeranges
    :param td_pre:      string to flag values earlier than event-start
    :param td_post:     string to flag values later than event-end
    :return TimeList:  (2xN array of [start/end] of timeperiods which match a single conditional equality
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
good_grades = []
bad_grades = []
for item in RawDF[gradetag].unique():
    icount = RawDF[RawDF[gradetag]==item][gradetag].count()
    if icount >= 10:
        good_grades.append((item,icount))
    else:
        bad_grades.append((item,icount))
        # # print("Grade '" + str(item) + "' only had " + str(icount) + " counts recorded and was ignored.")
        # print("Grade '%s' only had %s counts recorded and was ignored." %(item,icount))

# GradeException = ValueEquals(RawDF['1GRADECODE'],5505,True,True,'-2H','30m')
GradeException = ValueInequality(RawDF['1GRADECODE'],5505,'==',timeshift=True,td_pre='15m',td_post='15m')
print ("Grades Done")
print ("Processing SB")
# SBException = ValueEquals(RawDF['1SBFLG'],1,False,True,'-2m','15m')
SBException = ValueInequality(RawDF['1SBFLG'],1,'==',timeshift=True,td_pre='2m',td_post='15m')
print ("SB Done")

print("Processing BW Too High")
# UpperBWException = ValueInequality(RawDF['1BWSCNAV'],GradeLimits,'>',grade_series = RawDF['1GRADECODE'])
UpperBWException = ValueInequality(RawDF['1BWSCNAV'],55,'>')
print("BW Too High between:")
print (UpperBWException)

fig1 = plt.figure()
fig1.suptitle('Data Selection Example')
ax1 = fig1.add_subplot(311)
ax2 = fig1.add_subplot(312)
ax3 = fig1.add_subplot(313)

ax1.plot(RawDF['1BWSCNAV'])
# plt.plot(RawDF['1BWSCNAV'])
for item in SBException:
    # plt.axvspan(item[0], item[1], color='red', alpha=0.3)
    ax1.axvspan(item[0],item[1],color='red',alpha=0.3)

ax2.plot(RawDF['1BWSCNAV'])
for item in GradeException:
    # plt.axvspan(item[0],item[1],color='blue',alpha=0.3)
    ax2.axvspan(item[0],item[1],color='blue',alpha=0.3)

count = 0

ax3.plot(RawDF['1BWSCNAV'])
for item in UpperBWException:
    # plt.axvspan(item[0],item[1],color='green',alpha=0.3)
    if count < 10:
        print (item[0], item[1])
        count = count + 1
    ax3.axvspan(item[0], item[1], color='green', alpha=0.3)
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