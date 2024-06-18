import pandas as pd
import numpy as np  
from matplotlib import pyplot
from sklearn.preprocessing import LabelEncoder
import seaborn as sns
from scipy.stats import norm
from scipy import stats

def explore(df: pd.DataFrame) -> None:
    """
    Prints the data types and dimensions of the dataframe, and the count of columns for each data type.

    Parameters:
    df (pd.DataFrame): The dataframe to explore.
    """
    print(f"{df.dtypes}\n")
    print(f"Dimension: {df.shape[0]} x {df.shape[1]}\n")
    
    datatype_counts = df.dtypes.value_counts()
    for dtype, count in datatype_counts.items():
        print(f"{dtype}: {count} columns")

def col_category_text(df: pd.DataFrame) -> None:
    """
    Prints the frequency of each category in categorical columns of the dataframe.

    Parameters:
    df (pd.DataFrame): The dataframe to analyze.
    """
    for col in df.select_dtypes("object").columns:
        print(df[col].value_counts())
        print("\n")

def col_category_graph(df: pd.DataFrame) -> None:
    """
    Displays bar plots for the frequency of each category in categorical columns of the dataframe.

    Parameters:
    df (pd.DataFrame): The dataframe to analyze.
    """
    for col in df.select_dtypes("object").columns:
        value_counts = df[col].value_counts()
        pyplot.figure(figsize=(10, 6))  
        sns.barplot(x=value_counts.index, y=value_counts.values)
        pyplot.title(f'Bar Chart for {col}')
        pyplot.xlabel(col)
        pyplot.ylabel('Count')
        pyplot.xticks(rotation=45)  
        pyplot.tight_layout()  
        pyplot.show()
        print("\n")

def plot_boxplots(df: pd.DataFrame) -> None:
    """
    Displays box plots for all numeric columns in the dataframe to check for outliers.

    Parameters:
    df (pd.DataFrame): The dataframe to analyze.
    """
    numeric_columns = df.select_dtypes(include=['int64', 'float64'])
    
    for column in numeric_columns.columns:
        pyplot.figure(figsize=(8, 6))
        ax = df.boxplot(column=column)
        ax.set_ylim(df[column].min() - 0.1 * abs(df[column].min()), df[column].max() + 0.1 * abs(df[column].max()))
        pyplot.title(f'Boxplot of {column}')
        pyplot.ylabel(column)
        pyplot.show()

def null_check_text(df: pd.DataFrame) -> None:
    """
    Prints the count and percentage of missing values for each column in the dataframe.

    Parameters:
    df (pd.DataFrame): The dataframe to analyze.
    """
    null = df.isnull().sum()
    for i in range(len(df.columns)):
        print(f"{df.columns[i]}: {null[i]} ({(null[i]/len(df))*100}%)")
    total_cells = np.prod(df.shape)
    total_missing = null.sum()
    print(f"\nTotal missing values: {total_missing} ({(total_missing/total_cells) * 100}%)\n")

def null_check_graph(df: pd.DataFrame) -> None:
    """
    Displays a bar chart of the dataframe's missing values.

    Parameters:
    df (pd.DataFrame): The dataframe to analyze.
    """
    col_name = []
    null_num = []
    percentage = []
    col_type = []

    null = df.isnull().sum()
    for i in range(len(df.columns)):
        if null[i] != 0:
            col_name.append(df.columns[i])
            null_num.append(null[i])
            percentage.append((null[i]/len(df))*100)
            col_type.append(df[df.columns[i]].dtypes)
    total_cells = np.prod(df.shape)
    total_missing = null.sum()
    col_name.append("total_missing")
    null_num.append(total_missing)
    percentage.append((total_missing/total_cells) * 100)
    col_type.append("total_column")
    null_dict = {
        "col_name" : col_name,
        "null_num" : null_num,
        "percentage" : percentage,
        "col_type" : col_type
    }
    null_df = pd.DataFrame.from_dict(null_dict)
    ax = sns.barplot(x="col_name", y="percentage", hue="col_type", data=null_df)
    pyplot.xticks(rotation=90)
    pyplot.show()

