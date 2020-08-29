import sys, os, shutil
from mars_rover import Ui_MainWindow, QtWidgets
from PyQt5 import QtCore, QtGui, QtWidgets
import subprocess


class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.btnUpdateGridSize.clicked.connect(self.set_new_grid)
        self.btnNumRoversUpdate.clicked.connect(self.create_rovers_list)
        self.comboRoverSelect.currentTextChanged.connect(self.load_selected_rover)
        self.btnMoveForward.clicked.connect(self.move_rover_forward)
        self.btnTurnRight.clicked.connect(self.turn_rover_right)
        self.btnTurnLeft.clicked.connect(self.turn_rover_left)
        self.scene = None
        self.rovers_dict = {}
        self.rover_coords = {}
        self.selected_rover = None
        self.set_direction = 'N'
        self.grid_x_dimension = None
        self.grid_y_dimension = None
        self.read = True
        self.rovers_list = []

        data = {"Rover Name": [], "X-Coord": [], "Y-Coord": [], "Direction": [] }
        self.table_data = data
        self.setTableData()



    def setTableData(self):
        """Set output table default layout"""
        horHeaders = []
        header = self.tableRoverInfo.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        for n, key in enumerate((self.table_data.keys())):
            horHeaders.append(key)
            for m, item in enumerate(self.table_data[key]):
                newitem = QtWidgets.QTableWidgetItem(item)
                self.tableRoverInfo.setItem(m, n, newitem)
        self.tableRoverInfo.setHorizontalHeaderLabels(horHeaders)

    def set_new_grid(self):
        """Create new grid/coordinate field"""
        self.grid_x_dimension = self.spinXGrid.value()
        self.grid_y_dimension = self.spinYGrid.value()

        self.scene = QtWidgets.QGraphicsScene()
        self.graphGridView.setScene(self.scene)
        pen = QtGui.QPen(QtCore.Qt.green)

        side = 30

        for i in range(self.grid_x_dimension):
            for j in range(self.grid_y_dimension):
                grids = QtCore.QRectF(QtCore.QPointF(i*side, j*side), QtCore.QSizeF(side, side))
                self.scene.addRect(grids, pen)

    def create_rovers_list(self):
        """Create new rovers based on user input"""
        self.set_new_grid()
        self.comboRoverSelect.blockSignals(True)
        self.comboRoverSelect.setCurrentIndex(0)
        self.comboRoverSelect.blockSignals(False)
        x_grid_coord = self.grid_x_dimension
        y_grid_coord = self.grid_y_dimension
        num_of_rovers = self.spinNumOfRovers.value()
        self.tableRoverInfo.setRowCount(0)
        self.rovers_list = []
        for x in range(num_of_rovers):
            self.rovers_dict["rover" + str(x)] = QtWidgets.QGraphicsEllipseItem((30*1) - 38, (30*y_grid_coord) - 8, 15, 15)
            self.rovers_dict["rover" + str(x)].setPen(QtGui.QPen(QtGui.QColor("blue")))
            self.rover_coords["rover" + str(x)] = [0, 0, 'N']
            self.scene.addItem(self.rovers_dict["rover"+str(x)])
            self.rovers_list.append("rover" + str(x))
            rowPosition = self.tableRoverInfo.rowCount()
            self.tableRoverInfo.insertRow(rowPosition)
        self.comboRoverSelect.clear()
        rover_names_list = self.rovers_dict.keys()
        self.comboRoverSelect.addItem("[ Select Rover ]")
        self.comboRoverSelect.addItems(rover_names_list)
        # self.table_data = {"Rover Name": self.rovers_list, "X-Coord": [], "Y-Coord": [], "Direction": [] }
        self.reset_coordinates_table_data()
        self.setTableData()
        
    def reload_rovers(self):
        """Reload rovers list after user input"""
        self.set_new_grid()
        x_grid_coord = self.grid_x_dimension
        y_grid_coord = self.grid_y_dimension
        num_of_rovers = self.spinNumOfRovers.value()

        for x in range(num_of_rovers):
            rover_coords = self.rover_coords["rover" + str(x)]
            rover_y_coord = (y_grid_coord - rover_coords[1])
            rover_x_coord = rover_coords[0]
            self.rovers_dict["rover" + str(x)] = QtWidgets.QGraphicsEllipseItem((30*(rover_x_coord + 1)) - 38, (30*rover_y_coord) - 8, 15, 15)
            self.rovers_dict["rover" + str(x)].setPen(QtGui.QPen(QtGui.QColor("blue")))
            self.scene.addItem(self.rovers_dict["rover" + str(x)])

    def reset_coordinates_table_data(self):
        """Reset coordinates table after user input"""
        x_coords_list = []
        y_coords_list = []
        dir_list = []

        for x in self.rover_coords.keys():
            x_coords_list.append(str(self.rover_coords[x][0]))
            y_coords_list.append(str(self.rover_coords[x][1]))
            dir_list.append(self.rover_coords[x][2])
        self.table_data = {"Rover Name": self.rovers_list, "X-Coord": x_coords_list, "Y-Coord": y_coords_list, "Direction": dir_list }

    def load_selected_rover(self):
        self.selected_rover = self.comboRoverSelect.currentText()
        if self.selected_rover == "[ Select Rover ]":
            pass
        else:
            try:
                curr_coords = self.rover_coords[self.selected_rover]
                self.set_direction = curr_coords[2]
            except Exception:
                pass

    def check_rover_range(self, curr_coords):
        """Check if rover is in bounds before moving"""
        out_of_range = False
        curr_x_coord = curr_coords[0]
        curr_y_coord = curr_coords[1]
        curr_rover_dir = curr_coords[2]

        if curr_x_coord == 0 and self.set_direction == "W":
            out_of_range = True
        if curr_x_coord == self.grid_x_dimension and self.set_direction == "E":
            out_of_range = True
        if curr_y_coord == 0 and self.set_direction == "S":
            out_of_range = True
        if curr_y_coord == self.grid_y_dimension and self.set_direction == "N":
            out_of_range = True
        return out_of_range


    def initiate_rover_move(self, curr_coords):
        """Move rover in direction set by user"""
        curr_x_coord = curr_coords[0]
        curr_y_coord = curr_coords[1]
        curr_rover_dir = curr_coords[2]
        if self.set_direction == "N":
            new_y_coord = curr_y_coord + 1
            self.rover_coords[self.selected_rover] = [curr_x_coord, new_y_coord, self.set_direction]
            self.reload_rovers()
        elif self.set_direction == "W":
            new_x_coord = curr_x_coord - 1
            self.rover_coords[self.selected_rover] = [new_x_coord, curr_y_coord, self.set_direction]
            self.reload_rovers()
        elif self.set_direction == "S":
            new_y_coord = curr_y_coord - 1
            self.rover_coords[self.selected_rover] = [curr_x_coord, new_y_coord, self.set_direction]
            self.reload_rovers()
        elif self.set_direction == "E":
            new_x_coord = curr_x_coord + 1
            self.rover_coords[self.selected_rover] = [new_x_coord, curr_y_coord, self.set_direction]
            self.reload_rovers()
        self.reset_coordinates_table_data()
        self.setTableData()

    def move_rover_forward(self):
        """Call initiate move function if rover is in bounds"""
        curr_coords = self.rover_coords[self.selected_rover]
        
        if self.check_rover_range(curr_coords):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('Rover is out of range, Please change direction.')
            msg.setWindowTitle("Error")
            msg.exec_()
        else:
            self.initiate_rover_move(curr_coords)

    def check_selected_rover(self):
        """Check if combobox is set to a valid selection"""
        self.selected_rover = self.comboRoverSelect.currentText()
        if self.selected_rover == "[ Select Rover ]":
            return False
        else:
            return True
    def turn_rover_right(self):
        """Turn rover 90 degrees to the right"""
        curr_dir = self.set_direction
        if curr_dir == "N":
            self.set_direction = "E"
        elif curr_dir == "W":
            self.set_direction = "N"
        elif curr_dir == "S":
            self.set_direction = "W"
        elif curr_dir == "E":
            self.set_direction = "S"
        self.reset_coordinates_table_data()
        self.setTableData()

    def turn_rover_left(self):
        """Turn rover 90 degrees to the left"""
        curr_dir = self.set_direction
        if curr_dir == "N":
            self.set_direction = "W"
        elif curr_dir == "W":
            self.set_direction = "S"
        elif curr_dir == "S":
            self.set_direction = "E"
        elif curr_dir == "E":
            self.set_direction = "N"
        self.reset_coordinates_table_data()
        self.setTableData()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())


