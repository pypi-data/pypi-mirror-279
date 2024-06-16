
# econkit

`econkit` is a Python library that provides various statistical and econometric analysis tools, including descriptive statistics, correlation matrices, and tests for stationarity and autocorrelation.

## Installation

Ensure you have the required packages installed:
```bash
pip install pandas numpy scipy statsmodels tabulate yfinance
```

## Functions

### Descriptive Statistics

#### `descriptives(data)`

Computes descriptive statistics for each numeric column in a DataFrame.

**Parameters:**
- `data`: `pandas.DataFrame` containing the data to be analyzed.

**Returns:**
- None. Prints a summary table of the descriptive statistics.

**Example Usage:**
```python
import pandas as pd
from econkit import econometrics

df = pd.read_csv('your_data.csv')
econometrics.descriptives(df)
```

### Correlation Matrix

#### `correlation(df, method='Pearson', p=False)`

Calculates and prints the correlation matrix and p-values for numeric columns in the provided DataFrame. Supports Pearson, Spearman, and Kendall correlation methods.

**Parameters:**
- `df`: `pandas.DataFrame` containing the data to be analyzed.
- `method`: `str` (optional). Method of correlation ('Pearson', 'Spearman', or 'Kendall'). Default is 'Pearson'.
- `p`: `bool` (optional). If True, p-value matrix is also printed; if False, only the correlation matrix is printed. Default is False.

**Returns:**
- None. Prints the correlation matrix and optionally the p-value matrix.

**Example Usage:**
```python
import pandas as pd
from econkit import econometrics

df = pd.read_csv('your_data.csv')
econometrics.correlation(df, method='Spearman', p=True)
```

### Augmented Dickey-Fuller (ADF) Test

#### `adf(dataframe, maxlag=None, regression='c', autolag='AIC', handle_na='drop')`

Performs the ADF test on each column in the DataFrame and returns a summary table.

**Parameters:**
- `dataframe`: `pandas.DataFrame` containing the data to be tested.
- `maxlag`: `int` (optional). Maximum number of lags to use. Default is None.
- `regression`: `str` {'c', 'ct', 'ctt', 'nc'} (optional). Type of regression trend. Default is 'c'.
- `autolag`: `str` (optional). Method to use when automatically determining the lag length ('AIC', 'BIC', 't-stat'). Default is 'AIC'.
- `handle_na`: `str` {'drop', 'fill'} (optional). How to handle missing values. Default is 'drop'.

**Returns:**
- None. Prints a summary table of the ADF test results.

**Example Usage:**
```python
import pandas as pd
from econkit import econometrics

df = pd.read_csv('your_data.csv')
econometrics.adf(df, regression='ct', autolag='BIC')
```

### KPSS Test

#### `kpss(dataframe, regression='c', nlags='auto', handle_na='drop')`

Performs the KPSS test on each column in the DataFrame and returns a summary table.

**Parameters:**
- `dataframe`: `pandas.DataFrame` containing the data to be tested.
- `regression`: `str` {'c', 'ct'} (optional). Type of regression trend. Default is 'c'.
- `nlags`: `str` or `int` (optional). Number of lags to use. Default is 'auto'.
- `handle_na`: `str` {'drop', 'fill'} (optional). How to handle missing values. Default is 'drop'.

**Returns:**
- None. Prints a summary table of the KPSS test results.

**Example Usage:**
```python
import pandas as pd
from econkit import econometrics

df = pd.read_csv('your_data.csv')
econometrics.kpss(df, regression='ct', nlags='auto')
```

### Durbin-Watson Test

#### `dw(data)`

Performs the Durbin-Watson autocorrelation test and Ljung-Box test for each column of the dataset.

**Parameters:**
- `data`: `pandas.DataFrame` where each column is a time series.

**Returns:**
- None. Prints a summary table of the Durbin-Watson test results.

**Example Usage:**
```python
import pandas as pd
from econkit import econometrics

df = pd.read_csv('your_data.csv')
econometrics.dw(df)
```

### Financial Data Retrieval

#### `data(ticker_symbol, start_date, end_date, interval)`

Downloads stock data from Yahoo Finance and calculates daily returns.

**Parameters:**
- `ticker_symbol`: `str`. The stock ticker symbol.
- `start_date`: `str`. Start date in 'dd-mm-yyyy' format.
- `end_date`: `str`. End date in 'dd-mm-yyyy' format.
- `interval`: `str`. Data interval (e.g., '1d', '1wk', '1mo').

**Returns:**
- `pandas.DataFrame` containing the stock data and calculated returns.

**Example Usage:**
```python
from econkit import finance

data = finance.data('AAPL', '01-01-2020', '31-12-2020', '1d')
print(data)
```

## Usage Notes

- Ensure your data is clean and properly formatted before using these functions.
- Some functions handle missing values; specify your preferred method using the `handle_na` parameter.
- For time series analysis, ensure your data is indexed by date.

For more details, refer to the function docstrings or the examples provided above.
