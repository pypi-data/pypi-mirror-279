import pytest

from obfsc8.src.obfsc8.get_filetype import get_filetype


def test_that_string_returned():
    filename = "new_data/file1.csv"
    result = get_filetype(filename)

    assert isinstance(result, str)


@pytest.mark.parametrize("filename, expected",
                         [("new_data/file1.csv",
                           "csv"),
                          ("new_data/file1.parquet",
                           "parquet"),
                             ("new_data/file1.json",
                              "json")])
def test_correct_filetype_returned_for_all_expected_filetypes(
        filename,
        expected):
    result = get_filetype(filename)

    assert result == expected


def test_that_type_error_raised_if_input_filename_not_a_string():
    with pytest.raises(TypeError, match="must be a string"):
        get_filetype(674)


def test_that_value_error_raised_if_period_not_present_in_filename():
    with pytest.raises(ValueError, match="must contain a period"):
        get_filetype("new_data/file1")


def test_that_value_error_raised_if_filetype_not_CSV_Parquet_or_JSON():
    with (pytest.raises
          (ValueError, match="Filetype must be CSV, Parquet or JSON")):
        get_filetype("new_data/file1.jpg")
