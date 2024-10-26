"""
A multi-page Taipy application, which includes 3 pages:
- A rootpage which is shared by other pages.
- Two pages named page_1 and page_2.

Please refer to ../../manuals/userman/gui/pages for more details.
"""

from pages import data_viz, scenario_page, performance
print("Pages imported successfully")
from pages.root import *
print("Root page imported successfully")

from configuration.config import *

from taipy.gui import Gui
import taipy as tp

def on_change(state, var_name: str, var_value):
    state['scenario'].on_change(state, var_name, var_value)


pages = {
    "/": root_page,
    "data_viz": data_viz,
    "scenario": scenario_page,
    "performance": performance
}



if __name__ == "__main__":
    # Initialize Core first
    tp.Core().run()
    
    # Define a more comprehensive style dictionary
    style = {
        # Primary Colors
        "color_primary": "#1B2C5B",      # NJ Transit navy blue
        "color_secondary": "#FFFFFF",     # White
        "color_background": "#FFFFFF",    # White background
        "color_paper": "#F5F5F5",        # Light gray for cards/panels
        
        # Text Colors
        "color_text_primary": "#1B2C5B",  # Navy blue for primary text
        "color_text_secondary": "#666666", # Dark gray for secondary text
        
        # Component Colors
        "button": {
            "background_color": "#1B2C5B",
            "color": "#FFFFFF",
            "border_radius": "4px",
        },
        "button_secondary": {
            "background_color": "#FFFFFF",
            "color": "#1B2C5B",
            "border": "1px solid #1B2C5B",
            "border_radius": "4px",
        },
        
        # Chart Colors
        "chart_primary_color": "#1B2C5B",
        "chart_colors": ["#1B2C5B", "#4A90E2", "#E2844A", "#50C878"],
        
        # Tables
        "table_header_background": "#1B2C5B",
        "table_header_color": "#FFFFFF",
        "table_cell_background": "#FFFFFF",
        "table_cell_color": "#1B2C5B",
        
        # Controls
        "selector_background": "#FFFFFF",
        "selector_border": "1px solid #1B2C5B",
        "selector_color": "#1B2C5B",
        
        # Layout
        "margin": "1rem",
        "padding": "1rem",
        "border_radius": "8px",
    }

    # Create GUI with specific host and port
    gui = Gui(pages=pages)
    gui.run(
        title="NJ Transit Analysis",
        style=style,
        favicon="assets/NJ_Transit_Logo.png",  # Add the favicon path here
        port=5001,  # Use a specific different port
        host="0.0.0.0",
        debug=True
    )
