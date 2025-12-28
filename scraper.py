import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from config import BASE_URL, HEADERS, REQUEST_TIMEOUT


def fetch_page(url: str) -> Optional[str]:
    """
    Fetches HTML content of a page.
    Returns HTML as string if successful, else None.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return None


def parse_project_list(html: str) -> List[Dict]:
    """
    Parses the main projects listing page and extracts
    basic project information and detail page URLs.
    """
    soup = BeautifulSoup(html, "html.parser")
    projects = []

    project_cards = soup.select("div.views-row")

    for card in project_cards:
        title_tag = card.select_one("h3 a")
        country_tag = card.select_one(".field-name-field-country")
        sector_tag = card.select_one(".field-name-field-sector")

        project = {
            "title": title_tag.get_text(strip=True) if title_tag else None,
            "country": country_tag.get_text(strip=True) if country_tag else None,
            "sector": sector_tag.get_text(strip=True) if sector_tag else None,
            "detail_url": (
                "https://www.adb.org" + title_tag["href"]
                if title_tag and title_tag.has_attr("href")
                else None
            )
        }
        projects.append(project)

    return projects


def parse_project_detail(html: str) -> Dict:
    """
    Parses an individual project detail page and extracts
    additional attributes such as description and status.
    """
    soup = BeautifulSoup(html, "html.parser")

    description_tag = soup.select_one("div.field-name-body")
    status_tag = soup.select_one(".field-name-field-project-status")

    return {
        "description": description_tag.get_text(strip=True) if description_tag else None,
        "status": status_tag.get_text(strip=True) if status_tag else None
    }


def scrape_all_projects() -> List[Dict]:
    """
    Orchestrates scraping of all projects including pagination
    and individual project detail enrichment.
    """
    all_projects = []
    page_number = 0

    while True:
        page_url = f"{BASE_URL}?page={page_number}"
        html = fetch_page(page_url)

        if not html:
            break

        projects = parse_project_list(html)

        if not projects:
            break

        for project in projects:
            if project.get("detail_url"):
                detail_html = fetch_page(project["detail_url"])
                if detail_html:
                    project.update(parse_project_detail(detail_html))

            all_projects.append(project)

        page_number += 1

    return all_projects


if __name__ == "__main__":
    """
    Entry point of the scraper.
    In a real environment, this would persist data to a file or database.
    """
    projects_data = scrape_all_projects()
    print(f"Total projects extracted: {len(projects_data)}")
