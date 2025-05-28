import requests
from bs4 import BeautifulSoup

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
