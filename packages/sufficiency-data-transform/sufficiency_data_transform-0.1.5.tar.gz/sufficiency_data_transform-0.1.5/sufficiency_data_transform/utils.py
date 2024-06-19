import chardet
import pandas as pd
from fs import open_fs
import csv
import warnings


def remove_duplicate_columns(df):
    """
    Warns and removes duplicate columns from a DataFrame
    """
    duplicated_cols = df.columns[df.columns.duplicated()]

    # Drop duplicate columns if any are found
    if len(duplicated_cols) > 0:
        warnings.warn(f"Duplicate columns found: {duplicated_cols}")
        df.drop(columns=duplicated_cols, inplace=True)

    return df


def write_csv(df, fs, filename, index=False, buffer_size=1024 * 1024):
    df = remove_duplicate_columns(df)
    with fs.open(filename, "w") as stream:  # Open in binary write mode ('wb')
        writer = csv.writer(stream)  # Create a CSV writer using the stream
        writer.writerow(df.columns)
        if index:
            data = df.to_records(index=index).tolist()
        else:
            data = df.to_records().tolist()

        writer.writerows(data)


def open_location(path):
    return open_fs(path)


def open_file(fs, file, encoding=None):
    """
    Opens a file within a pyfilesystem
    """
    # Open the CSV file using the FS URL
    with fs.open(file, "rb") as f:
        # Read the file content into a pandas DataFrame
        if encoding:
            df = pd.read_csv(f, encoding=encoding)
        else:
            df = pd.read_csv(f)
    return df


def fillna_categorical_columns(df, columns):
    """
    Fill missing values in categorical columns with -1
    """
    for column in columns:
        df[column] = df[column].fillna(-1)
    return df


def fillna_date_columns(df, columns):
    """
    Fill missing values in date columns with 2999-12-31
    """
    for column in columns:
        df[column] = df[column].fillna("2999-12-31")
    return df


def check_encoding(file_path):
    """
    Check encoding of a file
    """
    with open(file_path, "rb") as rawdata:
        result = chardet.detect(rawdata.read())
    return result["encoding"]


def add_nan_row(df, dfKey):
    """
    Add rows with NaN values in all the columns
    """
    # add a row that simulates the scenario where all values are nan
    nan_col = {col: pd.NA for col in df.columns}
    nan_col[dfKey] = -1
    df.loc[len(df)] = nan_col
    return df


def generate_dim(data, filename, fs):
    write_csv(pd.DataFrame(data), fs, filename, False)


def check_encoding(fs, file_path):
    """
    Check encoding of a file
    """
    file = fs.open(file_path, "rb")

    bytes_data = file.read()  # Read as bytes
    result = chardet.detect(bytes_data)  # Detect encoding on bytes
    return result["encoding"]
