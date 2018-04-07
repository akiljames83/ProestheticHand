'''  
IBEHS 1P10  
Project Two: This is Getting Out of Hand  
Group 15 - T04  
Wednesday, December 6, 2017
'''
# Importing all the necessary libraries for GUI, plotting and movement calculations
from tkinter import Tk ,NE,N,W,S,E, Label, Button, Frame,Message, Menu, Menubutton
import tkinter as tk
import tkinter.font as tkFont
import time
import simpleaudio as sa
from tkinter import ttk
import math
import matplotlib.pyplot as plt
from matplotlib import animation

#=======================Subprogram 1 Variables=================
#Store Given Gear Ratio in a Variable
gearRatio = 8.125
#=======================Subprogram 1 Functions=================
def calculationsSubprogram1(otherTeamNumber):
    print('========================','#',otherTeamNumber,'========================')
    #Reading the File
    copiedFile = open("teamNumbers.txt",'r') #Opens a file with all the teams and team numbers 
    dataList = copiedFile.readlines() #Creates a list from the values
    copiedFile.close
    # Initiate a for loop to iterate over textfiles data and converting strings to floats after they have been split
    for i in range(len(dataList)): 
        dataList[i] = dataList[i].split()
        groupNumber = float(dataList[i][0])#Index 0 is group number
        inputSpeed = float(dataList[i][1]) #Index 1 is input speed
        # since if is embedded in for loop, it checks if each group number is the inputed group number
        if dataList[i][0] == otherTeamNumber:
            outputSpeedd = inputSpeed/(gearRatio*60)# Uses other team number to calculate speed (RPS)
            outputSpeed = "%.3f" % round(outputSpeedd,3)# Speed is subsequently rounded to 3 sig. fiigs.
            # Create a set of strings referring to various data collected through previous computations s they can be printed to the command line  
            ans1 = "Your team number is: " + str(otherTeamNumber)
            ans2 = "The given input speed in RPM is: " + str(inputSpeed)
            ans3 = "The calculated output speed in RPS is: " + str(outputSpeed)
            ans4 = "The gear ratio is: 8.125 : 1"
            successM = 'Computation Successful!'
            print(ans1,'\n'+ans2,'\n'+ans3,'\n'+ans4) # Prints values to command line
            return otherTeamNumber,inputSpeed,outputSpeed,'8.125 : 1',successM
    #If entire file is checked and its not there present the error statement
    error = 'Error 101: Invalid input. Try again.' # If team number is not in text file, print error statement 
    print(error)
    return error
#============================Inital Variables Sub2==========================
# starting positon = SP -> Open = 1, Closed = 0
# number of roations = NR -> Total number of rotations desired for motor
# number of increments = NI -> How to break up the movements of motor
# Empty array to assign values for plotting curves
graph_valT = []
graph_valI = []
# Empty string to assign individual summary statements of movement of fingers
summary = ''
globalCounter = 0
#==========================Global Variables for Functions==============
#currentPositionRitations CPR is value ranging from 0 to tdm
cpr = 0
indexX = 53
indexL=75
thumbY=26.5
thumbL=61
#===========================Functions Sub2===========================================
def angleT(angleReferenceFingT,arf):
    # angleReferenceFingT is the angle of the thumb above horizontal to the position of thumb at the point of intersection
    # arf is the angle between the current position of thumb and its position at the point of intersection
    thetaD = angleReferenceFingT + arf
    # conversion to radians
    thetaR = thetaD*math.pi/180
    # thumb speicifc calculations based on our interpretation of origin point, using trig to find new x and y coordinates
    y_dir = thumbL*(math.sin(thetaR)) + thumbY
    x_dir = thumbL*(math.cos(thetaR))
    # convert the output number from a long float to a number with 3 decimal places
    y = float("%.3f" % round(y_dir,3))
    x = float("%.3f" % round(x_dir,3))
    output = [x,y]
    return output

def angleI(angleReferenceFingI,arf):
    # angleReferenceFingT is the angle of the thumb above horizontal to the position of index at the point of intersection
    # arf is the angle between the current position of index and its position at the point of intersection
    thetaD = angleReferenceFingI - arf
    # conversion to radians
    thetaR = thetaD*math.pi/180
    # calculations of the new positions of the index finger's x and y coordinates using trig 
    y_dir = -1*indexL*(math.sin(thetaR))
    x_dir = -1*indexL*(math.cos(thetaR)) + indexX
    # convert the number from long float to a number with 3 decimal places
    y = float("%.3f" % round(y_dir,3))
    x = float("%.3f" % round(x_dir,3))
    output = [x,y]
    return output

def getKey(item):
    # function needed to order list when in tuples, used in sub program 3
    return item[0]

