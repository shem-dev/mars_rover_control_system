# Mars Rover Control System

The Mars Rover Control System is a Python PyQt GUI application which plots a grid based on user provided coordinates, allows for the creation of mars rovers on the grid and the control and tracking of the mars rovers along the coordinates of the grid. 


# Requirements
  - Python 3.6 =>
  - PyQt5 library 
  - virtualenv (In case python 3.6 => is not globally installed on your system)

# Installation

 - Navigate to your intended directory for storing this project
```sh
$ git clone https://github.com/shem-dev/mars_rover_control_system
$ cd mars_rover_control_system
$ virtualenv -p python3 pyenv
$ source pyenv/bin/activate
$ pip install -r requirements.txt
```

# How to run application
 - From the project directory
```sh
$ source pyenv/bin/activate
$ python index.py
```

### How to Use  the Application

- Select your preffered grid size on the 'Grid Settings' pane then click 'Update'
- Select the number of rovers you would like to introduce in the 'Rover Settings' pane then click 'Update'
- Select the rover you would like to move on the combo box in the 'Navigate Rover' pane then:
- Click 'M' to move the rover forward in the selected direction
- Click 'R' to turn the rover 90 degrees to the right
- Click 'L' to turn the rover 90 degrees to the left
- If the rover is about to go out of bounds, a pop-up will appear informing you of this and will request that you turn the rover to a valid direction

