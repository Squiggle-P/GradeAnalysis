# GradeAnalysis
Grade Sorting and Control Limits


Idea Function:

Determine control limits for large datasets using "best of" identifiers. 

    What about a scoring algorithm?

Additionally there's a need to graphically display the data, as well as display what information
has been stripped from the dataset due to filtering or categorizing. 

    Does the user need to be able to interact w/ the data at this stage, like Minitab? If the user could
    select data w/ their cursor by drawing a shape or at least a box, then manually filtering that data
    out/in.
    
Neat idea



Notes

    MatPlotLib has a functionality for LassoSelection - definitely necessary for displaying everything
    Pandas has the best time-series data, but I think there needs to be a conversion to let MatPlotLib play with it..


    When plotting a DataFrame, plotting normally w/ deleted or spliced-out data will give a single-line
    connector. Plotting w/ the argument "x=df.index.astype(str)" will remove that portion of the X-Axis
    (but also remove the axis titling - need to specify it again w/ PLT)









