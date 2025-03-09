import os
import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import random
import re



categories = {
    "Technology": ["https://spectrum.ieee.org/", "https://www.technologyreview.com/", "https://arstechnica.com"],
    "Science": ["https://www.newscientist.com/", "https://phys.org/", "https://www.nature.com"],
    "Health": ["https://www.mayoclinic.org/", "https://www.nih.gov/", "https://www.statnews.com/"],
    "Finance": ["https://www.ft.com/", "https://www.wsj.com/", "https://www.cnbc.com/"],
    "Sports": ["https://theathletic.com/", "https://www.si.com/", "https://sports.yahoo.com/"],
    "Education": ["https://www.insidehighered.com/", "https://www.chronicle.com/", "https://www.edweek.org"],
    "Entertainment": ["https://ew.com/", "https://deadline.com/", "https://www.rollingstone.com"],
    "Gaming": ["https://www.pcgamer.com/", "https://kotaku.com/", "https://www.eurogamer.net/"],
    "Politics": ["https://www.theatlantic.com/", "https://foreignpolicy.com/", "https://www.bbc.com/news/politics"],
    "Travel": ["https://www.travelandleisure.com/", "https://www.nationalgeographic.com/travel", "https://www.cntraveler.com"],
    "Food": ["https://www.eater.com/", "https://www.cooksillustrated.com/", "https://www.seriouseats.com"],
    "Fashion": ["https://wwd.com/", "https://www.thecut.com/", "https://www.gq.com"],
    "Business": ["https://fortune.com/", "https://www.fastcompany.com/", "https://www.economist.com"],
    "Environment": ["https://e360.yale.edu/", "https://grist.org/", "https://www.theguardian.com/environment"],
    "AI and Machine Learning": ["https://www.artificialintelligence-news.com", "https://indiaai.gov.in", "https://aimagazine.com"],
    "Automobiles": ["https://www.caranddriver.com/", "https://www.roadandtrack.com/", "https://www.autoblog.com"],
    "Cryptocurrency": ["https://decrypt.co/", "https://www.blockchainnews.com/", "https://www.cryptonews.com"],
    "History": ["https://www.worldhistory.org", "https://www.historyextra.com/", "https://www.britishmuseum.org/research/british-museum-publications"],
    "Startups": ["https://news.crunchbase.com/", "https://sifted.eu/", "https://www.startupgrind.com"],
    "Cybersecurity": ["https://www.wired.com/category/security/", "https://techcrunch.com/category/security/", "https://www.krebsonsecurity.com"]
}



output_dir = "text_dataset"
os.makedirs(output_dir, exist_ok=True)

def clean_text(text):
    """Clean and normalize extracted text."""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s.,!?-]', '', text)  
    return text.strip()

def extract_text(url):
    """Extract text content from a webpage and clean it."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        text = ' '.join([p.get_text() for p in soup.find_all('p')])
        cleaned_text = clean_text(text)
        return cleaned_text if len(cleaned_text) > 250 else None  
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return None

def get_internal_links(base_url):
    """Fetch internal links from a given website."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(base_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        links = set()
        for link in soup.find_all('a', href=True):
            full_url = urljoin(base_url, link['href'])
            if base_url in full_url:
                links.add(full_url)
        return list(links)[:5] 
    except Exception as e:
        print(f"Error fetching links from {base_url}: {e}")
        return []



for category, websites in categories.items():
    text_file_path = os.path.join(output_dir, f"{category}.txt")
    with open(text_file_path, 'w', encoding='utf-8') as f:
        for website in websites:
            links = get_internal_links(website)
            for link in links:
                print(f"Crawling: {link}")
                text = extract_text(link)
                if text:
                    f.write(text+'\n\n')
                time.sleep(random.uniform(1, 3)) 
    print(f"Completed {category}")


print("Text dataset collection completed!")
