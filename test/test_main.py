from pickem.main import display_week
from datetime import datetime


def test_display_week_before_season_start():
    # 2021: week 1 = "2021-09-08"
    before_w1 = datetime.strptime("2021-09-01", "%Y-%m-%d")
    assert display_week(before_w1) == 1


def test_display_week_start_edge():
    # test weeks - week 1: 09/08/2021
    w1_start = datetime.strptime("2021-09-08", "%Y-%m-%d")
    assert display_week(w1_start) == 1
    before_w2 = datetime.strptime("2021-09-14", "%Y-%m-%d")
    assert display_week(before_w2) == 1
    w2_start = datetime.strptime("2021-09-15", "%Y-%m-%d")
    assert display_week(w2_start) == 2


def test_display_week_midseason_edge():
    # test weeks - week 1: 09/08/2021
    w1_start = datetime.strptime("2021-09-08", "%Y-%m-%d")
    assert display_week(w1_start) == 1
    before_w2 = datetime.strptime("2021-09-14", "%Y-%m-%d")
    assert display_week(before_w2) == 1
    w2_start = datetime.strptime("2021-09-15", "%Y-%m-%d")
    assert display_week(w2_start) == 2


def test_display_week_season_end():
    # test weeks - week 18: 09/08/2021
    w16 = datetime.strptime("2022-01-04", "%Y-%m-%d")
    assert display_week(w16) == 17
    w17_start = datetime.strptime("2022-01-05", "%Y-%m-%d")
    assert display_week(w17_start) == 18
    w17_end = datetime.strptime("2022-01-11", "%Y-%m-%d")
    assert display_week(w17_end) == 18
    after_w17 = datetime.strptime("2022-01-12", "%Y-%m-%d")
    assert display_week(after_w17) == 18
