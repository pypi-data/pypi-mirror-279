import pickle
import re
from copy import copy, deepcopy
from datetime import datetime as py_datetime, timedelta, timezone
from typing import Any

import pytest
from hypothesis import given
from hypothesis.strategies import text

from whenever import (
    AmbiguousTime,
    Date,
    LocalSystemDateTime,
    NaiveDateTime,
    OffsetDateTime,
    SkippedTime,
    Time,
    UTCDateTime,
    ZonedDateTime,
    days,
    hours,
    microseconds,
    months,
    seconds,
    weeks,
    years,
)

from .common import (
    AlwaysEqual,
    AlwaysLarger,
    AlwaysSmaller,
    NeverEqual,
    ZoneInfo,
    local_ams_tz,
    local_nyc_tz,
)


class TestInit:
    @local_ams_tz()
    def test_basic(self):
        d = LocalSystemDateTime(2020, 8, 15, 5, 12, 30, nanosecond=450)

        assert d.year == 2020
        assert d.month == 8
        assert d.day == 15
        assert d.hour == 5
        assert d.minute == 12
        assert d.second == 30
        assert d.nanosecond == 450
        assert d.offset == hours(2)

    def test_optionality(self):
        assert (
            LocalSystemDateTime(2020, 8, 15, 12)
            == LocalSystemDateTime(2020, 8, 15, 12, 0)
            == LocalSystemDateTime(2020, 8, 15, 12, 0, 0)
            == LocalSystemDateTime(2020, 8, 15, 12, 0, 0, nanosecond=0)
            == LocalSystemDateTime(
                2020, 8, 15, 12, 0, 0, nanosecond=0, disambiguate="raise"
            )
        )

    @local_ams_tz()
    def test_ambiguous(self):
        kwargs: dict[str, Any] = {
            "year": 2023,
            "month": 10,
            "day": 29,
            "hour": 2,
            "minute": 15,
        }
        d = LocalSystemDateTime(**kwargs, disambiguate="earlier")
        assert d < LocalSystemDateTime(**kwargs, disambiguate="later")

        with pytest.raises(
            AmbiguousTime,
            match="2023-10-29 02:15:00 is ambiguous in the system timezone",
        ):
            LocalSystemDateTime(2023, 10, 29, 2, 15, disambiguate="raise")

        with pytest.raises(AmbiguousTime):
            LocalSystemDateTime(2023, 10, 29, 2, 15)

    @local_ams_tz()
    def test_nonexistent(self):
        kwargs: dict[str, Any] = {
            "year": 2023,
            "month": 3,
            "day": 26,
            "hour": 2,
            "minute": 30,
        }
        with pytest.raises(
            SkippedTime,
            match="2023-03-26 02:30:00 is skipped in the system timezone",
        ):
            LocalSystemDateTime(**kwargs)

        with pytest.raises(
            SkippedTime,
        ):
            LocalSystemDateTime(**kwargs, disambiguate="raise")

        assert LocalSystemDateTime(**kwargs, disambiguate="earlier").exact_eq(
            LocalSystemDateTime(**{**kwargs, "hour": 1})
        )
        assert LocalSystemDateTime(**kwargs, disambiguate="later").exact_eq(
            LocalSystemDateTime(**{**kwargs, "hour": 3})
        )
        assert LocalSystemDateTime(
            **kwargs, disambiguate="compatible"
        ).exact_eq(LocalSystemDateTime(**{**kwargs, "hour": 3}))

    def test_invalid(self):
        with pytest.raises(ValueError, match="range|time"):
            LocalSystemDateTime(2020, 1, 15, nanosecond=1_000_000_000)

    @local_ams_tz()
    def test_bounds_min(self):
        with pytest.raises((ValueError, OverflowError), match="range|year"):
            LocalSystemDateTime(1, 1, 1)

    @local_nyc_tz()
    def test_bounds_max(self):
        with pytest.raises((ValueError, OverflowError), match="range|year"):
            LocalSystemDateTime(9999, 12, 31)


class TestInUTC:
    @local_ams_tz()
    def test_common_time(self):
        d = LocalSystemDateTime(2020, 8, 15, 11)
        assert d.to_utc() == UTCDateTime(2020, 8, 15, 9)

    @local_ams_tz()
    def test_amibiguous_time(self):
        d = LocalSystemDateTime(2023, 10, 29, 2, 15, disambiguate="earlier")
        assert d.to_utc() == UTCDateTime(2023, 10, 29, 0, 15)
        assert d.replace(disambiguate="later").to_utc() == UTCDateTime(
            2023, 10, 29, 1, 15
        )


def test_naive():
    d = LocalSystemDateTime(2020, 8, 15, 12, 8, 30)
    assert d.naive() == NaiveDateTime(2020, 8, 15, 12, 8, 30)


@local_ams_tz()
def test_to_tz():
    assert (
        LocalSystemDateTime(2020, 8, 15, 12, 8, 30)
        .to_tz("America/New_York")
        .exact_eq(ZonedDateTime(2020, 8, 15, 6, 8, 30, tz="America/New_York"))
    )
    ams = LocalSystemDateTime(2023, 10, 29, 2, 15, 30, disambiguate="earlier")
    nyc = ZonedDateTime(2023, 10, 28, 20, 15, 30, tz="America/New_York")
    assert ams.to_tz("America/New_York").exact_eq(nyc)
    assert (
        ams.replace(disambiguate="later")
        .to_tz("America/New_York")
        .exact_eq(nyc.replace(hour=21))
    )
    assert nyc.to_local_system() == ams
    assert nyc.replace(hour=21).to_local_system() == ams.replace(
        disambiguate="later"
    )
    # disambiguation doesn't affect NYC time because there's no ambiguity
    assert nyc.replace(disambiguate="later").to_local_system() == ams


