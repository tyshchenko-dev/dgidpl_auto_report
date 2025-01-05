# Arrest Report for the Department of Main Inspection and Human Rights Compliance in Ukraine.

A simple Python console utility for generating arrest reports based on Excel files.

---

## Description

This repository contains a console application that automatically processes Excel files containing arrest data, filters them by regions and date ranges, aggregates the necessary metrics, and generates a final report. The application is also equipped with an interactive start menu for convenient selection of operation modes.

---

## Features

- **File Parsing**: Processes files named in the format `<region>_<month>_<year>.xlsx` (e.g., `Kyivska_01_2025.xlsx`).
- **Data Filtering**: Selects files based on specified regions and date ranges.
- **Data Aggregation**: Combines data from multiple files and calculates key metrics.
- **Report Generation**: Creates a final Excel file with the aggregated results.
- **Interactive Menu**: Allows users to choose the operation mode through a user-friendly text menu.
- **Logging**: Logs the utility's operations to track the process and errors.

---

## Repository Structure

- **`report.py`** — Module for processing and generating reports.
- **`main.py`** — Script with the start menu for selecting the operation mode.
- **`requirements.txt`** — List of required libraries.
- **`reports/`** — Directory for placing input Excel files.
- **`LICENSE`** — License file.
- **`README.md`** — This file.

---

## Installation

### Requirements

- **Python 3.6+**

**Libraries**:
- `pandas`
- `openpyxl`
- `questionary`
- `emoji`

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tyshchenko-dev/dgidpl_auto_report.git

2. **Navigate to the project directory:

```bash
cd dgidpl_auto_report
```

3. **Create and activate a virtual environment (optional):

```bash
python -m venv venv
source venv/bin/activate  # For Unix or MacOS
venv\Scripts\activate     # For Windows
```
4. **Install the required dependencies:

```bash
pip install -r requirements.txt
```

