import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

# Get institute websites from Google search
def get_institutes_by_state(state):
    query = f"top life science research institutes in {state} India site:.ac.in"
    headers = {"User-Agent": "Mozilla/5.0"}
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

    try:
        response = requests.get(search_url, headers=headers, timeout=10)
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
    except Exception as e:
        print(f"[Error] Google Search failed for {state}: {e}")
        return []

# Extract personnel from faculty/team/staff page
def extract_personnel_from_website(base_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(base_url, timeout=10, headers=headers)
        soup = BeautifulSoup(resp.text, "html.parser")
        all_links = soup.find_all("a", href=True)

        keywords = ["faculty", "team", "people", "staff", "researchers"]
        people_page = None

        # Find potential staff/faculty page
        for link in all_links:
            href = link['href'].lower()
            if any(k in href for k in keywords):
                people_page = urljoin(base_url, href)
                break

        if not people_page:
            return []

        team_resp = requests.get(people_page, headers=headers, timeout=10)
        team_soup = BeautifulSoup(team_resp.text, "html.parser")
        text = team_soup.get_text(separator=" ")

        # Extract emails and names (simplified)
        emails = list(set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)))
        names = list(set(re.findall(r"(?:Dr\.|Prof\.)\s+[A-Z][a-z]+\s+[A-Z][a-z]+", text)))

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
        print(f"[Error] Failed to extract from {base_url}: {e}")
        return []