class TestAsOffset:
    @local_ams_tz()
    def test_simple(self):
        assert (
            LocalSystemDateTime(2020, 8, 15, 12, 8, 30)
            .to_fixed_offset()
            .exact_eq(OffsetDateTime(2020, 8, 15, 12, 8, 30, offset=2))
        )

    @local_ams_tz()
    def test_ambiguous(self):
        assert (
            LocalSystemDateTime(
                2023, 10, 29, 2, 15, 30, disambiguate="earlier"
            )
            .to_fixed_offset()
            .exact_eq(OffsetDateTime(2023, 10, 29, 2, 15, 30, offset=hours(2)))
        )
        assert (
            LocalSystemDateTime(2023, 10, 29, 2, 15, 30, disambiguate="later")
            .to_fixed_offset()
            .exact_eq(OffsetDateTime(2023, 10, 29, 2, 15, 30, offset=hours(1)))
        )

    @local_ams_tz()
    def test_custom_offset(self):
        d = LocalSystemDateTime(2020, 8, 15, 12, 30)
        assert d.to_fixed_offset(hours(3)).exact_eq(
            OffsetDateTime(2020, 8, 15, 13, 30, offset=hours(3))
        )
        assert d.to_fixed_offset(hours(0)).exact_eq(
            OffsetDateTime(2020, 8, 15, 10, 30, offset=hours(0))
        )
        assert d.to_fixed_offset(-1).exact_eq(
            OffsetDateTime(2020, 8, 15, 9, 30, offset=hours(-1))
        )


class TestInLocalSystem:

    @local_ams_tz()
    def test_no_timezone_change(self):
        d = LocalSystemDateTime(2020, 8, 15, 12, 8, 30)
        assert d.to_local_system().exact_eq(d)

    @local_ams_tz()
    def test_timezone_change(self):
        d = LocalSystemDateTime(2020, 8, 15, 12, 8, 30)
        with local_nyc_tz():
            assert d.to_local_system().exact_eq(
                LocalSystemDateTime(2020, 8, 15, 6, 8, 30)
            )


@local_ams_tz()
def test_immutable():
    d = LocalSystemDateTime(2020, 8, 15)
    with pytest.raises(AttributeError):
        d.year = 2021  # type: ignore[misc]


class TestFormatCommonIso:
    @local_ams_tz()
    def test_simple(self):
        d = LocalSystemDateTime(2020, 8, 15, 23, 12, 9, nanosecond=987_654_300)
        expected = "2020-08-15T23:12:09.9876543+02:00"
        assert str(d) == expected
        assert d.format_common_iso() == expected

    @local_ams_tz()
    def test_ambiguous(self):
        d = LocalSystemDateTime(
            2023, 10, 29, 2, 15, 30, disambiguate="earlier"
        )
        expected = "2023-10-29T02:15:30+02:00"
        assert str(d) == expected
        assert d.format_common_iso() == expected
        d2 = d.replace(disambiguate="later")
        assert str(d2) == expected.replace("+02:00", "+01:00")
        assert d2.format_common_iso() == expected.replace("+02:00", "+01:00")


class TestEquality:
    def test_same_exact(self):
        d = LocalSystemDateTime(2020, 8, 15, 12, 8, 30, nanosecond=450)
        same = LocalSystemDateTime(2020, 8, 15, 12, 8, 30, nanosecond=450)
        assert d == same
        assert not d != same
        assert hash(d) == hash(same)

    @local_ams_tz()
    def test_same_moment(self):
        d = LocalSystemDateTime(2020, 8, 15, 12, 8, 30, nanosecond=450)
        with local_nyc_tz():
            same = LocalSystemDateTime(2020, 8, 15, 6, 8, 30, nanosecond=450)
        assert d == same
        assert not d != same
        assert hash(d) == hash(same)

    @local_ams_tz()
    def test_amibiguous(self):
        d = LocalSystemDateTime(
            2023, 10, 29, 2, 15, 30, disambiguate="earlier"
        )
        other = LocalSystemDateTime(
            2023, 10, 29, 2, 15, 30, disambiguate="later"
        )
        assert d != other
        assert not d == other
        assert hash(d) != hash(other)

    @local_ams_tz()
    def test_utc(self):
        d: LocalSystemDateTime | UTCDateTime = LocalSystemDateTime(
            2023, 10, 29, 2, 15, disambiguate="earlier"
        )
        same = UTCDateTime(2023, 10, 29, 0, 15)
        different = UTCDateTime(2023, 10, 29, 1, 15)
        assert d == same
        assert not d != same
        assert d != different
        assert not d == different

        assert hash(d) == hash(same)
        assert hash(d) != hash(different)

    @local_ams_tz()
    def test_offset(self):
        d: LocalSystemDateTime | OffsetDateTime = LocalSystemDateTime(
            2023, 10, 29, 2, 15, disambiguate="earlier"
        )
        same = d.to_fixed_offset(hours(5))
        different = d.to_fixed_offset(hours(3)).replace(minute=14)
        assert d == same
        assert not d != same
        assert d != different
        assert not d == different

        assert hash(d) == hash(same)
        assert hash(d) != hash(different)

    @local_ams_tz()
    def test_zoned(self):
        d: LocalSystemDateTime | ZonedDateTime = LocalSystemDateTime(
            2023, 10, 29, 2, 15, disambiguate="earlier"
        )
        same = d.to_tz("Europe/Paris")
        assert same.is_ambiguous()  # important we test this case
        different = d.to_tz("Europe/Amsterdam").replace(
            minute=14, disambiguate="earlier"
        )
        assert d == same
        assert not d != same
        assert d != different
        assert not d == different

        assert hash(d) == hash(same)
        assert hash(d) != hash(different)

    def test_notimplemented(self):
        d = LocalSystemDateTime(2020, 8, 15)
        assert d == AlwaysEqual()
        assert not d != AlwaysEqual()
        assert d != NeverEqual()
        assert not d == NeverEqual()

        assert not d == 3  # type: ignore[comparison-overlap]
        assert d != 3  # type: ignore[comparison-overlap]
        assert not 3 == d  # type: ignore[comparison-overlap]
        assert 3 != d  # type: ignore[comparison-overlap]

        assert not d == None  # noqa: E711
        assert d != None  # noqa: E711
        assert not None == d  # noqa: E711
        assert None != d  # noqa: E711


