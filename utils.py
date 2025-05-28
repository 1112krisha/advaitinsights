import requests
from bs4 import BeautifulSoup
import re

def get_institutes_by_state(state):
    query = f"top life science research institutes in {state} India site:.ac.in"
    headers = {"User-Agent": "Mozilla/5.0"}
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    institutes = []
    for link in soup.find_all("a"):
        href = link.get("href", "")
        if "/url?q=" in href and ".ac.in" in href:
            url = href.split("/url?q=")[-1].split("&")[0]
            if url not in institutes:
                institutes.append(url)
        if len(institutes) >= 5:
            break

    return institutes


def extract_personnel_from_website(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, timeout=10, headers=headers)
        soup = BeautifulSoup(resp.text, "html.parser")
        all_links = soup.find_all("a", href=True)

        # Try to find a faculty/team/people/staff page
        keywords = ["faculty", "team", "people", "staff", "researchers"]
        people_page = None

        for link in all_links:
            href = link['href'].lower()
            if any(k in href for k in keywords):
                if href.startswith("http"):
                    people_page = href
                elif href.startswith("/"):
                    people_page = url.rstrip("/") + href
                else:
                    people_page = url.rstrip("/") + "/" + href
                break

        if not people_page:
            return []

        team_resp = requests.get(people_page, headers=headers, timeout=10)
        team_soup = BeautifulSoup(team_resp.text, "html.parser")
        text = team_soup.get_text()

        emails = list(set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)))
        names = list(set(re.findall(r"Dr\.?\s+[A-Z][a-z]+\s+[A-Z][a-z]+", text)))

        personnel = []
        for i in range(min(len(emails), len(names))):
            personnel.append({
                "name": names[i],
                "email": emails[i],
                "designation": "Faculty/Researcher",
                "profile_link": people_page
            })

        return personnel

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return []
