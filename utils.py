import re
import requests
import logging
import shutil
import random
from datetime import datetime, timedelta


class Utils:

    def has_pattern(self, text, pattern):
        match = re.search(pattern=pattern, string=text)
        if match:
            return True
        return False
    
    def download_image(self, img_link, img_name):
        """
            Download the image and saves in the directory
            'images/' with the filaname 'img_name'.
        """
        response = requests.get(img_link, stream=True)

        if response.status_code == 200:
            with open(f"images/{img_name}", "wb") as f:
                shutil.copyfileobj(response.raw, f)
                logging.info(f"Image {img_name} downloaded.")
    
    def create_img_filename(self, text):
        """
            This method get the parameter 'text' replaces spaces with
            underline, turn it to lower and return the first 100 caracteres.
        """
        if text.strip() is "":
            aleatory_img_code = "".join(
                [str(random.randint(0, 9)) for i in range(6)])
            return f"article_image_{aleatory_img_code}.jpg"
        
        return f"{text.replace(' ', '_').replace('...', '').lower()}.jpg"
    
    def process_date(self, date):
        """
            Return the date in the format Year-month-day
        """
        date = date.rstrip()
        try:
            return datetime.strptime(date, '%b %d, %Y').strftime("%Y-%m-%d")
        except:
            date = date.rstrip().split(" ")

            if "second" in date[1]:
                return (datetime.now() - timedelta(seconds=int(date[0]))) \
                        .strftime("%Y-%m-%d")
            elif "minute" in date[1]:
                return (datetime.now() - timedelta(minutes=int(date[0]))) \
                        .strftime("%Y-%m-%d")
            elif "hour" in date[1]:
                return (datetime.now() - timedelta(hours=int(date[0]))) \
                        .strftime("%Y-%m-%d")
            elif "day" in date[1]:
                return (datetime.now() - timedelta(days=int(date[0]))) \
                        .strftime("%Y-%m-%d")
            else:
                return ""
    
    def filter_by_date(self, number_of_months, data_date):
        limit = datetime.now().month - number_of_months

        if number_of_months == 0:
            if datetime.strptime(data_date, "%Y-%m-%d").month >= limit:
                return True
        else:
            if datetime.strptime(data_date, "%Y-%m-%d").month > limit:
                return True
        
        return False