class TestComparison:
    @local_nyc_tz()
    def test_different_timezones(self):
        d = LocalSystemDateTime(2020, 8, 15, 12, 30)
        later = d.replace(hour=13)
        earlier = d.replace(hour=11)
        assert d < later
        assert d <= later
        assert later > d
        assert later >= d
        assert not d > later
        assert not d >= later
        assert not later < d
        assert not later <= d

        assert d > earlier
        assert d >= earlier
        assert earlier < d
        assert earlier <= d
        assert not d < earlier
        assert not d <= earlier
        assert not earlier > d
        assert not earlier >= d

    @local_ams_tz()
    def test_same_timezone_fold(self):
        d = LocalSystemDateTime(
            2023, 10, 29, 2, 15, 30, disambiguate="earlier"
        )
        later = d.replace(disambiguate="later")
        assert d < later
        assert d <= later
        assert later > d
        assert later >= d
        assert not d > later
        assert not d >= later
        assert not later < d
        assert not later <= d

    @local_ams_tz()
    def test_offset(self):
        d = LocalSystemDateTime(2020, 8, 15, 12, 30)
        same = d.to_fixed_offset(hours(5))
        later = same.replace(minute=31)
        earlier = same.replace(minute=29)
        assert d >= same
        assert d <= same
        assert not d > same
        assert not d < same

        assert d < later
        assert d <= later
        assert not d > later
        assert not d >= later

        assert d > earlier
        assert d >= earlier
        assert not d < earlier
        assert not d <= earlier

    @local_ams_tz()
    def test_zoned(self):
        d = LocalSystemDateTime(2020, 8, 15, 12, 30)
        same = d.to_tz("America/New_York")
        later = same.replace(minute=31)
        earlier = same.replace(minute=29)
        assert d >= same
        assert d <= same
        assert not d > same
        assert not d < same

        assert d < later
        assert d <= later
        assert not d > later
        assert not d >= later

        assert d > earlier
        assert d >= earlier
        assert not d < earlier
        assert not d <= earlier

    @local_ams_tz()
    def test_utc(self):
        d = LocalSystemDateTime(2020, 8, 15, 12, 30)
        same = d.to_utc()
        later = same.replace(minute=31)
        earlier = same.replace(minute=29)
        assert d >= same
        assert d <= same
        assert not d > same
        assert not d < same

        assert d < later
        assert d <= later
        assert not d > later
        assert not d >= later

        assert d > earlier
        assert d >= earlier
        assert not d < earlier
        assert not d <= earlier

    def test_notimplemented(self):
        d = LocalSystemDateTime(2020, 8, 15)
        assert d < AlwaysLarger()
        assert d <= AlwaysLarger()
        assert not d > AlwaysLarger()
        assert not d >= AlwaysLarger()
        assert not d < AlwaysSmaller()
        assert not d <= AlwaysSmaller()
        assert d > AlwaysSmaller()
        assert d >= AlwaysSmaller()

        with pytest.raises(TypeError):
            d < 42  # type: ignore[operator]

        with pytest.raises(TypeError):
            d <= 42  # type: ignore[operator]

        with pytest.raises(TypeError):
            d > 42  # type: ignore[operator]

        with pytest.raises(TypeError):
            d >= 42  # type: ignore[operator]

        with pytest.raises(TypeError):
            42 < d  # type: ignore[operator]

        with pytest.raises(TypeError):
            42 <= d  # type: ignore[operator]

        with pytest.raises(TypeError):
            42 > d  # type: ignore[operator]

        with pytest.raises(TypeError):
            42 >= d  # type: ignore[operator]


@local_ams_tz()
def test_exact_equality():
    a = LocalSystemDateTime(2020, 8, 15, 12, 8, 30, nanosecond=450)
    same = a.replace()
    with local_nyc_tz():
        same_moment = LocalSystemDateTime(
            2020, 8, 15, 6, 8, 30, nanosecond=450
        )
    assert same.to_utc() == same_moment.to_utc()
    different = a.replace(hour=13)

    assert a.exact_eq(same)
    assert same.exact_eq(a)
    assert not a.exact_eq(same_moment)
    assert not same_moment.exact_eq(a)
    assert not a.exact_eq(different)
    assert not different.exact_eq(a)


class TestParseCommonIso:
    @pytest.mark.parametrize(
        "s, expect, offset",
        [
            (
                "2020-08-15T12:08:30+05:00",
                NaiveDateTime(2020, 8, 15, 12, 8, 30),
                hours(5),
            ),
            (
                "2020-08-15T12:08:30+20:00",
                NaiveDateTime(2020, 8, 15, 12, 8, 30),
                hours(20),
            ),
            (
                "2020-08-15T12:08:30.0034+05:00",
                NaiveDateTime(2020, 8, 15, 12, 8, 30, nanosecond=3_400_000),
                hours(5),
            ),
            (
                "2020-08-15T12:08:30.000000010+05:00",
                NaiveDateTime(2020, 8, 15, 12, 8, 30, nanosecond=10),
                hours(5),
            ),
            (
                "2020-08-15T12:08:30.0034-05:00:01",
                NaiveDateTime(
                    2020,
                    8,
                    15,
                    12,
                    8,
                    30,
                    nanosecond=3_400_000,
                ),
                -hours(5) - seconds(1),
            ),
            (
                "2020-08-15T12:08:30+00:00",
                NaiveDateTime(2020, 8, 15, 12, 8, 30),
                hours(0),
            ),
            (
                "2020-08-15T12:08:30-00:00",
                NaiveDateTime(2020, 8, 15, 12, 8, 30),
                hours(0),
            ),
            (
                "2020-08-15T12:08:30Z",
                NaiveDateTime(2020, 8, 15, 12, 8, 30),
                hours(0),
            ),
        ],
    )
    def test_valid(self, s, expect, offset):
        dt = LocalSystemDateTime.parse_common_iso(s)
        assert dt.naive() == expect
        assert dt.offset == offset

    @pytest.mark.parametrize(
        "s",
        [
            "2020-08-15T2:08:30+05:00:01",  # unpadded
            "2020-8-15T12:8:30+05:00",  # unpadded
            "2020-08-15T12:08:30+05",  # no minutes offset
            "2020-08-15T12:08:30.0000000001+05:00",  # overly precise
            "2020-08-15T12:08:30+05:00:01.0",  # fractional seconds in offset
            "2020-08-15T12:08:30+05:00stuff",  # trailing stuff
            "2020-08-15T12:08+04:00",  # no seconds
            "2020-08-15",  # date only
            "2020-08-15 12:08:30+05:00"  # wrong separator
            "2020-08-15T12:08.30+05:00",  # wrong time separator
            "2020-08-15T12:08:30+24:00",  # too large offset
            "2020-08-15T23:12:09-99:00",  # invalid offset
            "",  # empty
            "garbage",  # garbage
            "20𝟚0-08-15T12:08:30+00:00",  # non-ASCII
        ],
    )
    def test_invalid(self, s):
        with pytest.raises(ValueError, match="format.*" + re.escape(repr(s))):
            LocalSystemDateTime.parse_common_iso(s)

    @pytest.mark.parametrize(
        "s",
        [
            "0001-01-01T02:08:30+05:00",
            "9999-12-31T22:08:30-05:00",
        ],
    )
    def test_bounds(self, s):
        with pytest.raises(ValueError):
            LocalSystemDateTime.parse_common_iso(s)

    @given(text())
    def test_fuzzing(self, s: str):
        with pytest.raises(
            ValueError,
            match=r"format.*" + re.escape(repr(s)),
        ):
            LocalSystemDateTime.parse_common_iso(s)