def find_unique_null_columns(train_df: pd.DataFrame, test_df: pd.DataFrame) -> pd.DataFrame:
    """
    Display null columns that only appear in one of the dataset

    Parameters:
    train_df (pd.DataFrame): The first dataframe to be checked.
    test_df (pd.DataFrame): The second dataframe to be checked.

    Returns:
    pd.DataFrame: A dataframe with columns "Column_Name" and "Exists_In", indicating which dataframe 
                  (train or test) contains the column with null values.
    """
    null_columns_train = train_df.columns[train_df.isnull().any()]
    null_columns_test = test_df.columns[test_df.isnull().any()]
    
    unique_null_columns_train = null_columns_train.difference(null_columns_test)
    unique_null_columns_test = null_columns_test.difference(null_columns_train)
    
    result_df = pd.DataFrame(columns=["Column_Name", "Exists_In"])
    
    result_df["Column_Name"] = unique_null_columns_train.union(unique_null_columns_test)
    result_df["Exists_In"] = ["Train" if col in unique_null_columns_train else "Test" for col in result_df["Column_Name"]]
    
    return result_df

def different_cardinality_columns(train_df: pd.DataFrame, test_df: pd.DataFrame) -> pd.DataFrame:
    """
    Display different cardinality columns in first and second dataset

    Parameters:
    train_df (pd.DataFrame): The first dataframe to be checked.
    test_df (pd.DataFrame): The second dataframe to be checked.

    Returns:
    pd.DataFrame: A dataframe with columns ["Column", "Origin", "Cnt Cardinality in Train", "Cnt Cardinality in Test"]
                  showing the columns with differing cardinalities, which dataframe has the greater cardinality, 
                  and the cardinality counts for both dataframes.
                  Returns empty dataframe if there are no columns with differing cardinalities.
    """
    differing_columns = []

    for column in train_df.columns:
        if column in test_df.columns:
            if train_df[column].dtype == 'object':
                unique_values_train = train_df[column].nunique()
                unique_values_test = test_df[column].nunique()

                if unique_values_train != unique_values_test:
                    differing_columns.append((column, "train" if unique_values_train > unique_values_test else "test", unique_values_train, unique_values_test))

    if differing_columns:
        diff_df = pd.DataFrame(differing_columns, columns=["Column", "Origin", "Cnt Cardinality in Train", "Cnt Cardinality in Test"])
        return diff_df
    else:
        return pd.DataFrame()

def duplicate_check(df: pd.DataFrame) -> None:
    """
    Display duplicate in the dataset

    Parameters:
    df (pd.DataFrame): The dataframe to be checked.
    """
    print(df[df.duplicated()])

def arithmetic_one_column(df: pd.DataFrame, result_col_name: str, operation_col_name: str, operation_type: str, number: int) -> pd.DataFrame:
    """
    Doing arithmetic operation in a column

    Parameters:
    df (pd.DataFrame): The dataframe that contains the data.
    result_col_name (str): The name of the column where the result will be stored.
    operation_col_name (str): The name of the column to perform the operation on.
    operation_type (str): The type of arithmetic operation to perform. 
                          Must be one of 'add', 'sub', 'mul', or 'div'.
    number (int): The number to use in the arithmetic operation.

    Returns:
    pd.DataFrame: The dataframe with the new column containing the result of the arithmetic operation.

    Raises:
    ValueError: If an invalid operation type is provided.
    """
    if operation_type == "add":
        df[result_col_name] = df[operation_col_name].add(number)
    elif operation_type == "sub":
        df[result_col_name] = df[operation_col_name].sub(number)
    elif operation_type == "mul":
        df[result_col_name] = df[operation_col_name].mul(number)
    elif operation_type == "div":
        df[result_col_name] = df[operation_col_name].div(number)
    else:
        raise ValueError("Invalid operation type. Choose from 'add', 'sub', 'mul', or 'div'")
    return df

