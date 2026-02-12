# Country Economics Dashboard

A comprehensive interactive dashboard for exploring global economic indicators and statistics across different countries and regions.

## Overview

This project creates an interactive visualization dashboard that displays economic data for countries worldwide. It provides multiple perspectives on economic metrics including GDP, unemployment rates, inflation, debt-to-GDP ratios, and interest rates.

## Features

- **Top 20 GDP Ranking**: Bar chart showing the 20 largest global economies by GDP with region-based color coding
- **Regional Unemployment Analysis**: Average unemployment rates aggregated by geographic region
- **Parallel Coordinates Plot**: Visualization of economic metrics (GDP Growth, Interest Rate, Debt to GDP Ratio) with interactive filtering
- **Interactive Filtering**: Selection and filtering capabilities across all visualizations for dynamic data exploration
- **Multi-view Dashboard**: Coordinated views that respond to user interactions

## Data

The project uses `country_economics_data.csv` which contains economic indicators for 175 countries including:

- **Basic Information**: Country name, ISO codes, currency, capital, language
- **Geographic Data**: Latitude, longitude, area, population, region, subregion
- **Economic Indicators**:
  - GDP (Billions USD)
  - GDP Growth (%)
  - Interest Rate (%)
  - Inflation Rate (%)
  - Unemployment Rate (%)
  - Government Budget
  - Debt to GDP Ratio (%)
  - Current Account

## Requirements

- Python 3.x
- pandas
- altair

## Installation

1. Clone the repository
2. Install required dependencies:
   ```bash
   pip install pandas altair
   ```

## Usage

Run the main script to generate the dashboard:

```bash
python main.py
```

This will create an interactive HTML dashboard (`final_dashboard.html`) that can be opened in a web browser.

## Files

- `main.py`: Main Python script that processes data and generates visualizations
- `country_economics_data.csv`: Economic dataset containing country-level statistics
- `final_dashboard.html`: Generated interactive dashboard (output)

## Dashboard Components

### View 1: Top 20 Global Economies
Bar chart ranking countries by GDP with interactive country selection highlighting.

### View 2: Regional Unemployment
Average unemployment rates by region with region-based filtering.

### View 3: Parallel Coordinates Plot
Multi-metric visualization showing relationships between GDP Growth, Interest Rate, and Debt to GDP Ratio.

## Interactive Features

- **Country Selection**: Click on bars to highlight specific countries
- **Region Filtering**: Interact with the unemployment chart to filter data by region
- **Tooltips**: Hover over data points to see detailed information
- **Cross-filtering**: Selections in one view automatically filter data in related views

## Author

CSC3833 Coursework Project

## License

This project is part of CSC3833 coursework.