class TestTimestamp:

    @local_nyc_tz()
    def test_default_seconds(self):
        assert LocalSystemDateTime(1969, 12, 31, 19).timestamp() == 0
        assert (
            LocalSystemDateTime(
                2020, 8, 15, 8, 8, 30, nanosecond=999_999_999
            ).timestamp()
            == 1_597_493_310
        )

        ambiguous = LocalSystemDateTime(
            2023, 11, 5, 1, 15, 30, disambiguate="earlier"
        )
        assert (
            ambiguous.timestamp()
            != ambiguous.replace(disambiguate="later").timestamp()
        )

    @local_nyc_tz()
    def test_millis(self):
        assert LocalSystemDateTime(1969, 12, 31, 19).timestamp_millis() == 0
        assert (
            LocalSystemDateTime(
                2020, 8, 15, 8, 8, 30, nanosecond=45_999_999
            ).timestamp_millis()
            == 1_597_493_310_045
        )

        ambiguous = LocalSystemDateTime(
            2023, 11, 5, 1, 15, 30, disambiguate="earlier"
        )
        assert (
            ambiguous.timestamp()
            != ambiguous.replace(disambiguate="later").timestamp_millis()
        )

    @local_nyc_tz()
    def test_nanos(self):
        assert LocalSystemDateTime(1969, 12, 31, 19).timestamp_nanos() == 0
        assert (
            LocalSystemDateTime(
                2020, 8, 15, 8, 8, 30, nanosecond=450
            ).timestamp_nanos()
            == 1_597_493_310_000_000_450
        )

        ambiguous = LocalSystemDateTime(
            2023, 11, 5, 1, 15, 30, disambiguate="earlier"
        )
        assert (
            ambiguous.timestamp()
            != ambiguous.replace(disambiguate="later").timestamp_nanos()
        )


class TestFromTimestamp:

    @pytest.mark.parametrize(
        "method, factor",
        [
            (LocalSystemDateTime.from_timestamp, 1),
            (LocalSystemDateTime.from_timestamp_millis, 1_000),
            (LocalSystemDateTime.from_timestamp_nanos, 1_000_000_000),
        ],
    )
    @local_ams_tz()
    def test_all(self, method, factor):
        assert method(0).exact_eq(LocalSystemDateTime(1970, 1, 1, 1))
        assert method(1_597_493_310 * factor).exact_eq(
            LocalSystemDateTime(2020, 8, 15, 14, 8, 30)
        )
        with pytest.raises((OSError, OverflowError, ValueError)):
            method(1_000_000_000_000_000_000 * factor)

        with pytest.raises((OSError, OverflowError, ValueError)):
            method(-1_000_000_000_000_000_000 * factor)

        with pytest.raises(TypeError):
            method()

    @local_ams_tz()
    def test_nanos(self):
        assert LocalSystemDateTime.from_timestamp_nanos(
            1_597_493_310_123_456_789
        ).exact_eq(
            LocalSystemDateTime(2020, 8, 15, 14, 8, 30, nanosecond=123_456_789)
        )

    @local_ams_tz()
    def test_millis(self):
        assert LocalSystemDateTime.from_timestamp_millis(
            1_597_493_310_123
        ).exact_eq(
            LocalSystemDateTime(2020, 8, 15, 14, 8, 30, nanosecond=123_000_000)
        )


@local_nyc_tz()
def test_repr():
    d = LocalSystemDateTime(2023, 3, 26, 2, 15)
    assert repr(d) == "LocalSystemDateTime(2023-03-26 02:15:00-04:00)"


@local_nyc_tz()
def test_py_datetime():
    d = LocalSystemDateTime(2020, 8, 15, 23, 12, 9, nanosecond=987_654_999)
    py = d.py_datetime()
    assert py == py_datetime(2020, 8, 15, 23, 12, 9, 987_654).astimezone(None)


class TestFromPyDateTime:
    @local_ams_tz()
    def test_basic(self):
        d = py_datetime(
            2020, 8, 15, 23, tzinfo=timezone(hours(2).py_timedelta())
        )
        assert LocalSystemDateTime.from_py_datetime(d).exact_eq(
            LocalSystemDateTime(2020, 8, 15, 23)
        )

    @local_ams_tz()
    def test_disambiguated(self):
        d = py_datetime(
            2023, 10, 29, 2, 15, 30, tzinfo=timezone(hours(1).py_timedelta())
        )
        assert LocalSystemDateTime.from_py_datetime(d).exact_eq(
            LocalSystemDateTime(2023, 10, 29, 2, 15, 30, disambiguate="later")
        )

    def test_wrong_tzinfo(self):
        with pytest.raises(ValueError, match="Paris"):
            LocalSystemDateTime.from_py_datetime(
                py_datetime(2020, 8, 15, 23, tzinfo=ZoneInfo("Europe/Paris"))
            )

    def test_bounds(self):
        with pytest.raises((ValueError, OverflowError), match="range|year"):
            LocalSystemDateTime.from_py_datetime(
                py_datetime(1, 1, 1, tzinfo=timezone(timedelta(hours=2)))
            )

        with pytest.raises((ValueError, OverflowError), match="range|year"):
            LocalSystemDateTime.from_py_datetime(
                py_datetime(
                    9999, 12, 31, hour=23, tzinfo=timezone(timedelta(hours=-2))
                )
            )


@local_nyc_tz()
def test_now():
    now = LocalSystemDateTime.now()
    assert now.offset == hours(-4)
    py_now = py_datetime.now(ZoneInfo("America/New_York"))
    assert py_now - now.py_datetime() < timedelta(seconds=1)


