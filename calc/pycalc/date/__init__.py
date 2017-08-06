"""Date class for time calculations
Possibly have array of special events in history?"""

import sys
sys.path.append("..")

from complexdecimal import ComplexDecimal
import re, datetime, math, time


class Date(object):
    def __init__(self,date=""):
        if type(date) == str:
            date = date.replace(")","").replace("(","").replace("ComplexDecimal","").replace("'","")
            
            date = date.replace("-","/")
            now = datetime.datetime.now()
            date_copy = date
        
            #Attempt to match hours, minutes, seconds, milliseconds
            hour = minute = second = millis = 0
            
            result1 = re.findall("(-?\d+):(-?\d+):(-?\d+):(-?\d+)",date)
            if len(result1) > 0:
                hour = int(result1[0][0])
                minute = int(result1[0][1])
                second = int(result1[0][2])
                millis = int(result1[0][3])
                date = date.replace(result1[0][0]+":"+result1[0][1]+":"+result1[0][2]+":"+result1[0][3], "")
            else:
                result2 = re.findall("(-?\d+):(-?\d+):(-?\d+)",date)
                if len(result2) > 0:
                    hour = int(result2[0][0])
                    minute = int(result2[0][1])
                    second = int(result2[0][2])
                    date = date.replace(result2[0][0]+":"+result2[0][1]+":"+result2[0][2], "")
                else:
                    result3 = re.findall("(-?\d+):(-?\d+)",date)
                    if len(result3) > 0:
                        hour = int(result3[0][0])
                        minute = int(result3[0][1])
                        date = date.replace(result3[0][0]+":"+result3[0][1], "")
                    elif date == "":
                        hour = now.hour
                        minute = now.minute
                        second = now.second
                        millis = 0
            if "pm" in date.lower(): hour += 12
            
            #Guess the year, month and day
            year = now.year
            month = now.month
            day = now.day
            
            #Detect full year string
            foundYear = False
            result = re.findall("(-?\d+)",date)
            for i in result:
                if int(i) > 10000000: 
                    i = int(i)
                    year, month = int(math.floor(i/10000)), int(math.floor((i - year*10000)/100))
                    day = i - year*10000 - month*100
                    foundYear = True
            
            #Detect year, month and day
            if not foundYear:
                result = re.findall("(-?\\d+)[/-\\\\](-?\\d+)[/-\\\\](-?\\d+)",date)
                if len(result) > 0:
                    y, m, d = int(result[0][0]),int(result[0][1]),int(result[0][2])
                    if d > 100:
                        y, d = d, y #Swap year and day if day = year
                    if m > 12 and d <= 12:
                        m, d = d,y
                    foundYear= True
                    year, month, day = y,m,d
                        
            #Detect just month and day, for example 9/11. Default to month-day unless it contradicts logic
            if not foundYear:
                result = re.findall("(-?\\d+)[/-\\\\](-?\\d+)",date)
                if len(result) > 0:
                    month = int(result[0][1])
                    day = int(result[0][0])
                    if month > 12 and day <= 12:
                        month, day = day, month
                        foundYear = True
            try: 
                a = datetime.datetime.fromtimestamp(int(date_copy))
                hour = a.hour
                minute = a.minute
                second = a.second
                day = a.day
                month = a.month
                year = a.year
            except: pass
            
            month, day, year = abs(month), abs(day), abs(year)
            
            if year <= 0: raise ArithmeticError("Invalid date: year must be 1 or higher")
            elif month < 1 or month > 12: raise ArithmeticError("Invalid date: month must be within range 1-12")
            elif day < 1 or day > 31: raise ArithmeticError("Invalid date: day must be within range 1-31")
            
            elif hour > 23 or hour < 0: raise ArithmeticError("Invalid date: hour must be within range 0-23")
            elif minute > 59 or minute < 0: raise ArithmeticError("Invalid date: minute must be within range 0-59")
            elif second > 59 or second < 0: raise ArithmeticError("Invalid date: second must be within range 0-59")
            elif hour > 999 or hour < 0: raise ArithmeticError("Invalid date: millis must be within range 0-999")
            
            self.hour, self.minute, self.second, self.millis = hour, minute, second, millis
            self.year, self.month, self.day = year, month, day
    
    def to_datetime(self):
        return datetime.datetime(self.year, self.month, self.day, self.hour, self.minute, self.second)
    def from_datetime(self,d):
        return Date(str(d))
        
    #Override functions
    def __str__(self):
        return "{}-{}-{} {}:{}:{}:{}".format(self.year,str(self.month).zfill(2),str(self.day).zfill(2),str(self.hour).zfill(2),str(self.minute).zfill(2),str(self.second).zfill(2),str(self.millis).zfill(3))
    
    def __sub__(self,other):
        return ComplexDecimal( abs((other.to_datetime() - self.to_datetime()).total_seconds()) )
        
    #Replace
    def weekday(self):
        return ["Monday","Tuesday","Wensday","Thursday","Friday","Saturday","Sunday"][self.to_datetime().weekday()]
        
    def leap_year(self):
        if (self.year % 4 == 0 and self.year % 100 != 0) or (self.year % 100 == 0 and self.year % 400 == 0): return True
        return False
        
    def unix_time(self):
        try: return time.mktime(self.to_datetime().timetuple())
        except: raise ArithmeticError("Year out of range for UNIX time")
        
    def ctime(self):
        try: return time.mktime(self.to_datetime().timetuple())
        except: raise ArithmeticError("Year out of range for UNIX time")
