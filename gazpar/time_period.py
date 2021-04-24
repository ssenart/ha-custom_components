from __future__ import annotations  # Python 3.7+: The annotations feature are referring to the PEP 563: Postponed evaluation of annotations. It's an enhancement to the existing annotations feature which was initially introduced in python 3.0 and redefined as type hints in python 3.5, that's why your code works under python 3.8.
from datetime import datetime
from pygazpar.enum import Frequency
import dateparser
import dateparser.search


# --------------------------------------------------------------------------------------------
class InvalidFormatError(ValueError):
    pass


# --------------------------------------------------------------------------------------------
class TimePeriod:

    HOURLY_FORMAT = "%d/%m/%Y %H:%M:%S"
    DAILY_FORMAT = "%d/%m/%Y"
    MONTHLY_FORMAT = "%B %Y"

    def __init__(self, startTime: datetime, endTime: datetime):

        self.__startTime = startTime
        self.__endTime = endTime

    @property
    def startTime(self) -> datetime:
        return self.__startTime

    @property
    def endTime(self) -> datetime:
        return self.__endTime

    @staticmethod
    def parse(timePeriodString: str, frequency: Frequency) -> TimePeriod:

        parserByFrequency = {
            Frequency.HOURLY: TimePeriod.__parseHourly,
            Frequency.DAILY: TimePeriod.__parseDaily,
            Frequency.WEEKLY: TimePeriod.__parseWeekly,
            Frequency.MONTHLY: TimePeriod.__parseMonthly,
        }

        return parserByFrequency[frequency](timePeriodString)

    @staticmethod
    def __parseHourly(timePeriodString: str) -> TimePeriod:
        dateTime = dateparser.parse(timePeriodString)

        startTime = dateTime.replace(minute=0, second=0)
        endTime = dateTime.replace(minute=59, second=59)

        res = TimePeriod(startTime, endTime)

        return res

    @staticmethod
    def __parseDaily(timePeriodString: str) -> TimePeriod:
        dateTime = dateparser.parse(timePeriodString)

        startTime = dateTime.replace(hour=0, minute=0, second=0)
        endTime = dateTime.replace(hour=23, minute=59, second=59)

        res = TimePeriod(startTime, endTime)

        return res

    @staticmethod
    def __parseWeekly(timePeriodString: str) -> TimePeriod:
        searchResult = dateparser.search.search_dates(timePeriodString)

        if len(searchResult) != 2:
            raise InvalidFormatError(f"The format of '{timePeriodString}' is not like 'Du DD/MM/YYYY au DD/MM/YYYY'")

        (from_date_string, startTime) = searchResult[0]
        (to_date_string, endTime) = searchResult[1]

        startTime = startTime.replace(hour=0, minute=0, second=0)
        endTime = endTime.replace(hour=23, minute=59, second=59)

        res = TimePeriod(startTime, endTime)

        return res

    @staticmethod
    def __parseMonthly(timePeriodString: str) -> TimePeriod:
        dateTime = dateparser.parse(timePeriodString, settings={'PREFER_DAY_OF_MONTH': 'last'})

        startTime = dateTime.replace(day=1, hour=0, minute=0, second=0)
        endTime = dateTime.replace(hour=23, minute=59, second=59)

        res = TimePeriod(startTime, endTime)

        return res
