from datetime import datetime, timedelta

def subtract_five_days():
    """Subtract five days from the current date"""
    today = datetime.now()
    five_days_ago = today - timedelta(days=5)
    print("Task 1: Subtract five days from current date")
    print(f"Today: {today}")
    print(f"Five days ago: {five_days_ago}\n")


def print_yesterday_today_tomorrow():
    """Print yesterday, today, and tomorrow dates"""
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)
    
    print("Task 2: Yesterday, Today, Tomorrow")
    print(f"Yesterday: {yesterday}")
    print(f"Today: {today}")
    print(f"Tomorrow: {tomorrow}\n")


def drop_microseconds():
    """Drop microseconds from datetime"""
    now = datetime.now()
    without_microseconds = now.replace(microsecond=0)
    
    print("Task 3: Drop microseconds from datetime")
    print(f"Original datetime: {now}")
    print(f"Without microseconds: {without_microseconds}\n")


def calculate_date_difference_in_seconds():
    """Calculate the difference between two dates in seconds"""
    date1 = datetime(2026, 2, 28, 10, 30, 0)
    date2 = datetime(2026, 3, 7, 15, 45, 30)
    
    difference = date2 - date1
    difference_in_seconds = difference.total_seconds()
    
    print("Task 4: Calculate two date difference in seconds")
    print(f"Date 1: {date1}")
    print(f"Date 2: {date2}")
    print(f"Difference: {difference}")
    print(f"Difference in seconds: {difference_in_seconds}\n")

if __name__ == "__main__":
    subtract_five_days()
    print_yesterday_today_tomorrow()
    drop_microseconds()
    calculate_date_difference_in_seconds()
