import pandas as pd
import numpy as np
from scipy.stats import kurtosis, skew, jarque_bera, spearmanr, pearsonr, kendalltau
from statsmodels.tsa.stattools import adfuller, kpss
import statsmodels.api as sm
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.stats.stattools import durbin_watson
from tabulate import tabulate
import yfinance as yf
from datetime import datetime
import os
import warnings


class econometrics:
    @staticmethod
    def descriptives(data):
        """
        Computes descriptive statistics for each numeric column in a DataFrame.

        Parameters:
        data: pandas.DataFrame
            The DataFrame from which the statistics will be calculated.

        Returns:
        None
            Prints a summary table of the descriptive statistics for each numeric column in the DataFrame.
        """
        statistics_labels = ["Mean", "Median", "Min", "Max", "St. Deviation", "Quartile Deviation", "Kurtosis Fisher", "Kurtosis Pearson", "Skewness", "Co-efficient of Q.D", "Jarque-Bera", "p-value"]
        descriptive_df = pd.DataFrame({'STATISTICS': statistics_labels})

        for name in data.columns:
            if pd.api.types.is_numeric_dtype(data[name]):
                column_data = data[name].dropna()

                jb_test = jarque_bera(column_data)
                jb_value = jb_test[0]
                p_value = jb_test[1]

                statistics_values = [
                    format(column_data.mean(), '.3f').lstrip('0') if column_data.mean() < 1 else format(column_data.mean(), '.3f'),
                    format(column_data.median(), '.3f').lstrip('0') if column_data.median() < 1 else format(column_data.median(), '.3f'),
                    format(column_data.min(), '.3f').lstrip('0') if column_data.min() < 1 else format(column_data.min(), '.3f'),
                    format(column_data.max(), '.3f').lstrip('0') if column_data.max() < 1 else format(column_data.max(), '.3f'),
                    format(column_data.std(), '.3f').lstrip('0') if column_data.std() < 1 else format(column_data.std(), '.3f'),
                    format((np.percentile(column_data, 75) - np.percentile(column_data, 25)) / 2, '.3f').lstrip('0') if (np.percentile(column_data, 75) - np.percentile(column_data, 25)) / 2 < 1 else format((np.percentile(column_data, 75) - np.percentile(column_data, 25)) / 2, '.3f'),
                    format(kurtosis(column_data, fisher=True, nan_policy='omit'), '.3f').lstrip('0') if kurtosis(column_data, fisher=True, nan_policy='omit') < 1 else format(kurtosis(column_data, fisher=True, nan_policy='omit'), '.3f'),
                    format(kurtosis(column_data, fisher=False, nan_policy='omit'), '.3f').lstrip('0') if kurtosis(column_data, fisher=False, nan_policy='omit') < 1 else format(kurtosis(column_data, fisher=False, nan_policy='omit'), '.3f'),
                    format(column_data.skew(), '.3f').lstrip('0') if column_data.skew() < 1 else format(column_data.skew(), '.3f'),
                    format((np.percentile(column_data, 75) - np.percentile(column_data, 25)) / 2 / column_data.median(), '.3f').lstrip('0') if column_data.median() != 0 and (np.percentile(column_data, 75) - np.percentile(column_data, 25)) / 2 / column_data.median() < 1 else format((np.percentile(column_data, 75) - np.percentile(column_data, 25)) / 2 / column_data.median(), '.3f') if column_data.median() != 0 else '0.000',
                    format(jb_value, '.3f').lstrip('0') if jb_value < 1 else format(jb_value, '.3f'),
                    format(p_value, '.3f').lstrip('0') if p_value < 1 else format(p_value, '.3f')
                ]

                descriptive_df[name] = statistics_values

        print("=" * (len("Descriptive Statistics") + 2) + "\n" + " Descriptive Statistics" + "\n" + "=" * (len("Descriptive Statistics") + 2) + "\n")
        print(tabulate(descriptive_df, headers='keys', tablefmt='pretty', showindex=False))


    @staticmethod
    def correlation(df, method="Pearson", pvalue=False):
        """
        Calculates and prints the correlation matrix and p-values for numeric columns 
        in the provided DataFrame. Supports Pearson, Spearman, and Kendall correlation methods.

        Parameters:
        df: pandas.DataFrame
            The DataFrame for which correlations are calculated.
        method: str, optional
            The method of correlation ('Pearson', 'Spearman', or 'Kendall'). Default is 'Pearson'.
        pvalue: bool, optional
            If True, p-value matrix is also printed; if False, only correlation matrix 
            is printed. Default is False.

        Returns:
        None
            This function prints the correlation matrix and optionally the p-value
            matrix directly to the console.
        """

        numeric_df = df.select_dtypes(include=[np.number])
        if method == "Pearson":
            print("=" * 21 + f"\n {method} Correlation\n" + "=" * 21)
        elif method == "Spearman":
            print("=" * 27 + f"\n {method} Rank Correlation\n" + "=" * 27)
        elif method == "Kendall":
            print("=" * 25 + f"\n {method} Tau Correlation\n" + "=" * 25)

        corr_matrix = pd.DataFrame(index=numeric_df.columns, columns=numeric_df.columns)
        pmatrix = pd.DataFrame(index=numeric_df.columns, columns=numeric_df.columns)

        keys = numeric_df.columns.tolist()

        for i, key1 in enumerate(keys):
            for j, key2 in enumerate(keys):
                if i > j:
                    continue

                data1 = numeric_df[key1].dropna()
                data2 = numeric_df[key2].dropna()

                common_index = data1.index.intersection(data2.index)
                data1 = data1.loc[common_index]
                data2 = data2.loc[common_index]

                if len(common_index) < 2:
                    corr_matrix.at[key1, key2] = 'nan'
                    corr_matrix.at[key2, key1] = 'nan'
                    continue

                if method == 'Spearman':
                    correlation, p_value = spearmanr(data1, data2)
                elif method == 'Pearson':
                    correlation, p_value = pearsonr(data1, data2)
                elif method == 'Kendall':
                    correlation, p_value = kendalltau(data1, data2)

                pmatrix.at[key1, key2] = format(p_value, '.3f')[1:] if p_value < 1 else format(p_value, '.3f')
                pmatrix.at[key2, key1] = format(p_value, '.3f')[1:] if p_value < 1 else format(p_value, '.3f')

                stars = "     "
                if p_value < 0.001:
                    stars = " *** "
                elif p_value < 0.01:
                    stars = " **  "
                elif p_value < 0.05:
                    stars = " *   "
                elif p_value < 0.1:
                    stars = " .   "

                correlation_str = f"{format(correlation, '.3f')[1:] if correlation < 1 else format(correlation, '.2f')}{stars}"
                corr_matrix.at[key1, key2] = correlation_str
                corr_matrix.at[key2, key1] = correlation_str

        corr_matrix_str = tabulate(corr_matrix, headers='keys', tablefmt='pretty')

        print("\n\n>> Correlation Matrix <<\n")
        print(corr_matrix_str)
        print("\n--\nSignif. codes:  0.001 '***', 0.01 '**', 0.05 '*', 0.1 '.'")

        if pvalue:
            pmatrix_str = tabulate(pmatrix, headers='keys', tablefmt='pretty')
            print("\n\n>> P-Value Matrix <<\n")
            print(pmatrix_str)
            print("\n")
        else:
            print("\n")


    @staticmethod    
    def adf(dataframe, maxlag=None, regression='c', autolag='AIC', handle_na='drop'):
        """
        Perform Augmented Dickey-Fuller (ADF) test on each column in the DataFrame and return a summary table.

        Parameters:
        dataframe: pandas.DataFrame or pandas.Series
            The DataFrame or Series containing time series data to be tested.
        maxlag: int, optional
            Maximum number of lags to use. Default is None, which means the lag length is automatically determined.
        regression: str {'c', 'ct', 'ctt', 'nc'}, optional
            Type of regression trend. Default is 'c' for constant only.
            'c' : constant only (default)
            'ct' : constant and trend
            'ctt' : constant, and linear and quadratic trend
            'nc' : no constant, no trend
        autolag: str, optional
            Method to use when automatically determining the lag length among 'AIC', 'BIC', 't-stat'. Default is 'AIC'.
        handle_na: str {'drop', 'fill'}, optional
            How to handle missing values:
            'drop' : drop missing values (default)
            'fill' : fill missing values forward and then backward

        Returns:
        None
            Prints a summary table of the ADF test results for each column in the DataFrame.

        The summary table includes:
        - ADF Statistic
        - Significance codes
        - P-value
        - Number of lags used
        - Number of observations
        - Information Criterion
        - Critical values at 1%, 5%, and 10%
        """
        def adf_test(series):
            # Handle NaN and infinite values
            if handle_na == 'drop':
                series = series.dropna()
            elif handle_na == 'fill':
                series = series.fillna(method='ffill').fillna(method='bfill')

            # Ensure no infinite values
            series = series[np.isfinite(series)]
            
            if series.size == 0:
                return {
                    'ADF Stat.': 'nan',
                    'P-Value': 'nan',
                    'Number of Lags Used': 'nan',
                    'Number of Observations': 'nan',
                    'Information Criterion': 'nan',
                    'critical value 1%': 'nan',
                    'critical value 5%': 'nan',
                    'critical value 10%': 'nan'
                }

            try:
                result = adfuller(series, maxlag=maxlag, regression=regression, autolag=autolag)
            except Exception as e:
                print(f"ADF test failed for series: {series.name}, error: {e}")
                return {
                    'ADF Stat.': 'nan',
                    'P-Value': 'nan',
                    'Number of Lags Used': 'nan',
                    'Number of Observations': 'nan',
                    'Information Criterion': 'nan',
                    'critical value 1%': 'nan',
                    'critical value 5%': 'nan',
                    'critical value 10%': 'nan'
                }

            adf_stat = round(result[0], 3)
            p_value = result[1]
            used_lag = result[2]
            n_obs = result[3]
            critical_values = result[4]
            ic_best = round(result[5], 3) if autolag is not None else None

            # Determine significance codes
            stars = ""
            if p_value < 0.001:
                stars = " ***"
            elif p_value < 0.01:
                stars = " **"
            elif p_value < 0.05:
                stars = " *"
            elif p_value < 0.1:
                stars = " ."

            summary = {
                'ADF Stat.': f"{adf_stat:.3f}{stars}",
                'P-Value': f"{p_value:.3f}",
                'Number of Lags Used': used_lag,
                'Number of Observations': n_obs,
                'Information Criterion': ic_best
            }

            # Adding critical values to the summary
            for key, value in critical_values.items():
                summary[f'critical value {key}'] = round(value, 3)

            return summary

        if isinstance(dataframe, pd.Series):
            # If the input is a Series, convert it to a DataFrame with one column
            dataframe = dataframe.to_frame(name=dataframe.name)

        # Apply the ADF test to each column in the DataFrame
        adf_results = dataframe.apply(adf_test)

        # Transform the results into a DataFrame with the desired structure
        result_dict = {series_name: results for series_name, results in adf_results.items()}

        # Create the result DataFrame
        results_df = pd.DataFrame(result_dict)

        print("=" * (len("Augmented Dickey-Fuller Test") + 2) + "\n" + " Augmented Dickey-Fuller Test" + "\n" + "=" * (len("Augmented Dickey-Fuller Test") + 2) + "\n")
        print(tabulate(results_df, headers='keys', tablefmt='pretty', showindex=True))
        print("\n--\n" + "Signif. codes:  0.001 '***', 0.01 '**', 0.05 '*', 0.1 '.'\n")



    @staticmethod    
    def kpss(dataframe, regression='c', nlags='auto', handle_na='drop'):
        """
        Perform Kwiatkowski-Phillips-Schmidt-Shin test on each column in the DataFrame and return a summary table.

        Parameters:
        dataframe: pandas.DataFrame or pandas.Series
            The DataFrame or Series containing time series data to be tested.
        regression: str {'c', 'ct'}, optional
            Type of regression trend. Default is 'c' for constant only.
            'c' : constant only (default)
            'ct' : constant and trend
        nlags: str or int, optional
            Number of lags to use. Default is 'auto' which uses automatic lag selection.
        handle_na: str {'drop', 'fill'}, optional
            How to handle missing values:
            'drop' : drop missing values (default)
            'fill' : fill missing values forward and then backward

        Returns:
        None
            Prints a summary table of the KPSS test results for each column in the DataFrame.

        The summary table includes:
        - KPSS Statistic
        - Significance codes
        - P-value
        - Number of lags used
        - Critical values at 1%, 5%, and 10%
        """
        def kpss_test(series):
            # Handle NaN values
            if handle_na == 'drop':
                series = series.dropna()
            elif handle_na == 'fill':
                series = series.fillna(method='ffill').fillna(method='bfill')

            # Ensure no infinite values
            series = series[np.isfinite(series)]
            
            if series.size == 0:
                return {
                    'KPSS Stat.': 'nan',
                    'P-Value': 'nan',
                    'Number of Lags Used': 'nan',
                    'critical value 1%': 'nan',
                    'critical value 5%': 'nan',
                    'critical value 10%': 'nan'
                }

            try:
                with warnings.catch_warnings(record=True) as w:
                    warnings.simplefilter("always")
                    result = kpss(series, regression=regression, nlags=nlags)
                    p_value = result[1]
                    if any("InterpolationWarning" in str(warn.message) for warn in w):
                        p_value = '> {}'.format(p_value)
            except Exception as e:
                print(f"KPSS test failed for series: {series.name}, error: {e}")
                return {
                    'KPSS Stat.': 'nan',
                    'P-Value': 'nan',
                    'Number of Lags Used': 'nan',
                    'critical value 1%': 'nan',
                    'critical value 5%': 'nan',
                    'critical value 10%': 'nan'
                }

            kpss_stat = round(result[0], 3)
            lags_used = result[2]
            critical_values = result[3]

            # Determine significance codes
            stars = "     "
            if p_value < 0.001:
                stars = " ***"
            elif p_value < 0.01:
                stars = " **"
            elif p_value < 0.05:
                stars = " *"
            elif p_value < 0.1:
                stars = " ."

            summary = {
                'KPSS Stat.': f"{kpss_stat:.3f}{stars}",
                'P-Value': f"{p_value:.3f}",
                'Number of Lags Used': lags_used,
                'critical value 1%': round(critical_values['1%'], 3),
                'critical value 5%': round(critical_values['5%'], 3),
                'critical value 10%': round(critical_values['10%'], 3)
            }

            return summary

        if isinstance(dataframe, pd.Series):
            # If the input is a Series, convert it to a DataFrame with one column
            dataframe = dataframe.to_frame()

        # Apply the KPSS test to each column in the DataFrame
        kpss_results = dataframe.apply(kpss_test).T

        # Transform the results into a DataFrame with the desired structure
        result_dict = {series_name: results for series_name, results in kpss_results.items()}

        # Create the result DataFrame
        results_df = pd.DataFrame(result_dict)

        print("=" * (len("Kwiatkowski-Phillips-Schmidt-Shin Test") + 2) + "\n" + " Kwiatkowski-Phillips-Schmidt-Shin Test" + "\n" + "=" * (len("Kwiatkowski-Phillips-Schmidt-Shin Test") + 2) + "\n")
        print(tabulate(results_df, headers='keys', tablefmt='pretty', showindex=True))
        print("\n--\n" + "Signif. codes:  0.001 '***', 0.01 '**', 0.05 '*', 0.1 '.'\n")

    
    @staticmethod 
    def dw(data):
        """
        Perform Durbin-Watson autocorrelation test and Ljung-Box test for each column of the dataset.
        
        Parameters:
        data (pd.DataFrame): A pandas DataFrame where each column is a time series.
        
        Returns:
        pd.DataFrame: A DataFrame containing the Durbin-Watson statistic and p-values for each column.
        """
        results = []

        for column in data.columns:
            time_series = data[column].dropna()
            if len(time_series) > 1:  # Ensure there are enough data points for regression
                X = sm.add_constant(range(len(time_series)))  # Add constant term for intercept
                model = sm.OLS(time_series, X).fit()
                dw_statistic = durbin_watson(model.resid)
                lb_test = acorr_ljungbox(model.resid, lags=[1], return_df=True)
                p_value = lb_test['lb_pvalue'].iloc[0]
                results.append((column, format(dw_statistic, '.3f'), format(p_value, '.3f')[1:] if p_value < 1 else format(p_value, '.3f')))
            else:
                results.append((column, None, None))  # Not enough data points for regression

        results_df = pd.DataFrame(results, columns=[' ', ' Stat.', 'P-Value'])
        results_df = results_df.set_index(' ')

        print("=" * (len("Durbin-Watson Test") + 2) + "\n" + " Durbin-Watson Test" + "\n" + "=" * (len("Durbin-Watson Test") + 2) + "\n\n")
        print(results_df.to_string(index=True))        

class finance:
    @staticmethod
    def data(ticker_symbol: str, start_date: str, end_date: str, interval: str) -> pd.DataFrame:
        def convert_date_format(date_string):
            return datetime.strptime(date_string, '%d-%m-%Y').strftime('%Y-%m-%d')

        start_date = convert_date_format(start_date)
        end_date = convert_date_format(end_date)

        stock_data = yf.download(ticker_symbol, start=start_date, end=end_date, interval=interval)
        stock_data['Returns'] = stock_data['Adj Close'].pct_change()

        folder_name = "Stocks"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        file_name = f"{folder_name}/{ticker_symbol}_{interval}.csv"
        stock_data.to_csv(file_name)

        return stock_data
