<p align="center">
  <img src="https://github.com/AminAkbariCodes/Hitchcock-Algorithm-for-the-Transportation-Problem/assets/132245731/91883895-9c3b-43db-8054-ee7dd802de8b">
</p>

<h1 align="center">University of California, Irvine</h1>
<h2 align="center">Department of Civil and Environmental Engineering</h2>
<h3 align="center">Institute of Transportation Studies</h3>

<h4 align="center">ENGRCEE 228A LEC A: URBAN TRANS NET I (15975)</h4>

<p align="center">
  <strong>Instructor</strong><br>
  Prof. Michael G. McNally
</p>

<p align="center">
  <strong>Project No.2</strong>
</p>

<p align="center">
  <strong>Written By</strong><br>
  Amin Akbari
</p>

<p align="center">
  <strong>Due Date</strong><br>
  June 20, 2023
</p>

# Hitchcock Algorithm for the Transportation Problem

The transportation problem, a type of network flow problem, is a classic optimization problem that originates from the field of operations research. It involves finding the most cost-effective way of transporting goods from factories (supply nodes) to customers (demand nodes). The challenge lies in determining the quantity of goods to be transported from each factory to each customer such that the total transportation cost is minimized and the supply and demand constraints at each node are satisfied.

One of the most widely used methods for solving transportation problems is the Hitchcock Transportation Algorithm, also known as the stepping-stone method or the MODI (Modified Distribution) method. The algorithm follows a series of steps to reach the optimal solution: starting from an initial feasible solution, it iteratively improves the solution until no further improvements can be made.

In this project, we've implemented the Hitchcock Transportation Algorithm in a Python application. We aimed to design an efficient, user-friendly tool that can take in supply and demand data, perform the necessary calculations, and visually represent the steps and results of the algorithm. We hope that this tool can serve as a valuable resource for understanding and applying the Hitchcock Transportation Algorithm.

# Overview

Our implementation of the Hitchcock Transportation Algorithm in Python involves several classes and methods that interact with one another to solve the problem. Here's a brief explanation of each part:

## TransportationProblem class

The core of our application. This class takes in the number of supply and demand nodes, their respective values, and the transportation costs. It then uses various methods to solve the transportation problem:


- `__init__`: Initializes the problem with the given parameters.
- `balance_problem`: Balances the supply and demand to ensure the total supply equals the total demand.
- `northwest_corner_rule`, `minimum_cost_rule`, `vogel_approximation_method`: These are different methods used to find an initial feasible solution to the problem.
- `calculate_shadow_prices`, `calculate_opportunity_costs`, `calculate_deltas`: These methods are used to calculate the necessary values for the stepping-stone (or MODI) method.
- `find_pivot_cell`: Identifies the cell to pivot on in the current iteration.
- `total_cost`: Calculates the total cost of the current solution.
- `identify_loop`: Identifies the loop formed by the pivot cell.
- `update_allocations`: Updates the allocations according to the loop and pivot cell.
- `has_positive_deltas`: Checks if there are any positive deltas left, i.e., if there are any improvements to be made.
- `generate_state`: Generates the current state of the problem.
- `reset`: Resets the problem to its initial state.

## State class

Keeps track of the current state of the problem, including allocations, u_values, v_values, and the iteration number.


## CustomCell class

A helper class used for creating custom cells in the Tkinter GUI. 


## DataInputDialog class

A helper class for creating input dialogs in the Tkinter GUI. 


## TableauGUI class

The main class for creating the graphical user interface. 


## get_inputs function

This function prompts the user to enter the necessary data for the problem.

## Introduction and Menu classes

These classes are responsible for providing a user-friendly introduction and menu to guide users through the use of the application.


# User Guide

## Initial Screen

When you first open the program, you'll be greeted with an introductory screen that covers the entire window.

![Intro Screen GIF](1.gif)

Click anywhere on this screen to continue to the main menu.


## Main Menu

The main menu provides several options:

