# Complete the function below.

def NumDaysBetween(year1, month1, day1, year2, month2, day2):
    # Compute the day offset:
    num_days = day2 - day1
    
    # Compute the month/year offset:
    while year1 < year2 or (year1 == year2 and month1 < month2):
        num_days += DaysInMonth(month1, year1)
        month1 += 1
        if month1 > 12:
            month1 = 1
            year1 += 1
    return num_days
    
#Do not edit below this line. It is only shown so you can see the function signature.
#The implementation of the function is hidden.
def DaysInMonth(month, year):