class TestReplace:
    @local_ams_tz()
    def test_basics(self):
        d = LocalSystemDateTime(2020, 8, 15, 23, 12, 9, nanosecond=987_654_321)
        assert d.replace(year=2021).exact_eq(
            LocalSystemDateTime(2021, 8, 15, 23, 12, 9, nanosecond=987_654_321)
        )
        assert d.replace(month=9).exact_eq(
            LocalSystemDateTime(2020, 9, 15, 23, 12, 9, nanosecond=987_654_321)
        )
        assert d.replace(day=16).exact_eq(
            LocalSystemDateTime(2020, 8, 16, 23, 12, 9, nanosecond=987_654_321)
        )
        assert d.replace(hour=1).exact_eq(
            LocalSystemDateTime(2020, 8, 15, 1, 12, 9, nanosecond=987_654_321)
        )
        assert d.replace(minute=1).exact_eq(
            LocalSystemDateTime(2020, 8, 15, 23, 1, 9, nanosecond=987_654_321)
        )
        assert d.replace(second=1).exact_eq(
            LocalSystemDateTime(2020, 8, 15, 23, 12, 1, nanosecond=987_654_321)
        )
        assert d.replace(nanosecond=1).exact_eq(
            LocalSystemDateTime(2020, 8, 15, 23, 12, 9, nanosecond=1)
        )

    def test_invalid(self):
        d = LocalSystemDateTime(2020, 8, 15, 23, 12, 9)
        with pytest.raises(TypeError, match="tzinfo"):
            d.replace(tzinfo=timezone.utc)  # type: ignore[call-arg]
        with pytest.raises(TypeError, match="fold"):
            d.replace(fold=1)  # type: ignore[call-arg]
        with pytest.raises(TypeError, match="foo"):
            d.replace(foo=1)  # type: ignore[call-arg]

    @local_ams_tz()
    def test_disambiguate(self):
        d = LocalSystemDateTime(
            2023, 10, 29, 2, 15, 30, disambiguate="earlier"
        )
        with pytest.raises(
            AmbiguousTime,
            match="2023-10-29 02:15:30 is ambiguous in the system timezone",
        ):
            d.replace(disambiguate="raise")
        with pytest.raises(
            AmbiguousTime,
            match="2023-10-29 02:15:30 is ambiguous in the system timezone",
        ):
            d.replace()

        assert d.replace(disambiguate="later").exact_eq(
            LocalSystemDateTime(2023, 10, 29, 2, 15, 30, disambiguate="later")
        )
        assert d.replace(disambiguate="earlier").exact_eq(d)

    @local_ams_tz()
    def test_nonexistent(self):
        d = LocalSystemDateTime(2023, 3, 26, 1, 15, 30)
        with pytest.raises(
            SkippedTime,
            match="2023-03-26 02:15:30 is skipped in the system timezone",
        ):
            d.replace(hour=2)

    @local_ams_tz()
    def test_bounds_min(self):
        d = LocalSystemDateTime(2020, 8, 15, 23, 12, 9)
        with pytest.raises((ValueError, OverflowError), match="range|year"):
            d.replace(year=1, month=1, day=1)

    @local_nyc_tz()
    def test_bounds_max(self):
        d = LocalSystemDateTime(2020, 8, 15, 23, 12, 9)
        with pytest.raises((ValueError, OverflowError), match="range|year"):
            d.replace(year=9999, month=12, day=31, hour=23)


class TestAddTimeUnits:
    @local_ams_tz()
    def test_zero(self):
        d = LocalSystemDateTime(2020, 8, 15, 23, 12, 9, nanosecond=987_654_321)
        assert (d + hours(0)).exact_eq(d)

        # the equivalent with the method
        assert d.add(hours=1).exact_eq(d + hours(1))

    @local_ams_tz()
    def test_ambiguous_plus_zero(self):
        d = LocalSystemDateTime(
            2023,
            10,
            29,
            2,
            15,
            30,
            disambiguate="earlier",
        )
        assert (d + hours(0)).exact_eq(d)
        assert (d.replace(disambiguate="later") + hours(0)).exact_eq(
            d.replace(disambiguate="later")
        )

        # the equivalent with the method
        assert d.add(hours=0).exact_eq(d)
        assert (
            d.replace(disambiguate="later")
            .add(hours=0)
            .exact_eq(d.replace(disambiguate="later"))
        )

    @local_ams_tz()
    def test_accounts_for_dst(self):
        d = LocalSystemDateTime(
            2023,
            10,
            29,
            2,
            15,
            30,
            disambiguate="earlier",
        )
        assert (d + hours(24)).exact_eq(
            LocalSystemDateTime(2023, 10, 30, 1, 15, 30)
        )
        assert (d.replace(disambiguate="later") + hours(24)).exact_eq(
            LocalSystemDateTime(2023, 10, 30, 2, 15, 30)
        )

        # the equivalent with the method
        assert d.add(hours=24).exact_eq(d + hours(24))
        assert (
            d.replace(disambiguate="later")
            .add(hours=24)
            .exact_eq(d.replace(disambiguate="later") + hours(24))
        )

    @local_ams_tz()
    def test_out_of_range(self):
        d = LocalSystemDateTime(2020, 8, 15)

        with pytest.raises((ValueError, OverflowError), match="range|year"):
            d + hours(24 * 366 * 8_000)

        # the equivalent with the method
        with pytest.raises((ValueError, OverflowError), match="range|year"):
            d.add(hours=24 * 366 * 8_000)

    @local_ams_tz()
    def test_not_implemented(self):
        d = LocalSystemDateTime(2020, 8, 15)
        with pytest.raises(TypeError, match="unsupported operand type"):
            d + 42  # type: ignore[operator]

        with pytest.raises(TypeError, match="unsupported operand type"):
            42 + d  # type: ignore[operator]

        with pytest.raises(TypeError, match="unsupported operand type"):
            years(1) + d  # type: ignore[operator]

        with pytest.raises(TypeError, match="unsupported operand type"):
            d + d  # type: ignore[operator]

        with pytest.raises(TypeError):
            d.add(4)  # type: ignore[misc]


