import pytest
import polars as pl
import polars.testing as pt

from obfsc8.src.obfsc8.obfuscate_parquet_file \
    import obfuscate_parquet_file
from test_data.test_dataframe import test_dataframe


def test_that_parquet_file_returned_is_equivalent_to_input_if_not_obfuscated(
        parquet_from_s3):
    columns_for_obfuscation = []
    buffer = obfuscate_parquet_file(
        parquet_from_s3, columns_for_obfuscation, "***")
    obfuscated_dataframe = pl.read_parquet(buffer)

    pt.assert_frame_equal(test_dataframe, obfuscated_dataframe)


def test_that_parquet_file_returned_is_not_equivalent_if_obfuscated(
        parquet_from_s3):
    columns_for_obfuscation = ["name", "email_address"]
    buffer = obfuscate_parquet_file(
        parquet_from_s3, columns_for_obfuscation, "***")
    obfuscated_dataframe = pl.read_parquet(buffer)

    pt.assert_frame_not_equal(test_dataframe, obfuscated_dataframe)


@pytest.mark.parametrize("columns_for_obfuscation, replacement_string",
                         [(["name",
                            "email_address"],
                           "***"),
                          (["cohort"],
                           "??"),
                             (["student_id",
                               "name",
                               "graduation_date"],
                              "")])
def test_that_all_values_in_non_target_columns_remain_unchanged(
        columns_for_obfuscation, replacement_string, parquet_from_s3):

    buffer = obfuscate_parquet_file(
        parquet_from_s3, columns_for_obfuscation, replacement_string)
    obfuscated_dataframe = pl.read_parquet(buffer)

    for column_name in obfuscated_dataframe.columns:
        if column_name not in columns_for_obfuscation:
            original_column_values = test_dataframe.get_column(column_name)
            obfuscated_column_values = (obfuscated_dataframe
                                        .get_column(column_name))

            (pt.assert_series_equal(original_column_values,
                                    obfuscated_column_values))


@pytest.mark.parametrize("columns_for_obfuscation, replacement_string",
                         [(["name",
                            "email_address"],
                           ""),
                          (["cohort"],
                           "***"),
                             (["student_id",
                               "name",
                               "graduation_date"],
                              "??")])
def test_that_all_values_in_target_columns_made_equal_to_replacement_string(
        columns_for_obfuscation, replacement_string, parquet_from_s3):

    buffer = obfuscate_parquet_file(
        parquet_from_s3, columns_for_obfuscation, replacement_string)
    obfuscated_dataframe = pl.read_parquet(buffer)

    obfuscated_column_values_list = []
    for column_name in columns_for_obfuscation:
        obfuscated_column_values = (obfuscated_dataframe
                                    .get_column(column_name))
        obfuscated_column_values_list.append(obfuscated_column_values)

    for i in range(1, len(obfuscated_column_values_list)):
        (pt.assert_series_equal(obfuscated_column_values_list[0],
                                obfuscated_column_values_list[i],
                                check_names=False))
    for j in range(0, len(obfuscated_column_values_list[0])):
        assert obfuscated_column_values_list[0][j] == replacement_string
