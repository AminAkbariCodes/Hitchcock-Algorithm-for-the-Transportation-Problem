# Hitchcock Algorithm for the Transportation Problem

The domain of operations research is renowned for tackling complex optimization problems, one of which is the notable Transportation Problem. This problem encapsulates the task of identifying the most cost-efficient means of transporting goods from multiple factories, termed supply nodes, to a network of customers, recognized as demand nodes. The crux of the problem lies in accurately determining the volume of goods each factory should supply to each customer, aiming to minimize the total cost of transportation while meeting the specific supply and demand constraints inherent to each node.

Among the myriad methodologies employed to resolve transportation problems, the Hitchcock Transportation Algorithm stands out as one of the most prevalent. This algorithm, alternatively referred to as the stepping-stone method or the MODI (Modified Distribution) method, follows a systematic series of steps designed to yield an optimal solution. The process begins with establishing an initial feasible solution and then, through iterative refinement, improves this solution until a point of optimality is reached where no further enhancements are possible.

This report presents a comprehensive study and implementation of the Hitchcock Transportation Algorithm through a Python-based application developed as part of this project. The overarching objective behind this initiative was to design an application that is both efficient and user-friendly. This software tool accepts supply and demand data as inputs, carries out the necessary computations guided by the Hitchcock Transportation Algorithm, and graphically depicts the sequential steps and results of the algorithmic process.

In essence, the aim of this project is not only to provide an operational tool for solving transportation problems but also to serve as an educational resource. By offering a tangible and interactive means of understanding and applying the Hitchcock Transportation Algorithm, the project strives to bridge the gap between theoretical concepts and practical applications in operations research.


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

Upon the execution of the Python application, users encounter an introductory interface that spans the entire window. A simple click anywhere on this screen allows users to navigate to the primary menu.

