import requests
from bs4 import BeautifulSoup
import time
import re

def scrape_zap_search(query, strict_filter=True):
    """
    מבצע חיפוש בזאפ לפי מילת החיפוש query (למשל 'iphone 12 pro')
    ומחזיר רשימת תוצאות המכילות:
      - מזהה הדגם (data-model-id)
      - שם המוצר המלא (כולל מותג)
      - כתובת תמונת המוצר (image_url)
      - פרמטרים (כגון: גודל מסך, נפח אחסון וכו')
      - טווח מחירים
      - מספר חנויות
      - דירוג (כוכבים) ומספר חוות דעת
      
    אם strict_filter=True, יוחזרו רק תוצאות שבהן full_title מכיל את המחרוזת של query (case-insensitive)
    וגם נוודא שלא מופיעה מילה "max" אם לא הוזנה בקלט.
    """
    base_url = "https://www.zap.co.il/search.aspx"
    params = {"keyword": query}
    
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/111.0.0.0 Safari/537.36"
        )
    }
    
    response = requests.get(base_url, params=params, headers=headers, timeout=15)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "html.parser")
    search_results_div = soup.find("div", id="divSearchResults")
    if not search_results_div:
        return []
    
    product_blocks = search_results_div.find_all("div", class_="withModelRow")
    data_list = []
    
    for block in product_blocks:
        model_id = block.get("data-model-id", "").strip()
        
        model_title_a = block.find("a", class_="ModelTitle")
        if not model_title_a:
            continue
        full_title = model_title_a.get_text(" ", strip=True)
        brand_span = model_title_a.find("span", class_="brand")
        brand = brand_span.get_text(strip=True) if brand_span else ""
        
        # ניסיון לשלוף כתובת תמונה מתכונות שונות
        model_pic_a = block.find("a", class_="ModelPic")
        img_tag = model_pic_a.find("img") if model_pic_a else None
        image_url = None
        if img_tag:
            for attr in ["data-src", "data-original", "src"]:
                if img_tag.has_attr(attr):
                    image_url = img_tag[attr]
                    break
        
        param_wrapper = block.find("div", class_="param-wrapper")
        param_data = {}
        if param_wrapper:
            rows = param_wrapper.find_all("div", class_="ParamRow")
            for row in rows:
                param_label = row.contents[0]
                param_value_tag = row.find("div", class_="ParamValue")
                param_value = param_value_tag.get_text(strip=True) if param_value_tag else ""
                param_value = param_value.rstrip(",")
                param_data[param_label.replace(":", "").strip()] = param_value
        
        price_wrapper = block.find("div", class_="price-wrapper")
        if price_wrapper:
            price_span = price_wrapper.find("span")
            price_text = price_span.get_text(strip=True) if price_span else ""
        else:
            price_text = "לא זמין"
        
        stores_div = block.find("div", class_="Stores")
        stores_text = stores_div.get_text(strip=True) if stores_div else ""
        
        rate_wrap = block.find("div", class_="rate-wrap")
        rating_stars = None
        rating_count = None
        if rate_wrap:
            rating_stars_div = rate_wrap.find("div", class_="RatingStars")
            if rating_stars_div and rating_stars_div.has_attr("title"):
                title_text = rating_stars_div["title"]
                match_rating = re.search(r"([\d.]+)\s+מתוך 5", title_text)
                if match_rating:
                    rating_stars = float(match_rating.group(1))
            rating_num_div = rate_wrap.find("div", class_="RateNum")
            if rating_num_div:
                rating_count_text = rating_num_div.get_text(strip=True)
                match_count = re.search(r"(\d+)\s*חוות\s*דעת", rating_count_text)
                if match_count:
                    rating_count = int(match_count.group(1))
        
        product_info = {
            "model_id": model_id,
            "brand": brand,
            "full_title": full_title,
            "image_url": image_url,
            "params": param_data,
            "price_range": price_text,
            "stores": stores_text,
            "rating": rating_stars,
            "rating_count": rating_count
        }
        data_list.append(product_info)
    
    time.sleep(2)
    
    if strict_filter:
        q_lower = query.lower().strip()
        filtered = []
        for item in data_list:
            title = item["full_title"].lower()
            # נבדוק שהקלט מופיע ושאין מילה "max" בתוצאה אם לא הוזנה
            if q_lower in title:
                if "max" in title and "max" not in q_lower:
                    continue
                filtered.append(item)
        data_list = filtered
    return data_list

if __name__ == "__main__":
    results = scrape_zap_search("iphone 12 pro", strict_filter=True)
    print(f"נמצאו {len(results)} תוצאות.")
    for i, r in enumerate(results, start=1):
        print(f"{i}. {r['full_title']}")
