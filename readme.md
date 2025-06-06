# 🛍️ Django Price Comparison App

<img src="">

A Django-based web application that allows users to search for electronic gadgets and compares prices across major e-commerce platforms including **Amazon**, **Flipkart**, **Gadget Snow**, **Reliance Digital**, and **Croma**. The app also stores search results into a database for **historical tracking** and **later reference**.

## 🚀 Features

- 🔍 **Product Search**: Enter a product name and compare prices from multiple retailers.
- 🛒 **Retailers Included**:
  - Amazon
  - Flipkart
  - Gadget Snow
  - Reliance Digital
  - Croma
- 💾 **Data Persistence**: Stores product title, price, and source store in a database.
- 📜 **Search History**: View previous searches and compare how prices have changed over time.
- 🧼 **Clean & Simple UI** using Django templates.

---

## 🧰 Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS (Django Templates)
- **Database**: SQLite (default), can be upgraded to PostgreSQL
- **Web Scraping/APIs**: BeautifulSoup, Requests, or platform-specific APIs (if available)

---

## 🛠️ Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your-username/django-price-compare.git
   cd django-price-compare


2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt


3. **Start the development server**:
    ```bash
    python manage.py runserver


## 🔎 How It Works

1. **User Input**:  
   The user enters a product name (e.g., `iPhone 15`) into the search bar.

2. **Data Collection via Web Scraping**:  
   The backend uses **Selenium** to automate a headless browser that performs real-time scraping from the following retailers:
   - 🛒 **Amazon**
   - 🛒 **Flipkart**
   - 🛒 **Gadget Snow**
   - 🛒 **Reliance Digital**
   - 🛒 **Croma**

3. **Scraped Data Includes**:
   - 📌 **Product Title**
   - 💲 **Price**
   - 🏬 **Store Name**
   - 🔗 **Product URL** (optional)

4. **Data Storage**:
   - All search results are stored in the database (e.g., SQLite or PostgreSQL) along with a **timestamp**.
   - If the same product is searched again, the app records new entries for comparison over time.

5. **Search History**:
   - Users can view their previous searches.
   - Historical price data is available to observe **price fluctuations** across different retailers.

6. **Display**:
   - Results are displayed in a table format with product details and pricing from each store.
   - If a product is not found on a specific platform, it will be marked accordingly.