def mover_(startingPosition,numRotations,numIncrements):
    global globalCounter
    global cpr
    global graph_valT
    global graph_valI
    global summary
    #======================Inital Variables**======================
    # This is the Theta angle in drawn diagram
    angleReferenceFrame = 40
    gearRatio = 8.125
    totalDegreesRotation = angleReferenceFrame*gearRatio
    end = math.floor(totalDegreesRotation)
    # Pre-calculated
    angleReferenceFingT = 50.554
    angleReferenceFingI = -78.935
    # This is currentDegreeRotation (cdr) current position in reference frame
    cdr = 0
    #initializing direction, value will be overwritten
    direct = 0
    #======================Initialization===========================
    #Initializing the Bool statements for the position of the motor
    # 0 is closed, 1 is open
    if startingPosition == 0:
        position = True
        cdr = 0
    elif startingPosition == 1:
        position = False
        cdr = end
    #Quick Check
    # Initializing the Total Degrees of Motion (TDM) of motor
    tdm = numRotations*360
    # Initializing the degrees the motor adds progressively (AD)
    ad = int(math.floor(tdm/numIncrements))
    # Initializing Movement of Motor (MM)
    mm = tdm/totalDegreesRotation
    # Number of switches of Motor // changes in rotation CW or CCW
    switches = math.floor(mm)
    # For loop initiation ===========================================================
    for num in range(numIncrements): ## Goes from 0 to (numI -1)
        # Just a reminder, cpr is the current position of rotation which ranges from 0 to numRotations*360 (total degrees of rotation
        # Incremental increase of cpr for each iteration of the for loop
        cpr += ad
        for degree in range(1,(ad+1)):
            # This is identifying a turning point; when direction switches from increasing to decreassing, we want it to bounce from 0 and switch directions
            # This initializes the new value of cdr and then switches the direction
            if cdr==0:
                cdr=1
                direct = True
            # Second turning point; works on the same principle as the first turning point
            elif cdr == end:
                cdr = end-1
                direct = False
            # Identifies behavior of the cpr in the range of 0 to TotalDegreeofRotation, conditions based on whther direction is positive - true; or negative - flase
            else:
                if direct == True:
                    cdr +=1
                else:
                    cdr -= 1
        # Angle of Rotation relative to fingers
        arf = cdr/gearRatio
        # Print statements based current direction of fingers
        if direct == True:
            # Changed the floats to 3 decimal places with [ "%.3f" % round(arf,3) ] instead of (str(arf))
            out1 = ('Thumb is moving counter clockwise and is ' + "%.2f" % round(arf,3) +" degrees away from closed position.")
            out2 = ('Index is moving clockwise and is ' + "%.3f" % round(arf,3) +' degrees away from closed postion.')
            arfStatement = (out1 +'\n' +out2)
        elif direct == False:
            out1 = ('Thumb is moving clockwise and is ' + "%.3f" % round(arf,3) +' degrees away from closed position.')
            out2 = ('Index is moving counter clockwise and is ' + "%.3f" % round(arf,3) +' degrees away from closed postion.')
            arfStatement = (out1 +'\n' +out2)
        # arm : angle of rotation motor
        arm = ('The angle of rotation of the motor is ' + str(cdr) + ' degrees relative to closed position.')
#       ### Check which is which after
        # Print statement for motor if its rotation clockwise or if its rotation counterclockwise based on the specific iteration of numIncrements for loop
        if direct == True:
            direction = 'Motor is rotating clockwise -> Opening.'
        if direct == False:
            direction = 'Motor is rotating counter-clockwise -> Closing.'
        # Calling the predefined angleT function using the current arf determining the x,y coordinates of thumb and storing it as a tuple
        thumb = angleT(angleReferenceFingT,arf)
        # calling the global variables for the Thumb coordinates list and Index coordiantes list
        # append the values to their respective lists
        graph_valT.append(thumb)
        # printstatements for thumb and index fingers
        thumbStatement = 'The coordiantes of the thumb are ' + str(thumb) + '.'
        index = angleI(angleReferenceFingI,arf)
        graph_valI.append(index)
        indexStatement = 'The coordinates of the index finger are ' + str(index) + '.'
        # mini summary is all the required information of thumb, index finger and motor, this value is concatenated
        miniSummary = arm + '\n' + direction +'\n'+ thumbStatement + '\n' + indexStatement + '\n' + arfStatement + '\n'
        linebreak = '================='+'Increment #'+str(num+1)+'=================' + '\n'
        miniSummaryFinal = linebreak + miniSummary
        summary += miniSummaryFinal
        # minisummary is then  printed and the for loop will begin its second loo
        print(miniSummary)

    # Create Name for textfile
    name = 'Subprogram2MovementSummary#' + str(globalCounter) +'.txt'
    globalCounter += 1
    # opening and the writing of the data to the textfile
    file = open(name,'w')
    file.write(summary)
    file.close()
    
    # Initializing Graph Arrays
    # Thumb Array
    xT = []
    yT = []
    # Index Array
    xI = []
    yI = []

    # Defining coordinates for Thumb and Index movement 
    for el in range(numIncrements):
        xx = graph_valT[el][0]
        xT.append(xx)
        xxx = graph_valI[el][0]
        xI.append(xxx)
        yy = graph_valT[el][1]
        yT.append(yy)
        yyy = graph_valI[el][1]
        yI.append(yyy)

    # if statement for plotting beginning and end points
    if switches == 0 and position == True:
        xT.append(38.7)
        yT.append(73.6)
        xI.append(38.7)
        yI.append(73.6)
    elif switches == 0 and position == False:
        xT.append(-0.6)
        yT.append(87.5)
        xI.append(89.4)
        yI.append(65.6)
    elif switches >0:
        xT.append(38.7)
        yT.append(73.6)
        xT.append(-0.6)
        yT.append(87.5)
        xI.append(38.7)
        yI.append(73.6)
        xI.append(89.4)
        yI.append(65.6)
            
    # Make points graph in order so curves are more visually appealing :)
    # turn two pairs of lists into two tuples
    thumbGraphList = zip(xT,yT)
    indexGraphList = zip(xI,yI)

    # Order list of tuples
    thumbGraphOrdered = sorted(thumbGraphList,key=getKey)
    indexGraphOrdered = sorted(indexGraphList,key=getKey)
    #print(thumbGraphOrdered,'\n',indexGraphOrdered)

    # unzip list of tuples
    xvarT, yvarT = zip(*thumbGraphOrdered)
    xvarI, yvarI = zip(*indexGraphOrdered)

    # Clear arrays
    graph_valT = []
    graph_valI = []
    cpr = 0
    summary = ''

    # Creating PyPlot figure and associating values with index
    #and making use of subplot to plot two sets of values on same graph
    
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    #Joint Locations
    ax1.scatter(0,26.5,c='g',label='Thumb Joint',s=60,marker='D')
    ax1.scatter(53.15,0,c='m',label='Index Joint',s=60,marker='D')
    
    ax1.scatter(xvarT,yvarT,c='b',label='Thumb',marker=',')
    ax1.plot(xvarT,yvarT)

    ax1.scatter(xvarI,yvarI,c='r',label='Index')
    plt.legend(loc='lower right')
    ax1.plot(xvarI,yvarI)
    # Stylistic aspects of the graph
    plt.xlabel('X Direction')
    plt.ylabel('Y Direction')
    plt.title('Graph Depicting the Movement of Thumb and Index Finger\n In Relation to Each Other')
    plt.show()
