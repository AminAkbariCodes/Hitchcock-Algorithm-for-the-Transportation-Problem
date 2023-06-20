import numpy as np
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from PIL import ImageGrab, ImageTk
from tkinter import filedialog, Button

import pygame
import pygame.freetype
import webbrowser

class TransportationProblem:
    def __init__(self, num_supply_nodes, num_demand_nodes, supply_values, demand_values, transportation_costs):
        self.num_supply_nodes = num_supply_nodes
        self.num_demand_nodes = num_demand_nodes
        self.supply_values = supply_values
        self.demand_values = demand_values
        self.transportation_costs = transportation_costs
        self.allocations = np.zeros((num_supply_nodes, num_demand_nodes), dtype=int)

        # initialize u_values and v_values
        self.u_values = np.zeros(num_supply_nodes, dtype=int)
        self.v_values = np.zeros(num_demand_nodes, dtype=int)

        self.balance_problem()
        self.allocations = np.zeros((self.num_supply_nodes, self.num_demand_nodes), dtype=int)
        self.iteration = 0

    def balance_problem(self):
        total_supply = sum(self.supply_values)
        total_demand = sum(self.demand_values)

        if total_supply != total_demand:
            if total_supply > total_demand:
                self.num_demand_nodes += 1
                self.demand_values.append(total_supply - total_demand)
                for i, row in enumerate(self.transportation_costs):
                    self.transportation_costs[i] = np.append(row, 0)
                self.allocations = np.append(self.allocations, np.zeros((self.num_supply_nodes, 1)), axis=1)
            else:
                self.num_supply_nodes += 1
                self.supply_values.append(total_demand - total_supply)
                new_row = np.array([0] * self.num_demand_nodes)
                self.transportation_costs.append(new_row)
                self.allocations = np.append(self.allocations, np.zeros((1, self.num_demand_nodes)), axis=0)

    def northwest_corner_rule(self): 
        i = j = 0
        remaining_supply = self.supply_values.copy()
        remaining_demand = self.demand_values.copy()
        while i < self.num_supply_nodes and j < self.num_demand_nodes:
            allocation = min(remaining_supply[i], remaining_demand[j])
            self.allocations[i, j] = allocation
            remaining_supply[i] -= allocation
            remaining_demand[j] -= allocation

            if remaining_supply[i] == 0 and i < self.num_supply_nodes - 1:
                i += 1
            elif remaining_demand[j] == 0 and j < self.num_demand_nodes - 1:
                j += 1
            else:
                break

    def minimum_cost_rule(self):
        remaining_supply = self.supply_values.copy()
        remaining_demand = self.demand_values.copy()
        costs = np.array(self.transportation_costs, dtype=float)

        while any(remaining_supply) and any(remaining_demand):
            min_cost_index = np.unravel_index(np.argmin(costs, axis=None), costs.shape)
            allocation = min(remaining_supply[min_cost_index[0]], remaining_demand[min_cost_index[1]])
            self.allocations[min_cost_index] = allocation
            remaining_supply[min_cost_index[0]] -= allocation
            remaining_demand[min_cost_index[1]] -= allocation

            if remaining_supply[min_cost_index[0]] == 0:
                costs[min_cost_index[0], :] = np.finfo(float).max
            if remaining_demand[min_cost_index[1]] == 0:
                costs[:, min_cost_index[1]] = np.finfo(float).max

            if remaining_supply[min_cost_index[0]] == 0 and remaining_demand[min_cost_index[1]] == 0:
                costs[min_cost_index[0], :] = np.finfo(float).max
                costs[:, min_cost_index[1]] = np.finfo(float).max

    def vogel_approximation_method(self):
        remaining_supply = self.supply_values.copy()
        remaining_demand = self.demand_values.copy()
        costs = np.array(self.transportation_costs, dtype=float)

        while any(remaining_supply) and any(remaining_demand):
            penalty_costs = []

            for i in range(self.num_supply_nodes):
                if remaining_supply[i] > 0:
                    row = costs[i, :]
                    smallest_cost, next_smallest_cost = np.partition(row, 2)[:2]
                    penalty_costs.append((next_smallest_cost - smallest_cost, i, -1))
                else:
                    penalty_costs.append((np.finfo(float).min, i, -1))

            for j in range(self.num_demand_nodes):
                if remaining_demand[j] > 0:
                    column = costs[:, j]
                    smallest_cost, next_smallest_cost = np.partition(column, 2)[:2]
                    penalty_costs.append((next_smallest_cost - smallest_cost, -1, j))
                else:
                    penalty_costs.append((np.finfo(float).min, -1, j))

            max_penalty_cost, max_i, max_j = max(penalty_costs, key=lambda x: x[0])
            if max_i == -1:
                i = np.argmin(costs[:, max_j])
                j = max_j
            else:
                i = max_i
                j = np.argmin(costs[i, :])

            allocation = min(remaining_supply[i], remaining_demand[j])
            self.allocations[i, j] = allocation
            remaining_supply[i] -= allocation
            remaining_demand[j] -= allocation

            if remaining_supply[i] == 0:
                costs[i, :] = np.finfo(float).max
            if remaining_demand[j] == 0:
                costs[:, j] = np.finfo(float).max

    def calculate_shadow_prices(self):
        allocations = self.allocations.copy()
        transportation_costs = self.transportation_costs
        num_supply_nodes, num_demand_nodes = allocations.shape
        u_values = [None] * num_supply_nodes
        v_values = [None] * num_demand_nodes

        u_values[0] = 0

        while any(u is None for u in u_values) or any(v is None for v in v_values):
            for i in range(num_supply_nodes):
                for j in range(num_demand_nodes):
                    if allocations[i, j] > 0:
                        if u_values[i] is not None and v_values[j] is None:
                            v_values[j] = transportation_costs[i][j] - u_values[i]
                        elif u_values[i] is None and v_values[j] is not None:
                            u_values[i] = transportation_costs[i][j] - v_values[j]

        u_values = [-u for u in u_values]

        return u_values, v_values

    def calculate_opportunity_costs(self):
        opportunity_costs = np.zeros((self.num_supply_nodes, self.num_demand_nodes), dtype=int)
        for i in range(self.num_supply_nodes):
            for j in range(self.num_demand_nodes):
                if self.allocations[i, j] == 0:
                    opportunity_costs[i, j] = self.v_values[j] - self.u_values[i]
        return opportunity_costs

    def calculate_deltas(self):
        deltas = np.zeros((self.num_supply_nodes, self.num_demand_nodes), dtype=int)
        for i in range(self.num_supply_nodes):
            for j in range(self.num_demand_nodes):
                if self.allocations[i, j] == 0:
                    deltas[i, j] = -(self.transportation_costs[i][j] - self.v_values[j] + self.u_values[i])

        return deltas

    def find_pivot_cell(self):
        deltas = self.calculate_deltas()
        pivot_cell = np.unravel_index(np.argmax(deltas, axis=None), deltas.shape)
        return pivot_cell

    def total_cost(self):
        return np.sum(self.allocations * self.transportation_costs)

    def identify_loop(self, pivot):
        allocated_cells = list(zip(*np.where(self.allocations > 0)))
        visited = set()

        def loop_search(current_path, current_direction):
            last_cell = current_path[-1]
            visited.add(last_cell)
            candidates = []

            if current_direction == 'horizontal':
                candidates = [(last_cell[0], j) for j in range(self.num_demand_nodes) if (last_cell[0], j) != last_cell]
            elif current_direction == 'vertical':
                candidates = [(i, last_cell[1]) for i in range(self.num_supply_nodes) if (i, last_cell[1]) != last_cell]

            for cell in candidates:
                if cell in allocated_cells and cell not in visited:
                    new_path = current_path.copy()
                    new_path.append(cell)

                    if len(new_path) >= 4 and (new_path[0][0] == new_path[-1][0] or new_path[0][1] == new_path[-1][1]):
                        # Check if the loop is formed with the correct sequence of horizontal and vertical moves
                        valid_loop = True
                        for idx in range(len(new_path) - 2):
                            if (new_path[idx][0] == new_path[idx + 1][0]) == (
                                    new_path[idx + 1][0] == new_path[idx + 2][0]):
                                valid_loop = False
                                break

                        if valid_loop:
                            return new_path

                    alternate_direction = 'horizontal' if current_direction == 'vertical' else 'vertical'
                    result = loop_search(new_path, alternate_direction)
                    if result:
                        return result
            visited.remove(last_cell)
            return None

        loop = loop_search([pivot], 'horizontal') or loop_search([pivot], 'vertical')
        if loop:
            loop = [loop[i] if i % 2 == 0 else loop[-(i % len(loop))] for i in range(len(loop))]
        return loop

    def update_allocations(self, loop):
        self.iteration += 1
        min_allocation = min(self.allocations[cell] for i, cell in enumerate(loop) if i % 2 == 1)

        for i, cell in enumerate(loop):
            if i % 2 == 1:
                self.allocations[cell] -= min_allocation
            else:
                self.allocations[cell] += min_allocation

    def has_positive_deltas(self):
        for row in self.calculate_opportunity_costs():
            if any(d > 0 for d in row):
                return True
        return False

    def generate_state(self):
        return State(self.allocations, self.u_values, self.v_values, self.iteration)

    def reset(self):
        # Reset all instance variables to their initial state
        self.__init__(self.num_supply_nodes, self.num_demand_nodes, self.supply_values, self.demand_values,
                      self.transportation_costs)


