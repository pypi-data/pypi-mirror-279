# PySideExtn

An extension for the Python PySide2, PyQt5, PySide6 or PyQt6 Qt Framework which expands the scope of the PySide2, PyQt5, PySide6 or PyQt6 package with many different modern widgets. Current release is occupied with two widget which are not natively present in the PySide2, PyQt5, PySide6 or PyQt6 package.

*RoundProgressBar*

<p align="center">
  <img src="assets/rpb.png">
</p>

*SpiralProgressBar*

<p align="center">
  <img src="assets/spb.png">
</p>

Go to [Home Page](https://khamisikibet.github.io/PySideExtn/) of Documentation for further Help

## Getting Started

* Install PySideExtn using `pip`

``` python
pip install PySideExtn
```

* Build from source: After cloning the repo, go to the directory and open `cmd` or `terminal`

``` bash
$ python3 setup.py sdist bdist_wheel
```

* Install from `.whl` file.

```python
pip install <PySideExtn------.whl>file
```

To verify that installation is complete, print out the `pip list` and search for the PySideExtn package. 

For more details go to the [Official PySideExtn Documentation Getting Started](https://khamisikibet.github.io/PySideExtn/pages/get_started)

## Quick Demo

Quick demo help you to check weather you have successfully installed the Python Package. It comes with a UI loaded with all the widgets in this package with its different customized views. Users can easily differentiate the different styling elements used by widgets.

After installing the PySideExtn/PyQtExtn the users can try out quick demo by:

1. Open the `cmd` or `terminal`. Open `Python`

```python
>> from PySideExtn.demo import demo
>> demo.main()   #PRESS ENTER AND YOU WILL GET A DEMO APPLICATION
```

<p align="center">
  <img src="assets/demo/rpb.PNG">
</p>

## Documentation

Official Documentation for PySideExtn is detailed in: [PySideExtn Documentation](https://khamisikibet.github.io/PySideExtn/).

[Getting Started](https://khamisikibet.github.io/PySideExtn/pages/get_started)

[Examples](https://khamisikibet.github.io/PySideExtn/pages/example)

[Classes](https://khamisikibet.github.io/PySideExtn/pages/classes)

[Errors and Exceptions](https://khamisikibet.github.io/PySideExtn/pages/error&exception)

[Version History](https://khamisikibet.github.io/PySideExtn/pages/version)

[FAQ's](https://khamisikibet.github.io/PySideExtn/pages/faqs)

[Official PySideExtn/PyQtExtn Form](https://forms.gle/yfKVK85sLLMJMCfJA)

## Examples

* **Default Round Progress Bar**

```python
import sys
# update this import
from PySide2, PyQt5, PySide6 or PyQt6 import QtCore, QtWidgets, QtGui

from PySideExtn.RoundProgressBar import RoundProgressBar #IMPORT THE EXTENSION LIBRARY

x = 0
p = 1

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.hello = 'Round Progress Bar'
        self.button = QtWidgets.QPushButton("Click me to change Value")
        self.text = QtWidgets.QLabel("Round Progress Bar")
        self.text.setAlignment(QtCore.Qt.AlignCenter)
        
        #CREATING THE ROUND PROGRESS BAR OBJECT
        self.rpb = RoundProgressBar()
        
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        
        # ADDING THE ROUND PROGRESS BAR OBJECT TO THE                                             # BOTTOM OF THE LAYOUT
        self.layout.addWidget(self.rpb)

        self.setLayout(self.layout)
        self.button.clicked.connect(self.magic) #BUTTON PRESSED EVENT
        
    def magic(self):
        global x, p
        x = x + 10*p
        if x==100:
            p = -1
        elif x==0:
            p = 1
        self.rpb.setValue(x)        #CHANGING THE VALUE OF THE PROGRESS BAR
        out_text = 'Round Progress Bar: ' + str(x) + '%'
        self.text.setText(out_text)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())
```

<p align="center">
  <img src="assets/rpb/rpb_demo.PNG">
</p>

In this demo, we first created an object of the Round Progress Bar:

```python
self.rpb = RoundProgressBar() #CREATING THE ROUND PROGRESS BAR OBJECT
```

After that calling the Round Progress Bar object to display the value of progress using:

```python
self.rpb.setValue(x) #CHANGING THE VALUE OF THE PROGRESS BAR
```

The `setValue(value)` takes an `int` as an argument and updates to change the value of the progress bar to the value given.

For More examples on Round Progress Bar go to: [Official PySideExtn Documentation Examples](https://khamisikibet.github.io/PySideExtn/pages/examples/rpbExamples)

* **Default Spiral Progress Bar**

```python
import sys
# update this import
from PySide2, PyQt5, PySide6 or PyQt6 import QtCore, QtWidgets, QtGui

#IMPORT THE EXTENSION  LIBRARY
from PySideExtn.SpiralProgressBar import SpiralProgressBar 

x = 0
p = 1

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.hello = 'Spiral Progress Bar'
        self.button = QtWidgets.QPushButton("Click me to change Value")
        self.text = QtWidgets.QLabel("Spiral Progress Bar")
        self.text.setAlignment(QtCore.Qt.AlignCenter)
        
        #CREATING THE SPIRAL PROGRESS BAR OBJECT
        self.spb = SpiralProgressBar()    
        
        #ADDING WIDGETS TO THE VERTICAL LAYOUT
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        
        # ADDING THE SPIRAL PROGRESS BAR OBJECT TO THE LAYOUT
        self.layout.addWidget(self.spb) 
        
        self.setLayout(self.layout)
        self.button.clicked.connect(self.magic) #BUTTON PRESSED EVENT
        
    def magic(self):
        global x, p
        x = x + 10*p
        if x==100:
            p = -1
        elif x==0:
            p = 1
            
        #CHANGING THE VALUE OF THE 3 DEFAULT PROGRESS BAR
        self.spb.setValue((x, x*2, x*3)) 
        
        out_text = 'Spiral Progress Bar: '  
        out_text = out_text + str(x) + '%, ' + str(2*x) + '%, ' + str(3*x) + '%'
        self.text.setText(out_text)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())
```

<p align="center">
  <img src="assets/spb/spb_defEx.PNG">
</p>

- Here first create a SpiralProgressBar object and then add the progress bar to a layout and control the steps of the progress bar by the clicking of the button. 

  ```python
  self.spb = SpiralProgressBar()		
  ```

- Here we create a SpiralProgressBar object instance and then use the `self.spb` as the spiral progress bar to influence its charactor like:

  ```python
  self.spb.setValue((x, x*2, x*3))
  ```

- Since the default progress bar has 3 individual concentric circle, where each can be controlled individually, we pass a tuple containing the individual value for manipulating each concentric progress bar, to the function `setValue()` , which only accepts a tuple of length equal to the number of concentric progress bar. Every function which can manipulate the properties of the Spiral Progress Bar uses the same idea. The order of entering the value are shown below:

<p align="center">
  <img src="assets/spb/spb_order.png">
</p>

For More examples on Spiral Progress Bar go to: [Official PySideExtn Documentation Examples](https://khamisikibet.github.io/PySideExtn/pages/examples/spbExamples)

## Help

- **PySideExtn/PyQtExtn is not working in my setup**: Go to Github [PySideExtn](https://github.com/khamisikibet/PySideExtn) repo. and raise an issue or just fill the official [PySideExtn/PyQtExtn Form](https://forms.gle/yfKVK85sLLMJMCfJA).
- **Unknown errors**: Raise a GitHub issue or fill the official [PySideExtn/PyQtExtn Form](https://forms.gle/yfKVK85sLLMJMCfJA)

## Support
- Please feel free to contribute to the project by sharing the idea you have, which is not natively present in the PySide2, PyQt5, PySide6 or PyQt6/PyQt5 but essential for your workflow.

- If your idea worth the use, then definitely it will be available in the next update of the PySideExtn/PyQtExtn.

:smiley: Support like this motivates me to do more creative, work for Open Source.

