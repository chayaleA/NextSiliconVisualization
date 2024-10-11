# Visual Analyzer for HW Simulator

## Description:
This project provides a visual analyzer for the full application execution in a hardware simulator. It acts as a debugging tool after the full execution of an application on a chip. With this tool, you can easily track logs passing from one component to another across all chip layers and visually identify bugs.

## Features:
- **Top Navigation**: Displays top components. Clicking on a component allows navigation to its lower layers.
- **Thread Coloring**: Each thread ID is assigned a unique color. When a component is selected, it is highlighted in the color of the thread that first entered it.
- **Multiple Threads**: If several threads pass through a component, it will display the color of the first thread.
- **Component Interaction**: Right-click on any component to view all threads and packets passing through it. This allows for easy tracking of threads across components to identify bugs and crash locations.
- **Inactive Components**: These components are displayed as inactive and cannot be clicked.

### Main Interface and Die Visualization

<div style="display: flex; flex-wrap: wrap;">
    <img src="images/die_display.png" alt="Main Interface" width="300" style="margin-right:5px;"/>
    <img src="images/host_interface_display.png" alt="Host Interface Layer" width="300" style="margin-right:5px;"/>
        <img src="images/clusters_display.png" alt="Die Visualization" width="300"/>

</div>

## Filtering and Timeline:
- The application includes filtering options based on specific categories. 
- Filters can be toggled on and off by clicking on the relevant filter.
- A dedicated button is available to clear all filters.
- The timeline shows two points indicating the start and end of the time range used to filter logs.

### Filter Images

<div style="display: flex; flex-wrap: wrap;">
    <img src="images/filters_menu_display.png" alt="Filter List" width="200" style="margin-right: 40px;"/>
    <img src="images/filter_by_clusterId_window_display.png" alt="Filter Window" width="350"/>
    <img src="images/filters_selected_in_menu_display.png" alt="Filter List Vertical" width="200" style="margin-right: 20px;"/>
</div>

## Initial Setup:

Upon launching the application, you will be prompted to select two files:
1. **SL File**: This file contains the configuration data for the system.
2. **Log File**: This file contains the execution logs.

Only after selecting both files and pressing the **Proceed** button will the program start processing the data and display the visual analysis.

<div style="display: flex; justify-content: center;">
    <img src="images/file_selection_window_display.png" alt="File Selection" width="300"/>
</div>

## Installation and Setup:

To install the necessary dependencies, use the following commands:

```bash
cd NextUtils\Visualization\Visualization_Python
pip install -r requirements.txt
py utils/setup.py clean --all
py utils/setup.py build_ext --inplace
py main.py
```

## Contributors

This project was developed by a talented and dedicated team:
- [Adina kashash](https://github.com/adinakashash)
- [Dvori Stern](https://github.com/DvoriStern)
- [Ruth Shalom](https://github.com/ruty888)
- [Eti Avni](https://github.com/ett5)
- [Yael Frank](https://github.com/yuliftank)