def arithmetic_two_column(df: pd.DataFrame, result_col_name: str, operation_col_name_1: str, operation_col_name_2: str, operation_type: str) -> pd.DataFrame:
    """
    Doing arithmetic operation in two columns and save the result in a new column

    Parameters:
    df (pd.DataFrame): The dataframe that contains the data.
    result_col_name (str): The name of the column where the result will be stored.
    operation_col_name_1 (str): The name of the first column to perform the operation on.
    operation_col_name_2 (str): The name of the second column to perform the operation on.
    operation_type (str): The type of arithmetic operation to perform. 
                          Must be one of 'add', 'sub', 'mul', or 'div'.

    Returns:
    pd.DataFrame: The dataframe with the new column containing the result of the arithmetic operation.

    Raises:
    ValueError: If an invalid operation type is provided.
    """
    if operation_type == "add":
        df[result_col_name] = df[operation_col_name_1] + df[operation_col_name_2]
    elif operation_type == "sub":
        df[result_col_name] = df[operation_col_name_1] - df[operation_col_name_2]
    elif operation_type == "mul":
        df[result_col_name] = df[operation_col_name_1] * df[operation_col_name_2]
    elif operation_type == "div":
        df[result_col_name] = df[operation_col_name_1] / df[operation_col_name_2]
    else:
        raise ValueError("Invalid operation type. Choose from 'add', 'sub', 'mul', or 'div'")
    return df

def change_date_format(df: pd.DataFrame, result_col_name: str, date_col: str, date_format: str) -> pd.DataFrame:
    """
    Changes the format of a date column and stores the result in a new column.

    Parameters:
    df (pd.DataFrame): The dataframe containing the date column.
    result_col_name (str): The name of the new column to store the formatted dates.
    date_col (str): The name of the column containing dates.
    date_format (str): The desired date format.

    Returns:
    pd.DataFrame: The dataframe with the new column containing formatted dates.
    """
    df[result_col_name] = df[date_col].dt.strftime(date_format)
    return df

def taking_date_element(df: pd.DataFrame, new_col_name: str, date_col_name: str, element_taken: str) -> pd.DataFrame:
    """
    Parameters:
    df (pd.DataFrame): The dataframe containing the date column.
    new_col_name (str): The name of the new column to store the extracted element.
    date_col_name (str): The name of the column containing dates.
    element_taken (str): The date element to extract. Must be one of 'day', 'dow', 'month', or 'year'.

    Returns:
    pd.DataFrame: The dataframe with the new column containing the extracted date element.

    Raises:
    ValueError: If an invalid element is specified.
    """
    if element_taken == "day":
        df[new_col_name] = df[date_col_name].dt.day
    elif element_taken == "dow":
        df[new_col_name] = df[date_col_name].dt.dayofweek
    elif element_taken == "month":
        df[new_col_name] = df[date_col_name].dt.month
    elif element_taken == "year":
        df[new_col_name] = df[date_col_name].dt.year
    else:
        raise ValueError("Invalid element taken. Choose from 'day', 'dow', 'month', or 'year'")
    return df

def casting(df: pd.DataFrame, new_col_name: str, target_col: str, operation_type: str) -> pd.DataFrame:
    """
    Parameters:
    df (pd.DataFrame): The dataframe containing the column to cast.
    new_col_name (str): The name of the new column to store the casted values.
    target_col (str): The name of the column to cast.
    operation_type (str): The type of casting operation. Must be one of 'str_to_int', 'str_to_datetime', 'int_to_str', or 'str_to_bool'.

    Returns:
    pd.DataFrame: The dataframe with the new column containing the casted values.

    Raises:
    ValueError: If an invalid operation type is specified.
    """
    if operation_type == "str_to_int":
        df[new_col_name] = df[target_col].astype(int)
    elif operation_type == "str_to_datetime":
        user_format = input("Input format: ")
        df[new_col_name] = pd.to_datetime(df[target_col], format=user_format)
    elif operation_type == "int_to_str":
        df[new_col_name] = df[target_col].apply(str)
    elif operation_type == "str_to_bool":
        df = df.replace({'True': True, 'False': False})
    else:
        raise ValueError("Invalid operation type. Choose from 'str_to_int', 'str_to_datetime', 'int_to_str', or 'str_to_bool'")
    return df

