from datetime import date


class Date:
    date_format = "%Y-%m-%d"

    @classmethod
    def today(cls):
        return date.today().strftime(cls.date_format)

    @classmethod
    def first_day_this_month(cls):
        today = date.today()
        return date(today.year, today.month, 1).strftime(cls.date_format)
