import smtplib

my_email = "theunbakeablemuffin@gmail.com"
password = "geaujcngfvtniwyy"


class NotificationManager:

    def send_emails(self,message, google_flight_link):

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            for email in emails:
                connection.sendmail(
                    from_addr=my_email,
                    to_addrs="theunbakeablemuffin@yahoo.com",
                    msg=f"Subject:New Low Price Flight!\n\n{message}\n{google_flight_link}".encode('utf-8')
                                    )



