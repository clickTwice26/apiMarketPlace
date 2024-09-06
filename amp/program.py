from datetime import datetime
import pytz
import random
import string
import uuid
from wtforms.validators import email


def cTime(timeType : str = "both"): # returns current time
        dhaka_tz = pytz.timezone('Asia/Dhaka')

        now = datetime.now(dhaka_tz)
        dt_string = now.strftime("%d/%m/%y %H:%M:%S").split(" ")

        if timeType == "date":
            return dt_string[0]
        elif timeType == "time":
            return dt_string[1]
        else:
            return " ".join(dt_string)
def newUsernameGenerator(emailAddress : str, fullName : str):
    emailAddress.replace("@", '')
    fullName.replace(" ", '')
    # print(string.digits)
    characters = string.ascii_letters + string.digits + '.' + emailAddress + fullName
    username = ''.join(random.choice(characters) for _ in range(10))
    return username
def tokenGen(type : str = "login"):
    if type == "login":
        return str(uuid.uuid4())
if __name__ == "__main__":
    print(cTime())
    print(newUsernameGenerator("hello@gmail.com", "john doe"))