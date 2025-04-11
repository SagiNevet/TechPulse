import streamlit as st

st.set_page_config(
    page_title="TechPulse – Product LifeCycle Analysis",
    page_icon="🚀"
)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pytrends.request import TrendReq
from zap_scraper import scrape_zap_search
from trends_scraper import scrape_google_trends
import numpy as np
from datetime import datetime

sns.set_theme()

#####################################
# Helper Functions
#####################################
def rating_to_stars(rating, max_stars=5):
    if rating is None:
        return "לא דורג"
    full_stars = int(rating)
    half_star = (rating - full_stars) >= 0.5
    stars_str = "★" * full_stars
    if half_star:
        stars_str += "½"
    empty_stars = max_stars - full_stars - (1 if half_star else 0)
    stars_str += "☆" * empty_stars
    return stars_str

def get_product_info(product_name):
    """
    מנסה לקבל מידע ממערכת זאפ עבור מוצר.
    מחזיר את התוצאה הראשונה שתואמת בדיוק, כלומר אם המחרוזת אינה כוללת "max" במידה ולא הוזנה.
    """
    results = scrape_zap_search(product_name, strict_filter=True)
    for res in results:
        title_lower = res['full_title'].lower()
        if product_name.lower() in title_lower:
            if "max" in title_lower and "max" not in product_name.lower():
                continue
            return res
    return None

#####################################
# Google Trends (pytrends) Functions
#####################################
def fetch_google_trends_data(keywords, timeframe='today 5-y', geo='US'):
    pytrend = TrendReq(hl='en-US', tz=360)
    pytrend.build_payload(kw_list=keywords, timeframe=timeframe, geo=geo)
    df_trends = pytrend.interest_over_time()
    if not df_trends.empty and 'isPartial' in df_trends.columns:
        df_trends.drop(labels=['isPartial'], axis='columns', inplace=True)
    return df_trends

