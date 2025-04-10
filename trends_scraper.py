import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def scrape_google_trends(queries="iphone 12 pro", 
                         timeframe="today 5-y", 
                         geo="IL",
                         gprop="froogle", 
                         lang="iw",
                         chrome_driver_path=r"C:\Users\i9\Desktop\All projects\TechPulse\chrome-win64\chromedriver.exe"):
    """
    סקרייפר של Google Trends באמצעות Selenium.
    ניתן להזין רשימת חיפושים, מופרדים בפסיק, להשוואה.
    המונח הראשון משמש כחיפוש הראשי, וכל מונח נוסף מתווסף באמצעות לחיצה על כפתור "הוסף מונח להשוואה".
    לאחר מכן, הקוד מחפש טבלה עם הנתונים ומחזיר רשימה של tuples: (תאריך, ענין).

    שימו לב:
      - הקוד משתמש ב-Chrome Headless.
      - הנתיב ל‑chromedriver מועבר דרך chrome_driver_path, ויש לכלול את שם הקובץ (chromedriver.exe).
    """
    # פילוח רשימת המונחים
    terms = [term.strip() for term in queries.split(",") if term.strip()]
    if not terms:
        return []
    
    first_query = terms[0]
    query_param = first_query.replace(" ", "%20")
    base_url = (
        f"https://trends.google.com/trends/explore"
        f"?date={timeframe}&geo={geo}&gprop={gprop}&hl={lang}"
        f"&q={query_param}"
    )
    print(f"Opening Google Trends URL:\n {base_url}")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.get(base_url)
    time.sleep(5)
    
    for term in terms[1:]:
        try:
            add_term_button = driver.find_element(By.XPATH, '//span[contains(text(), "הוסף מונח להשוואה")]')
            add_term_button.click()
            time.sleep(2)
            
            new_search_box = driver.find_element(By.ID, "input-99")
            new_search_box.clear()
            new_search_box.send_keys(term)
            time.sleep(1)
            new_search_box.send_keys(Keys.ENTER)
            time.sleep(5)
        except Exception as e:
            print("לא נמצאה אפשרות להוסיף מונח להשוואה או שהקלט כבר קיים:", e)
    
    data = []
    try:
        table_div = driver.find_element(By.XPATH, '//div[@aria-label="A tabular representation of the data in the chart."]')
        table = table_div.find_element(By.TAG_NAME, 'table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        for row in rows[1:]:
            cols = row.find_elements(By.TAG_NAME, 'td')
            if len(cols) >= 2:
                date_val = cols[0].text
                interest_val = cols[1].text
                data.append((date_val, interest_val))
    except Exception as e:
        print("Could not parse the trends table:", e)
    
    driver.quit()
    return data

if __name__ == "__main__":
    results = scrape_google_trends("iphone 12 pro, iphone 13 pro", chrome_driver_path=r"C:\Users\i9\Desktop\All projects\TechPulse\chrome-win64\chromedriver.exe")
    print("Found rows:", len(results))
    for row in results[:10]:
        print(row)
