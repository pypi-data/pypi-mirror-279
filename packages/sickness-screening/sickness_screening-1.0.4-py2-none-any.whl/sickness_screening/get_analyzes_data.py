import pandas as pd


def get_analyzes_data(analyzes_df=None, analyzes_csv='chartevents.csv', subject_id_col='subject_id',
                      itemid_col='itemid',
                      charttime_col='charttime', value_col='value', valuenum_col='valuenum', valueuom_col='valueuom',
                      itemids=None, rest_columns=None, output_csv=None):
    """
    Extracts specific item IDs from chartevents data, pivots the table, and optionally saves the result to a CSV file.
    This function reads chartevents data from a DataFrame or a CSV file, filters it based on specified item IDs, pivots the table to
    have item IDs as columns, and optionally saves the resulting data to a CSV file.

    Args:
        analyzes_df (pd.DataFrame, optional): DataFrame containing chartevents data. Default is None.
        analyzes_csv (str, optional): Path to the CSV file containing chartevents data. Default is 'chartevents.csv'.
        subject_id_col (str): Column name for subject IDs. Default is 'subject_id'.
        itemid_col (str): Column name for item IDs. Default is 'itemid'.
        charttime_col (str): Column name for chart times. Default is 'charttime'.
        value_col (str): Column name for values. Default is 'value'.
        valuenum_col (str): Column name for numeric values. Default is 'valuenum'.
        valueuom_col (str): Column name for units of measurement. Default is 'valueuom'.
        itemids (list of int, optional): List of item IDs to filter. Default is None, which uses [220045, 220210, 223762, 223761, 225651].
        rest_columns (list of str, optional): List of column names for the pivot table. Default is None, which uses a predefined list, needed to realize does the patient have SSIR or not.
        output_csv (str, optional): Path to the output CSV file. Default is None.

    Returns:
        pd.DataFrame: The processed data.
    """
    if rest_columns is None:
        rest_columns = ['Heart rate', 'Respiratory rate', 'Temperature Fahrenheit', 'Temperature Celsius',
                        'Direct Bilirubin', 'Heart rate_valueuom', 'Respiratory rate_valueuom',
                        'Temperature Fahrenheit_valueuom', 'Temperature Celsius_valueuom', 'Direct Bilirubin_valueuom']
    if itemids is None:
        itemids = [220045, 220210, 223762, 223761, 225651]
    if analyzes_df is None and analyzes_csv is not None:
        chartevents_df = pd.read_csv(analyzes_csv,
                                     usecols=[subject_id_col, itemid_col, charttime_col, value_col, valuenum_col,
                                              valueuom_col])
    elif analyzes_df is not None:
        chartevents_df = analyzes_df
    else:
        raise ValueError("Either analyzes_df or analyzes_csv must be provided.")

    filtered_df = chartevents_df[chartevents_df[itemid_col].isin(itemids)]
    pivot_df = filtered_df.pivot_table(index=[subject_id_col, charttime_col], columns=itemid_col,
                                       values=[value_col, valueuom_col], aggfunc='first').reset_index()
    pivot_df.columns = [subject_id_col, charttime_col] + rest_columns
    if output_csv is not None:
        pivot_df.to_csv(output_csv, index=False)

    return pivot_df

# df = pd.read_csv('chartevents.csv')
# analyzes_data = get_analyzes_data(analyzes_df=df, subject_id_col='subject_id', itemid_col='itemid')
# analyzes_data.to_csv('ssir.csv', index=False)
