# Fast_Profiling_UI

Fast_Profiling_UI is an Exploratory Data Analysis (EDA) package designed for data engineers, providing a user-friendly UI to perform various data analysis tasks efficiently. This package leverages `pandas`, `numpy`, and `tkinter` to offer insightful and interactive data analysis.

## Features

- **Overview**: Get a comprehensive summary of your dataset, including statistics such as the number of columns, rows, duplicate rows, missing values, and memory usage.
- **Sample**: View sample data from the dataset, including top and bottom rows.
- **Variables**: Analyze individual columns, displaying statistics such as distinct values, missing values, mean, minimum, maximum, and more.

## Installation

To install the Fast_Profiling_UI package, you need to have Python 3.6 or later installed on your system. You can install the package using `pip`:

```sh
pip install Fast_Profiling_UI
```

## Usage

Here's a quick guide on how to use the Fast_Profiling_UI package.

### Importing the Package

First, import the package in your Python script:

```python
import Fast_Profiling_UI
```

### Loading a DataFrame

Load your data into a pandas DataFrame. For example:

```python
import pandas as pd

# Load your dataset
df = pd.read_csv('your_data.csv')
```

### Performing EDA

Use the `de_analysis` function to start the UI for exploratory data analysis:

```python
Fast_Profiling_UI.de_analysis(df)
```

This will open a UI window with buttons for different analysis options:

- **Overview**: Provides a summary of the dataset.
- **Missing Values**: Analyzes and displays missing values in the dataset.
- **Variable**: Displays detailed statistics for each column in the dataset.
- **Sample**: Allows viewing samples of the dataset (top and bottom rows).

## Detailed Example

Here is a detailed example to help you get started:

```python
import pandas as pd
import Fast_Profiling_UI

# Load your dataset
df = pd.read_csv('your_data.csv')

# Start the EDA UI
Fast_Profiling_UI.de_analysis(df)
```

## Development

### Setting Up the Development Environment

If you want to contribute to the development of Fast_Profiling_UI, follow these steps to set up your development environment:

1. Clone the repository:
    ```sh
    git clone https://github.com/Mukesh-Kumar-Madhur
    cd Fast_Profiling_UI
    ```

2. Create a virtual environment:
    ```sh
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:
        ```sh
        venv\Scripts\activate
        ```

    - On macOS and Linux:
        ```sh
        source venv/bin/activate
        ```

4. Install the package in development mode:
    ```sh
    pip install -e .
    ```

### Running Tests

Ensure your changes do not break any functionality by running tests. You can add tests in the `tests` directory and run them using a testing framework like `pytest`.

### Code Structure

- `Fast_Profiling_UI/`
    - `__init__.py`: Initializes the package and defines the main `de_analysis` function.
    - `Sample.py`: Defines the `Sample` function for displaying sample data.
    - `Variables.py`: Defines the `Variables` function for analyzing individual columns.
    - `Overview.py`: Defines the `show_overview` function for summarizing the dataset.
