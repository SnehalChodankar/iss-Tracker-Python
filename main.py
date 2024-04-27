import datetime
import smtplib

import requests
import time

MY_LAT = 15.645460
MY_LONG = 73.828030

MY_EMAIL = "snehalchodankar357@gmail.com"
PASSWORD = "chiyuicppmxfkyzt"


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    data = response.json()

    longitude = float(data["iss_position"]["longitude"])
    latitude = float(data["iss_position"]["latitude"])

    iss_pos = (latitude, longitude)

    print(iss_pos)
    if (MY_LAT - 5) <= latitude <= (MY_LAT + 5) and (MY_LONG - 5) <= longitude <= (MY_LONG + 5):
        return True


def is_night():
    # Get Sunrise, Sunset times
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0
    }

    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()

    data = response.json()
    sunrise = data["results"]["sunrise"]
    sunset = data["results"]["sunset"]

    sunrise = sunrise.split("T")[1]
    sunrise = sunrise.split(":")[0]

    sunset = sunset.split("T")[1]
    sunset = sunset.split(":")[0]

    print(sunrise, sunset)

    time_now = datetime.datetime.now()
    print(time_now.hour)

    if time_now.hour >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL,
                                to_addrs="snehalchodankar955@gmail.com",
                                msg=f"Subject:Look Up\n\nThe Iss is above your head!!!")
