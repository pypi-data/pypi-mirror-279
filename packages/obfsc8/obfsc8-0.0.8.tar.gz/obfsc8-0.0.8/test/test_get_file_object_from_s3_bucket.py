import polars.testing as pt
import polars as pl

from test_data.test_dataframe import test_dataframe


def test_that_s3_csv_written_and_retrieved_without_data_change(csv_from_s3):
    csv_file_from_s3_as_df = pl.read_csv(csv_from_s3)
    pt.assert_frame_equal(test_dataframe, csv_file_from_s3_as_df)


def test_that_s3_parquet_written_and_retrieved_without_data_change(
        parquet_from_s3):
    parquet_file_from_s3_as_df = pl.read_parquet(parquet_from_s3)
    pt.assert_frame_equal(test_dataframe, parquet_file_from_s3_as_df)


def test_that_s3_json_written_and_retrieved_without_data_change(json_from_s3):
    json_file_from_s3_as_df = pl.read_json(json_from_s3.read())
    pt.assert_frame_equal(test_dataframe, json_file_from_s3_as_df)
