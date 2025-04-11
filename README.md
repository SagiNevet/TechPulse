# 📊 TechPulse – Product Lifecycle & Trend Analyzer

**TechPulse** is a smart, interactive tool built with Streamlit for analyzing product lifecycles using real Google Trends data (via PyTrends and Selenium fallback), combined with real-time scraping from Zap.co.il for price, specs, and product interest.

---

## 🚀 Features

- 📈 Analyze product trends across 5+ years of Google search data
- ⚰️ Detect product “death” based on sharp interest drops
- 🛒 Scrape product info from Zap (name, image, rating, specs, etc.)
- 🎨 Visualize lifecycle curves via Matplotlib + Seaborn
---

## 🖼️ Demo Screenshot

![Screenshot 2025-04-10 at 13.28.38.png](<https://media-hosting.imagekit.io/60f8cba1e7d04e17/Screenshot%202025-04-10%20at%2013.28.38.png?Expires=1838995190&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=eC3Qo7ahWeiqN8ZvITQH8f3caFMZBUVG0kRob9-dNYJirRXV4yFFrryqF~EX-tNffYVk-bd1oNp9j2qG9Tnw7r0JK4AEgCBA3-QY5rzI9fXPcSBIk0XByJIe5HxF~MTbg2nwLHUHd4loqaCjTrhOiXZ7nER9CcX25izbtuS17~vtxf4cXVw0tS~Z7k8WpN9DHnN14d2Y0b~hh9K3Tfu7DTmxtwaFWOQJJy4K~P-E3esN0sPm1hnrAR5M414QdRoXejikLYbx~4KT07sY3dAf4YywFVUCySfC6i9CSKukuvpn4ECJmPkN0Y4y6y7dG~mViQPcNpJD9UOy5JY0JNMZ7w__>)



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
- Python 3

- Streamlit

- PyTrends

- Selenium

- BeautifulSoup

- Pandas / NumPy

- Matplotlib / Seaborn

# 🧩 Requirements
- Google Chrome must be installed

- Make sure ChromeDriver matches your local Chrome version

Expected path for driver:
```bash
/chromedriver-win64/chromedriver.exe
```
- If PyTrends fails with error 429 (too many requests), the app will automatically switch to Selenium scraping

- For Selenium scraping, ensure ChromeDriver opens a visible browser or update headless mode if needed

# 🚧 Roadmap
- Add country selector for localized trends

- Add Amazon/B&H scraping fallback

- Save & export lifecycle reports

 # 🙌 Contributions Welcome
Pull requests, ideas, and feature suggestions are more than welcome. Let’s improve TechPulse together!

