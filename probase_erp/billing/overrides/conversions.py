from datetime import datetime , timedelta
from operator import truediv
from dateutil.relativedelta import relativedelta

def create_date(date):
#     month_number = date_obj.month
    date = datetime(int(date.year), int(date.month), int(date.day))
    return date

# create string formatted date
def create_date_string(date):
    month = datetime.strptime(f"{date.month}", "%m").strftime("%b")
    return  f"{date.day} {month} {date.year}"

def increment_day(date):
    date = datetime(date.year,date.month,date.day)
    date += timedelta(days=1)
    return date

def increment_week(date):
    date = datetime(date.year,date.month,date.day)
    date += timedelta(days=7)
    return date

def increment_month(date):
    date = datetime(int(date.year), date.month + 1, int(date.day))
    return date

def increment_year(date):
    date = datetime(int(date.year) + 1, int(date.month), int(date.day))
    return date

def calculate_monthly_due_date(date):
    date = datetime(int(date.year), int(date.month), int(date.day))
    date +=  timedelta(days=30)
    return date
def create_date_from_object(date_object):
    date = f"{date_object}"
    return datetime(int(date.split('-')[0]),int(date.split('-')[1]),int(date.split('-')[2]))