![Capture_2023_06_20_12_14_05_317](https://github.com/AminAkbariCodes/Hitchcock-Algorithm-for-the-Transportation-Problem/assets/132245731/41b7afb1-6445-425b-962e-581d2d78562d)


1. **Start the Algorithm**: Click this button to begin the Hitchcock Transportation Algorithm. You'll be prompted to enter the necessary data (number of supply and demand nodes, their respective values, and the transportation costs), after which the algorithm will begin solving the problem.

2. **User Manual**: This option provides a detailed description of the software and instructions on how to use it.

![Capture_2023_06_20_12_16_10_419](https://github.com/AminAkbariCodes/Hitchcock-Algorithm-for-the-Transportation-Problem/assets/132245731/5a7eb75c-4059-4297-b595-abf4dc7abf16)

3. **About**: This section provides a brief about the developer and contains links to various resources:
   - UCI ITS website: [https://its.uci.edu/](https://its.uci.edu/)
   - Professor McNally's website: [https://its.uci.edu/~mmcnally](https://its.uci.edu/~mmcnally)
   - Developer's GitHub page: [https://github.com/AminAkbariCodes](https://github.com/AminAkbariCodes)
   - Developer's Email: [makbarik@uci.edu](mailto:makbarik@uci.edu)
   - Developer's LinkedIn: [https://linkedin.com/in/amin-akbari](https://linkedin.com/in/amin-akbari)
   - Back: This button will take you back to the introductory screen. 

![Capture_2023_06_20_12_16_15_203](https://github.com/AminAkbariCodes/Hitchcock-Algorithm-for-the-Transportation-Problem/assets/132245731/2c3998a6-4322-453a-ab91-d79ae53a7fc5)

4. **Exit**: Clicking this will close the program.

Choose the option that suits your needs to proceed.


# Running the Algorithm

## Starting the Algorithm

Click on the "Start the Algorithm" button to begin the Hitchcock Transportation Algorithm. You'll be prompted to enter the necessary data (number of supply and demand nodes, their respective values, and the transportation costs).

![Capture_2023_06_20_12_58_28_60](https://github.com/AminAkbariCodes/Hitchcock-Algorithm-for-the-Transportation-Problem/assets/132245731/7a0629ae-13b0-4656-b0a8-a6a96a44245e)


After entering the data, the initial tableau will be displayed.

![Capture_2023_06_20_12_58_17_619](https://github.com/AminAkbariCodes/Hitchcock-Algorithm-for-the-Transportation-Problem/assets/132245731/2570346c-a6dd-4acc-9b63-f43f91299eb0)


## User Interface

Once the algorithm starts, you will see a menu with several options:

![Capture_2023_06_20_12_58_48_42](https://github.com/AminAkbariCodes/Hitchcock-Algorithm-for-the-Transportation-Problem/assets/132245731/9c8a80f4-7d43-4fbc-9268-83af07da1ef0)


- **File Menu**: Here you can open a saved problem data, restart the tableau and all data, or exit the application.
- **Algorithm Menu**: Under this menu, you have options to enter new problem data or modify the current data, and select the Initial Feasible Solution (IFS) method. Options include NWCR (Northwest Corner Rule), MCR (Minimum Cost Rule), or VA (Vogel's Approximation).
- **View Menu**: This menu allows you to capture a screenshot of the current state of the tableau and save it, or print out the current state of the tableau. Users can save each step of the tableau as a PDF or PNG file in their desired locations.
- **Help Menu**: Here you can find information about the author and the program, as well as details on how to reach out for help.

Below the menus, there are navigation buttons. You can use the "Back" button to revert to the previous step in the algorithm, or the "Next" button to move to the next step.

Here's a gif that illustrates the process:

![Intro Screen GIF](2.gif)


# Example Walkthrough

For this example, we will be using data from an exercise available on the [UCI course website](https://its.uci.edu/~mmcnally/cee/cee228a/):

Number of supply nodes: 3
Number of demand nodes: 3
Supply values: [40, 30, 30]
Demand values: [60, 20, 20]
Transportation costs: 

| 16 | 10 |  2 |
| 12 |  4 |  6 |
|  9 |  7 |  5 |


Here are the steps to input this data and solve the problem:

1. Start the algorithm and input the data as shown above.

2. Choose the Initial Feasible Solution (IFS) method. We will demonstrate using all three options: Northwest Corner Rule (NWCR), Minimum Cost Rule (MCR), and Vogel's Approximation (VA).

Here are the resulting tableaux for the different IFS methods:

- NWCR:

![NWCR Image](link_to_nwcr_image)

- MCR:

![MCR Image](link_to_mcr_image)

- VA:

![VA Image](link_to_va_image)

3. Now, let's solve the problem using the Northwest Corner Rule (NWCR). The algorithm will iterate through the steps of calculating shadow prices, opportunity costs, and deltas, finding the pivot cell, identifying the loop, and updating the allocations. Here are the screenshots for each step:

![Step 1 Image](link_to_step_1_image)
![Step 2 Image](link_to_step_2_image)
...continue this pattern until...
![Step 7 Image](link_to_step_7_image)

4. After the last step, you will arrive at the optimal solution which can be verified against the solution provided on the course website.

# Handling Unequal Supply and Demand

The software is capable of handling scenarios where the total supply does not equal the total demand. It achieves this by adding a "dummy" node. The transportation cost assigned to this dummy node is a large value, which ensures that it will not be part of the optimal solution unless absolutely necessary (i.e., when there's no other path).

This strategy effectively balances the total supply and demand without affecting the integrity of the optimal solution.

For instance, if we had an additional supply node with a supply value of 10 and no corresponding demand, the software would add a dummy demand node with a demand value of 10 and a very high transportation cost.

The tableau after adding the dummy node would look something like this:

| 16 | 10 | 2 | High |
|----|----|---|------|
| 12 |  4 | 6 | High |
|  9 |  7 | 5 | High |
| High | High | High | 0 |

This new row and column ensure that the total supply equals the total demand, allowing the algorithm to proceed.

