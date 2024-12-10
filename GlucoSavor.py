#GlucoSavor Computer Application
#Michael Edwin Gage
#12/05/2024

#DESCRIPTION: This program can be utilized to search a food database and determine if the food of interest has a
#High, Medium, or Low Glycemic Load. This data helps those with diabetes determine what is safe to eat, and helps guide
#theminto better informed dietary habits and decisions.



#------------------------------------- LOADING IN DATA/LIBRARIES AND INSPECTING THE DATA ----------------------------------------------

import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import font
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import PhotoImage

# Load the CSV file
file_path = "C:/Users/micha/OneDrive/Documents/GlucoSaver/gi_gl_data.csv"  # Replace with the correct path

#Inspecting the data to make sure everything is a-ok
#try:
   # data = pd.read_csv(file_path)
    #print("Data loaded successfully!\n")
    #print("Dataset preview:")
    #print(data.head())  # Show first few rows
    #print("\nDataset info:")
    #print(data.info())  # Show dataset structure
#except Exception as e:
    #print(f"Error loading data: {e}")



# ---------------------------------- SEARCH FUNCTION AND MAIN PROGRAM PROCESSING --------------------------------------

# Search function
def search_food(data, keyword):
    """
    Search for a food item in the dataset (case-insensitive).
    :param data: Pandas DataFrame containing the data.
    :param keyword: Search term (string).
    :return: Filtered DataFrame with search results.
    """
    results = data[data['Food'].str.contains(keyword, case=False, na=False)]
    return results


# ---------------------------------------- GUI IMPLEMENTATION ----------------------------------------------------------

def display_results():
    """
    Display the search results in the GUI.
    """
    keyword = search_entry.get()  # Get user input from the entry widget
    results = search_food(data, keyword)

    # Clear previous results
    for row in results_tree.get_children():
        results_tree.delete(row)

    if not results.empty:
        # Populate the results tree
        for _, row in results.iterrows():
            gl_rating = row['GL_Rating'].strip().lower()  # Trim whitespace and normalize case
            if gl_rating == 'low':
                color = 'green'
            elif gl_rating == 'med':
                color = 'yellow'
            elif gl_rating == 'high':
                color = 'red'
            else:
                color = 'gray'  # Handle unexpected values gracefully

            results_tree.insert('', 'end', values=(row['Food'], row['GI'], row['GL'], row['GL_Rating']), tags=(color,))
    else:
        results_tree.insert('', 'end', values=("No results found.", "", "", ""), tags=('gray',))

def show_food_details(event):  # *** Updated Function ***
    """
    Display details about the selected food in a popup window.
    """
    selected_item = results_tree.selection()  # Get selected item
    if selected_item:
        item_values = results_tree.item(selected_item, "values")
        food, gi, gl, gl_rating = item_values

        # Create a popup window
        details_window = tk.Toplevel(window)
        details_window.title(f"{food}")
        details_window.geometry("400x670")  # Adjusted height for better spacing

        # Display food title with underline
        title_font = ("Arial Rounded MT", 18, "underline", "bold")  # *** Added Underline Style ***
        tk.Label(details_window, text=f"{food}", font=title_font).pack(pady=(20, 10))

        # Display details (center-aligned)
        detail_labels = [
            ("Glycemic Index (GI):", gi),
            ("Glycemic Load (GL):", gl),
            ("GL Zone:", gl_rating.capitalize())
        ]
        for label, value in detail_labels:
            tk.Label(details_window, text=label, font=("Arial Rounded MT", 12, "bold"), justify="center").pack(pady=(5, 0))  # *** Center-Aligned Label ***
            tk.Label(details_window, text=value, font=("Arial Rounded MT", 12), justify="center").pack(pady=(0, 10))  # *** Center-Aligned Value ***

        # Add explanations
        tk.Label(details_window, text="\nWhat the numbers mean:", font=subheading_font).pack(pady=10)

        explanation_texts = [
            ("Glycemic Index (GI):", "Measures how quickly a food raises blood sugar."),
            ("Glycemic Load (GL):", "Considers both the quality (GI) and quantity of carbs."),
            ("GL Zone:", "Categorizes food as Low (0-10), Medium (10-20), or High (20-30).")
        ]
        for title, explanation in explanation_texts:
            tk.Label(details_window, text=title, font=("Arial Rounded MT", 12, "bold"), anchor="w").pack(anchor="w", padx=20)
            tk.Label(details_window, text=explanation, font=label_font, wraplength=350, justify="left").pack(anchor="w", padx=20, pady=(0, 10))

        # Draw bar gauge
        draw_bar_gauge(details_window, float(gl))


