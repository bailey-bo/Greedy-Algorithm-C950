from datetime import date, datetime

# Function used to input a string and return a datetime object with a given format
# Runtime: O(1)
def parse_string(string):
    format = '%I:%M%p'
    todayDate = date.today()
    datetime_str = datetime.strptime(string, format)
    combinedDatetime = datetime.combine(todayDate, datetime_str.time())
    return combinedDatetime

# Function used to input a time object and return a datetime object at today's date
# Runtime: O(1)
def parse_time(time):
    todayDate = date.today()
    combinedDatetime = datetime.combine(todayDate,time)
    return combinedDatetime




