
""" Dependancies """
import numpy as np, pandas as pd, matplotlib.pyplot as plt, pkgutil as pkg, timeit

# Configuration Stuff - To be red from file / GUI

CSVFileName = "PM1 KPI Determinants.csv"
TagCoding = {'1GRADECODE':'A',
             '1BWSCNAV':'B',
             '1CWSCNAV':'C',
             '1CWTGT':'D',
             '1MACHSPD':'E',
             '1MSTSCAV':'F',
             '1SBFLG':'G'
             }
SB_RemovePrior = pd.to_timedelta('-2m')
SB_RemoveAfter = pd.to_timedelta('15m')

# User-Defined Rules:
"""
I'd like users to be able to write their own conditionals but that's going to require a lot more effort.
"""
# Remove data that is less than 2 minutes prior to a sheet break
# Remove data that is during a sheetbreak
# Remove data that is within 15 minutes of getting back on the reel

# Split data into grades - within the base dataframe we can probably just use the existing grade code flag and conditionals.
# # This might change when lasso functionality is implemented - I'm not sure how that works at this point in time.


# Build Pandas Arrays
print("Reading BW CSV")
RawDF = pd.read_csv(CSVFileName, sep=";", header=0, index_col = 0)

print("Converting DateTimes")
# OK Woah - getting the formatting right increases the speed by almost %100,000 - that's not an exaggeration.
RawDF.index = pd.to_datetime(RawDF.index, format="%m/%d/%Y %I:%M:%S %p")
print("Converted")

# Need to sanitize headers here, as items starting w/ numbers are a problem
ColumnRenameList = [TagCoding[item] for item in RawDF.columns.tolist()]
RawDF.columns = ColumnRenameList

print("Process SheetBreaks")
# TimeShift by 1 interval
RawDF['H'] = RawDF.G.shift(1)


def SBFlag(row):
    if row['G'] > 0 and row['H'] == 0:
        val = "Start"
    elif row['G'] == 0 and row['H'] >0:
        val = "End"
    # elif row['G'] > 0 and row['H'] > 0:
    #     val = "Mid"
    else:
        val = np.nan
    return val

RawDF['SB_Flag'] = RawDF.apply(SBFlag,axis=1)

# Save the Time Indices for SBs
SB_StartList = RawDF.index[RawDF.SB_Flag=="Start"]
SB_EndList = RawDF.index[RawDF.SB_Flag == "End"]

## Validate lists to get pairs
# If timestamps are uneven lengths, a sheetbreak was probably split
# Need to chop one off.
if not len(SB_StartList) == len(SB_EndList):
    if not SB_StartList[0] < SB_EndList[0]:
        SB_StartList = SB_StartList[1:]
    elif not SB_EndList[len(SB_EndList)] > SB_StartList[len(SB_StartList)]:
        SB_EndList = SB_EndList[:-1]
# If timestamps were uneven but it still isn't right, two SBs were probably split.
# How unlucky.
else:
    if not (SB_StartList[0] < SB_EndList[0]) and not (SB_EndList[len(SB_EndList)] > SB_StartList[len(SB_StartList)]):
        SB_StartList = SB_StartList[1:].tolist()
        SB_EndList = SB_EndList[:-1].tolist()

SB_TimesList = []
for index in range(len(SB_StartList)):
    SB_TimesList.append((SB_StartList[index],SB_EndList[index]))

# Apply time shifts to encapsulate more data
print("Build Sheetbreak Lists")
SB_ExtendedTimesList = []
for index in range(len(SB_TimesList)):
    new_start = SB_TimesList[index][0] + SB_RemovePrior
    new_end = SB_TimesList[index][1] + SB_RemoveAfter
    SB_ExtendedTimesList.append([new_start,new_end])

# print(SB_TimesList[0:2])
# print(SB_ExtendedTimesList[0:2])


RawDF['SB_Removal'] = 0
for item in SB_ExtendedTimesList:
    RawDF.SB_Removal[item[0]:item[1]] = 1


plt.figure()
plt.plot(RawDF.B)
for item in SB_ExtendedTimesList:
    plt.axvspan(item[0],item[1],color='red',alpha=0.3)
# plt.plot(RawDF.G)
# plt.plot(RawDF.SB_Removal)
plt.show()

#List of Run Grades:
Temp = RawDF.groupby('A').A.count()
GradeList = Temp[Temp>10].sort_values(ascending = False)
Temp = []
#
# def plotfunc(dataframe):
#     global ax
#     b, g, r, c, m, y, k, w
#     color = 'b' if (dataframe['A'] == 5505) else 'g'
#     ax.plot(dataframe.index, dataframe.B, c=color, linewidth=2)