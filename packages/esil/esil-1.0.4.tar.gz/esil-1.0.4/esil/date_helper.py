from datetime import datetime, timedelta, timezone
import pytz
import time
import calendar

def timer_decorator(func): 
    '''
    @description: 计时装饰器，测量函数执行时间
    @param: func: 被装饰的函数
    @return: wrapper: 装饰器函数
    @usage:
    @timer_decorator
    def test():
    print("Hello, world!")
    time.sleep(1)
    print("Goodbye, world!")
    test()
    # 输出：
    # 函数 test 执行耗时: 1.000000 秒       
    '''   
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"函数 {func.__name__} 执行耗时: {end_time - start_time:.6f} 秒")
        return result
    return wrapper


def convert_julian_regular_date(julian_date):
    # 将Julian日期转换为正常的日期
    year = int(str(julian_date)[:4])  # 提取年份
    day_of_year = int(str(julian_date)[4:])  # 提取一年中的第几天
    # 创建日期对象
    date = datetime(year=year, month=1, day=1)  # 设置为当年的第一天
    date += timedelta(days=day_of_year - 1)  # 增加相应天数
    print("转换后的日期:", date.strftime("%Y-%m-%d"))
    return date

def get_UTC_time(start_date,days=0):
    '''

    Args:
        start_date: str, 如'2000-01-01 00:00:00'
        days: float,如7670.0625

    Returns:返回utc时间
    '''
    # 定义起始时间
    start_time_utc=None
    if isinstance(start_date,datetime):
        start_time_utc=start_date.replace(tzinfo=timezone.utc)        
    else:
       start_time_utc = datetime.strptime(start_date.astype(str).replace("000000000",'00'), '%Y-%m-%dT%H:%M:%S.%f').replace(tzinfo=timezone.utc)
    # 定义时间增量（7670.0625 天）
    days_increment = timedelta(days=days)
    # 计算当前时间
    current_time = start_time_utc + days_increment
    return current_time


def get_Beijing_time_from_timezone(date_with_timezone,days=0):
    '''
    Args:
    @ date_with_timezone: 如'2020-12-31T01:30:00.000000000'
       
    Returns:返回北京时间
    '''
    # 将UTC时间转换为北京时间
    utc_timezone = pytz.timezone('UTC')
    beijing_timezone = pytz.timezone('Asia/Shanghai')

    # 将带有时区信息的时间字符串转换为 datetime 对象
    datetime_obj = datetime.strptime(date_with_timezone.astype(str).replace("000000000",'00'), '%Y-%m-%dT%H:%M:%S.%f')
    utc_datetime = utc_timezone.localize(datetime_obj)
    beijing_datetime = utc_datetime.astimezone(beijing_timezone)
    beijing_datetime=beijing_datetime+ timedelta(days=days)
    return beijing_datetime.astimezone(tz=None).replace(tzinfo=None)
    # 将 datetime 对象转换为常规时间字符串
    #formatted_time = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')


def get_Beijing_time(start_date, days):
    '''
    Args:
        start_date: datetime
        days: float,如7670.0625
    Returns:返回beijing时间
    '''
    days_increment = timedelta(days=days)
    # 计算当前时间
    current_time = start_date + days_increment
    current_time = current_time.astimezone(tz=None).replace(tzinfo=None)  # 将时间转换为本地时区
    # print(f"当前时间：{current_time}")
    return current_time

def get_Beijing_time_from_UTC(start_date, days):
    '''
    Args:
        start_date: str, 如'2000-01-01 00:00:00'
        days: float,如7670.0625
    Returns:返回beijing时间
    '''
    current_time = get_UTC_time(start_date, days)
    current_time = current_time.astimezone(tz=None).replace(tzinfo=None)  # 将时间转换为本地时区
    print(f"当前时间：{current_time}")
    return current_time

def get_Beijing_time_from_UTC(utc_time):
    '''
    Args:
        start_date: datetime, 如2020-12-31 01:30:00+00:00
    Returns:返回beijing时间
    '''
    current_time = utc_time.astimezone(tz=None).replace(tzinfo=None)  # 将时间转换为本地时区
    print(f"当前时间：{current_time}")
    return current_time

def get_closest_date_index(datetime_list,given_time):
    '''
    Args:
        datetime_list:datetime 对象的集合
        given_time:给定的时间
    Returns:
    '''

    # 查找集合中最接近给定时间的元素的索引
    closest_index = min(range(len(datetime_list)), key=lambda i: abs(datetime_list[i] - given_time))
    return closest_index

def get_closest_hour_index(datetime_list,given_time):
    '''
    Args:
        datetime_list:datetime 对象的集合
        given_time:给定的时间
    Returns:
    '''
    # 查找集合中最接近给定时间的元素的索引
    closest_day_index = min(range(len(datetime_list)), key=lambda i: abs(datetime_list[i] - given_time))
    closest_date=datetime_list[closest_day_index]
    hours=[]
    for date in datetime_list:
        if date.year==closest_date.year and date.month==closest_date.month and date.day==closest_date.day:
            hours.append(date.hour)
    closest_hour_index = min(range(len(hours)), key=lambda i: abs(hours[i] - given_time.hour))
    if given_time.tzinfo is not None:
        closest_hour_date=datetime(closest_date.year,closest_date.month,closest_date.day,hours[closest_hour_index],closest_date.minute,tzinfo=given_time.tzinfo)
    else:
        closest_hour_date=datetime(closest_date.year,closest_date.month,closest_date.day,hours[closest_hour_index],closest_date.minute)    
    closest_index=datetime_list.index(closest_hour_date)
    return closest_index



def get_hour_of_year(date):
    '''
    @description: 获取指定日期属于当年第x个小时
    @param: date: 日期
    @return: 获取指定日期属于当年第x个小时
    @usage:
    '''  
    # 获取当年的第一天
    start_of_year = datetime(date.year, 1, 1)    
    # 计算给定日期与当年第一天之间的时间差
    time_difference = date - start_of_year    
    # 将时间差转换为小时数
    hours_of_year = time_difference.total_seconds() / 3600    
    # 加上当前日期的小时数
    hours_of_year += date.hour    
    return int(hours_of_year)


def get_days_in_month(month, year):
    '''
    @description: 获取指定月份的天数
    @param: month: 月份
    @param: year: 年份
    @return: 月份的天数
    @usage:
    print(get_days_in_month(2, 2021))  # 29
    print(get_days_in_month(4, 2021))  # 30
    '''
    return calendar.monthrange(year, month)[1]