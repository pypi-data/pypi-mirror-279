#############################################################################################
# CREATOR:  ANJAL.P                                                                         #
# ON:       2020 NOV.                                                                       #
# AIM:      To Extend the capability of the PySide2 and PyQt5 Python library with easy to   #
#           use extension containing commonly used widgets which is not natively supported  #
#           by the Qt Frame work (or atleast for Python version of Qt).                     #
# VERSION:  v1.0.0                                                                          #
# NOTES:    CLASS : SpiralProgressBar : Can be accessed by : importing                      #
#           from PySideExtn.SpiralProgressBar import SpiralProgressBar                     #
# REFER:    Github: https://github.com/anjalp/PySideExtn                                   #
#############################################################################################


from qtpy import QtWidgets, QtCore
from qtpy.QtCore import Qt, QSize, QEvent
from qtpy.QtGui import QBrush, QColor, QPainter, QPen, QPaintEvent, QFont, QResizeEvent, QLinearGradient

class SpiralProgressBar(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(SpiralProgressBar, self).__init__(parent)

        self.positionX = 0 
        self.positionY = 0
        self.Size = 0
        self.posFactor = 0
        self.sizeFactor = 0

        self.maximSize = (0, 0)
        self.minimSize = (0, 0)

        self.noProgBar = 3

        self.value = [-48*16, -24*16, -12*16]
        self.minimValue = [0, 0, 0]
        self.maximValue = [100, 100, 100]
        self.startPos = [self.startPosFlags.North, self.startPosFlags.North, self.startPosFlags.North]
        self.direction = [self.rotationFlags.Clockwise, self.rotationFlags.Clockwise, self.rotationFlags.Clockwise]

        self.lineWidth = 5
        self.lineColor = [QColor(0, 159, 227), QColor(0, 159, 227), QColor(0, 159, 227)]
        self.lineStyle = [self.lineStyleFlags.SolidLine, self.lineStyleFlags.SolidLine, self.lineStyleFlags.SolidLine]
        self.lineCap = [self.lineCapFlags.RoundCap, self.lineCapFlags.RoundCap, self.lineCapFlags.RoundCap]
        self.varWidth = False
        self.widthIncr = 1
        
        self.pathWidth = 5
        self.pathColor = [QColor(179, 241, 215), QColor(179, 241, 215), QColor(179, 241, 215)]
        self.pathPresent = True
        self.pathStyle = [self.lineStyleFlags.SolidLine, self.lineStyleFlags.SolidLine, self.lineStyleFlags.SolidLine]
        self.pathIndepend = False

        self.gap = self.lineWidth*2   #GAP BETWEEN THE ROUNDPROGRESS BAR MAKING A SPIRAL PROGRESS BAR.
        self.gapCngd = False
        self.cngSize = 1

        self.setMinimumSize(QSize(self.lineWidth*6 + self.pathWidth*6, self.lineWidth*6 + self.pathWidth*6))

#------------------------------------------------------CLASS ENUMERATORS
    class lineStyleFlags:
        SolidLine = Qt.SolidLine
        DotLine = Qt.DotLine
        DashLine = Qt.DashLine

    class lineCapFlags:
        SquareCap = Qt.SquareCap
        RoundCap = Qt.RoundCap

    class rotationFlags:
        Clockwise = -1
        AntiClockwise = 1

    class startPosFlags:
        North = 90*16
        South = -90*16
        East = 0*16
        West = 180*16


#------------------------------------------------------METHODS FOR CHANGING THE PROPERTY OF THE SPIRALPROGRESSBAR :SOLTS

    def eventFilter(self, obj, e: QEvent):
        if obj is self.window():
            if e.type() == QEvent.Resize:
                re = QResizeEvent(e)
                self.resize(re.size())

        return super().eventFilter(obj, e)
    
    def resizeEvent(self, e):
        self.adjustSize()
    
    def showEvent(self, e):
        self.adjustSize()
        super().showEvent(e)

    def setGeometry(self, posX, posY):
        """
        Set the X and Y position of the round progress bar.
        ...

        Parameters
        --------------

        posX : int
            The position of the round progress bar in int for X axis.

        posY : int
            The position of the round progress bar in int for Y axis.

        Raises
        --------------
        none
        """
        
        if self.positionX != posX:
            self.positionX = posX
        if self.positionY != posY:
            self.positionY = posY
        self.update()

    def adjustMinimumSize(self):
        """
        Minimum size calculating code: Takes consideration of the width of the line/path/circle/pie and the user defined
        width and also the size of the frame/window of the application.

        """

        Height = self.height()
        Width = self.width()
        if Width >= Height and Height >= self.minimumHeight():
            self.Size = Height
        elif Width < Height and Width >= self.minimumHeight():
            self.Size = Width

    def setNumberOfProgressBar(self, num):
        """
        By default the Number of progress bar in SpiralProgressBar is: 3,
        Users can increase the number of progress bar upto 6.(min: 2), this function
        is used to do exactly that.
        ...

        Parameters
        --------------
        num : int
            Number of progress bar.

        Raises
        --------------
        Exception : "Supported Format: int and not: " + type(num)
            raised when the user passes a non-int 'num' to the method.
        """
        if type(num)!=type(5):                            #MAKING SURE THAT THE ENTERED IS A NUMBER AND NOT A STRING OR OTHERS
            raise Exception("Supported Format: int and not: " + str(type(num)))
        if num<=6 and num>=2:
            self.noProgBar = num
            self.value = []
            self.maximValue = []
            self.minimValue = []
            self.startPos = []
            self.direction = []
            self.lineColor = []
            self.lineStyle = []
            self.lineCap = []
            for each in range(0, self.noProgBar, 1):
                self.value.append(-12*self.noProgBar*16/(each+1))
                self.maximValue.append(100)
                self.minimValue.append(0)
                self.startPos.append(self.startPosFlags.North)
                self.direction.append(self.rotationFlags.Clockwise)
                self.lineColor.append(QColor(0, 159, 227))
                self.lineStyle.append(self.lineStyleFlags.SolidLine)
                self.lineCap.append(self.lineCapFlags.RoundCap)
                self.pathColor.append(QColor(179, 241, 215))
                self.pathStyle.append(self.lineStyleFlags.SolidLine)
            self.update()


    def setValue(self, value):                                 #value: TUPLE OF (value1, value2, value3)
        """
        Set the current value of the Progress Bar. maximum value >= Value >= minimum Value
        The user can set the value of each progress bar within the spiralprogressbar independely.
        The 'value' tuple element order corresponds to the outer to inner most progressbar.
        ...

        Parameters
        --------------
        value : tuple
            Ex: value = (0, 50, 22), this means value of outermost progress bar has the value of 0, 
            midden one to 50, and innermost to 22.

        Raises
        --------------
        Exception : "Value should be a tuple and not " + type(value)
            Rasied when the user passes a non-tuple data type to the module.

        ValueError : "Tuple length more than number of Progress Bars"
            Raised when the tuple contains more element than the number of concentric progress bar in the SpiralProgressBar widget.

        ValueError : "Tuple length less than the number of Progress Bars"
            Raised when the tuple contains less element than the number of concentric progress bar in the SpiralProgressBar widget.
        """

        if type(value)!=type(()):                                  #IF INPUT IS NOT A TUPLE
            raise Exception("Value should be a Tuple and not " + str(type(value)))
        elif len(value) > self.noProgBar:                        #IF TUPLE LENGTH IS MORE THAN THE NUMBER OF PROGRESS BAR
            raise ValueError("Tuple length more than number of Progress Bars")
        elif len(value) < self.noProgBar:                        #IF INPUT TUPLE LENGTH IS LESS THAN THE NUMBER OF PROGRESS BAR
            raise ValueError("Tuple length less than the number of Progress Bars")
        elif self.value!=value:                                #IF EVERY THING GOES RIGHT
            for each in range(0, self.noProgBar, 1):
                if value[each]!='nc':                           #nc: NOC CHANGE STRING FOR ELEIMINATING THE NO CHANGE PROGRESS VALUES
                    if value[each] < self.minimValue[each]:
                        SpiralProgressBar.convValue(self, self.minimValue[each], each)
                    elif value[each] > self.maximValue[each]:
                        SpiralProgressBar.convValue(self, self.maximValue[each], each)
                    else:
                        SpiralProgressBar.convValue(self, value[each], each)
            self.update()


    def setMaximumValue(self, maxVal):
        """
        Maximum Value of the progressbar, default is 100.
        ...

        Parameters
        --------------
        maxVal : tuple
            Maximum value of each progressbar, in tuple, with elements in order 
            Ex: maxVal = (100, 200, 300) : corresponding to 100 for the outermost, 200
            for middle progress bar, 300 for innermost progressbar. 

        Raises
        --------------
        Exception : "The Max. for should be in form of a Tuple and not: " + type(maxVal)
            Rasied when the user passes a non-tuple data type to the module.

        ValueError : "Tuple length more than number of Progress Bars"
            Raised when the tuple contains more element than the number of concentric progress bar in the SpiralProgressBar widget.

        ValueError : "Tuple length less than the number of Progress Bars"
            Raised when the tuple contains less element than the number of concentric progress bar in the SpiralProgressBar widget.
        """

        if type(maxVal)!=type(()):                              #IF INPUT IS NOT A TUPLE
            raise Exception("The Max. for should be in form of a Tuple and not: " + str(type(maxVal)))
        elif len(maxVal) > self.noProgBar:                        #IF TUPLE LENGTH IS MORE THAN THE NUMBER OF PROGRESS BAR
            raise ValueError("Tuple length more than number of Progress Bars")
        elif len(maxVal) < self.noProgBar:                        #IF INPUT TUPLE LENGTH IS LESS THAN THE NUMBER OF PROGRESS BAR
            raise ValueError("Tuple length less than the number of Progress Bars")
        elif self.maximValue!=maxVal:
            for each in range(0, self.noProgBar, 1):               #TO AVOID FUTURE DIVISION BY ZERO ERROR
                if maxVal[each]==self.minimValue[each]:
                    raise ValueError("Maximum and Minimum Value Cannot be the Same")
            self.maximValue = list(maxVal)
            self.update()


    def setMinimumValue(self, minVal):
        """
        Minimum Value of the progressbar, default is 0.
        ...

        Parameters
        --------------
        minVal : tuple
            Minimum value of each progressbar, in tuple, with elements in order 
            Ex: minVal = (0, 10, 20) : corresponding to 0 for the outermost, 10
            for middle progress bar, 20 for innermost progressbar. 

        Raises
        --------------
        Exception : "The Min. for should be in form of a Tuple and not: " + type(minVal)
            Rasied when the user passes a non-tuple data type to the module.

        ValueError : "Tuple length more than number of Progress Bars"
            Raised when the tuple contains more element than the number of concentric progress bar in the SpiralProgressBar widget.

        ValueError : "Tuple length less than the number of Progress Bars"
            Raised when the tuple contains less element than the number of concentric progress bar in the SpiralProgressBar widget.
        """

        if type(minVal)!=type(()):                              #IF INPUT IS NOT A TUPLE
            raise Exception("The Min. for should be in form of a Tuple and not: " + str(type(minVal)))
        elif len(minVal) > self.noProgBar:                        #IF TUPLE LENGTH IS MORE THAN THE NUMBER OF PROGRESS BAR
            raise ValueError("Tuple length more than number of Progress Bars")
        elif len(minVal) < self.noProgBar:                        #IF INPUT TUPLE LENGTH IS LESS THAN THE NUMBER OF PROGRESS BAR
            raise ValueError("Tuple length less than the number of Progress Bars")
        elif self.minimValue!=minVal:
            for each in range(0, self.noProgBar, 1):               #TO AVOID FUTURE DIVISION BY ZERO ERROR
                if minVal[each]==self.maximValue[each]:
                    raise ValueError("Maximum and Minimum Value Cannot be the Same")
            self.minimValue = list(minVal)
            self.update()


    def setRange(self, minTuple, maxTuple):
        """
        This function does the job of setting the Maximum value and Minimum value in one go.
        ...

        Parameters
        --------------
        maxTuple : tuple
            Maximum value of each progressbar, in tuple, with elements in order 
            Ex: maxVal = (100, 200, 300) : corresponding to 100 for the outermost, 200
            for middle progress bar, 300 for innermost progressbar. 

        minVal : tuple
            Minimum value of each progressbar, in tuple, with elements in order 
            Ex: minVal = (0, 10, 20) : corresponding to 0 for the outermost, 10
            for middle progress bar, 20 for innermost progressbar. 

        Raises
        --------------
        Exception : "The Minimum and Maximum should be a Tuple"
            Rasied when the user passes a non-tuple data type to the module.

        ValueError : "Tuple length more than number of Progress Bars"
            Raised when the tuple contains more element than the number of concentric progress bar in the SpiralProgressBar widget.

        ValueError : "Tuple length less than the number of Progress Bars"
            Raised when the tuple contains less element than the number of concentric progress bar in the SpiralProgressBar widget.
        """

        if type(minTuple)!=type(()) or type(maxTuple)!=type(()):
            raise Exception("The Minimum and Maximum should be a Tuple")
        elif len(minTuple) > self.noProgBar or len(maxTuple) > self.noProgBar:
            raise ValueError("Minimum/Maximum Tuple length exceeds the number of Progress Bar")
        elif len(minTuple) < self.noProgBar or len(maxTuple) < self.noProgBar:
            raise ValueError("Minimum/Maximum Tuple length is less than the number of Progress Bar")
        for each in range(0, self.noProgBar, 1):
            if minTuple[each]==maxTuple[each]:
                raise ValueError("Minimum and Maximum cannot be the Same")
        self.minimValue = minTuple
        self.maximValue = maxTuple
        self.update()


    def setGap(self, gap):
        """
        Set the Gap between each concentric circle in the SpiralProgressBar.
        Default is : gap = 2*line width
        ...

        Parameters
        --------------
        gap : int
        Try different settings by passing an int to the function: 'int' corresponds to the "px" seperation
        between the concentric circles.  

        Raises
        --------------
        Exception : "Gap should be an integer and not: " + type(gap)
            Rasied when the user passes a non-tuple data type to the module.
        """

        if type(gap)!=type(5):
            raise ValueError("Gap should be an integer and not: " + str(type(gap)))
        else:
            self.gap = gap
            self.gapCngd = True
            self.update()


    def setInitialPos(self, position):
        """
        Sets the statring point of the progress bar or the 0% position.
        Default is 'North'
        ...

        Parameters
        --------------
        position : tuple
            The tuple elements accepts only string of : 'North', 'South', 'East' and 'West'.
            The order of arrangment matters i.e. the first element corresponds to the outer most concentric 
            progress bar and the last element correspinds to the innermost circle. 
            Ex : position = ('North', 'South', 'East')

        Raises
        --------------
        Exception : "Position should be a Tuple and not " + type(position)
            Rasied when the user passes a non-tuple data type to the module.

        ValueError : "Tuple length more than number of Progress Bars"
            Raised when the tuple contains more element than the number of concentric progress bar in the SpiralProgressBar widget.

        ValueError : "Tuple length less than the number of Progress Bars"
            Raised when the tuple contains less element than the number of concentric progress bar in the SpiralProgressBar widget.
        """

        if type(position)!=type(()):                                  #IF INPUT IS NOT A TUPLE
            raise Exception("Position should be a Tuple and not " + str(type(position)))
        elif len(position) > self.noProgBar:                        #IF TUPLE LENGTH IS MORE THAN THE NUMBER OF PROGRESS BAR
            raise ValueError("Tuple length more than number of Progress Bars")
        elif len(position) < self.noProgBar:                        #IF INPUT TUPLE LENGTH IS LESS THAN THE NUMBER OF PROGRESS BAR
            raise ValueError("Tuple length less than the number of Progress Bars")
        else:
            for each in range(0, self.noProgBar, 1):
                if type(position[each])!=type("string"):
                    raise Exception("Position Tuple elements should be String and not: " + str(type(position[each])))
                elif position[each]=='North':
                    self.startPos[each] = self.startPosFlags.North
                elif position[each]=='South':
                    self.startPos[each] = self.startPosFlags.South
                elif position[each]=='East':
                    self.startPos[each] = self.startPosFlags.East
                elif position[each]=='West':
                    self.startPos[each] = self.startPosFlags.West
                else:
                    raise Exception("Position can hold Property: 'North', 'South', 'East' and 'West' and not: " + position[each])
            self.update()


    def reset(self):
        """
        Resets the progress bar to the 0%.
        ...

        Parameters
        --------------
        none

        Raises
        --------------
        none
        """

        for each in range(0, self.noProgBar, 1):
            SpiralProgressBar.convValue(self, self.minimValue[each], each)
        self.update()


    def setGeometry(self, posX, posY):
        """
        This module changes the position of the widget. Default it is : (0, 0).
        ...

        Parameters
        --------------
        posX : int
            The vertical position of the widget from the top of the window inside which the widget lies.
            By default it is 0. The user can change the position to better suite his style and positioning of the
            widget.

        posY : int

        Raises
        --------------
        Exception : Position should be an int
            If the user passes a non-int data type.
        """ 

        if type(posX)!=type(5) or type(posY)!=type(5):
            raise Exception("Position should be a int and not: X" + str(type(posX))) + ", Y: " + str(type(posY))
            return
        if self.positionX!=posX:
            self.positionX = posX
        if self.positionY!=posY:
            self.positionY = posY
        self.update()


    def setDirection(self, direction):
        """
        Direction of rotation of the spiral progress bar.
        ...

        Parameters
        --------------
        direction : tuple
            Direction that the round progress bar can hold are : 'Clockwise' and 'AntiClockwise'
            Default is 'Clockwise'. The tuple take string as elements corresponding to the direction of
            each of the concentric circles.

        Raises
        --------------
        Exception : "Direction should be a Tuple"
            Rasied when the user passes a non-tuple data type to the module.

        ValueError : "Tuple length more than number of Progress Bars"
            Raised when the tuple contains more element than the number of concentric progress bar in the SpiralProgressBar widget.

        ValueError : "Tuple length less than the number of Progress Bars"
            Raised when the tuple contains less element than the number of concentric progress bar in the SpiralProgressBar widget.

        Exception : "Direction Tuple elements should be String"
            Rasies when the elements of the tuple is not a string.
        """

        if type(direction)!=type(()):                                  #IF INPUT IS NOT A TUPLE
            raise Exception("Direction should be a Tuple and not " + str(type(direction)))
        elif len(direction) > self.noProgBar:                        #IF TUPLE LENGTH IS MORE THAN THE NUMBER OF PROGRESS BAR
            raise ValueError("Tuple length more than number of Progress Bars")
        elif len(direction) < self.noProgBar:                        #IF INPUT TUPLE LENGTH IS LESS THAN THE NUMBER OF PROGRESS BAR
            raise ValueError("Tuple length less than the number of Progress Bars")
        else:
            for each in range(0, self.noProgBar, 1):
                if type(direction[each])!=type("String"):
                    raise Exception("Direction Tuple elements should be String and not: " + str(type(direction[each])))
                elif direction[each]=='Clockwise':
                    self.direction[each] = self.rotationFlags.Clockwise
                elif direction[each]=='AntiClockwise':
                    self.direction[each] = self.rotationFlags.AntiClockwise
                else:
                    raise Exception("Direction can hold Property: 'Clockwise'/'AntiClockwise' and not: " + str(type(direction[each])))
            self.update()


    def variableWidth(self, inp):
        """
        A flag for varing the progress bar size.
        ...

        Parameters
        --------------
        inp : bool
            True : Changes the size of the width of line progressely.

        Raises
        --------------
        Exception : Variable width should be a bool : True/False
            Rasied when the user passes a non-bool data type to the module.
        """

        if type(inp)!=type(True):
            raise Exception("Variable Width should be a Bool and not " + str(type(inp)))
        else:
            self.varWidth = inp
            self.update()


    def widthIncrement(self, increm):
        """
        Width increment for incrment in the line width. Default is 1px. User can sepcify the
        amount of px to increment form the outer to inner circle progressbar.
        ...

        Parameters
        --------------
        incrment : int
            Increment passed to the module as int px.

        Raises
        --------------
        Exception : Increment should be an integer
            Rasied when the user passes a non-int data type to the module.
        """

        if type(increm)!=type(5):
            raise Exception("Increment should be an integer and not " + str(type(increm)))
        else:
            self.widthIncr = increm
            self.update()


    def setLineWidth(self, width):
        """
        Line width of the circles in the spiral progress bar.
        ...

        Parameters
        --------------
        width : int

        Raises
        --------------
        Exception : Width should be an Integer
            Rasied when the user passes a non-int data type to the module.
        """

        if type(width)!=type(5):
            raise Exception("Width should be an Integer and not " + str(type(width)))
        else:
            self.lineWidth = width
            if self.gapCngd!=True:
                self.gap = self.lineWidth*2
            self.update()

    def setLineColor(self, colors):
        """
        Set the color of lines in the spiral progress bar. Each concentric progress bar has its own color settings.

        Parameters
        ----------
        colors : tuple
            A tuple of QColor objects. Each QColor corresponds to the color of each line.
            Example: colors = (QColor(28, 129, 196), QColor(90, 193, 211))
            The order of the QColor objects corresponds to the order of the progress bars from outermost to innermost.

        Raises
        ------
        TypeError
            Raised if the input is not a tuple or if any element in the tuple is not a QColor instance.
        ValueError
            Raised if the tuple contains more or fewer elements than the number of concentric progress bars.
        """
        
        if not isinstance(colors, tuple):
            raise TypeError(f"Colors should be a tuple, got {type(colors).__name__}")

        if len(colors) != self.noProgBar:
            raise ValueError(f"Expected {self.noProgBar} color tuples, but got {len(colors)}")

        for color in colors:
            if not isinstance(color, QColor) and  not isinstance(color, QLinearGradient):
                raise TypeError(f"Each color must be a QColor instance, got {type(color).__name__}")

        for i in range(self.noProgBar):
            if self.lineColor[i] != colors[i]:
                self.lineColor[i] = colors[i]

        self.update()



    def setLineStyle(self, style):
        """
        line style of the spiral progress bar.
        ...

        Parameters
        --------------
        style : tuple
            Style types : 'SolidLine', 'DotLine' and 'DashLine'.
            Users can pass the style for each progress bar in the order : first element corresponds 
            to the styleof outermost progressbar and viceversa.

        Raises
        --------------
        Exception : Style should be a tuple
            Rasied when the user passes a non-tuple data type to the module.

        ValueError : "Tuple length more than number of Progress Bars"
            Raised when the tuple contains more element than the number of concentric progress bar in the SpiralProgressBar widget.

        ValueError : "Tuple length less than the number of Progress Bars"
            Raised when the tuple contains less element than the number of concentric progress bar in the SpiralProgressBar widget.
        """

        if type(style)!=type(()):
            raise Exception("Style should be a tuple and not: " + str(type(style)))
        elif len(style) > self.noProgBar:                        #IF TUPLE LENGTH IS MORE THAN THE NUMBER OF PROGRESS BAR
            raise ValueError("Tuple length more than number of Progress Bars")
        elif len(style) < self.noProgBar:                        #IF INPUT TUPLE LENGTH IS LESS THAN THE NUMBER OF PROGRESS BAR
            raise ValueError("Tuple length less than the number of Progress Bars")
        else:
            for each in range(0, self.noProgBar, 1):
                if type(style[each])!=type("String"):
                    raise Exception("Style Tuple element should be a String and not: " + str(type(style[each])))
                elif style[each]=='SolidLine':
                    self.lineStyle[each] = self.lineStyleFlags.SolidLine
                elif style[each]=='DotLine':
                    self.lineStyle[each] = self.lineStyleFlags.DotLine
                elif style[each]=='DashLine':
                    self.lineStyle[each] = self.lineStyleFlags.DashLine
                else:
                    raise Exception("Style can hold 'SolidLine', DotLine' and 'DashLine' only.")
            self.update()


    def setLineCap(self, cap):
        """
        Cap i.e. the end of the line : to be Round or Square.
        ...

        Parameters
        --------------
        cap : tuple
            Cap : 'RoundCap' and 'SquareCap'.
            Users can pass the desired cap of the line as a string passed in the following order of : 
            Outer progress bar : first element in the tuple and viceversa.

        Raises
        --------------
        Exception : Cap should be a tuple
            Rasied when the user passes a non-tuple data type to the module.

        ValueError : "Tuple length more than number of Progress Bars"
            Raised when the tuple contains more element than the number of concentric progress bar in the SpiralProgressBar widget.

        ValueError : "Tuple length less than the number of Progress Bars"
            Raised when the tuple contains less element than the number of concentric progress bar in the SpiralProgressBar widget.
        """
        
        if type(cap)!=type(()):
            raise Exception("Cap should be a tuple and not: " + str(type(cap)))
        elif len(cap) > self.noProgBar:                        #IF TUPLE LENGTH IS MORE THAN THE NUMBER OF PROGRESS BAR
            raise ValueError("Tuple length more than number of Progress Bars")
        elif len(cap) < self.noProgBar:                        #IF INPUT TUPLE LENGTH IS LESS THAN THE NUMBER OF PROGRESS BAR
            raise ValueError("Tuple length less than the number of Progress Bars")
        else:
            for each in range(0, self.noProgBar, 1):
                if type(cap[each])!=type("String"):
                    raise Exception('Cap Tuple element should be a String and not a: ' + str(type(cap[each])))
                elif cap[each]=='SquareCap':
                    self.lineCap[each] = self.lineCapFlags.SquareCap
                elif cap[each]=='RoundCap':
                    self.lineCap[each] = self.lineCapFlags.RoundCap
                else:
                    raise Exception("Cap can hold 'SquareCap' and 'RoundCap' only")
            self.update()


    def setPathHidden(self, hide):
        """
        Hides the path in the spiral progress bar.
        ...

        Parameters
        --------------
        hide : bool

        Raises
        --------------
        Exception : Hidden accept a bool
            Rasied when the user passes a non-bool data type to the module.
        """

        if type(hide)!=type(True):
            raise Exception("Hidden accept a bool and not: " + str(type(hide)))
        elif hide==True:
            self.pathPresent = False
        else:
            self.pathPresent = True

    def setPathColor(self, colors):
        """
        Set the color of lines in the spiral progress bar. Each concentric progress bar has its own color settings.

        Parameters
        ----------
        colors : tuple
            A tuple of QColor objects. Each QColor corresponds to the color of each line.
            Example: colors = (QColor(28, 129, 196), QColor(90, 193, 211))
            The order of the QColor objects corresponds to the order of the progress bars from outermost to innermost.

        Raises
        ------
        TypeError
            Raised if the input is not a tuple or if any element in the tuple is not a QColor instance.
        ValueError
            Raised if the tuple contains more or fewer elements than the number of concentric progress bars.
        """
        
        if not isinstance(colors, tuple):
            raise TypeError(f"Colors should be a tuple, got {type(colors).__name__}")

        if len(colors) != self.noProgBar:
            raise ValueError(f"Expected {self.noProgBar} color tuples, but got {len(colors)}")

        for color in colors:
            if not isinstance(color, QColor):
                raise TypeError(f"Each color must be a QColor instance, got {type(color).__name__}")

        for i in range(self.noProgBar):
            for i in range(self.noProgBar):
                if self.pathColor[i] != colors[i]:
                    self.pathColor[i] = colors[i]
            self.update()



#------------------------------------------------------METHODS FOR GETTING THE PROPERTY OF SPIRALPROGRESSBAR SLOTS

#------------------------------------------------------ENGINE: WHERE ALL THE REAL STUFF TAKE PLACE: WORKING OF THE SPIRALPROGRESSBAR



    def geometricFactor(self):
        """
        Width of the line should be subrtracted from the size of the progrress bar, inorder to properly 
        fit inot the layout properly without any cut in the widget margins.
        
        ...
        Parameters
        --------------
        none.

        Return
        --------------
        none.
        """
        self.posFactor = self.lineWidth/2 + 1
        self.sizeFactor = self.lineWidth + 1


    def convValue(self, value, pos):
        """
        Convert the value from the user entered to the percentage depending on the maximum and minimum value.
        Calculagted by the relation : (value - minimum)/(maximum - minimum)
        
        ...
        Parameters
        --------------
        none.

        Return
        --------------
        none.
        """

        self.value[pos] = ((value - self.minimValue[pos])/(self.maximValue[pos] - self.minimValue[pos]))*360*16
        self.value[pos] = self.direction[pos]*self.value[pos]



    def paintEvent(self, event: QPaintEvent):
        """
        The place where the drawing takes palce.
        
        ...
        Parameters
        --------------
        none.

        Return
        --------------
        none.
        """
        self.setMinimumSize(QSize(self.lineWidth*6 + self.pathWidth*6, self.lineWidth*6 + self.pathWidth*6))
        self.setMinimumSize(self.size())

        self.adjustMinimumSize()
        self.geometricFactor()

        spiralIncrem = 0
        spiralIncrem2 = 0


        if self.pathIndepend!=True:
            self.pathWidth = self.lineWidth
        self.tempWidth = self.pathWidth
        if self.pathPresent:
            for path in range(0, self.noProgBar, 1):
                if self.varWidth==True:   #CREAETS A INCREASING OR DECREASING TYPE OF WITH 
                    self.tempWidth = self.tempWidth + self.widthIncr
                    if self.gapCngd!=True:
                        self.gap = self.tempWidth*2
                self.pathPainter = QPainter(self)
                self.pathPainter.setRenderHint(QPainter.Antialiasing)
                self.penPath = QPen()
                self.penPath.setStyle(self.pathStyle[path])
                self.penPath.setWidth(self.tempWidth)
                self.penPath.setBrush(self.pathColor[path])
                self.pathPainter.setPen(self.penPath)
                self.pathPainter.drawArc(self.positionX + self.posFactor + self.cngSize*spiralIncrem2, self.positionY + self.posFactor + self.cngSize*spiralIncrem2, self.Size - self.sizeFactor - 2*self.cngSize*spiralIncrem2, self.Size - self.sizeFactor - 2*self.cngSize*spiralIncrem2, self.startPos[path], 360*16)
                self.pathPainter.end()
                spiralIncrem2 = spiralIncrem2 + self.gap
                

        self.tempWidth = self.lineWidth   #TEMPWIDTH TEMPORARLY STORES THE LINEWIDTH, USEFUL IN VARIABLE WIDTH OPTION.
        for bar in range(0, self.noProgBar, 1):
            if self.varWidth==True:   #CREAETS A INCREASING OR DECREASING TYPE OF WITH 
                self.tempWidth = self.tempWidth + self.widthIncr
                if self.gapCngd!=True:
                    self.gap = self.tempWidth*2
            self.linePainter = QPainter(self)
            self.linePainter.setRenderHint(QPainter.Antialiasing)
            self.penLine = QPen()
            self.penLine.setStyle(self.lineStyle[bar])
            self.penLine.setWidth(self.tempWidth)
            self.penLine.setCapStyle(self.lineCap[bar])
            try:
                self.penLine.setBrush(self.lineColor[bar])
            except:
                print(self.lineColor[bar])
            self.linePainter.setPen(self.penLine)
            self.linePainter.drawArc(self.positionX + self.posFactor + self.cngSize*spiralIncrem, self.positionY + self.posFactor + self.cngSize*spiralIncrem, self.Size - self.sizeFactor - 2*self.cngSize*spiralIncrem, self.Size - self.sizeFactor - 2*self.cngSize*spiralIncrem, self.startPos[bar], self.value[bar])
            self.linePainter.end()
            spiralIncrem = spiralIncrem + self.gap