class State:
    def __init__(self, allocations, u_values, v_values, iteration):
        self.allocations = allocations.copy()
        self.u_values = u_values.copy()
        self.v_values = v_values.copy()
        self.iteration = iteration


class CustomCell(tk.Frame):
    def __init__(self, parent, allocation, cost, opportunity_cost=None, delta=None, font_size=24, **kwargs):
        super().__init__(parent, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.canvas = tk.Canvas(self, width=100, height=100, bd=0, highlightthickness=0)
        self.canvas.grid(row=0, rowspan=2, column=0, columnspan=2, sticky='nsew')

        self.cost_label = ttk.Label(self, text=cost, foreground="red", font=("Arial", font_size))
        self.cost_label.grid(row=0, column=1, sticky="w")

        self.allocation_label = ttk.Label(self, text=allocation, foreground="green", font=("Arial", font_size))
        self.allocation_label.grid(row=1, column=0, sticky="e")

        if opportunity_cost is not None:
            self.opportunity_cost_label = ttk.Label(self, text=opportunity_cost, foreground="yellow",
                                                    font=("Arial", font_size))
            self.opportunity_cost_label.grid(row=0, column=0, sticky="e")

        if delta is not None:
            self.delta_label = ttk.Label(self, text=delta, foreground="blue", font=("Arial", font_size))
            self.delta_label.grid(row=1, column=1, sticky="w")

    def draw_arrow(self, direction):
        if direction == "right":
            self.canvas.create_line(10, 50, 90, 50, arrow=tk.LAST, width=5)
        elif direction == "left":
            self.canvas.create_line(90, 50, 10, 50, arrow=tk.LAST, width=5)
        elif direction == "down":
            self.canvas.create_line(50, 10, 50, 90, arrow=tk.LAST, width=5)
        elif direction == "up":
            self.canvas.create_line(50, 90, 50, 10, arrow=tk.LAST, width=5)

    def clear_canvas(self):
        self.canvas.delete('all')

        if hasattr(self, 'opportunity_cost_label'):
            self.opportunity_cost_label['text'] = ""

        if hasattr(self, 'delta_label'):
            self.delta_label['text'] = ""

    def draw_loop_outline(self):
        self.canvas.create_rectangle(3, 3, 97, 97, outline='orange', width=3)


class DataInputDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None, initial_data=None):
        self.result = None
        self.e1 = None
        self.e2 = None
        self.e3 = None
        self.e4 = None
        self.e5 = None
        self.initial_data = initial_data
        super().__init__(parent, title=title)

    def body(self, master):
        tk.Label(master, text="Number of supply nodes:").grid(row=0)
        tk.Label(master, text="Number of demand nodes:").grid(row=1)
        tk.Label(master, text="Supply values (comma-separated):").grid(row=2)
        tk.Label(master, text="Demand values (comma-separated):").grid(row=3)
        tk.Label(master, text="Transportation costs (comma-separated rows):").grid(row=4)

        self.e1 = tk.Entry(master)
        self.e2 = tk.Entry(master)
        self.e3 = tk.Entry(master)
        self.e4 = tk.Entry(master)
        self.e5 = tk.Entry(master)

        if self.initial_data:
            self.e1.insert(0, self.initial_data["num_supply_nodes"])
            self.e2.insert(0, self.initial_data["num_demand_nodes"])
            self.e3.insert(0, self.initial_data["supply_values"])
            self.e4.insert(0, self.initial_data["demand_values"])
            self.e5.insert(0, self.initial_data["transportation_costs"])

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        self.e3.grid(row=2, column=1)
        self.e4.grid(row=3, column=1)
        self.e5.grid(row=4, column=1)

        return self.e1  # initial focus

    def apply(self):
        self.result = {
            "num_supply_nodes": int(self.e1.get()),
            "num_demand_nodes": int(self.e2.get()),
            "supply_values": [int(i) for i in self.e3.get().split(',')],
            "demand_values": [int(i) for i in self.e4.get().split(',')],
            "transportation_costs": [[int(j) for j in i.split()] for i in self.e5.get().split(',')]
        }


