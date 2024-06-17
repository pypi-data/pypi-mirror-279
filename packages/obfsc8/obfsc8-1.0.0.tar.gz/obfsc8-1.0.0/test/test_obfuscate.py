import pandas as pd
import io

from obfsc8.src.obfsc8.obfuscate \
    import obfuscate
from test_data.test_dataframe import test_dataframe


def test_that_csv_file_results_in_csv_bytes_object(s3_client, test_bucket):
    test_csv = test_dataframe.write_csv()
    s3_client.put_object(
        Bucket="test_bucket",
        Key="test_csv.csv",
        Body=test_csv)

    test_csv_json = """{
    "file_to_obfuscate": "s3://test_bucket/test_csv.csv",
    "pii_fields": ["name", "email_address"]
    }"""

    buffer = obfuscate(test_csv_json)
    df = pd.read_csv(buffer)
    assert isinstance(df, pd.DataFrame)


def test_that_parquet_file_results_in_parquet_bytes_object(
        s3_client, test_bucket):
    test_parquet = io.BytesIO()
    test_dataframe.write_parquet(test_parquet)
    test_parquet.seek(0)
    s3_client.put_object(
        Bucket="test_bucket",
        Key="test_parquet.parquet",
        Body=test_parquet)

    test_parquet_json = """{
    "file_to_obfuscate": "s3://test_bucket/test_parquet.parquet",
    "pii_fields": ["name", "email_address"]
    }"""
    buffer = obfuscate(test_parquet_json)
    df = pd.read_parquet(buffer)
    assert isinstance(df, pd.DataFrame)


def test_that_json_file_results_in_json_bytes_object(s3_client, test_bucket):
    test_json_file = test_dataframe.write_json(row_oriented=True)
    s3_client.put_object(
        Bucket="test_bucket",
        Key="test_json.json",
        Body=test_json_file)

    test_json_json = """{
    "file_to_obfuscate": "s3://test_bucket/test_json.json",
    "pii_fields": ["name", "email_address"]
    }"""
    buffer = obfuscate(test_json_json)
    df = pd.read_json(buffer)
    assert isinstance(df, pd.DataFrame)
