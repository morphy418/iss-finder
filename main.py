import requests
from datetime import datetime
import smtplib
import time

MY_EMAIL = ""
MY_PASSWORD = ""

MY_LAT = 51.499630
MY_LONG = -0.035400


def is_iss_in_range():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])

    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True

def is_it_dark():
    is_iss_in_range()

    parameters = {
        "lat": MY_LAT,
        "long": MY_LONG,
        "formatted": 0
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()

    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now > sunset or time_now < sunrise:
        return True

while True:
    time.sleep(60)
    if is_iss_in_range() and is_it_dark():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg="Subject:Look UP ☝️\n\nThe ISS is above you in the sky."
            )

    else:
        print("ISS is not visible")