def combine_str_col(df: pd.DataFrame, new_col_name: str, col_name_1: str, col_name_2: str, sep=" ") -> pd.DataFrame:
    """
    Concatenate strings from two columns of a DataFrame into a new column.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    new_col_name (str): Name for the new concatenated column.
    col_name_1 (str): Name of the first column to concatenate.
    col_name_2 (str): Name of the second column to concatenate.
    sep (str, optional): Separator between the concatenated strings (default is a single space).

    Returns:
    pd.DataFrame: DataFrame with the new concatenated column added.
    """
    df[new_col_name] = df[col_name_1] + sep + df[col_name_2]
    return df

def merge(df1: pd.DataFrame, df2: pd.DataFrame, axis = 0, join = "inner") -> pd.DataFrame:
    """
    Merge two DataFrames along rows or columns.

    Parameters:
    df1 (pd.DataFrame): First DataFrame.
    df2 (pd.DataFrame): Second DataFrame.
    axis (int, optional): Axis to concatenate along (0 for rows, 1 for columns, default is 0).
    join (str, optional): Type of join to perform ('inner', 'outer', 'left', 'right', default is 'inner').

    Returns:
    pd.DataFrame: Merged DataFrame.
    """
    result = pd.concat([df1, df2], axis=axis, join=join)
    return result

def add_column(df: pd.DataFrame, new_column_name: str, column: list) -> pd.DataFrame:
    """
    Add a new column to a DataFrame.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    new_column_name (str): Name for the new column.
    column (list): List of values to populate the new column.

    Returns:
    pd.DataFrame: DataFrame with the new column added.
    """
    df[new_column_name] = column
    return df

def delete_column(df: pd.DataFrame, col_list: list) -> pd.DataFrame:
    """
    Delete specified columns from a DataFrame.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    col_list (list): List of column names to delete.

    Returns:
    pd.DataFrame: DataFrame with specified columns deleted.
    """
    df = df.drop(col_list, axis = 1)
    return df

def remove_na(df: pd.DataFrame, subset_in: str) -> pd.DataFrame:
    """
    Remove rows with missing values in a specific column of a DataFrame.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    subset_in (str): Column name to consider for missing values.

    Returns:
    pd.DataFrame: DataFrame with rows containing missing values in the specified column removed.
    """
    df = df.dropna(subset = [subset_in], axis = 0)
    df.reset_index(drop=True, inplace=True)
    return df

