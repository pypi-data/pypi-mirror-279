import datetime
from dateutil.relativedelta import relativedelta


def format_now(date):
    datetime_object = datetime.datetime.strptime(date, '%y-%m-%d %H:%M:%S')
    return datetime_object
def format_all(date):
    datetime_object = datetime.datetime.strptime(date, '%d-%m-%y %H:%M:%S')
    return datetime_object

def format(date):
    try:
        datetime_object = datetime.datetime.strptime(date, '%d-%m-%y')
        return datetime_object
    except ValueError:
        try:
            datetime_object = datetime.datetime.strptime(date, '%d-%m-%y %H:%M:%S')
            return datetime_object
        except ValueError:
            try:
                datetime_object = datetime.datetime.strptime(date, '%y-%m-%d %H:%M:%S')
                return datetime_object
            except ValueError:
                try:
                    datetime_object = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
                    return datetime_object
                except ValueError:
                    try:
                        datetime_object = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                        return datetime_object
                    except Exception:
                        print(date)

def current():
    now = datetime.datetime.now()
    return now

def add(date, months:int=0, days:int=0, years:int=0, minutes:int=0, seconds:int=0, hours:int=0):
    if months != 0:
        return date + relativedelta(months=months)
    if days != 0:
        return date + relativedelta(days=days)
    if years != 0:
        return date + relativedelta(years=years)
    if minutes != 0:
        return date + relativedelta(minutes=minutes)
    if seconds != 0:
        return date + relativedelta(seconds=seconds)
    if hours != 0:
        return date + relativedelta(hours=hours)

def covert_relativtimedelta(date):
    relative_date = relativedelta(years=date.year, months=date.month, days=date.day, hours=date.hour,
                                  minutes=date.minute, seconds=date.second, microseconds=date.microsecond)
    return relative_date

def datetime_to_String(date):
    part1 = list()
    part2 = list()
    if date.microsecond != 0:
        part1.append(str(date.microsecond))
    if date.second != 0:
        part1.append(str(date.second))
    if date.minute != 0:
        part1.append(str(date.minute))
    if date.hour != 0:
        part1.append(str(date.hour))
    part1 = part1[::-1]
    part1 = ':'.join(part1)
    if date.day != 0:
        part2.append(str(date.day))
    if date.month != 0:
        part2.append(str(date.month))
    if date.year != 0:
        part2.append(str(date.year))
    part2 = part2[::-1]
    part2 = '-'.join(part2)
    if part1 == '':
        return part2
    else:
        return ' '.join([part2, part1])
