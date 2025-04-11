# 📊 TechPulse – Product Lifecycle & Trend Analyzer

**TechPulse** is a smart, interactive tool built with Streamlit for analyzing product lifecycles using real Google Trends data (via PyTrends and Selenium fallback), combined with real-time scraping from Zap.co.il for price, specs, and product interest.

---

## 🚀 Features

- 📈 Analyze product trends across 5+ years of Google search data
- ⚰️ Detect product “death” based on sharp interest drops
- 🛒 Scrape product info from Zap (name, image, rating, specs, etc.)
- 🎨 Visualize lifecycle curves via Matplotlib + Seaborn
---

## 🖼 Demo Screenshot

![TechPulse UI Demo](https://ibb.co/pv4MCdQB)

---

## 🛠 Setup & Run


# Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/TechPulse.git
cd TechPulse
```

# Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```
# Install dependencies
```bash
pip install -r requirements.txt
```
# Run the app
```bash
streamlit run app.py
```

# 💡 Technologies Used
Python 3

Streamlit

PyTrends

Selenium

BeautifulSoup

Pandas / NumPy

Matplotlib / Seaborn

# 🧩 Requirements
Google Chrome must be installed

Make sure ChromeDriver matches your local Chrome version

Expected path for driver:
```bash
/chromedriver-win64/chromedriver.exe
```
If PyTrends fails with error 429 (too many requests), the app will automatically switch to Selenium scraping

For Selenium scraping, ensure ChromeDriver opens a visible browser or update headless mode if needed

# 🚧 Roadmap
 Add country selector for localized trends

 Add Amazon/B&H scraping fallback

 Save & export lifecycle reports

 # 🙌 Contributions Welcome
Pull requests, ideas, and feature suggestions are more than welcome. Let’s improve TechPulse together!

