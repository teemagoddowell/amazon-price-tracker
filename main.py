import requests
import os
from bs4 import BeautifulSoup
import smtplib

# AUTHENTICATION
headers = {
    "User-Agent": "MMozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.5"
}

my_email = os.environ["EMAIL"]
password = os.environ["PASSWORD"]

# ASK FOR PRODUCT LINK, TARGET PRICE & RECIPIENT EMAIL
product_link = input("Paste the product link: ")
target_price = float(input("Enter Target Price: $"))
recipient_email = input("Your Email Address: ")

# SCRAPE AMAZON FOR CURRENT PRICE
try:
    response = requests.get(product_link, headers=headers)
    product_data = response.text
    soup = BeautifulSoup(product_data, "html.parser")
    product_price = float(soup.find(class_="a-offscreen").getText().strip("$"))
    product_title = soup.find(name="span", id="productTitle").getText().strip("       ")

except requests.exceptions.ConnectionError:
    print("No Internet Connection. Turn on WI-Fi and try again")


else:
    try:
        if product_price <= target_price:
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(user=my_email, password=password)
                connection.sendmail(
                from_addr=my_email,
                to_addrs=recipient_email,
                msg=f"Subject:Amazon Price Alert\n"
                    f"{product_title} is now ${product_price}\n"
                    f"Buy Now: {product_link}",
                )
                print("Message Sent")

    except smtplib.SMTPConnectError:
        print("Unable to Connect to SMTP Server. Try Again Later (Turn Off/On your VPN)")
