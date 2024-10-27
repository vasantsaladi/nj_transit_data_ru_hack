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
    
    # Define Stylekit theme based on NJ Transit branding
    stylekit = {
        # Core brand colors
        "--tp-color-primary": "#1B2C5B",        # NJ Transit Navy Blue
        "--tp-color-secondary": "#FFFFFF",       # White
        "--tp-color-background": "#FFFFFF",      # White background
        
        # Text colors
        "--tp-color-text-primary": "#1B2C5B",   # Navy text
        "--tp-color-text-secondary": "#666666",  # Secondary text
        "--tp-color-text-inverse": "#FFFFFF",    # White text for dark backgrounds
        
        # Component specific
        "--tp-border-radius": "8px",
        "--tp-border-color": "#1B2C5B",
        
        # Cards and containers
        "--tp-card-background": "#FFFFFF",
        "--tp-card-border": "1px solid #1B2C5B",
        "--tp-card-shadow": "0 2px 4px rgba(27, 44, 91, 0.1)",
        
        # Buttons
        "--tp-button-background": "#1B2C5B",
        "--tp-button-text": "#FFFFFF",
        "--tp-button-border": "none",
        "--tp-button-hover-background": "#2d4580",
        
        # Charts
        "--tp-chart-primary": "#1B2C5B",
        "--tp-chart-grid": "#E5E5E5",
        "--tp-chart-text": "#1B2C5B",
        
        # Metrics
        "--tp-metric-text": "#1B2C5B",
        "--tp-metric-font-size": "24px",
        "--tp-metric-font-weight": "bold",
        
        # Selectors
        "--tp-selector-border": "1px solid #1B2C5B",
        "--tp-selector-border-radius": "4px",
        "--tp-selector-padding": "0.5rem",
        
        # Tables
        "--tp-table-header-background": "#1B2C5B",
        "--tp-table-header-text": "#FFFFFF",
        "--tp-table-border": "1px solid rgba(27, 44, 91, 0.2)",
        
        # Spacing
        "--tp-spacing-1": "0.5rem",
        "--tp-spacing-2": "1rem",
        "--tp-spacing-3": "1.5rem",
        
        # Custom classes
        "text-center": {"text-align": "center"},
        "color-primary": {"color": "#1B2C5B"},
        "text-bold": {"font-weight": "bold"},
        "mb-3": {"margin-bottom": "1rem"},
        "mb-4": {"margin-bottom": "1.5rem"},
        "mt-4": {"margin-top": "1.5rem"},
        "p-2": {"padding": "0.5rem"},
        "p-4": {"padding": "1.5rem"},
        "gap-3": {"gap": "1rem"},
        "gap-4": {"gap": "1.5rem"}
    }

    # Create GUI with Stylekit
    gui = Gui(pages=pages)
    gui.run(
        title="NJ Transit Analysis",
        stylekit=stylekit,
        favicon="assets/NJ_Transit_Logo.png",
        dark_mode=False,  # Ensure light mode for NJ Transit branding
        port=5001,
        host="0.0.0.0",
        debug=True
    )