class TestAddDateUnits:

    @local_ams_tz()
    def test_zero(self):
        d = LocalSystemDateTime(2020, 8, 15, 23, 12, 9, nanosecond=987_654_321)
        assert (d + days(0)).exact_eq(d)

        # the equivalent with the method
        assert d.add(days=0).exact_eq(d)
        assert d.add().exact_eq(d)

    @local_ams_tz()
    def test_simple_date(self):
        d = LocalSystemDateTime(2020, 8, 15, 23, 12, 9, nanosecond=987_654_321)
        assert (d + days(1)).exact_eq(d.replace(day=16))
        assert (d + years(1) + weeks(2) + days(-2)).exact_eq(
            d.replace(year=2021, day=27)
        )

        # the equivalent with the method
        assert d.add(days=1).exact_eq(d + days(1))
        assert d.add(years=1, weeks=2, days=-2).exact_eq(
            d + years(1) + weeks(2) + days(-2)
        )

    @local_ams_tz()
    def test_ambiguity(self):
        d = LocalSystemDateTime(
            2023,
            10,
            29,
            2,
            15,
            30,
            disambiguate="later",
        )
        assert (d + days(0)).exact_eq(d)
        assert (d + (days(7) - weeks(1))).exact_eq(d)
        assert (d + days(1)).exact_eq(d.replace(day=30))
        assert (d + days(6)).exact_eq(d.replace(month=11, day=4))
        assert (d + hours(-1)).exact_eq(d.replace(disambiguate="earlier"))
        assert (d + hours(1)).exact_eq(d.replace(hour=3))
        assert (d.replace(disambiguate="earlier") + hours(1)).exact_eq(d)

        # transition to another fold
        assert (d + years(1) + days(-2)).exact_eq(
            d.replace(year=2024, day=27, disambiguate="earlier")
        )
        # transition to a gap
        assert (d + months(5) + days(2)).exact_eq(
            d.replace(year=2024, month=3, day=31, disambiguate="later")
        )
        # transition over a gap
        assert (d + months(5) + days(2) + hours(2)).exact_eq(
            d.replace(year=2024, month=3, day=31, hour=5)
        )
        assert (d + months(5) + days(2) + hours(-1)).exact_eq(
            d.replace(year=2024, month=3, day=31, disambiguate="earlier")
        )

        # the equivalent with the method
        assert d.add(days=0).exact_eq(d)
        assert d.add(days=7, weeks=-1).exact_eq(d)
        assert d.add(days=1).exact_eq(d + days(1))
        assert d.add(days=6).exact_eq(d + days(6))
        assert d.add(hours=-1).exact_eq(d + hours(-1))
        assert d.add(hours=1).exact_eq(d + hours(1))
        assert d.replace(disambiguate="earlier").add(hours=1).exact_eq(d)
        assert d.add(years=1, days=-2, disambiguate="compatible").exact_eq(
            d + years(1) + days(-2)
        )
        assert d.add(months=5, days=2, disambiguate="compatible").exact_eq(
            d + months(5) + days(2)
        )
        assert d.add(
            months=5, days=2, hours=2, disambiguate="compatible"
        ).exact_eq(d + months(5) + days(2) + hours(2))
        assert d.add(
            months=5, days=2, hours=-1, disambiguate="compatible"
        ).exact_eq(d + months(5) + days(2) + hours(-1))

    @local_ams_tz()
    def test_out_of_bounds_min(self):
        d = LocalSystemDateTime(2000, 1, 1)
        with pytest.raises((ValueError, OverflowError), match="range|year"):
            d + years(-1999)

        # the equivalent with the method
        with pytest.raises((ValueError, OverflowError), match="range|year"):
            d.add(years=-1999)

    @local_nyc_tz()
    def test_out_of_bounds_max(self):
        d = LocalSystemDateTime(2000, 12, 31, hour=23)
        with pytest.raises((ValueError, OverflowError), match="range|year"):
            d + years(7999)

        # the equivalent with the method
        with pytest.raises((ValueError, OverflowError), match="range|year"):
            d.add(years=7999)


class TestSubtractTimeUnits:
    @local_ams_tz()
    def test_zero(self):
        d = LocalSystemDateTime(2020, 8, 15, 23, 12, 9, nanosecond=987_654_321)
        assert (d - hours(0)).exact_eq(d)

        # the equivalent with the method
        assert d.subtract(hours=0).exact_eq(d)
        assert d.subtract().exact_eq(d)

    @local_ams_tz()
    def test_ambiguous_minus_zero(self):
        d = LocalSystemDateTime(
            2023,
            10,
            29,
            2,
            15,
            30,
            disambiguate="earlier",
        )
        assert (d - hours(0)).exact_eq(d)
        assert (d.replace(disambiguate="later") - hours(0)).exact_eq(
            d.replace(disambiguate="later")
        )

        # the equivalent with the method
        assert d.subtract(hours=0).exact_eq(d)
        assert (
            d.replace(disambiguate="later")
            .subtract(hours=0)
            .exact_eq(d.replace(disambiguate="later"))
        )

    @local_ams_tz()
    def test_accounts_for_dst(self):
        d = LocalSystemDateTime(
            2023,
            10,
            29,
            2,
            15,
            30,
            disambiguate="earlier",
        )
        assert (d - hours(24)).exact_eq(
            LocalSystemDateTime(2023, 10, 28, 2, 15, 30)
        )
        assert (d.replace(disambiguate="later") - hours(24)).exact_eq(
            LocalSystemDateTime(2023, 10, 28, 3, 15, 30)
        )

        # the equivalent with the method
        assert d.subtract(hours=24).exact_eq(d - hours(24))
        assert (
            d.replace(disambiguate="later")
            .subtract(hours=24)
            .exact_eq(d.replace(disambiguate="later") - hours(24))
        )

    def test_subtract_not_implemented(self):
        d = LocalSystemDateTime(2020, 8, 15)
        with pytest.raises(TypeError, match="unsupported operand type"):
            d - 42  # type: ignore[operator]

        with pytest.raises(TypeError, match="unsupported operand type"):
            42 - d  # type: ignore[operator]

        with pytest.raises(TypeError, match="unsupported operand type"):
            hours(1) - d  # type: ignore[operator]

        with pytest.raises(TypeError):
            d.subtract(4)  # type: ignore[misc]