![image](https://github.com/AminAkbariCodes/Hitchcock-Algorithm-for-the-Transportation-Problem/assets/132245731/81f60338-03ed-457e-bd9b-3ee460e508e7)


Click anywhere on this screen to continue to the main menu.

## Main Menu Overview

The primary menu is designed with a user-friendly approach and presents a variety of options to users:

![Capture_2023_06_20_12_14_05_317](https://github.com/AminAkbariCodes/Hitchcock-Algorithm-for-the-Transportation-Problem/assets/132245731/41b7afb1-6445-425b-962e-581d2d78562d)

1. **Start the Algorithm**: The selection of this option initiates the Hitchcock Transportation Algorithm. Users are required to input the necessary data, including the number of supply and demand nodes, the respective values for these nodes, and the associated transportation costs. Once these details are entered, the algorithm sets in motion to solve the proposed transportation problem.

2. **User Manual**: This feature provides an in-depth guide on how to navigate and utilize the software effectively. The manual elaborates on the software's features and presents step-by-step instructions for its usage.

![Capture_2023_06_20_12_16_10_419](https://github.com/AminAkbariCodes/Hitchcock-Algorithm-for-the-Transportation-Problem/assets/132245731/5a7eb75c-4059-4297-b595-abf4dc7abf16)

3. **About**: This section offers a brief introduction about the developer and provides a collection of relevant links. These include:
   - UCI ITS website: [https://its.uci.edu/](https://its.uci.edu/)
   - Professor McNally's website: [https://its.uci.edu/~mmcnally](https://its.uci.edu/~mmcnally)
   - Developer's GitHub page: [https://github.com/AminAkbariCodes](https://github.com/AminAkbariCodes)
   - Developer's Email: [makbarik@uci.edu](mailto:makbarik@uci.edu)
   - Developer's LinkedIn: [https://linkedin.com/in/amin-akbari](https://linkedin.com/in/amin-akbari)
   - Back: This button will take you back to the introductory screen. 

![Capture_2023_06_20_12_16_15_203](https://github.com/AminAkbariCodes/Hitchcock-Algorithm-for-the-Transportation-Problem/assets/132245731/2c3998a6-4322-453a-ab91-d79ae53a7fc5)

4. **Exit**: The selection of this option results in the termination of the program.

Users can select any of the options as per their requirements to proceed further in the application.

![Intro Screen GIF](1.gif)


# Running the Algorithm

## Starting the Algorithm

The Hitchcock Transportation Algorithm is set into action by clicking on the "Start the Algorithm" button in the main menu. Upon selection, users are guided to input essential data. This data includes the number of supply and demand nodes, their corresponding values, and the costs associated with transportation.

![Capture_2023_06_20_12_58_28_60](https://github.com/AminAkbariCodes/Hitchcock-Algorithm-for-the-Transportation-Problem/assets/132245731/7a0629ae-13b0-4656-b0a8-a6a96a44245e)


After the successful submission of these data, the initial tableau – a critical component of the algorithm that visually represents the problem data and the progress of the algorithm – is showcased to the users.

![Capture_2023_06_20_12_58_17_619](https://github.com/AminAkbariCodes/Hitchcock-Algorithm-for-the-Transportation-Problem/assets/132245731/2570346c-a6dd-4acc-9b63-f43f91299eb0)


## User Interface

When the Hitchcock Transportation Algorithm commences, users are presented with a comprehensive menu hosting several options:

![Capture_2023_06_20_12_58_48_42](https://github.com/AminAkbariCodes/Hitchcock-Algorithm-for-the-Transportation-Problem/assets/132245731/9c8a80f4-7d43-4fbc-9268-83af07da1ef0)

- **File Menu**: This menu serves as the tool for managing problem data. Users can utilize it to load previously saved problem data, restart the tableau and all associated data, or exit the application entirely.

![image](https://github.com/AminAkbariCodes/Hitchcock-Algorithm-for-the-Transportation-Problem/assets/132245731/ee42a453-fe9c-4d67-bbed-9547adac4f96)

- **Algorithm Menu**: This menu is an interactive part of the application that allows users to engage with the algorithm actively. Users can input new problem data or modify the existing data. It also provides the choice to select the Initial Feasible Solution (IFS) method. Users have the option to opt for the Northwest Corner Rule (NWCR), Minimum Cost Rule (MCR), or Vogel’s Approximation (VA).

![image](https://github.com/AminAkbariCodes/Hitchcock-Algorithm-for-the-Transportation-Problem/assets/132245731/d1864a7c-89bb-4019-a2f7-cf1105360ffc)
![image](https://github.com/AminAkbariCodes/Hitchcock-Algorithm-for-the-Transportation-Problem/assets/132245731/a3cbd0fb-bfbd-4641-9831-66ffde79fa1f)
![image](https://github.com/AminAkbariCodes/Hitchcock-Algorithm-for-the-Transportation-Problem/assets/132245731/d76de314-e86c-472d-a6e0-d2a59d27bb0d)

- **View Menu**: The View Menu enhances the user experience by enabling them to capture a snapshot of the tableau at any given state. They can save this snapshot for later reference or print it directly from the application. Users can save each tableau snapshot as a PDF or PNG file in their preferred locations.

  ![image](https://github.com/AminAkbariCodes/Hitchcock-Algorithm-for-the-Transportation-Problem/assets/132245731/49083f71-ae37-47da-8849-55b60d2ced42)

- **Help Menu**: The Help Menu serves as a hub for additional information about the application and the developer. Users can access details on how to get help and support when required.

![image](https://github.com/AminAkbariCodes/Hitchcock-Algorithm-for-the-Transportation-Problem/assets/132245731/42f17aa8-efeb-48a3-a94d-a92c8f576d18)

Below the menus, there are navigation buttons. You can use the "Back" button to revert to the previous step in the algorithm, or the "Next" button to move to the next step.

In addition to the menus, there are navigational buttons available to users. The "Back" button enables users to go back to the previous step of the algorithm, while the "Next" button allows for the progression to the following step. This interactive feature ensures users have full control over the pace at which they navigate the algorithm.

![Intro Screen GIF](2.gif)


# Example Walkthrough

For this example, we will be using data from an exercise available on the [UCI course website](https://its.uci.edu/~mmcnally/cee/cee228a/):

Number of supply nodes: 3
Number of demand nodes: 3
Supply values: [40, 30, 30]
Demand values: [60, 20, 20]
Transportation costs: 

|    | D1 | D2 | D3 |
|----|----|----|----|
| S1 | 16 | 10 |  2 |
| S2 | 12 |  4 |  6 |
| S3 |  9 |  7 |  5 |




Here are the steps to input this data and solve the problem:

1. Start the algorithm and input the data as shown above.

2. Choose the Initial Feasible Solution (IFS) method. We will demonstrate using all three options: Northwest Corner Rule (NWCR), Minimum Cost Rule (MCR), and Vogel's Approximation (VA).

Here are the resulting tableaux for the different IFS methods:

- NWCR:

![Capture_2023_06_20_13_33_38_856](https://github.com/AminAkbariCodes/Hitchcock-Algorithm-for-the-Transportation-Problem/assets/132245731/b864005e-962b-4efd-b9b7-32ff4fa088da)


- MCR:

![Capture_2023_06_20_13_33_21_302](https://github.com/AminAkbariCodes/Hitchcock-Algorithm-for-the-Transportation-Problem/assets/132245731/193e0cbb-498a-4f1f-8d31-5d7ca95eab5f)


- VA:

![Capture_2023_06_20_13_33_32_165](https://github.com/AminAkbariCodes/Hitchcock-Algorithm-for-the-Transportation-Problem/assets/132245731/ce62b5e1-3b01-4d0e-84f4-a35aa01e0b9f)

3. Now, let's solve the problem using the Northwest Corner Rule (NWCR). The algorithm will iterate through the steps of calculating shadow prices, opportunity costs, and deltas, finding the pivot cell, identifying the loop, and updating the allocations. Here are the screenshots for each step:

- Iteration 1: 
![Capture_2023_06_20_13_33_45_167](https://github.com/AminAkbariCodes/Hitchcock-Algorithm-for-the-Transportation-Problem/assets/132245731/6d5ae74f-6548-4086-968a-db5da4182e59)
![Capture_2023_06_20_13_33_48_462](https://github.com/AminAkbariCodes/Hitchcock-Algorithm-for-the-Transportation-Problem/assets/132245731/3c16f9b6-801e-4800-bc57-610985059c0d)
![Capture_2023_06_20_13_33_54_425](https://github.com/AminAkbariCodes/Hitchcock-Algorithm-for-the-Transportation-Problem/assets/132245731/0cc5a56b-b369-44ba-9b8c-456f0875a706)

- Iteration 2: 
![Capture_2023_06_20_13_33_59_56](https://github.com/AminAkbariCodes/Hitchcock-Algorithm-for-the-Transportation-Problem/assets/132245731/b73e9f5e-a1ea-4c30-bd4e-1355bff8bca3)
![Capture_2023_06_20_13_34_01_436](https://github.com/AminAkbariCodes/Hitchcock-Algorithm-for-the-Transportation-Problem/assets/132245731/f1ba4ada-e240-4963-b856-937d809f5eec)
![Capture_2023_06_20_13_34_04_769](https://github.com/AminAkbariCodes/Hitchcock-Algorithm-for-the-Transportation-Problem/assets/132245731/71617657-db71-4ac5-aa5e-4284b7bdae3e)


4. After the last step, you will arrive at the optimal solution which can be verified against the solution provided on the course website.

![Capture_2023_06_20_13_34_08_497](https://github.com/AminAkbariCodes/Hitchcock-Algorithm-for-the-Transportation-Problem/assets/132245731/fc8f7a3e-79b9-4296-ba73-cbbb5796d37e)


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


## Software Performance and Limitations

The Hitchcock Transportation Algorithm implementation in this software has been designed with efficiency in mind, allowing it to handle transportation networks with a high number of nodes effectively. Indeed, our testing has shown that the software can solve problems involving more than 50 nodes.

However, it's worth noting that while the algorithm itself can handle large networks, the graphical representation and tableau can become overloaded due to the sheer size of the matrices involved. For such large networks, the graphical user interface may not display the results optimally due to space constraints.

Nonetheless, users can leverage the source code directly to solve problems involving large networks and retrieve results without relying on the graphical explanation. It's important to mention that this assertion is based on our preliminary testing where we used randomly generated examples. While the code ran efficiently and the final solutions for different Initial Feasible Solution methods were consistent, this does not constitute comprehensive validation of the software's performance.

The graphical representation was primarily designed and optimized for problems of moderate size, maintaining a balance between usability, comprehensibility, and aesthetic appeal.

## Future Work and Conclusion

There are always opportunities to improve and enhance a software tool, and this one is no exception. Future work might involve refining the graphical user interface to handle larger problems more effectively or including additional algorithms for solving transportation problems. Additionally, a more comprehensive validation process could be conducted, involving a wide variety of test cases and more extensive performance profiling.

In conclusion, this software provides an efficient and user-friendly tool for understanding and solving transportation problems using the Hitchcock Transportation Algorithm. Despite some limitations with the graphical representation of larger problems, the software remains an effective and valuable resource in the field of operations research and transportation studies.

We encourage users to explore the software, provide feedback, and contribute to its continued development.

## References

1. [CEE 228A URBAN TRANSPORTATION NETWORKS I course page](https://its.uci.edu/~mmcnally/cee/cee228a/)