class TableauGUI(tk.Tk):
    def __init__(self, transportation_problem):
        super().__init__()

        self.transportation_problem = transportation_problem
        self.state = 0

        self.states = [self.transportation_problem.generate_state()]

        # Add a new variable to hold the selected IFS
        self.selected_ifs = tk.StringVar(value="NWCR")

        # create a menu
        self.menu = tk.Menu(self)

        # create the File menu
        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label='Open', command=self.open_data)  # add 'open_data' method
        file_menu.add_command(label='Restart', command=self.restart)  # add 'restart' method
        file_menu.add_command(label='Exit', command=self.confirm_exit)

        # create the Algorithm menu
        algorithm_menu = tk.Menu(self.menu, tearoff=0)
        algorithm_submenu = tk.Menu(algorithm_menu, tearoff=0)  # create a new submenu for 'Data'
        algorithm_submenu.add_command(label='New', command=self.new_data)  # 'New' option
        algorithm_submenu.add_command(label='Change', command=self.change_data)  # 'Change' option
        algorithm_menu.add_cascade(label='Data', menu=algorithm_submenu)  # add the submenu to the 'Data' option

        # Add the new IFS menu under the "Algorithm" tab
        ifs_menu = tk.Menu(algorithm_menu, tearoff=0)
        ifs_menu.add_radiobutton(label='NWCR', variable=self.selected_ifs, command=self.change_ifs)
        ifs_menu.add_radiobutton(label='MCR', variable=self.selected_ifs, command=self.change_ifs)
        ifs_menu.add_radiobutton(label='VA', variable=self.selected_ifs, command=self.change_ifs)
        algorithm_menu.add_cascade(label='IFS', menu=ifs_menu)

        # create the View menu
        view_menu = tk.Menu(self.menu, tearoff=0)
        view_menu.add_command(label='Screenshot', command=self.screenshot)  # add 'screenshot' method
        view_menu.add_command(label='Print', command=self.print_out)  # add 'print_out' method

        # create the Help menu
        help_menu = tk.Menu(self.menu, tearoff=0)
        help_menu.add_command(label='About', command=self.show_about)  # add 'show_about' method
        help_menu.add_command(label='Contact Support', command=self.show_support)  # add 'show_support' method

        # add the File, Algorithm and Help menu to the menu bar
        self.menu.add_cascade(label='File', menu=file_menu)
        self.menu.add_cascade(label='Algorithm', menu=algorithm_menu)
        self.menu.add_cascade(label='View', menu=view_menu)
        self.menu.add_cascade(label='Help', menu=help_menu)

        # attach the menu bar to the window
        self.config(menu=self.menu)

        self.title("Transportation Tableau")
        self.create_tableau()
        self.create_legend()

        self.previous_button = ttk.Button(self, text="Back", command=self.previous_step)
        self.previous_button.grid(row=self.transportation_problem.num_supply_nodes + 6, column=2, sticky='w')

        self.next_button = ttk.Button(self, text="Next", command=self.next_step)
        self.next_button.grid(row=self.transportation_problem.num_supply_nodes + 5, column=2, sticky='w')

        self.iteration_label = ttk.Label(self, text=f"Iteration: {transportation_problem.iteration}",
                                         font=("Arial", 18), foreground="blue", background="lightgray")
        self.iteration_label.grid(row=transportation_problem.num_supply_nodes + 6,
                                  column=transportation_problem.num_demand_nodes + 2,
                                  padx=5, pady=5)

    def open_data(self):
        pass

    def restart(self):
        self.destroy()  # close the current window
        initial_data = get_inputs()  # get new inputs
        tp = TransportationProblem(*initial_data)  # create a new instance
        app = TableauGUI(tp)  # create a new window
        app.mainloop()  # restart the algorithm

    def confirm_exit(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

    def new_data(self):
        data = DataInputDialog(self, "New Data").result
        if data:
            self.create_new_problem(data)

    def change_data(self):
        initial_data = {
            "num_supply_nodes": self.transportation_problem.num_supply_nodes,
            "num_demand_nodes": self.transportation_problem.num_demand_nodes,
            "supply_values": ','.join(map(str, self.transportation_problem.supply_values)),
            "demand_values": ','.join(map(str, self.transportation_problem.demand_values)),
            "transportation_costs": ','.join(
                [' '.join(map(str, row)) for row in self.transportation_problem.transportation_costs])
        }
        data = DataInputDialog(self, "Change Data", initial_data=initial_data).result
        if data:
            self.create_new_problem(data)

    def create_new_problem(self, data):
        try:
            tp = TransportationProblem(data["num_supply_nodes"], data["num_demand_nodes"],
                                       data["supply_values"], data["demand_values"], data["transportation_costs"])
            self.destroy()  # close the current window
            app = TableauGUI(tp)  # create a new instance with the new data
            app.mainloop()  # restart the algorithm
        except Exception as e:
            messagebox.showerror("Error", str(e))

            algorithm_menu.add_command(label='New Data', command=self.new_data)
            algorithm_menu.add_command(label='Change Data', command=self.change_data)

    def change_ifs(self):
        self.transportation_problem.reset()  # reset the problem state
        self.show_initial_solution()

    def screenshot(self):
        x = self.winfo_rootx()
        y = self.winfo_rooty()
        w = self.winfo_width()
        h = self.winfo_height()
        screenshot = ImageGrab.grab((x, y, x + w, y + h))
        screenshot.save('screenshot.png', 'PNG')

        # Create a new window to display the screenshot
        screenshot_window = tk.Toplevel(self)
        screenshot_window.title('Screenshot')

        # Convert the PIL Image object to a PhotoImage object which tkinter can display
        screenshot_photoimage = ImageTk.PhotoImage(screenshot)

        # Create a label containing the screenshot and add it to the window
        screenshot_label = tk.Label(screenshot_window, image=screenshot_photoimage)
        screenshot_label.image = screenshot_photoimage  # Keep a reference to prevent garbage collection
        screenshot_label.pack()

    def print_out(self):
        x = self.winfo_rootx()
        y = self.winfo_rooty()
        w = self.winfo_width()
        h = self.winfo_height()
        screenshot = ImageGrab.grab((x, y, x + w, y + h))
        
        # Create a new window to display the screenshot
        screenshot_window = tk.Toplevel(self)
        screenshot_window.title('Print')

        # Convert the PIL Image object to a PhotoImage object which tkinter can display
        screenshot_photoimage = ImageTk.PhotoImage(screenshot)

        # Create a label containing the screenshot and add it to the window
        screenshot_label = tk.Label(screenshot_window, image=screenshot_photoimage)
        screenshot_label.image = screenshot_photoimage  # Keep a reference to prevent garbage collection
        screenshot_label.pack()

        # Add a button which will ask the user where to save the file when clicked
        save_button = Button(screenshot_window, text='Save as...', command=lambda: self.save_screenshot(screenshot), width=20, height=2, bg='white', fg='black', 
                             font=('helvetica', 12, 'bold'), borderwidth=0, relief='flat', activebackground='gray', activeforeground='white', cursor='hand2', highlightthickness=0,
                             highlightbackground='white', highlightcolor='white', pady=0, padx=0, anchor='center', justify='center', wraplength=0, takefocus=False)
        save_button.pack()

    def save_screenshot(self, screenshot):
        # Ask the user where to save the file
        filetypes = [('PNG images', '*.png'), ('PDF files', '*.pdf'), ('All files', '*.*')]
        file_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=filetypes)

        # Save the file
        if file_path:
            if file_path.endswith('.png'):
                screenshot.save(file_path, 'PNG')
            elif file_path.endswith('.pdf'):
                screenshot.save(file_path, 'PDF')

    @staticmethod
    def show_about():
        about_text = """
        TransportationProblem Solver 2023.1 (Educational Edition)

        Build #TPS-231.8109.197, built on May 30, 2023
        Licensed to Amin Akbari
        Subscription is active until April 5, 2024.
        For educational use only.

        Runtime version: Python 3.9.1
        Supported by: numpy 1.21.0, tkinter 8.6
        Operating System: Windows 11.0

        Features:

        Balancing supply and demand
        Initial solution using Northwest Corner Rule
        Optimization using Minimum Cost Rule and Vogel's Approximation Method
        Calculation of shadow prices, opportunity costs, and deltas
        Ability to pivot cells for optimal solution
        Tracking of total cost, allocation state and iteration number
        Registry:
        debugger.new.tool.window.layout=true
        ide.experimental.ui=true

        Non-Bundled Plugins:

        None
        """
        messagebox.showinfo("About", about_text)

    @staticmethod
    def show_support():
        support_text = """
        For support, please reach out to us through one of the following methods:

        Amin Akbari
        Email: [makbarik@uci.edu]
        GitHub: https://github.com/AminAkbariCodes
        Linkedin: https://www.linkedin.com/in/amin-akbari

        Powered by open-source software
        Copyright © 2023 ITS UCI.
        """
        messagebox.showinfo("Contact Support", support_text)

    def create_tableau(self, show_allocations=False, show_shadow_prices=False, show_opportunity_costs=False, loop=None):
        transportation_problem = self.transportation_problem

        ttk.Label(self, text="Demand", font=("Arial", 24)).grid(row=transportation_problem.num_supply_nodes + 2,
                                                                column=0, padx=5, pady=5)

        bold_font = ("Arial", 24, "bold")

        for j, header in enumerate(
                ["D" + str(i + 1) for i in range(transportation_problem.num_demand_nodes)] + ["Supply"] + ["U"]):
            ttk.Label(self, text=header, font=bold_font).grid(row=1, column=j + 1, padx=5, pady=5)

        for i, header in enumerate(
                ["S" + str(i + 1) for i in range(transportation_problem.num_supply_nodes)] + ["Demand"] + ["V"]):
            ttk.Label(self, text=header, font=bold_font).grid(row=i + 2, column=0, padx=5, pady=5)

        opportunity_costs = transportation_problem.calculate_opportunity_costs() if show_opportunity_costs else None
        deltas = transportation_problem.calculate_deltas() if show_opportunity_costs else None
        for i in range(self.transportation_problem.num_supply_nodes):
            for j in range(self.transportation_problem.num_demand_nodes):
                opportunity_cost = opportunity_costs[
                    i, j] if show_opportunity_costs and opportunity_costs is not None and opportunity_costs[
                    i, j] != 0 else None
                delta = deltas[i, j] if show_opportunity_costs and deltas is not None and deltas[i, j] != 0 else None
                if show_allocations:
                    cell = CustomCell(self, self.transportation_problem.allocations[i, j],
                                      self.transportation_problem.transportation_costs[i][j],
                                      opportunity_cost=opportunity_cost, delta=delta)
                else:
                    cell = CustomCell(self, "", self.transportation_problem.transportation_costs[i][j],
                                      opportunity_cost=opportunity_cost, delta=delta)
                cell.grid(row=i + 2, column=j + 1, padx=5, pady=5)

        for i, supply in enumerate(transportation_problem.supply_values):
            label = ttk.Label(self, text=supply, font=("Arial", 24), relief="ridge", borderwidth=1)
            label.grid(row=i + 2, column=transportation_problem.num_demand_nodes + 1, padx=5, pady=5)

        for j, demand in enumerate(transportation_problem.demand_values):
            label = ttk.Label(self, text=demand, font=("Arial", 24), relief="ridge", borderwidth=1)
            label.grid(row=transportation_problem.num_supply_nodes + 2, column=j + 1, padx=5, pady=5)

        if show_shadow_prices:
            for i, u_value in enumerate(transportation_problem.u_values):
                label = ttk.Label(self, text=u_value, font=("Arial", 24), relief="ridge", borderwidth=1)
                label.grid(row=i + 2, column=transportation_problem.num_demand_nodes + 2, padx=5, pady=5)
            for j, v_value in enumerate(transportation_problem.v_values):
                label = ttk.Label(self, text=v_value, font=("Arial", 24), relief="ridge", borderwidth=1)
                label.grid(row=transportation_problem.num_supply_nodes + 3, column=j + 1, padx=5, pady=5)

        if show_opportunity_costs:
            pivot_cell = self.transportation_problem.find_pivot_cell()
            pivot_text = f"Pivot Cell: S{pivot_cell[0] + 1}D{pivot_cell[1] + 1}"
            pivot_label = ttk.Label(self, text=pivot_text, font=("Arial", 18), background="lightgray", foreground="purple")
            pivot_label.grid(row=transportation_problem.num_supply_nodes + 5,
                                  column=transportation_problem.num_demand_nodes + 2,
                                  padx=5, pady=5)
        total_cost_text = f"Total Cost: {self.transportation_problem.total_cost()}"
        total_cost_label = ttk.Label(self, text=total_cost_text, font=("Arial", 18), background="lightgray", foreground="firebrick")
        total_cost_label.grid(row=0, column=0,
                            padx=5, pady=5)
        
        if loop:
            for cell in loop:
                canvas_cell = self.grid_slaves(row=cell[0] + 2, column=cell[1] + 1)[0]
                if isinstance(canvas_cell, CustomCell):
                    canvas_cell.draw_loop_outline()
            for i, cell in enumerate(loop[:-1]):
                next_cell = loop[i + 1]
                if cell[0] == next_cell[0]:  # Horizontal move
                    direction = "right" if cell[1] < next_cell[1] else "left"
                else:  # Vertical move
                    direction = "down" if cell[0] < next_cell[0] else "up"
                canvas_cell = self.grid_slaves(row=cell[0] + 2, column=cell[1] + 1)[0]
                if isinstance(canvas_cell, CustomCell):
                    canvas_cell.draw_arrow(direction)

    def create_legend(self):
        legend_items = [
            ("Yellow", "Opportunity Costs"),
            ("Red", "Transportation Costs"),
            ("Green", "Solutions"),
            ("Blue", "Delta"),
        ]

        legend_frame = tk.Frame(self, relief="sunken", borderwidth=1.5, background="lightgray", width=200, height=200)
        legend_frame.grid(row=self.transportation_problem.num_supply_nodes + 5,  # Shift to lower left corner
                        column=0,  # Shift to lower left corner
                        rowspan=2,  # Allow it to span multiple rows so it doesn't get squished
                        columnspan=2,  # Allow it to span multiple columns so it doesn't get squished
                        sticky='nsew',  # Stretch the frame to fill the grid cell
                        padx=10, pady=10)  # Add some padding so it doesn't touch the grid border


        # Create labels for the legend items
        for i, (color, text) in enumerate(legend_items):
            row = i // 2  # This will place first two items on the first row and the next two on the second row
            column = i % 2  # This will place the items alternatively in the first and second columns
            label = ttk.Label(legend_frame, text=text, foreground=color, font=("Arial", 18))
            label.grid(row=row, column=column, padx=20, pady=10)

    def clear_cells(self):
        for i in range(self.transportation_problem.num_supply_nodes):
            for j in range(self.transportation_problem.num_demand_nodes):
                cell = self.grid_slaves(row=i + 2, column=j + 1)[0]
                if isinstance(cell, CustomCell):
                    cell.clear_canvas()
                    cell.allocation_label['text'] = ""
                    if hasattr(cell, 'opportunity_cost_label'):
                        cell.opportunity_cost_label['text'] = ""
                    if hasattr(cell, 'delta_label'):
                        cell.delta_label['text'] = ""

    def clear_shadow_prices(self):
        # Clear u_values
        for i in range(self.transportation_problem.num_supply_nodes):
            u_label_list = self.grid_slaves(row=i + 2, column=self.transportation_problem.num_demand_nodes + 2)
            if u_label_list:
                u_label = u_label_list[0]
                u_label.config(text="")

        # Clear v_values
        for j in range(self.transportation_problem.num_demand_nodes):
            v_label_list = self.grid_slaves(row=self.transportation_problem.num_supply_nodes + 3, column=j + 1)
            if v_label_list:
                v_label = v_label_list[0]
                v_label.config(text="")

    def update_pivot_cell(self, pivot_cell):
        pivot_label = self.grid_slaves(row=self.transportation_problem.num_supply_nodes + 4,
                                       column=self.transportation_problem.num_demand_nodes + 2)[0]
        if isinstance(pivot_label, ttk.Label):
            pivot_text = f"Pivot Cell: V{pivot_cell[0] + 1}D{pivot_cell[1] + 1}"
            pivot_label['text'] = pivot_text

    def update_total_cost(self):
        total_cost_label = self.grid_slaves(row=self.transportation_problem.num_supply_nodes + 5,
                                            column=self.transportation_problem.num_demand_nodes + 2)[0]
        if isinstance(total_cost_label, ttk.Label):
            total_cost_text = f"Total Cost: {self.transportation_problem.total_cost()}"
            total_cost_label['text'] = total_cost_text

    def update_iteration_count(self):
        self.iteration_label['text'] = f"Iteration: {self.transportation_problem.iteration}"

    def previous_step(self):
        if len(self.states) > 1:  # Ensure there is a previous state
            self.states.pop()  # Remove the current state
            previous_state = self.states[-1]  # Get the previous state

            # Restore the previous state
            self.transportation_problem.allocations = previous_state.allocations
            self.transportation_problem.u_values = previous_state.u_values
            self.transportation_problem.v_values = previous_state.v_values
            self.transportation_problem.iteration = previous_state.iteration

            self.clear_cells()
            self.clear_shadow_prices()

            # Render the previous state to the UI
            self.create_tableau(show_allocations=True, show_shadow_prices=True)
            self.update_total_cost()
            self.update_iteration_count()
            self.state -= 1  # move to previous state

    def next_step(self):
        self.clear_cells()
        self.clear_shadow_prices()

        if self.state == 0:
            self.show_initial_solution()
        elif self.state == 1:
            self.show_shadow_prices_opportunity_costs()
        elif self.state == 2:
            self.show_loop()
        elif self.state == 3:
            self.show_updated_solution()

        self.update_iteration_count()  # update the iteration count on the GUI after each step
        self.states.append(self.transportation_problem.generate_state())  # Save the current state before proceeding

    def show_initial_solution(self):
        if self.selected_ifs.get() == 'NWCR':
            self.transportation_problem.northwest_corner_rule()
        elif self.selected_ifs.get() == 'MCR':
            self.transportation_problem.minimum_cost_rule()
        elif self.selected_ifs.get() == 'VA':
            self.transportation_problem.vogel_approximation_method()

        self.create_tableau(show_allocations=True)
        self.state = 1
        # As soon as the IFS is changed and applied, calculate the shadow prices again
        self.transportation_problem.calculate_shadow_prices()

    def show_shadow_prices_opportunity_costs(self):
        self.transportation_problem.u_values, self.transportation_problem.v_values = self.transportation_problem.calculate_shadow_prices()
        self.create_tableau(show_allocations=True, show_shadow_prices=True, show_opportunity_costs=True)
        self.state = 2

    def show_loop(self):
        pivot_cell = self.transportation_problem.find_pivot_cell()
        loop = self.transportation_problem.identify_loop(pivot_cell)
        self.create_tableau(show_allocations=True, show_shadow_prices=True, show_opportunity_costs=True, loop=loop)
        self.state = 3

    def show_updated_solution(self):
        pivot_cell = self.transportation_problem.find_pivot_cell()
        loop = self.transportation_problem.identify_loop(pivot_cell)
        if loop:
            self.transportation_problem.update_allocations(loop)
        self.create_tableau(show_allocations=True, show_shadow_prices=True, show_opportunity_costs=True)
        if self.transportation_problem.has_positive_deltas():
            self.state = 1
        else:
            self.next_button.config(state="disabled")