#============================Initial Variables Sub3=============================
a = False
gc=0
song=[]
bbytes = 0
maxbytes = 0
#============================PreCompile Sounds=============================
sound1 = sa.WaveObject.from_wave_file("squiggle.wav")
sound2 = sa.WaveObject.from_wave_file("piston.wav")
sound3 = sa.WaveObject.from_wave_file("prism.wav")
#==========================================================================
# Creating initial class for the Opener GUI; this gui contains all the information for the 3 sub programs embedded into its 3 main buttons
# This GUI using simple tkinter framework, not the more stylistic ttk framework
class Parent(tk.Frame):
    def __init__(self, master):
        super(Parent, self).__init__()
        self.master = master
        # Create a custom font
        self.customFont = tkFont.Font(family="Helvetica",size=20,weight='bold')
        self.customFont2 = tkFont.Font(family="Helvetica",size=8)
        self.customFont3 = tkFont.Font(family="Helvetica",size=11)
        self.customFont4 = tkFont.Font(family="Helvetica",size=10)
        # Dissallow, changes in size in both x and y directions
        self.master.resizable(False,False)
        #change background color
        self.master.tk_setPalette(background='#e6e7f2')
        master.title("Prosthetic Hand Controller Version 1.2.1")        
        self.master.geometry("+{}+{}".format(500,170))
        #=====================================================
        self.master.config(menu = tk.Menu(self.master))
        self.label = Label(master,font=self.customFont, text="The Prosthetic Hand Controller!")
        self.label.grid(row=0,column=1)

        tk.Message(master, text="Please select which Subprogram you would like to run before continuing.",font=self.customFont3,aspect=897).grid(row=2,column=1)

        self.option_first = tk.Label(master,font=self.customFont4, text ='SubProgram 1: Calculates output gear speed based on user input.  ').grid(row=4,column=1, sticky='w')
        tk.Button(master,font=self.customFont2, text='Sub Program 1',bg='#686c72',command=self.subprogramOne).grid(row=4,column=2)

       
        self.option_first = tk.Label(master,font=self.customFont4, text ='SubProgram 2: Allows user to modify the movement of the fingers.    ',).grid(row=6,column=1, sticky='w')
        tk.Button(master,font=self.customFont2, text='Sub Program 2',bg='#686c72',command=self.subprogramTwo).grid(row=6,column=2)

        self.option_first = tk.Label(master,font=self.customFont4, text ='SubProgram 3: Allows user to create music using the movement of the fingers.').grid(row=8,column=1, sticky='w')
        tk.Button(master,font=self.customFont2, text='Sub Program 3',bg='#686c72',command=self.subprogramThree).grid(row=8,column=2)
        # Make sure you include "master" as first attribute when placing widgets and not self
        # this idetfies the 'positions' of the various attributes of the opener gui
        self.label = Label(master).grid(row=9,stick='e')
        self.label = Label(master).grid(row=7,column=4)
        self.label = Label(master).grid(row=1,stick='e')
        self.label = Label(master).grid(row=5,stick='e')
        self.label = Label(master).grid(row=3,stick='e')
        
        tk.Button(master,font=self.customFont2, text='OK',bg='#31ed63', default='active',command=self.click_ok).grid(row=10,column=2 )
        tk.Button(master,font=self.customFont2, text='Cancel',bg='#ed3131',command=self.click_cancel).grid(row=10, column=3)
        
        #=============================User Control=============================

        self.master.bind('<Return>',self.return_ok)
        self.master.bind('<Escape>',self.esc_cancel)
        
        # On Click Functions
    def click_ok(self):
        print("The user clicked 'OK'")
        pass

    def click_cancel(self):
        #print("The user clicked 'Cancel'")
        self.master.destroy()

    def return_ok(self,arg):
        print("The user clicked 'OK'")

    def esc_cancel(self,arg):
        #print("The user clicked 'Cancel'")
        self.master.destroy()
    #=======================================================================================Initializing subprogram 1==============================
    def subprogramOne(arg):
        #=======================================================
        #=======================Button Functions========================
        # this on click function perfroms the calulations for sub 1
        def runSub1():
            #get other team number
            otherTeamNumber = teamNumberR.get()
            answer = calculationsSubprogram1(otherTeamNumber)
            #Clear TextBoxes if necessary
            if len(otherTeamNumberOutR.get()) > 0:
                clearSub1()
            if len(answer) == 5:
                otherTeamNumberOutR.insert(0,answer[0])
                inputSpeedOutR.insert(0,answer[1])
                outputSpeedOutR.insert(0,answer[2])
                gearRatioOutR.insert(0,answer[3])
                calcCheck.insert(0,answer[4])
            else:# len(answer) == 1:
                calcCheck.insert(0,answer)
        # this on click event clears all the text boxes 
        def clearSub1():
            calcCheck.delete(0,'end')
            teamNumberR.delete(0,'end')
            otherTeamNumberOutR.delete(0,'end')
            inputSpeedOutR.delete(0,'end')
            outputSpeedOutR.delete(0,'end')
            gearRatioOutR.delete(0,'end')
            #pass

        # different approach to making the GUI's encorporating the ttk framework instead of tk
        # specifcs are not explained
        sub1 = Tk()
        sub1.title('Subprogram 1')
        sub1.resizable(False, False)
        contentSub1 = ttk.Frame(sub1, padding=(3,3,12,12))
        #=======Font======
        sub1Font = tkFont.Font(family = 'Helvetica', size=11)
        #======Border=====
        sub1Frame = ttk.Frame(contentSub1)
        #======Widgets====
        header1 = ttk.Label(contentSub1,font=sub1Font, text='Subprogram 1')
        teamNumberQ = ttk.Label(contentSub1, text='Please enter your team number: ')
        otherTeamNumberOut = ttk.Label(contentSub1, text = 'Your team number is: ')
        inputSpeedOut = ttk.Label(contentSub1, text = 'The given input speed in RPM is: ')
        outputSpeedOut = ttk.Label(contentSub1, text = 'The calculated output speed in RPS is: ')
        gearRatioOut = ttk.Label(contentSub1, text = 'The gear ratios is: ')
        teamNumberR = ttk.Entry(contentSub1)
        otherTeamNumberOutR = ttk.Entry(contentSub1)
        inputSpeedOutR = ttk.Entry(contentSub1)
        outputSpeedOutR = ttk.Entry(contentSub1)
        gearRatioOutR = ttk.Entry(contentSub1)
        # Buttons
        sub1Calculation = ttk.Button(contentSub1, text='Calculate',command=runSub1)
        calcCheck = ttk.Entry(contentSub1)
        sub1Clear = ttk.Button(contentSub1, text='Clear',command=clearSub1)
        #=====Grid=========
        contentSub1.grid(column=0,row=0,sticky=(N, S, E, W))
        sub1Frame.grid(column=0, row=0,columnspan=2, sticky=(N, S, E, W))
        header1.grid(column=0,row=0,columnspan=2)
        teamNumberQ.grid(column=0,row=1,sticky=(W))
        teamNumberR.grid(column=0,row=2,columnspan=2,sticky=(W,E),pady=3)
        sub1Calculation.grid(column=0,row=3, columnspan=2)
        calcCheck.grid(column=0,row=4,columnspan=2,sticky=(W,E),pady=3)
        otherTeamNumberOut.grid(column=0,row=5,sticky=(W))
        otherTeamNumberOutR.grid(column=0,row=6,columnspan=2,sticky=(W,E),pady=3)
        inputSpeedOut.grid(column=0,row=7,sticky=(W))
        inputSpeedOutR.grid(column=0,row=8,columnspan=2,sticky=(W,E),pady=3)
        outputSpeedOut.grid(column=0,row=9,sticky=(W))
        outputSpeedOutR.grid(column=0,row=10,columnspan=2,sticky=(W,E),pady=3)
        gearRatioOut.grid(column=0,row=11,sticky=(W))
        gearRatioOutR.grid(column=0,row=12,columnspan=2,sticky=(W,E),pady=3)
        sub1Clear.grid(column=0,row=13, columnspan=2,pady=(3,0))

        sub1.geometry("+{}+{}".format(300,20))
        #sub2.geometry('320x190')
        sub1.mainloop()
        #=======================================================
        return
    # functions and the GUI for subprogram 3
    def subprogramTwo(arg):
        #=====================Button Functions====================
        # clear subprogram 2's text boxes
        def clearSub2():
            inputSPQ.delete(0,'end')
            inputMRQ.delete(0,'end')
            inputRIQ.delete(0,'end')
            outputMessage.delete(0,'end')
        # Run sub2 as name implies
        def runSub2():
            # begins by collecting the information from the various text boxes
            # not the best checker for functionality, but it relatively works
            # first input
            firstInput = inputSPQ.get()
            if '1' in firstInput:
                startingPosition = 1
            elif '0' in firstInput:
                startingPosition = 0
            else:
                outputMessage.delete(0,'end')
                # appends error message to the gui box
                outputMessage.insert(0,'Error 101: Invalid Input. Try Again.')
                return
            # second input
            secondInput = inputMRQ.get()
            # all inputed values are strings so they must be converted into floats first
            # TRY and EXCEPT statement to work around any errors for like text in the box instead of integers, same conditional statement is applied for input #3
            try:
                numRotations = abs(float(secondInput))
            except ValueError:
                outputMessage.delete(0,'end')
                outputMessage.insert(0, 'Error 101: Invalid Input. Try Again.')
                return
            #third input
            thirdInput = inputRIQ.get()
            # this number should be an integer
            try:
                numIncrements = int(thirdInput)
            except (ValueError, TypeError) as e:
                outputMessage.delete(0,'end')
                outputMessage.insert(0, 'Error 101: Invalid Input. Try Again.')
                return
            # call final function, delete output message contents, print new message
            if len(outputMessage.get()) > 1:
                outputMessage.delete(0,'end')
            outputMessage.insert(0, 'Computation Succesful! Movement information is printed to Idle Command Line and Saved to .txt file.')
            # Since a lot of information to be computed, I did not create a gui box for them, I simply placed these value directly on idle command line and
            # qued users to check this command or text file to see these values
            # calling the predefined mover function
            mover_(startingPosition,numRotations,numIncrements)
            
        #=====================Window=========================
        # this window is for subprogram ; same ttk format as in sub 1; again not explained in detail
        sub2 = Tk()
        sub2.title('Subprogram 2')
        sub2.resizable(False,False)
        content2 = ttk.Frame(sub2, padding=(3,3,12,12))
        #========Font=========
        sub2Font = tkFont.Font(family = 'Helvetica', size=11)
        #========Border=======
        sub2Frame = ttk.Frame(content2)
        #========Widgets======
        header2 = ttk.Label(content2,font=sub2Font, text='Subprogram 2')
        startingPositionQ = ttk.Label(content2, text='What is the starting position of the forefinger-tip and thumb-tip?')
        startingPositionQ2 = ttk.Label(content2, text='Enter: 0- Fully Closed 1- Fully Opened')
        inputSPQ = ttk.Entry(content2)

        motorRotaionQ = ttk.Label(content2, text = 'How many times would you like the motor to rotate?')
        inputMRQ = ttk.Entry(content2)

        rotationIncrementsQ = ttk.Label(content2, text = 'Please enter the number of rotational increments')
        inputRIQ = ttk.Entry(content2)

        doSub2 = ttk.Button(content2, text='Calculate', command=runSub2)
        clearSub2 = ttk.Button(content2, text='Clear All', command=clearSub2)
        outputMessageLabel = ttk.Label(content2, text='Subprogram 2 Output:')
        outputMessage = ttk.Entry(content2, text='')
        #========Grid=========
        content2.grid(column=0,row=0,sticky=(N, S, E, W))
        sub2Frame.grid(column=0, row=0,columnspan=2, sticky=(N, S, E, W))
        header2.grid(column=0,row=0,columnspan=2)
        startingPositionQ.grid(column=0,row=1,sticky=(W))
        startingPositionQ2.grid(column=0,row=2,sticky=(W))
        inputSPQ.grid(column=0,row=3,columnspan=2,sticky=(E,W),pady=3)
        motorRotaionQ.grid(column=0,row=4,sticky=(W))
        inputMRQ.grid(column=0,row=5,columnspan=2,sticky=(E,W),pady=3)
        rotationIncrementsQ.grid(column=0,row=6,sticky=(W))
        inputRIQ.grid(column=0,row=7,columnspan=2,sticky=(E,W),pady=3)
        doSub2.grid(column=0,row=9,columnspan=2)
        clearSub2.grid(column=0,row=12, columnspan=2,pady=(3,0))
        outputMessageLabel.grid(column=0,row=10,sticky=(W))
        outputMessage.grid(column=0,row=11,columnspan=2,sticky=(E,W),pady=(3,0))
        #========Position=====
        sub2.geometry("+{}+{}".format(800,20))
        sub2.mainloop()
        # ^^ is a loop the gui
        return
    # This is the function to begin subprogram 3, it includes the required custom functions for the guis functionality
    def subprogramThree(arg):
    	# Opens Sub3 Window
    	# Reinserted Functions
    	#=========================================================================================
                # clears the text boxes
                def clear():
                    global bbytes
                    bbytes = 0
                    progress["value"] = 0
                    outputArr.delete(0,'end')
                    
                # essentially a for loop to demonstarte the progressive time increase of the user once the start button has been clicked
                # Uses the after loop for every 100ms to append a new value to the contents of the progressive bar
                # global values had to be declared for functionallity
                def read_bytes():
                    global bbytes
                    global maxbytes
                    # for loop adding 500 pixels to the current number; the vaye maxes at 300,000 bytes
                    # variables called bbytes instead of bytes as bytes as a special name in python (in case you were wondering)
                    bbytes = bbytes + 500
                    # appending to the progress bar
                    progress["value"] = bbytes
                    if bbytes < maxbytes:
                        # read more bytes after 100 ms
                        # this is the loop
                        rooty.after(100, read_bytes)

                def start():
                    # this begins the appending of values to the progress bare bar by calling the read_bytes function at the end of function; as mentioned
                    # before, the read_bytes function is iterable overitself as long as the # of bytes does not become larger than maxbytes 300,000
                    global a
                    a = True
                    progress["value"] = 15000
                    global maxbytes
                    maxbytes = 300000
                    progress["maximum"] = 300000
                    read_bytes()
                    
                # Custom sound sample (VBS- text to wav compressed and Batch - ffmpeg (mp3 to uncompressed wav) used for creating and editing text files)
                # sound files 'borrowed' (with permission of course) from source code of patatap website (patatap.com)
                def sampler_():
                    # process all files
                    part1 = sa.WaveObject.from_wave_file("part1.wav")
                    part2 = sa.WaveObject.from_wave_file("part2.wav")
                    part3 = sa.WaveObject.from_wave_file("squiggle.wav")
                    part4 = sa.WaveObject.from_wave_file("part3.wav")
                    part5 = sa.WaveObject.from_wave_file("piston.wav")
                    part6 = sa.WaveObject.from_wave_file("part4.wav")
                    part7 = sa.WaveObject.from_wave_file("prism.wav")
                    #play each files
                    player = part1.play()
                    time.sleep(3)
                    player2 = part2.play()
                    time.sleep(1)
                    player3 = part3.play()
                    time.sleep(1)
                    player4 = part4.play()
                    time.sleep(1)
                    player5 = part5.play()
                    time.sleep(1)
                    player6 = part6.play()
                    time.sleep(1)
                    player7 = part7.play()
                    return
                # appending of sound 1 to the the 'song' string // should also enduce motion of fingers however gpio.rpi will not run on windows
                def soundOne():
                    global a
                    a = not a
                    global bbytes
                    bbytes = bbytes + 15000
                    progress["value"] = bbytes
                    global song
                    song = song + [0,1,0,0]
                    global gc
                    gc +=3
                    # time offset allowed for movement of hands from opened to closed position
                    time.sleep(3)
                    a = not a
                    
                # appending sound 2
                def soundTwo():
                    global a
                    a = not a
                    global bbytes
                    bbytes = bbytes + 15000
                    progress["value"] = bbytes
                    global song
                    song = song + [0,2,0,0]
                    global gc
                    gc +=3
                    time.sleep(3)
                    a = not a
                # appending sound 3
                def soundThree():
                    global a
                    a = not a
                    global bbytes
                    bbytes = bbytes + 15000
                    progress["value"] = bbytes
                    global song
                    song = song + [0,3,0,0]
                    global gc
                    gc +=3
                    time.sleep(3)
                    a = not a
                # this is an iterable function for the creation of the song; it works by contunually adding 0's for ~ 60-70's based
                # on the number of button clicks will offset this property; when button is clicked; 3 ( representing 3 seconds) is added to the gc
                # global iteration counter and an arry of either 0's 1's 2's and 3's are added to the song array
                # when gc is > 70; the songs compilation is finished and is subsequently printed an the output array
                def scanner():
                    global song
                    global gc
                    global a
                    if a:
                        song.append(0)
                        if gc <70:
                            gc+=1
                        else:
                            a = False
                            song = song[:-1]
                            outputArr.insert(0,song)
                            gc = 0
                            song = []
                    rooty.after(1000, scanner)
                # This was included to model the movement of the fingers in realtime on each click of the button
                # This is supposed to close then open but it was bugging out so this is what were working with
                # Essentially just graphing with matplotlib and using the animation library
                def movementExample_():
                    fig = plt.figure()
                    ax1 = plt.axes(xlim=(-5, 100), ylim=(55,95))
                    line, = ax1.plot([], [], lw=4)
                    plt.xlabel('X Direction')
                    plt.ylabel('Y Direction')
                    plt.title('Movement of Fingers onClick')

                    plotlays, plotcols,labels = [4], ["black","red","blue","green"],['Thumb Closing', 'Index Closing','Thumb Opening','Index Opening']
                    lines = []
                    for index in range(4):
                        lobj = ax1.plot([],[],lw=4,label=labels[index],color=plotcols[index])[0]
                        lines.append(lobj)
                        
                    plt.legend(loc='upper right')

                    def init():
                        for line in lines:
                            line.set_data([],[])
                        return lines

                    x1,y1 = [],[]
                    x2,y2 = [],[]
                    x3,y3 = [],[]
                    x4,y4 = [],[]

                    frame_num = 1000
                    indexX = 53.15
                    indexL=75
                    thumbY=26.5
                    thumbL=61


                    def angleT(arf):
                        if arf <41:
                            angleReferenceFingT = 90.554
                            thetaD = angleReferenceFingT - arf
                            thetaR = thetaD*math.pi/180
                            y_dir = thumbL*(math.sin(thetaR)) + thumbY
                            x_dir = thumbL*(math.cos(thetaR))
                            y = float("%.3f" % round(y_dir,3))
                            x = float("%.3f" % round(x_dir,3))
                            return x,y,38.756, 73.606
                        elif arf>=41 and arf <=50:
                            return 38.756, 73.606,38.756, 73.606
                        elif arf >50 and arf<91:
                            angleReferenceFingT = 50.554
                            arf = arf-51
                            thetaD = angleReferenceFingT + arf
                            thetaR = thetaD*math.pi/180
                            y_dir = thumbL*(math.sin(thetaR)) + thumbY
                            x_dir = thumbL*(math.cos(thetaR))
                            y = float("%.3f" % round(y_dir,3))
                            x = float("%.3f" % round(x_dir,3))
                            return x,y,x,y
                        else:
                            return -0.59, 87.497,-0.59, 87.497
                            

                    def angleI(arf):
                        if arf < 41:
                            angleReferenceFingI = -118.935
                            thetaD = angleReferenceFingI + arf
                            thetaR = thetaD*math.pi/180
                            y_dir = -1*indexL*(math.sin(thetaR))
                            x_dir = -1*indexL*(math.cos(thetaR)) + indexX
                            y = float("%.3f" % round(y_dir,3))
                            x = float("%.3f" % round(x_dir,3))
                            return x,y,38.756, 73.606
                        elif arf>=41 and arf <=50:
                            return 38.756, 73.606,38.756, 73.606
                        elif arf >50 and arf<91:
                            angleReferenceFingI = -78.935
                            arf = arf-51
                            thetaD = angleReferenceFingI - arf
                            thetaR = thetaD*math.pi/180
                            y_dir = -1*indexL*(math.sin(thetaR))
                            x_dir = -1*indexL*(math.cos(thetaR)) + indexX
                            y = float("%.3f" % round(y_dir,3))
                            x = float("%.3f" % round(x_dir,3))
                            return x,y,x,y
                        else:
                            return 89.436, 65.538,89.436, 65.538
                        
                    def animate(i):
                        x,y,xBlue,yBlue = angleT(i)
                        x1.append(x)
                        y1.append(y)
                        x3.append(xBlue)
                        y3.append(yBlue)

                        xx,yy,xxGreen, yyGreen= angleI(i)
                        x2.append(xx)
                        y2.append(yy)
                        x4.append(xxGreen)
                        y4.append(yyGreen)

                        xlist = [x1, x2, x3, x4]#x1,x2
                        ylist = [y1, y2,y3,y4]#y1,y2

                        #for index in range(0,1):
                        for lnum,line in enumerate(lines):
                            line.set_data(xlist[lnum], ylist[lnum]) # set data for each line separately. 

                        return lines

                    # call the animator.  blit=True means only re-draw the parts that have changed.
                    anim = animation.FuncAnimation(fig, animate, init_func=init,frames=frame_num, interval=70, blit=True)

                    plt.show()

                # functions for compiler Gui which saves and plays the song created in its parent gui window
                def compile_():
                    #==================================Compiler============================
                        #============================Functions Complier============================
                        # writing of the output array to a custom text file // just the function tho, not the onClick event
                        def write_(name,array):
                                try:
                                        name = name + '.txt'
                                        file = open(name,'w')
                                        file.write('File Name: ' + name+ '\n'+ 'Your compiled song is as follows: '+ '\n' + array)
                                        file.close()
                                except (TypeError, NameError) as e:
                                        print('Error: Invalid input. Try again.')
                        # clears the entry boxes
                        def clear_():
                            # Get clear function from morse coder
                            saveEntry.delete(0,'end')
                            inputArr.delete(0,'end')
                            
                        # on click event for button, this takes the information from array and writes it to text file; in a sense 'saving' the song
                        def save_():
                            # Essentialy, filesaver thingy
                            #get file from text entry box
                            file = saveEntry.get()
                            array = inputArr.get()
                            write_(file, array)
                        # stylistic changes to song array to make the output song more appealing
                        def split_(array,size):
                            n = size
                            line = array
                            new = [line[i:i+n] for i in range(0, len(line),n)]
                            return new
                        # this onclick events modies the song and using the predefined sound files (initalized at the very beginning of the code) it is played
                        def play_():
                            #Get song
                            song = inputArr.get()
                            #splice song -> speed up
                            sSong = split_(song,3)
                            #play song
                            # this is a time offset between the calling of new sounds to be applayed
                            delay = 0.4
                            for el in sSong:
                                val = str(el)
                                if '1' in val:
                                    #play sound clip
                                    sound1.play()
                                    #rest for 1 second
                                    time.sleep(delay)
                                elif '2' in val:
                                    #play sound clip
                                    sound2.play()
                                    #rest for 1 second
                                    time.sleep(delay)
                                elif '3' in val:
                                    #play sound clip
                                    sound3.play()
                                    #rest for 1 second
                                    time.sleep(delay)
                                else:
                                    pass
                            return
                        # Gui for the compiler; again not explaied
                        roote = Tk()
                        roote.title('D.J. Digits Compiler')
                        roote.resizable(False,False)
                        vcontent = ttk.Frame(roote, padding=(3,3,12,12))

                        #====================Font=======================
                        customFont = tkFont.Font(family="Helvetica",size=11, weight='bold')
                        #===================Border=======================
                        frame = ttk.Frame(vcontent, borderwidth=5, relief="sunken",height=30)

                        #===================Widgets=========================
                        header = ttk.Label(vcontent,font=customFont, text='D.J Digits Complier')
                        saveTxt = ttk.Label(vcontent,text='Save file as: ')
                        saveEntry = ttk.Entry(vcontent)
                        inputTxt = ttk.Label(vcontent, text='Input Array to be compiled: ')
                        inputArr = ttk.Entry(vcontent)
                        saveButton = ttk.Button(vcontent,text='Save',command=save_)
                        playButton = ttk.Button(vcontent, text='Play',command=play_)
                        clearButton = ttk.Button(vcontent, text='Clear', command=clear_)

                        #=======================Grid========================
                        vcontent.grid(column=0, row=0, sticky=(N, S, E, W))
                        frame.grid(column=0, row=0, columnspan=3, sticky=(N, S, E, W),pady=3)
                        header.grid(column=0,row=0,sticky=(E,W),padx=(3,0))
                        saveTxt.grid(column=0,row=1,sticky=(N,W))
                        saveEntry.grid(column=0,row=2,columnspan=3,sticky=(N,E,W),pady=5)
                        inputTxt.grid(column=0,row=3,sticky=(W))
                        inputArr.grid(column=0,row=4,columnspan=3,sticky=(N,E,W),pady=5)
                        saveButton.grid(column=0,row=5,sticky=(N))
                        playButton.grid(column=1,row=5,sticky=(N),padx=(0,30))
                        clearButton.grid(column=2,row=5,sticky=(N,W))


                        #====================Position==========================
                        roote.geometry("+{}+{}".format(0,400))
                        roote.mainloop()
    	#=========================================================================================
                # Gui for the song creation section of sub program 3; final gui; again not explained in detail
                rooty = Tk()
                rooty.title('D.J. Digits')
                rooty.resizable(False,False)
                content = ttk.Frame(rooty, padding=(3,3,12,12))
                bbytes = 0
                maxbytes = 0
	#====================Font=======================
                customer = tkFont.Font(family="Helvetica",size=11, weight='bold')
                customFonted = tkFont.Font(family="Helvetica",size=9, weight='bold')
        #===================Border=======================
                frame = ttk.Frame(content, borderwidth=5, relief="sunken",height=30)

	#===================Widgets=========================
                header = ttk.Label(content,font=customer, text='D.J. Digits')
                startBut = ttk.Button(content,text='Start', command=start)
	#Sound Buttons
                instruct = ttk.Label(content,font=customFonted, text='Instructions:')
                instruct1 = ttk.Label(content, text = '1: Touch each button to start finger movement.')
                instruct2= ttk.Label(content, text='2: When the fingers touch, the specific sound is appended to your song.')
                instruct3 = ttk.Label(content, text = '3: Compile your song by pasting output array into input Array.')
                instruct4 = ttk.Label(content, text = '4: Click "Play" and listen to your very own D.J. Digits Song!')
                instruct5 = ttk.Label(content, text= 'Click "Movement" button to see the movement of the fingers')
                instruct6= ttk.Label(content,text=  'graphically modelled.')
                firstSound = ttk.Button(content,text='Squiggle', command=soundOne)
                secondSound = ttk.Button(content,text='Piston', command=soundTwo)
                thirdSound = ttk.Button(content,text='Prism', command=soundThree)
                # Movement Button
                movement = ttk.Button(content, text='Movement', command=movementExample_)
                # End
                compiler = ttk.Button(content,text='Compile',command=compile_)
                clearbut = ttk.Button(content,text='Clear', command=clear)
                progress = ttk.Progressbar(content,orient='horizontal',length=200,mode='determinate')
                sampler = ttk.Button(content, text='Sample', command=sampler_)
                outputArr = ttk.Entry(content)

	#=======================Grid========================
                content.grid(column=0, row=0, sticky=(N, S, E, W))
                frame.grid(column=0, row=0, columnspan=4, sticky=(N, S, E, W),pady=3)
                instruct.grid(column=0,row=1, sticky=(W),columnspan=4)
                instruct1.grid(column=0,row=2,sticky=(W),columnspan=4)
                instruct2.grid(column=0,row=3,sticky=(W),columnspan=4)
                instruct3.grid(column=0,row=4,sticky=(W),columnspan=4)
                instruct4.grid(column=0,row=5,sticky=(W),columnspan=4)
                instruct5.grid(column=0,row=6,sticky=(W),columnspan=4)
                instruct6.grid(column=0,row=7,sticky=(W),columnspan=4)
                movement.grid(column=2, row = 8, sticky=(N))
                header.grid(column=1, row=0, columnspan=2)
                sampler.grid(column=1,row=8,sticky=(N))
                progress.grid(column=0,row=9,sticky=(N,E,S,W),columnspan=4,pady=5)
                startBut.grid(column=0,row=10,sticky=(N,W))
                firstSound.grid(column=1,row=10,sticky=(N))
                secondSound.grid(column=2,row=10,sticky=(N,W))
                thirdSound.grid(column=3,row=10,sticky=(N,E))
                outputArr.grid(column=0,row=11,sticky=(N,E,W,S), columnspan=4,pady=5)
                compiler.grid(column=1,row=12,sticky=(N))
                clearbut.grid(column=2,row=12,sticky=(N))

	#====================Position==========================
                rooty.geometry("+{}+{}".format(0,0))
                rooty.after(1000,scanner)
                rooty.mainloop()
#==============================================================================
root = Tk()
my_gui = Parent(root)
# looping the PARENT Gui (class gui - Parent GUI)
root.mainloop()
