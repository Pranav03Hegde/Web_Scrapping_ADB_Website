# 🌐 ADB Projects Web Scraper

A Python-based **web scraping application** that extracts structured project data from the **Asian Development Bank (ADB) Projects Portal**.  
Designed with a focus on **clean architecture, modularity, and real-world scraping practices**.

This project demonstrates how to build a maintainable scraper that handles pagination, detail-page enrichment, and common web scraping edge cases.

---

## ✨ Key Features

- Scrapes project listings from the ADB projects portal
- Supports **pagination** to collect data across multiple pages
- Visits **individual project detail pages** for enriched information
- Extracts:
  - Project Title
  - Country
  - Sector
  - Description
  - Project Status
  - Detail Page URL
- Gracefully handles:
  - Missing or optional fields
  - Network timeouts and request failures
  - End-of-pagination scenarios

---

## 🛠 Tech Stack

- **Python 3**
- **Requests** – HTTP requests and session handling
- **BeautifulSoup (bs4)** – HTML parsing
- **Typing module** – Improved readability and maintainability

---

## ⚙️ How It Works

1. Fetches the main ADB projects listing page
2. Parses project cards to extract basic metadata
3. Follows each project’s detail page
4. Extracts additional attributes like description and status
5. Iterates through paginated pages until no data remains
6. Aggregates all project data into structured Python dictionaries

---

## ▶️ Getting Started
```bash
pip install -r requirements.txt
python scraper.py