def plot_trends_multi(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    for column in df.columns:
        ax.plot(df.index, df[column], label=column)
    ax.set_title("השוואת מגמות עבור מספר מוצרים")
    ax.set_xlabel("תאריך")
    ax.set_ylabel("רמת עניין (Google Trends)")
    ax.legend()
    ax.grid(True)
    fig.tight_layout()
    return fig

#####################################
# Lifecycle Analysis Functions
#####################################
def compute_lifecycle(df, threshold=20):
    """
    עבור כל מוצר (עמודה ב-df):
      - מוצאים את התאריך שבו הערך הממוצע (rolling window=3) מגיע לשיא (peak_date).
      - מחפשים את התאריך הראשון לאחר השיא שבו הערך נופל מתחת ל-threshold.
      - מחשבים את משך הזמן מהשיא עד ירידה זו.
    מחזיר מילון { מוצר: (peak_date, first_below_date, duration) }
    """
    results = {}
    for col in df.columns:
        series_rolled = df[col].rolling(window=3).mean()
        if series_rolled.empty:
            results[col] = None
            continue
        peak_date = series_rolled.idxmax()
        subsequent = series_rolled[peak_date:]
        below = subsequent < threshold
        if below.any():
            first_below = below.idxmax()
            lifecycle_duration = first_below - peak_date
            results[col] = (peak_date, first_below, lifecycle_duration)
        else:
            results[col] = None
    return results

def format_duration(td):
    """
    ממיר timedelta למחרוזת בפורמט: X שנים, Y חודשים, Z ימים.
    מתבסס על 365 ימים לשנה ו-30 ימים לחודש.
    """
    days = td.days
    years = days // 365
    rem = days % 365
    months = rem // 30
    days_left = rem % 30
    return f"{years} שנים, {months} חודשים, {days_left} ימים"

#####################################
# Tabs – Lifecycle Tab
#####################################
def lifecycle_tab():
    st.header("⏳Product Lifecycle Analysis")
    st.write("Write products you would like to analyze, for example: `iphone 12 pro, iphone 13 pro, iphone 14 pro`")
    product_query = st.text_input("Enter Product Names (seperated by comma)", "iphone 12 pro, iphone 13 pro, iphone 14 pro", key="lifecycle_query")
    
    timeframe_options = ["Last 5 Years", "Last 12 Months", "Last 3 Months", "Last 1 Month"]
    selected_timeframe = st.selectbox("Choose time range", options=timeframe_options, index=0, key="lifecycle_timeframe")
    
    geo_options = {"ארה\"ב (US)": "US", "ישראל (IL)": "IL", "בריטניה (GB)": "GB", "עולמי (אין קוד)": ""}
    selected_geo_label = st.selectbox("Choose location", list(geo_options.keys()), index=1, key="lifecycle_geo")
    selected_geo = geo_options[selected_geo_label]
    
    threshold = st.number_input("When is the product dying? (depending on company standard, interest rate)", value=20)
    
    if st.button("🧠Click To Start Analyzing Products", key="lifecycle_analyze"):
        with st.spinner("אוסף נתוני Google Trends..."):
            keywords = [k.strip() for k in product_query.split(",") if k.strip()]
            if not keywords:
                st.error("לא הוקלדו מוצרים.")
                return
            df = fetch_google_trends_data(keywords, timeframe=selected_timeframe, geo=selected_geo)
            if df.empty:
                st.error("לא נמצאו נתונים עבור המוצרים שהוזנו.")
                return
            
            st.subheader("גרף מגמות כולל")
            fig_multi = plot_trends_multi(df)
            st.pyplot(fig_multi)
            
            lifecycle_results = compute_lifecycle(df, threshold=threshold)
            
            st.subheader("ניתוח חיי מוצר לפי מוצר:")
            for product in keywords:
                st.markdown(f"### {product}")
                product_info = get_product_info(product)
                if product_info and product_info.get("image_url"):
                    st.image(product_info.get("image_url"), width=120)
                    st.write(f"**שם מלא:** {product_info.get('full_title')}")
                # הצגת דיאגרמה אישית למוצר אם קיימת עמודה
                if product in df.columns:
                    fig, ax = plt.subplots(figsize=(6, 3))
                    ax.plot(df.index, df[product], label=product)
                    ax.set_title(f"מגמת חיפוש עבור {product}")
                    ax.set_xlabel("תאריך")
                    ax.set_ylabel("רמת עניין")
                    ax.grid(True)
                    ax.legend()
                    st.pyplot(fig)
                res = lifecycle_results.get(product)
                if res is None:
                    st.write(f"לא נמצא תאריך שבו רמת העניין ירדה מתחת ל-{threshold}.")
                else:
                    peak_date, first_below, duration = res
                    formatted_duration = format_duration(duration)
                    st.write(f"**שיא:** {peak_date.strftime('%d/%m/%Y')}  |  **ירידה מתחת ל-{threshold}:** {first_below.strftime('%d/%m/%Y')}")
                    st.write(f"**חיי המוצר (מהשיא עד ירידה משמעותית):** {formatted_duration}")
                st.write("---")
            
            st.subheader("טבלת נתונים גלויה")
            st.dataframe(df)

#####################################
# Other Tabs (דוגמאות)
#####################################
def google_trends_tab_pytrends():
    st.header("📈 Google Trends (pytrends)")
    user_keywords = st.text_input("Enter Product Names (seperated by comma)", value="iPhone 13 Pro, iPhone 12 Pro", key="gt_keywords")
    keywords_list = [kw.strip() for kw in user_keywords.split(",") if kw.strip()]
    timeframe_options = ["Last 5 Years", "Last 12 Months", "Last 3 Months", "Last 1 Month"]
    selected_timeframe = st.selectbox("Choose time range", options=timeframe_options, index=0, key="gt_timeframe")
    geo_options = {"ארה\"ב (US)": "US", "ישראל (IL)": "IL", "בריטניה (GB)": "GB", "עולמי (אין קוד)": ""}
    selected_geo_label = st.selectbox("Choose location", list(geo_options.keys()), index=0, key="gt_geo")
    selected_geo = geo_options[selected_geo_label]
    if st.button("🧠 Click To Analyze", key="gt_compare"):
        if not keywords_list:
            st.error("נא להזין לפחות ביטוי אחד לחיפוש.")
        else:
            with st.spinner("טוען נתונים מ-Google Trends..."):
                trends_df = fetch_google_trends_data(keywords_list, timeframe=selected_timeframe, geo=selected_geo)
                if trends_df.empty:
                    st.error("לא הוחזרו נתונים.")
                else:
                    st.success("נתונים נטענו בהצלחה!")
                    fig = plot_trends_multi(trends_df)
                    st.pyplot(fig)
                    st.subheader("טבלת נתונים גלויה")
                    st.dataframe(trends_df)

def zap_search_tab():
    st.header("🔍 Zap Search")
    query = st.text_input("What would you like to search on Zap?", "iphone 12 pro", key="zap_query")
    if st.button("🔍 Click to search on Zap", key="zap_search"):
        with st.spinner("סורק את זאפ..."):
            results = scrape_zap_search(query)
            if not results:
                st.warning("לא נמצאו תוצאות או שהאתר שינה את המבנה.")
            else:
                st.success("סיימנו לסרוק בהצלחה!")
                for item in results:
                    st.markdown(f"**{item['full_title']}**")
                    if item.get("image_url"):
                        st.image(item.get("image_url"), width=120)
                    st.write(f"**דירוג:** {rating_to_stars(item['rating'])} ({item['rating_count']} חוות דעת)")
                    st.write(f"**טווח מחירים:** {item['price_range']}")
                    st.write(f"**חנויות:** {item['stores']}")
                    st.write("---")

def trends_scraper_tab():
    st.header("🕷️ Google Trends Scraper (Selenium)")
    user_query = st.text_input("Enter Product Names (seperated by comma)", "iphone 12 pro", key="ts_query")
    if st.button("🕷️Scan Google Trends (Using Selenium)", key="ts_scrape"):
        with st.spinner("מריץ דפדפן..."):
            data = scrape_google_trends(user_query)
            if not data:
                st.warning("לא הוחזרו נתונים או שה-HTML השתנה.")
            else:
                df = pd.DataFrame(data, columns=["תאריך", "ענין"])
                st.dataframe(df)

#####################################
# Main App: Tabs Interface
#####################################
def main():
    st.title("🚀TechPulse - Product LifeCycle⏳")
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈Google Trends (pytrends)", 
        "🔍Zap Search", 
        "🕷️Google Trends Scraper", 
        "⏳Product Lifecycle"
    ])
    with tab1:
        google_trends_tab_pytrends()
    with tab2:
        zap_search_tab()
    with tab3:
        trends_scraper_tab()
    with tab4:
        lifecycle_tab()

if __name__ == "__main__":
    main()