class TestSubtractDateUnits:
    @local_ams_tz()
    def test_zero(self):
        d = LocalSystemDateTime(2020, 8, 15, 23, 12, 9, nanosecond=987_654_321)
        assert (d - days(0)).exact_eq(d)

        # the equivalent with the method
        assert d.subtract(days=0).exact_eq(d)
        assert d.subtract().exact_eq(d)

    @local_ams_tz()
    def test_simple_date(self):
        d = LocalSystemDateTime(2020, 8, 15, 23, 12, 9, nanosecond=987_654_321)
        assert (d - days(1)).exact_eq(d.replace(day=14))
        assert (d - years(1) - weeks(2) - days(-2)).exact_eq(
            d.replace(year=2019, day=3)
        )

        # the equivalent with the method
        assert d.subtract(days=1).exact_eq(d - days(1))
        assert d.subtract(years=1, weeks=2, days=-2).exact_eq(
            d - years(1) - weeks(2) - days(-2)
        )

    @local_ams_tz()
    def test_ambiguity(self):
        d = LocalSystemDateTime(
            2023,
            10,
            29,
            2,
            15,
            30,
            disambiguate="later",
        )

        # the above, but with exact_eq:
        assert (d - days(0)).exact_eq(d)
        assert (d - (days(7) - weeks(1))).exact_eq(d)
        assert (d - days(1)).exact_eq(d.replace(day=28))
        assert (d - days(6)).exact_eq(d.replace(month=10, day=23))
        assert (d - hours(1)).exact_eq(d.replace(disambiguate="earlier"))
        assert (d - hours(-1)).exact_eq(d.replace(hour=3))
        assert (d.replace(disambiguate="earlier") - hours(-1)).exact_eq(d)

        # transition to another fold
        assert (d - years(1) - days(-1)).exact_eq(
            d.replace(year=2022, day=30, disambiguate="earlier")
        )
        # transition to a gap
        assert (d - months(7) - days(3)).exact_eq(
            d.replace(month=3, day=26, disambiguate="later")
        )
        # transition over a gap
        assert (d - months(7) - days(3) - hours(1)).exact_eq(
            d.replace(month=3, day=26, hour=1)
        )
        assert (d - months(7) - days(3) - hours(-1)).exact_eq(
            d.replace(month=3, day=26, hour=4)
        )

        # the equivalent with the method
        assert d.subtract(days=0).exact_eq(d)
        assert d.subtract(days=7, weeks=-1).exact_eq(d)
        assert d.subtract(days=1).exact_eq(d - days(1))
        assert d.subtract(days=6).exact_eq(d - days(6))
        assert d.subtract(hours=1).exact_eq(d - hours(1))
        assert d.subtract(hours=-1).exact_eq(d - hours(-1))
        assert d.replace(disambiguate="earlier").subtract(hours=-1).exact_eq(d)
        assert d.subtract(
            years=1, days=-1, disambiguate="compatible"
        ).exact_eq(d - years(1) - days(-1))
        assert d.subtract(
            months=7, days=3, disambiguate="compatible"
        ).exact_eq(d - months(7) - days(3))
        assert d.subtract(
            months=7, days=3, hours=1, disambiguate="compatible"
        ).exact_eq(d - months(7) - days(3) - hours(1))
        assert d.subtract(
            months=7, days=3, hours=-1, disambiguate="compatible"
        ).exact_eq(d - months(7) - days(3) - hours(-1))

    @local_ams_tz()
    def test_out_of_bounds_min(self):
        d = LocalSystemDateTime(2000, 1, 1)
        with pytest.raises((ValueError, OverflowError), match="range|year"):
            d - years(1999)

        with pytest.raises((ValueError, OverflowError), match="range|year"):
            d.subtract(years=1999)

    @local_nyc_tz()
    def test_out_of_bounds_max(self):
        d = LocalSystemDateTime(2000, 12, 31, hour=23)
        with pytest.raises((ValueError, OverflowError), match="range|year"):
            d - years(-7999)

        with pytest.raises((ValueError, OverflowError), match="range|year"):
            d.subtract(years=-7999)


class TestSubtractOtherDateTime:

    @local_ams_tz()
    def test_subtract_datetime(self):
        d = LocalSystemDateTime(2023, 10, 29, 5)
        other = LocalSystemDateTime(2023, 10, 28, 3, nanosecond=2_000)
        assert d - other == (hours(27) - microseconds(2))
        assert other - d == -(hours(27) - microseconds(2))

    @local_ams_tz()
    def test_subtract_amibiguous_datetime(self):
        d = LocalSystemDateTime(2023, 10, 29, 2, 15, disambiguate="earlier")
        other = LocalSystemDateTime(2023, 10, 28, 3, 15)
        assert d - other == hours(23)
        assert d.replace(disambiguate="later") - other == hours(24)
        assert other - d == hours(-23)
        assert other - d.replace(disambiguate="later") == hours(-24)

    @local_ams_tz()
    def test_utc(self):
        d = LocalSystemDateTime(2023, 10, 29, 2, disambiguate="earlier")
        assert d - UTCDateTime(2023, 10, 28, 20) == hours(4)
        assert d.replace(disambiguate="later") - UTCDateTime(
            2023, 10, 28, 20
        ) == hours(5)

    @local_ams_tz()
    def test_offset(self):
        d = LocalSystemDateTime(2023, 10, 29, 2, disambiguate="earlier")
        assert d - OffsetDateTime(2023, 10, 28, 22, offset=hours(1)) == hours(
            3
        )
        assert d.replace(disambiguate="later") - OffsetDateTime(
            2023, 10, 28, 22, offset=hours(1)
        ) == hours(4)

    @local_ams_tz()
    def test_zoned(self):
        d = LocalSystemDateTime(2023, 10, 29, 2, disambiguate="earlier")
        assert d - ZonedDateTime(
            2023, 10, 28, 17, tz="America/New_York"
        ) == hours(3)
        assert d.replace(disambiguate="later") - ZonedDateTime(
            2023, 10, 28, 17, tz="America/New_York"
        ) == hours(4)


