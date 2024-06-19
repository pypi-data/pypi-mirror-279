# from datetime import datetime, date

# day_release = (datetime.today().date() - date(year_release, month_release, 1)).days
day_release = 1

year_release = 2024
month_release = 3

__version__ = f"{str(year_release)[-2:]}.{str(month_release).zfill(2)}.{str(day_release).zfill(3)}"