def replace_avg(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Replace NaN values in a specific column of a DataFrame with the column's average.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    col (str): Column name where NaN values are to be replaced.

    Returns:
    pd.DataFrame: DataFrame with NaN values replaced by the column's average.
    """
    avg = df[col].astype("float").mean(axis=0)
    df[col].replace(np.nan, avg, inplace=True)
    return df

def replace_median(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Replace NaN values in a specific column of a DataFrame with the column's median.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    col (str): Column name where NaN values are to be replaced.

    Returns:
    pd.DataFrame: DataFrame with NaN values replaced by the column's median.
    """
    median = df[col].median()
    df[col].replace(np.nan, median, inplace=True)
    return df

def replace_mode(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Replace NaN values in a specific column of a DataFrame with the column's mode (most frequent value).

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    col (str): Column name where NaN values are to be replaced.

    Returns:
    pd.DataFrame: DataFrame with NaN values replaced by the column's mode.
    """
    mode = df[col].value_counts().idxmax()
    df[col].replace(np.nan, mode, inplace = True)
    return df

def one_hot(df: pd.DataFrame, col_list: list) -> pd.DataFrame:
    """
    Perform one-hot encoding on specified columns of a DataFrame.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    col_list (list): List of column names to perform one-hot encoding.

    Returns:
    pd.DataFrame: DataFrame with specified columns one-hot encoded.
    """
    df = pd.get_dummies(df, columns=col_list)
    return df

def label_enc(df: pd.DataFrame, col_list: list) -> pd.DataFrame:
    """
    Perform label encoding on specified columns of a DataFrame.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    col_list (list): List of column names to perform label encoding.

    Returns:
    pd.DataFrame: DataFrame with specified columns label encoded.
    """
    df[col_list] = df[col_list].apply(LabelEncoder().fit_transform)
    return df   

def set_index(df: pd.DataFrame, col_name: str) -> pd.DataFrame:
    """
    Set a column of the DataFrame as the index.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    col_name (str): Name of the column to set as the index.

    Returns:
    pd.DataFrame: DataFrame with the specified column set as the index.
    """
    df.set_index(col_name)
    df.index.name = None
    return df

def rename_col(df: pd.DataFrame, change_dict: dict) -> pd.DataFrame:
    """
    Rename columns of the DataFrame based on the provided dictionary.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    change_dict (dict): Dictionary where keys are current column names and values are new column names.

    Returns:
    pd.DataFrame: DataFrame with columns renamed according to the dictionary.
    """
    df.rename(columns = change_dict, inplace=True)
    return df

def filter_rows(df: pd.DataFrame, col: str, word: str) -> pd.DataFrame:
    """
    Filter rows of the DataFrame where a specific column contains a piece of string.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    col (str): Column name to filter.
    word (str): Substring to search for within the column.

    Returns:
    pd.DataFrame: Filtered DataFrame with rows where the specified column contains the substring.
    """
    result = df[df[col].str.contains(word)]
    return result

def del_row_c(df: pd.DataFrame, col_name: str, word: str) -> pd.DataFrame:
    """
    Delete rows from the DataFrame where a specific column contains a certain word.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    col_name (str): Column name to check for the word.
    word (str): Word to check for in the column.

    Returns:
    pd.DataFrame: DataFrame with rows removed where the specified column contains the word.
    """
    df = df.loc[df[col_name] != word]
    return df

def del_row_nc(df: pd.DataFrame, col_name: str, word: str) -> pd.DataFrame:
    """
    Delete rows from the DataFrame where a specific column does not contain a certain word.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    col_name (str): Column name to check for the absence of the word.
    word (str): Word to check for absence in the column.

    Returns:
    pd.DataFrame: DataFrame with rows removed where the specified column does not contain the word.
    """
    df = df.loc[df[col_name] == word]
    return df

def replace_str(df: pd.DataFrame, str1: str, str2: str) -> None:
    """
    Replace occurrences of a string/character in the entire DataFrame.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    str1 (str): String to be replaced.
    str2 (str): String to replace str1.

    Returns:
    pd.DataFrame: DataFrame with specified string replacements applied.
    """
    df = df.replace(str1, str2, regex=True)
    return df

def remove_duplicate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplicate rows from the DataFrame.

    Parameters:
    df (pd.DataFrame): Input DataFrame.

    Returns:
    pd.DataFrame: DataFrame with duplicate rows removed.
    """
    bool_duplicate_series = df.duplicated()
    return(df[~bool_duplicate_series])

def rm_old_rows(df: pd.DataFrame, time_column: str, duration_inc: str) -> pd.DataFrame:
    """
    Remove rows from the DataFrame where a specified time column is less than a certain duration.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    time_column (str): Name of the column containing time-related data.
    duration_inc (str): Time duration threshold (e.g., '2023-01-01').

    Returns:
    pd.DataFrame: DataFrame with rows removed where the time column is less than duration_inc.
    """
    print(f"Before Cleaning: {df.shape}")
    df = df.loc[df[time_column] >= duration_inc]
    print(f"\nAfter Cleaning: {df.shape}\n")
    return df

def fix_typo(df: pd.DataFrame, col_name: str, old_value: str, new_value: str) -> pd.DataFrame:
    """
    Replace occurrences of a specific value in a column of the DataFrame, useful for fixing typo in a column.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    col_name (str): Name of the column where replacement is to be applied.
    old_value (str): Value to be replaced.
    new_value (str): Value to replace old_value.

    Returns:
    pd.DataFrame: DataFrame with specified replacements in the specified column.
    """
    df[col_name] = df[col_name].replace(to_replace=old_value, value=new_value)
    return df

def fix_whitespace(df: pd.DataFrame, col_name: str) -> pd.DataFrame:
    """
    Remove leading and trailing whitespace characters from a column in the DataFrame.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    col_name (str): Name of the column to remove whitespace.

    Returns:
    pd.DataFrame: DataFrame with leading and trailing whitespace removed from the specified column.
    """
    df[col_name] = df[col_name].str.strip()
    return df

def corr_matrix(df: pd.DataFrame, target_col_name: str, annot=False, full=True, var_shown=10) -> None:
    """
    Create a correlation matrix for the DataFrame, focusing on correlations with a target column.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    target_col_name (str): Name of the target column for correlation analysis.
    annot (bool, optional): Whether to annotate the correlation matrix heatmap (default is False).
    full (bool, optional): Whether to show a full correlation matrix or just correlations with the target column (default is True).
    var_shown (int, optional): Number of variables to show in the full correlation matrix (default is 10).
    """
    if not full:
        correlation = df.corrwith(df[target_col_name])
        correlation_df = pd.DataFrame(correlation, columns=[target_col_name])

        if annot:
            sns.heatmap(
            correlation_df.transpose(),
            vmin=correlation.values.min(),
            vmax=1,
            square=True,
            cmap="YlGnBu",
            linewidths=0.1,
            annot=True,
            annot_kws={"fontsize":8}
            )
            pyplot.show()
        else:
            sns.heatmap(correlation_df.transpose(), cmap="YlGnBu")  
            pyplot.show()
    else:
        corr = df.corr()
        cols = corr.nlargest(var_shown, target_col_name)[target_col_name].index
        cm = np.corrcoef(df[cols].values.T)
        sns.set_theme(font_scale=1.25)
        hm = sns.heatmap(cm, cbar=True, annot=True, square=True, fmt='.2f', annot_kws={'size': 10}, yticklabels=cols.values, xticklabels=cols.values)
        pyplot.show()

def pairplot(df: pd.DataFrame, cols: list) -> None:
    """
    Create a pairplot to visualize relationships between variables in the DataFrame.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    cols (list): List of column names to include in the pairplot.
    """
    sns.pairplot(df[cols], size = 2.5)
    pyplot.show()

def scatter(df: pd.DataFrame, target: str) -> None:
    """
    Create scatter plots to visualize relationships between a target column and all other columns in the DataFrame.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    target (str): Name of the target column for scatter plots.
    """
    for col in df.columns:
        pyplot.scatter(x=df[target], y=df[col])
        pyplot.xlabel(target)
        pyplot.ylabel(col)
        pyplot.show()

def hist(df: pd.DataFrame) -> None:
    """
    Create histograms to visualize distributions of all columns in the DataFrame, can be used to check for outlier.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    """
    for col in df.columns:
        pyplot.hist(df[col], bins=10)  
        pyplot.xlabel(col)
        pyplot.ylabel('Frequency')
        pyplot.title(f'{col}')
        pyplot.show()

def norm_check(df: pd.DataFrame, cols: list) -> None:
    """
    Create histograms and probability plots to check for normal distribution of columns in the DataFrame.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    cols (list): List of column names to check for normal distribution.
    """
    def normal(mean, std, color="black"):
        x = np.linspace(mean-4*std, mean+4*std, 200)
        p = stats.norm.pdf(x, mean, std)
        z = pyplot.plot(x, p, color, linewidth=2)

    for col_name in cols:
        fig1, ax1 = pyplot.subplots()
        sns.histplot(x=df[col_name], stat="density", ax=ax1)
        normal(df[col_name].mean(), df[col_name].std())
        
        fig2, ax2 = pyplot.subplots()
        stats.probplot(df[col_name], plot=ax2)
        
        pyplot.show()

