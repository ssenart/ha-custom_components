from pygazpar.enum import Frequency
from gazpar.time_period import TimePeriod
from datetime import datetime


# --------------------------------------------------------------------------------------------
class TestTimePeriod:

    # ----------------------------------
    def test_parse_hourly(self):

        timePeriod = TimePeriod.parse("23/04/2021 11:14:38", Frequency.HOURLY)

        assert(datetime(2021, 4, 23, 11, 0, 0) == timePeriod.startTime)
        assert(datetime(2021, 4, 23, 11, 59, 59) == timePeriod.endTime)

    # ----------------------------------
    def test_parse_daily(self):

        timePeriod = TimePeriod.parse("23/04/2021", Frequency.DAILY)

        assert(datetime(2021, 4, 23, 0, 0, 0) == timePeriod.startTime)
        assert(datetime(2021, 4, 23, 23, 59, 59) == timePeriod.endTime)

    # ----------------------------------
    def test_parse_weekly(self):

        timePeriod = TimePeriod.parse("Du 19/04/2021 au 25/04/2021", Frequency.WEEKLY)

        assert(datetime(2021, 4, 19, 0, 0, 0) == timePeriod.startTime)
        assert(datetime(2021, 4, 25, 23, 59, 59) == timePeriod.endTime)

    # ----------------------------------
    def test_parse_monthly(self):

        timePeriod = TimePeriod.parse("Avril 2021", Frequency.MONTHLY)

        assert(datetime(2021, 4, 1, 0, 0, 0) == timePeriod.startTime)
        assert(datetime(2021, 4, 30, 23, 59, 59) == timePeriod.endTime)