def get_inputs():
    # Hardcoded values
    num_supply_nodes = 3
    num_demand_nodes = 3
    supply_values = [40, 30, 30]
    demand_values = [60, 20, 20]
    transportation_costs = [
        [16, 10, 2],
        [12, 4, 6],
        [9, 7, 5]
    ]
    # num_supply_nodes = 3
    # num_demand_nodes = 4
    # supply_values = [45, 60, 50]
    # demand_values = [45, 30, 40, 40]
    # transportation_costs = [
    #     [8, 6, 10, 9],
    #     [9, 12, 13, 7],
    #     [14, 9, 16, 5],
    # ]

    # Convert costs to numpy arrays
    for i in range(num_supply_nodes):
        transportation_costs[i] = np.array(transportation_costs[i])

    return num_supply_nodes, num_demand_nodes, supply_values, demand_values, transportation_costs
    # num_supply_nodes = int(input("Enter the number of supply nodes: "))
    # num_demand_nodes = int(input("Enter the number of demand nodes: "))
    #
    # supply_values = [int(input(f"Enter the supply value for S{i + 1}: ")) for i in range(num_supply_nodes)]
    # demand_values = [int(input(f"Enter the demand value for D{i + 1}: ")) for i in range(num_demand_nodes)]
    #
    # transportation_costs = []
    # for i in range(num_supply_nodes):
    #     row_costs = []
    #     for j in range(num_demand_nodes):
    #         cost = input(f"Enter the transportation cost from S{i + 1} to D{j + 1} or type 'No': ")
    #         if cost.lower() == "no":
    #             row_costs.append(float("inf"))
    #         else:
    #             row_costs.append(int(cost))
    #     transportation_costs.append(np.array(row_costs))
    #
    # return num_supply_nodes, num_demand_nodes, supply_values, demand_values, transportation_costs