def draw_bar_gauge(parent, gl_value):  # *** Updated Function ***
    """
    Draw a segmented horizontal bar gauge with a dynamic tick mark and number scale.
    """
    canvas_width = 320
    canvas_height = 100
    bar_start = 30  # Padding for scale
    bar_width = canvas_width - 2 * bar_start
    bar_height = 20

    # Create canvas
    canvas = tk.Canvas(parent, width=canvas_width, height=canvas_height, bg="#f0f0f0", highlightthickness=0)
    canvas.pack(pady=20)

    # Define GL ranges and colors
    ranges = [
        (0, 10, 'green'),  # Low
        (10, 20, 'yellow'),  # Medium
        (20, 30, 'red')  # High
    ]

    # Draw the segmented bar
    for start, end, color in ranges:
        x1 = bar_start + (start / 30) * bar_width
        x2 = bar_start + (end / 30) * bar_width
        canvas.create_rectangle(x1, canvas_height // 2 - bar_height // 2, x2, canvas_height // 2 + bar_height // 2, fill=color, outline=color)

    # Draw number scale and ticks
    for i in range(0, 31, 10):  # Numbers: 0, 10, 20, 30
        x = bar_start + (i / 30) * bar_width
        canvas.create_line(x, canvas_height // 2 + bar_height // 2, x, canvas_height // 2 + bar_height // 2 + 10, fill="black")
        canvas.create_text(x, canvas_height // 2 + bar_height // 2 + 20, text=str(i), font=("Arial Rounded MT", 10), fill="black")

    # Add dynamic tick mark for GL value
    tick_x = bar_start + (gl_value / 30) * bar_width
    canvas.create_line(tick_x, canvas_height // 2 - bar_height // 2 - 10, tick_x, canvas_height // 2 + bar_height // 2 + 10, fill="black", width=2)
    canvas.create_text(
        tick_x, canvas_height // 2 - bar_height // 2 - 20,  # Adjust position above the tick
        text=f"{int(round(gl_value))}",  # Display rounded whole number
        font=("Arial Rounded MT", 12, "bold"),  # Larger and bold font
        fill="black"
    )

# Create GUI Window
window = tk.Tk()
# Load and display the GlucoSavor logo
try:
    logo = PhotoImage(file="C:/Users/micha/OneDrive/Documents/GlucoSaver/GlucoSavorLogo.png")
    logo_label = tk.Label(window, image=logo, bg="#f0f0f0")
    logo_label.image = logo  # Keep a reference to prevent garbage collection
    logo_label.pack(pady=20)  # Adjust padding as needed
except Exception as e:
    print(f"Error loading logo: {e}")

window.title("GlucoSavor: A Food Glucose Search Tool")
window.geometry("800x900")
window.configure(bg="#f0f0f0")


# Custom fonts
header_font = font.Font(family="Arial Rounded MT", size=18)
label_font = font.Font(family="Arial Rounded MT", size=12)
button_font = font.Font(family="Arial Rounded MT", size=12)
results_font = font.Font(family="Arial Rounded MT", size=12)
exp_font = font.Font(family="Arial Rounded MT", size=10)
subheading_font = font.Font(family="Arial Rounded MT", size=15, weight="bold")


# Search bar
search_frame = tk.Frame(window, bg="#f0f0f0")
search_frame.pack(pady=10)

tk.Label(search_frame, text="Search Food:", font=label_font, bg="#f0f0f0").grid(row=0, column=0, padx=5)
search_entry = tk.Entry(search_frame, font=label_font, width=30)
search_entry.grid(row=0, column=1, padx=5)
search_entry.bind("<Return>", lambda event: display_results())  # Bind Enter key (already present but highlighted)

search_button = tk.Button(search_frame, text="Search", font=button_font, command=display_results)
search_button.grid(row=0, column=2, padx=5)

# Results table
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", font= results_font, rowheight=25)
style.configure("Treeview.Heading", font=(None, 12, "bold"), background="#d3d3d3")
style.map("Treeview.Heading", background=[("active", "#a9a9a9")])

columns = ('Food', 'GI', 'GL', 'GL_Rating')
results_tree = ttk.Treeview(window, columns=columns, show='headings', height=15)
results_tree.pack(pady=20, padx=20)

for col in columns:
    results_tree.heading(col, text=col, anchor="w")
    results_tree.column(col, width=150, anchor="w")

# Adjust column widths
results_tree.heading('Food', text='Food')
results_tree.column('Food', width=200)  # Increased width for the Food column

results_tree.heading('GI', text='GI')
results_tree.column('GI', width=50)

results_tree.heading('GL', text='GL')
results_tree.column('GL', width=50)

results_tree.heading('GL_Rating', text='GL Rating')
results_tree.column('GL_Rating', width=100)

results_tree.pack(pady=10)

# Add color coding for results
results_tree.tag_configure('green', background='lightgreen')
results_tree.tag_configure('yellow', background='#FFD700')
results_tree.tag_configure('red', background='lightcoral')
results_tree.tag_configure('gray', background='lightgray')

# Bind event to display food details
results_tree.bind("<Double-1>", show_food_details)  # *** Added Event Binding ***

# ----------------------------------------- RUN THE APPLICATION --------------------------------------------------------

try:
    data = pd.read_csv(file_path)
    print("Data loaded successfully!")
    window.mainloop()  # *** Added for GUI ***
except Exception as e:
    print(f"Error: {e}")