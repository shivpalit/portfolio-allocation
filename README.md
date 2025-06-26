# Portfolio Allocation Tool (Early Learning Project)

> **Note**: This was an early side project when I first started learning about portfolio analytics and was never completed. It serves as a snapshot of my initial exploration into financial programming.

## Project Overview
A simple Python tool that experiments with portfolio optimization using the Sharpe ratio. The program allows users to:
- Input a list of stock tickers
- Set investment amount and exposure limits
- Generate portfolio allocations based on historical data
- Calculate expected returns, volatility, and Sharpe ratios

## Features
- Monte Carlo simulation for portfolio optimization
- Efficient frontier visualization
- Basic portfolio metrics calculation
- Stock data fetching using Yahoo Finance API

## Example Usage
See `Example.ipynb` for a demonstration of:
- Creating a portfolio with multiple stocks
- Setting investment constraints
- Generating optimal allocations
- Viewing performance metrics

## Technical Stack
- Python
- pandas_datareader for stock data
- NumPy for calculations
- Matplotlib for visualizations
- SciPy for optimization

## Running the Code
1. Ensure you have the required packages installed
2. Import the `Portfolio` class from `MontePython.py`
3. Follow the example in `Example.ipynb`

## Limitations
This was a learning exercise and has several limitations:
- Basic optimization strategy
- Limited risk metrics
- No transaction costs consideration
- No regular rebalancing logic