# Get initial inputs and create TransportationProblem instance
# initial_data = get_inputs()
# tp = TransportationProblem(*initial_data)

# # Create and display the GUI
# app = TableauGUI(tp)
# app.mainloop()


class Introduction:
    def __init__(self):
        pygame.init()

        # Specify window width and height
        self.width, self.height = 800, 600  # Change as per your requirement
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.font = pygame.freetype.SysFont('Arial', 24, bold=True)  # Change font as per your requirement
        self.font.render_to(self.screen, (self.width // 2 - 100, self.height // 2 - 100), "Introduction", (0, 0, 0))
        
        # Display UCI logo
        self.logo = pygame.image.load('uci_logo.png')  # Replace with your actual logo path
        self.logo = pygame.transform.scale(self.logo, (200, 200))  # Adjust as per your requirement

        # Background image
        self.background = pygame.image.load('background.png')  # Replace with your actual background image path
        self.background = pygame.transform.scale(self.background, (self.width, self.height))  # Resize to window size

        # Color change properties
        self.color_change_time = 1  # Change color every second
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255),
                       (0, 255, 255)]  # RGB colors to cycle through
        self.current_color = 0
        
        # GitHub Link
        self.github_link = "https://github.com/AminAkbariCodes"  # replace with your GitHub link
        self.link_color = (0, 0, 255)  # color for hyperlink
        

    def display_text(self, text, pos_y, color=(0, 0, 0), clickable=False): 
        text_surface, rect = self.font.render(text, color)
        text_rect = text_surface.get_rect(center=(self.width / 2, pos_y))
        self.screen.blit(text_surface, text_rect)
        if clickable:  # If the text is clickable, return both text and rect
            return text, text_rect
        return text_rect

    def run(self):
        global hitchcock_rect, github_rect
        clock = pygame.time.Clock()
        color_time = 0

        hitchcock_text = "Click here to start"

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                # Check for mouse click
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()

                    # Check if Hitchcock text has been clicked
                    if hitchcock_rect.collidepoint(pos):
                        pygame.quit()
                        return

                    # Check if GitHub link has been clicked
                    if github_rect.collidepoint(pos):
                        import webbrowser
                        webbrowser.open(self.github_link)  # Open the GitHub link in the default web browser

            # Display background
            self.screen.blit(self.background, (0, 0))

            # Display logo
            self.screen.blit(self.logo, ((self.width - self.logo.get_width()) // 2, 30))

            # Display institute and university name at the top
            self.display_text("Institute of Transportation Studies", 250, (0, 225, 0))  
            self.display_text("University of California Irvine", 280, (0, 225, 0))

            # Display Hitchcock text in the middle
            self.display_text("The Hitchcock Transportation Problem", 350, (255, 0, 0))
            if pygame.time.get_ticks() - color_time >= self.color_change_time * 1000:  # 1 second has passed
                color_time = pygame.time.get_ticks()
                self.current_color = (self.current_color + 1) % len(self.colors)
            hitchcock_rect = self.display_text(hitchcock_text, 375, color=self.colors[self.current_color])

            # Display developer name and GitHub link at the bottom of the screen
            self.display_text("Developed by Amin Akbari", self.height - 70, color=(255, 255, 0))  
            _, github_rect = self.display_text("GitHub Profile", self.height - 30, color=self.link_color, clickable=True)  

            pygame.display.flip()
            clock.tick(60)

intro = Introduction()
intro.run()


class Menu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))  # Change window size as per your requirement
        self.background = pygame.transform.scale(pygame.image.load('background.png'), (800, 600))
        
        self.screen = pygame.display.set_mode((800, 600))  # Change window size as per your requirement

        self.scroll_y = 0  # variable to control the scroll

        self.manual = self.load_manual()
        self.scroll_x = 0

        self.buttons = {
            "Start the Algorithm": {"action": self.start_algorithm, "icon": pygame.transform.scale(pygame.image.load('start_button.png'), (64, 64))},  # replace 'icon_path' with actual icon path
            "Users Manual": {"action": self.user_manual, "icon": pygame.transform.scale(pygame.image.load('Users_button.png'), (64, 64))},
            "About": {"action": self.about, "icon": pygame.transform.scale(pygame.image.load('help_button.png'), (64, 64))},
            "Exit": {"action": self.exit, "icon": pygame.transform.scale(pygame.image.load('exit_button.png'), (64, 64))},
        }
        self.about_buttons = {
            "UCI": {"url": "https://its.uci.edu/", "icon": pygame.transform.scale(pygame.image.load('uci.jpg'), (64, 64))},
            "Website": {"url": "https://its.uci.edu/~mmcnally", "icon": pygame.transform.scale(pygame.image.load('Website.jpg'), (64, 64))},
            "GitHub": {"url": "https://github.com/AminAkbariCodes", "icon": pygame.transform.scale(pygame.image.load('GitHub.jpg'), (64, 64))},
            "Email": {"url": "mailto:makbarik@uci.edu", "icon": pygame.transform.scale(pygame.image.load('Email.jpg'), (64, 64))},
            "LinkedIn": {"url": "https://linkedin.com/in/amin-akbari", "icon": pygame.transform.scale(pygame.image.load('LinkedIn.jpg'), (64, 64))},
            "Back": {"action": self.display, "icon": pygame.transform.scale(pygame.image.load('back_button.jpg'), (64, 64))},
        }

    def display(self):
        self.running = True
        while self.running:
            self.screen.blit(self.background, (0, 0))  # Add this line to draw the background image
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    for button_name, button_info in self.buttons.items():
                        if button_info["rect"].collidepoint(pos):
                            button_info["action"]()

            for i, (button_name, button_info) in enumerate(self.buttons.items()):
                button_info["rect"] = self.screen.blit(button_info["icon"], ((self.screen.get_width() - button_info["icon"].get_width()) // 2, (i * (button_info["icon"].get_height() + 20)) + (self.screen.get_height() - (len(self.buttons) * (button_info["icon"].get_height() + 20))) // 2))

            pygame.display.flip()

        pygame.quit()

    def start_algorithm(self):

        initial_data = get_inputs()
        tp = TransportationProblem(*initial_data)

        app = TableauGUI(tp)
        app.mainloop()

    def load_manual(self):
        manual = """
        -----------------------USER MANUAL-----------------------

        1. START THE ALGORITHM:
            - Press this button to start the transportation problem solver.
            - You will be prompted to input initial data for the problem.
            - Once the data is entered, the program will display
              the initial tableau.

        2. USER'S MANUAL:
            - You're reading it! This manual helps you understand 
              the functionalities of the application.

        3. ABOUT:
            - This button takes you to a menu with information about 
              the University of California, Irvine (UCI) and 
              the author of this program.
            - You can navigate to UCI's website, the author's website, 
              GitHub page, email, or LinkedIn profile.

        4. EXIT:
            - This button closes the application.

        Once you start the algorithm, you will see the tableau 
        and a menu with the following options:

        1. FILE MENU:
            - OPEN: Load saved problem data.
            - RESTART: Resets the tableau and all data.
            - EXIT: Closes the application.

        2. ALGORITHM MENU:
            - DATA:
                - NEW: Enter new problem data.
                - CHANGE: Modify the current problem data.
            - IFS: Select the Initial Feasible Solution (IFS) method.
                   Options include NWCR (Northwest Corner Rule), MCR 
                   (Minimum Cost Rule), or VA (Vogel's Approximation).

        3. VIEW MENU:
            - SCREENSHOT: Captures a screenshot of the current state of 
              the tableau and saves it.
            - PRINT: Prints out the current state of the tableau.

        4. HELP MENU:
            - ABOUT: Information about the author and the program.
            - CONTACT SUPPORT: Details on how to reach out for help.

        NAVIGATION BUTTONS:
            - BACK: Reverts to the previous step in the algorithm.
            - NEXT: Moves to the next step in the algorithm.

        Enjoy solving transportation problems!

        ---------------------------------------------------------
        """
        return manual.split('\n')

    def user_manual(self):
        manual_screen = True
        while manual_screen:
            self.screen.fill((0, 0, 0))  # fill the screen with black color
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    manual_screen = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:  # mouse wheel rolled up
                        self.scroll_y = min(self.scroll_y + 15, 0)
                    if event.button == 5:  # mouse wheel rolled down
                        self.scroll_y = max(self.scroll_y - 15, -len(self.manual)*30 + 600)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:  # left arrow key pressed
                        self.scroll_x = min(self.scroll_x + 15, 0)
                    if event.key == pygame.K_RIGHT:  # right arrow key pressed
                        self.scroll_x = max(self.scroll_x - 15, -600)  # -600 is an arbitrary limit for the example

            # render the manual text
            for i, line in enumerate(self.manual):
                font = pygame.font.Font(None, 32)  # choose the font for the text (None means default font)
                text = font.render(line, True, (255, 255, 255))  # the text to render, and the color (white)
                self.screen.blit(text, (20 + self.scroll_x, 20 + i*30 + self.scroll_y))  # position of the text

            pygame.display.flip()

    def about(self):
        running = True
        while running:
            self.screen.blit(self.background, (0, 0))  # Add this line to draw the background image
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    for button_name, button_info in self.about_buttons.items():
                        if button_name == "Back":
                            if button_info["rect"].collidepoint(pos):
                                return button_info["action"]()
                        else:
                            if button_info["rect"].collidepoint(pos):
                                webbrowser.open(button_info["url"])

            for i, (button_name, button_info) in enumerate(self.about_buttons.items()):
                button_info["rect"] = self.screen.blit(button_info["icon"], ((self.screen.get_width() - button_info["icon"].get_width()) // 2, (i * (button_info["icon"].get_height() + 20)) + (self.screen.get_height() - (len(self.about_buttons) * (button_info["icon"].get_height() + 20))) // 2))

            pygame.display.flip()

    def exit(self):
        self.running = False  # Add this attribute to signal the game to stop


# Start from the main menu
menu = Menu()
menu.display()
