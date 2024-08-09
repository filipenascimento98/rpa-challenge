from robocorp.tasks import task
from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
from datetime import timedelta, datetime
from selenium.webdriver.common.by import By
from utils import Utils

browser = Selenium()
excel = Files()


#Parameters
search_phrase = "Olympics"
category = 'PHOTO GALLERIES'
number_of_months = 3

@task
def minimal_task():
    utils= Utils()

    #Open browser and set an wait to load elements on page
    browser.open_available_browser("https://www.aljazeera.com/")
    browser.set_browser_implicit_wait(timedelta(seconds=10))

    # Click on button search
    browser.click_element_when_clickable("xpath://button[@class='no-styles-button' and @type='button']")

    # Input the search phrase on the search field
    browser.input_text_when_element_is_visible("xpath://input[@class='search-bar__input' and @type='text' and @title='Type search term here']", search_phrase)

    # Submit the search phrase
    browser.click_element_when_clickable("xpath://button[@class='css-sp7gd' and @type='submit']")

    # Sort by most recentes articles
    browser.click_element_when_visible("xpath://option[text()='Date']")

    # Show all articles hidden
    while browser.is_element_visible("xpath://button[@class='show-more-button grid-full-width']"):
        browser.click_element_when_clickable("xpath://button[@class='show-more-button grid-full-width']")
    
    # Get all articles from search
    articles = browser.find_elements("xpath://article[@class='gc u-clickable-card gc--type-customsearch#result gc--list gc--with-image']")

    # Create an excel file
    worksheet_name = "articles"
    excel_filename = f"data_{datetime.strftime(datetime.now(), '%Y-%m-%d_%H:%M:%S')}.xlsx"
    excel.create_workbook(path=excel_filename, sheet_name=worksheet_name)

    titles = []
    descriptions = []
    dates = []
    all_count_search_phrases = []
    all_picture_file_name= []
    all_contains_amount_money = []

    # Get informations about each article and put in an excel file
    for article in articles:
        body_desc = article.find_element(By.CLASS_NAME, "gc__excerpt").text.split("...", 1)
        date = utils.process_date(body_desc[0])

        if utils.filter_by_date(number_of_months, date):
            description = body_desc[1]
            title = article.find_element(By.CLASS_NAME, "gc__title").text
            count_search_phrases = title.lower().count(search_phrase.lower()) \
                                + description.lower().count(search_phrase.lower())
            
            # Search for the pattern described by regex in the title and description
            contains_amount_money = utils.has_pattern(title+description, "\$\d{2}\.\d{1}|\$\d{3},\d{3}\.\d{2}|\d{2} dollars|\d{2} USD")

            # Download the image's article
            img = article.find_element(By.CLASS_NAME, "article-card__image")

            # The original picture filename is encrypted,
            # so the solution is use the article's title.
            picture_file_name = utils.create_img_filename(title)
            utils.download_image(img.get_dom_attribute("src"), 
                                picture_file_name)

            titles.append(title)
            dates.append(date)
            descriptions.append(description)
            all_picture_file_name.append(picture_file_name)
            all_count_search_phrases.append(count_search_phrases)
            all_contains_amount_money.append(str(contains_amount_money))
        

    data = {
        "title": titles,
        "date": dates,
        "description": descriptions,
        "picture_filename": all_picture_file_name,
        "count_search_phrase": all_count_search_phrases,
        "contains_amount_money": all_contains_amount_money,
    }
    excel.append_rows_to_worksheet(content=data, 
                                       name=worksheet_name, 
                                       header=True)
    excel.save_workbook(path=excel_filename)





    # browser.open_available_browser("https://apnews.com/")

    # browser.alert_should_not_be_present()
    # browser.click_element_when_clickable("class:SearchOverlay-search-button")
    # browser.input_text_when_element_is_visible("class:SearchOverlay-search-input", "Olympics")
    # browser.click_element_when_clickable("class:SearchOverlay-search-submit")
    # browser.click_element_when_clickable("class:SearchFilter-content")
    # browser.click_element_when_clickable("class:SearchFilter-seeAll-button")

    # checkboxes = browser.find_elements("name:f2")

    # for checkbox in checkboxes:
    #     if checkbox.accessible_name == category:
    #         print("Achou")
    #         checkbox.click()
    #         break
    
    # browser.click_element_when_clickable("class:Select-input")
    # browser.click_element_when_visible("xpath://option[text()='Newest']")
    # print("teste")