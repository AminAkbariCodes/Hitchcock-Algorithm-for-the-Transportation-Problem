# Hitchcock-Transportation-Problem-Solver

The Hitchcock-Transportation-Problem-Solver is a Python application that implements the Hitchcock algorithm for solving transportation problems in operations research. The software accepts supply and demand data as inputs, carries out the necessary computations guided by the Hitchcock algorithm, and provides a graphical representation of the algorithm's step-by-step process and results.


## Project Description

Transportation problems involve determining the most cost-efficient way of transporting goods from multiple supply nodes (factories) to multiple demand nodes (customers). The challenge lies in deciding the volume of goods each factory should supply to each customer while minimizing the total transportation cost and meeting the supply and demand constraints of each node.

The Hitchcock Transportation Algorithm, also known as the stepping-stone method or the MODI (Modified Distribution) method, is a common method for solving such problems. It involves finding an initial feasible solution and then iteratively improving it until an optimal solution is achieved. 

This application serves not only as an operational tool for solving transportation problems but also as an educational resource for understanding and applying the Hitchcock algorithm. 

## Getting Started

You can run this application in two ways:

1. **Running the Source Code:** Make sure to place any additional resources like images (those in the resources folder) in the same path as the source code. You need Python installed on your system to run the code. 

2. **Running the Executable File:** Download the executable file from this [link](https://drive.google.com/drive/folders/1DxIXA5hL3sJQEENOdbhqFdXavTEkFn_E?usp=drive_link). Make sure to place any additional resources like images in the same path as the executable file.

## Usage

1. Start the application.
2. Follow the prompts to input the supply and demand data.
3. Choose the method for finding the initial feasible solution.
4. The application will then solve the problem step-by-step, displaying the results graphically.

## Classes & Functions

- `TransportationProblem`: The core class of the application. It defines the problem and uses various methods to solve it.

- `State`: Tracks the current state of the problem.

- `CustomCell`: A helper class for creating custom cells in the Tkinter GUI.

- `DataInputDialog`: A helper class for creating input dialogs in the Tkinter GUI.

- `TableauGUI`: The main class for creating the graphical user interface.

- `get_inputs()`: A function that prompts the user to enter the necessary data for the problem.

- `Introduction` and `Menu`: Classes that provide a user-friendly introduction and menu to guide users through the use of the application.

## Dependencies

- numpy
- tkinter
- PIL (Pillow)
- pygame

## Contact

For any inquiries, issues, or contributions, feel free to open an issue in this repository. 

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## Acknowledgments

- Thanks to the open-source community for the continuous inspiration and resources that helped in building this project.

## License

This project is licensed under the terms of the MIT license.
