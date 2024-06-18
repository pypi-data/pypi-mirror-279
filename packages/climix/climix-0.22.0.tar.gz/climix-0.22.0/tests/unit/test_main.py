import pytest
from contextlib import nullcontext as does_not_raise

from climix import main


TEST_FILE_LIST_TO_GUESS_OUTPUT_TEMPLATE = [
    (
        ["tas_foo_historical_bar_day_19700101.nc"],
        None,
        does_not_raise(
            "{var_name}_foo_historical_bar_{frequency}_19700101-19700101.nc"
        ),
    ),
    (
        ["tas_foo_historical_bar_day_19700101-19801231.nc"],
        None,
        does_not_raise(
            "{var_name}_foo_historical_bar_{frequency}_19700101-19801231.nc"
        ),
    ),
    (
        [
            "tas_foo_historical_bar_day_19700101-19801231.nc",
            "tas_foo_historical_bar_day_19800101-19901231.nc",
        ],
        None,
        does_not_raise(
            "{var_name}_foo_historical_bar_{frequency}_19700101-19901231.nc"
        ),
    ),
    (
        [
            "tas_foo_historical_bar_day_19900101-20001231.nc",
            "tas_foo_rcp26_bar_day_20010101-20101231.nc",
        ],
        None,
        does_not_raise(
            "{var_name}_foo_historical-rcp26_bar_{frequency}_19900101-20101231.nc"
        ),
    ),
    (
        [
            "tas_foo_historical_bar_day_19900101-20001231.nc",
            "tas_foo_rcp85_bar_day_20010101-20101231.nc",
        ],
        None,
        does_not_raise(
            "{var_name}_foo_historical-rcp85_bar_{frequency}_19900101-20101231.nc"
        ),
    ),
    (
        [
            "tas_foo_historical_bar_day_19900101-20001231.nc",
            "tas_foo_ssp119_bar_day_20010101-20101231.nc",
        ],
        None,
        does_not_raise(
            "{var_name}_foo_historical-ssp119_bar_{frequency}_19900101-20101231.nc"
        ),
    ),
    (
        [
            "tas_foo_historical_bar_day_19900101-20001231.nc",
            "tas_foo_ssp585_bar_day_20010101-20101231.nc",
        ],
        None,
        does_not_raise(
            "{var_name}_foo_historical-ssp585_bar_{frequency}_19900101-20101231.nc"
        ),
    ),
    (
        ["tas_foo_historical_bar_day.nc"],
        None,
        does_not_raise("{var_name}_foo_historical_bar_{frequency}.nc"),
    ),
    (
        ["tas_foo_historical_bar_day_notimerange.nc"],
        None,
        does_not_raise("{var_name}_foo_historical_bar_{frequency}.nc"),
    ),
    (
        ["tas_foo_historical_bar_notimerange.nc", "tas_foo_rcp45_bar_notimerange.nc"],
        None,
        does_not_raise("{var_name}_foo_historical-rcp45_bar_{frequency}.nc"),
    ),
    (["foobar.nc"], None, does_not_raise("{var_name}_{frequency}.nc")),
    (
        [
            "tas_foo_historical_bar_day_19700101-19801231.nc",
            "tas_foo_historical_bar_day_19800101-19901231.nc",
        ],
        "1970-02-03/1990-01-15",
        does_not_raise(
            "{var_name}_foo_historical_bar_{frequency}_19700203-19900115.nc"
        ),
    ),
    (
        ["tas_foo_historical_bar_day_19700101-19801231.nc"],
        "1970-02-03/1970-02-15",
        does_not_raise(
            "{var_name}_foo_historical_bar_{frequency}_19700203-19700215.nc"
        ),
    ),
    (
        [
            "tas_foo_historical_bar_day_19700101-19801231.nc",
            "tas_foo_historical_bar_day_19800101-19901231.nc",
        ],
        "1960-02-03/1990-01-15",
        pytest.raises(ValueError),
    ),
    (
        [
            "tas_foo_historical_bar_day_19700101-19801231.nc",
            "tas_foo_historical_bar_day_19800101-19901231.nc",
        ],
        "1970-02-03/2000-01-15",
        pytest.raises(ValueError),
    ),
    (
        [
            "tas_foo_historical_bar_day_19700101-19801231.nc",
        ],
        "1960-02-03/2000-01-15",
        pytest.raises(ValueError),
    ),
    (
        ["tas_foo_historical_bar_notimerange.nc", "tas_foo_rcp45_bar_notimerange.nc"],
        "1970-02-03/2000-01-15",
        does_not_raise("{var_name}_foo_historical-rcp45_bar_{frequency}.nc"),
    ),
]


@pytest.mark.parametrize(
    "file_list, computational_period, expected_output_template",
    TEST_FILE_LIST_TO_GUESS_OUTPUT_TEMPLATE,
)
def test_guess_output_template(
    file_list, computational_period, expected_output_template
):
    """Test ``guess_output_template``."""
    with expected_output_template:
        output_template = main.guess_output_template(file_list, computational_period)
        assert output_template == expected_output_template.enter_result
