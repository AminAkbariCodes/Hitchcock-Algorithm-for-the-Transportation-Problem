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