class TestReplaceDate:
    @local_ams_tz()
    def test_unambiguous(self):
        d = LocalSystemDateTime(2020, 8, 15, 14)
        assert d.replace_date(Date(2021, 1, 2)) == LocalSystemDateTime(
            2021, 1, 2, 14
        )

    @local_ams_tz()
    def test_ambiguous(self):
        d = LocalSystemDateTime(2020, 1, 1, 2, 15, 30)
        date = Date(2023, 10, 29)
        with pytest.raises(AmbiguousTime):
            assert d.replace_date(date)

        assert d.replace_date(date, disambiguate="earlier") == d.replace(
            year=2023, month=10, day=29, disambiguate="earlier"
        )
        assert d.replace_date(date, disambiguate="later") == d.replace(
            year=2023, month=10, day=29, disambiguate="later"
        )
        assert d.replace_date(date, disambiguate="compatible") == d.replace(
            year=2023, month=10, day=29, disambiguate="compatible"
        )

    @local_ams_tz()
    def test_nonexistent(self):
        d = LocalSystemDateTime(2020, 1, 1, 2, 15, 30)
        date = Date(2023, 3, 26)
        with pytest.raises(SkippedTime):
            assert d.replace_date(date)

        assert d.replace_date(date, disambiguate="earlier") == d.replace(
            year=2023, month=3, day=26, disambiguate="earlier"
        )
        assert d.replace_date(date, disambiguate="later") == d.replace(
            year=2023, month=3, day=26, disambiguate="later"
        )
        assert d.replace_date(date, disambiguate="compatible") == d.replace(
            year=2023, month=3, day=26, disambiguate="compatible"
        )

    def test_invalid(self):
        d = LocalSystemDateTime(2020, 8, 15, 14)
        with pytest.raises((TypeError, AttributeError)):
            d.replace_date(object())  # type: ignore[arg-type]

        with pytest.raises(ValueError, match="disambiguate"):
            d.replace_date(Date(2020, 8, 15), disambiguate="foo")  # type: ignore[arg-type]

        with pytest.raises(TypeError, match="got 2|foo"):
            d.replace_date(Date(2020, 8, 15), disambiguate="raise", foo=4)  # type: ignore[call-arg]

        with pytest.raises(TypeError, match="foo"):
            d.replace_date(Date(2020, 8, 15), foo="raise")  # type: ignore[call-arg]

    def test_out_of_range_due_to_offset(self):
        with local_ams_tz():
            d = LocalSystemDateTime(2020, 1, 1)
            with pytest.raises(
                (ValueError, OverflowError), match="range|year"
            ):
                d.replace_date(Date(1, 1, 1))

        with local_nyc_tz():
            d2 = LocalSystemDateTime(2020, 1, 1, hour=23)
            with pytest.raises(
                (ValueError, OverflowError), match="range|year"
            ):
                d2.replace_date(Date(9999, 12, 31))


class TestReplaceTime:
    @local_ams_tz()
    def test_unambiguous(self):
        d = LocalSystemDateTime(2020, 8, 15, 14)
        assert d.replace_time(Time(1, 2, 3, nanosecond=4_000)).exact_eq(
            LocalSystemDateTime(2020, 8, 15, 1, 2, 3, nanosecond=4_000)
        )

    @local_ams_tz()
    def test_fold(self):
        d = LocalSystemDateTime(2023, 10, 29, 0, 15, 30)
        time = Time(2, 15, 30)
        with pytest.raises(AmbiguousTime):
            assert d.replace_time(time)

        assert d.replace_time(time, disambiguate="earlier").exact_eq(
            d.replace(hour=2, minute=15, second=30, disambiguate="earlier")
        )
        assert d.replace_time(time, disambiguate="later").exact_eq(
            d.replace(hour=2, minute=15, second=30, disambiguate="later")
        )
        assert d.replace_time(time, disambiguate="compatible").exact_eq(
            d.replace(hour=2, minute=15, second=30, disambiguate="compatible")
        )

    @local_ams_tz()
    def test_gap(self):
        d = LocalSystemDateTime(2023, 3, 26, 8, 15)
        time = Time(2, 15)
        with pytest.raises(SkippedTime):
            assert d.replace_time(time)

        assert d.replace_time(time, disambiguate="earlier").exact_eq(
            d.replace(hour=2, minute=15, disambiguate="earlier")
        )
        assert d.replace_time(time, disambiguate="later").exact_eq(
            d.replace(hour=2, minute=15, disambiguate="later")
        )
        assert d.replace_time(time, disambiguate="compatible").exact_eq(
            d.replace(hour=2, minute=15, disambiguate="compatible")
        )

    def test_invalid(self):
        d = LocalSystemDateTime(2020, 8, 15, 14)
        with pytest.raises((TypeError, AttributeError)):
            d.replace_time(object())  # type: ignore[arg-type]

        with pytest.raises(ValueError, match="disambiguate"):
            d.replace_time(Time(1, 2, 3), disambiguate="foo")  # type: ignore[arg-type]

        with pytest.raises(TypeError, match="got 2|foo"):
            d.replace_time(Time(1, 2, 3), disambiguate="raise", foo=4)  # type: ignore[call-arg]

        with pytest.raises(TypeError, match="foo"):
            d.replace_time(Time(1, 2, 3), foo="raise")  # type: ignore[call-arg]

    def test_out_of_range_due_to_offset(self):
        with local_ams_tz():
            try:
                d = UTCDateTime.MIN.to_local_system()
            except OverflowError as e:
                # For some platforms, this cannot be represented as a time_t.
                # we skip the test in this case.
                assert "time_t" in str(e)
                pytest.skip("time_t overflow")

            with pytest.raises(
                (ValueError, OverflowError), match="range|year"
            ):
                d.replace_time(Time(0))

        with local_nyc_tz():
            d2 = UTCDateTime.MAX.to_local_system()
            with pytest.raises(
                (ValueError, OverflowError), match="range|year"
            ):
                d2.replace_time(Time(23))


@local_ams_tz()
def test_pickle():
    d = LocalSystemDateTime(2020, 8, 15, 23, 12, 9, nanosecond=987_654_321)
    dumped = pickle.dumps(d)
    assert len(dumped) <= len(pickle.dumps(d.py_datetime()))
    assert pickle.loads(pickle.dumps(d)).exact_eq(d)


@local_ams_tz()
def test_old_pickle_data_remains_unpicklable():
    # Don't update this value -- the whole idea is that it's a pickle at
    # a specific version of the library.
    dumped = (
        b"\x80\x04\x953\x00\x00\x00\x00\x00\x00\x00\x8c\x08whenever\x94\x8c\x0c_unp"
        b"kl_local\x94\x93\x94C\x0f\xe4\x07\x08\x0f\x17\x0c\t\xb1h\xde: \x1c\x00\x00"
        b"\x94\x85\x94R\x94."
    )
    assert pickle.loads(dumped).exact_eq(
        LocalSystemDateTime(2020, 8, 15, 23, 12, 9, nanosecond=987_654_321)
    )


def test_copy():
    d = LocalSystemDateTime(2020, 8, 15, 23, 12, 9, nanosecond=987_654)
    assert copy(d) is d
    assert deepcopy(d) is d
