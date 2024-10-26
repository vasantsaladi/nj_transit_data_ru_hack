"""
The first page of the application.
Page content is imported from the page_1.md file.

Please refer to ../../manuals/userman/gui/pages for more details.
"""

from taipy.gui import Markdown
import pandas as pd
import matplotlib.pyplot as plt

def get_data(path_to_csv: str):
    # pandas.read_csv() returns a pd.DataFrame
    dataset = pd.read_csv(path_to_csv)
    dataset["Date"] = pd.to_datetime(dataset["Date"])
    return dataset

# Read the dataframe
path_to_csv = "data/dataset.csv"
dataset = get_data(path_to_csv)

# Initial value
n_week = 10

# Select the week based on the slider value
dataset_week = dataset[dataset["Date"].dt.isocalendar().week == n_week]

def slider_moved(state):
    state.dataset_week = dataset[dataset["Date"].dt.isocalendar().week == state.n_week]


data_viz = Markdown("pages/data_viz/data_viz.md")

chart_style = {
    "color": "#1B2C5B",
    "backgroundColor": "#FFFFFF",
    "borderColor": "#1B2C5B",
    "grid": {
        "color": "#E5E5E5"
    }
}

# Use this style in your charts
plot = plt.figure()

# Plot using dataset_week instead of the placeholder
plt.plot(dataset_week["Date"], dataset_week["Value"], color="#1B2C5B")  # Replace "Value" with your actual column name
