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

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/TechPulse.git
cd TechPulse

# Create virtual environment
python3 -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
