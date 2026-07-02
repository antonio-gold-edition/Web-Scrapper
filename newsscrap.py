import requests
from bs4 import BeautifulSoup

NEWS_SITES = {
    "1": ("CNN", "https://edition.cnn.com"),
    "2": ("BBC", "https://www.bbc.com/news"),
    "3": ("NBC News", "https://www.nbcnews.com"),
    "4": ("IGN India", "https://in.ign.com"),
}

def scrape_headlines(url, site_name):
    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        headlines = []

        # CNN
        if site_name == "CNN":
            for tag in soup.select('[data-link-type="article"] span'):
                text = tag.get_text(strip=True)
                if len(text) > 20 and text not in headlines:
                    headlines.append(text)

        # BBC
        elif site_name == "BBC":
            for tag in soup.select("h2"):
                text = tag.get_text(strip=True)
                if len(text) > 20 and text not in headlines:
                    headlines.append(text)

        # NBC News
        elif site_name == "NBC News":
            for tag in soup.select("h2"):
                text = tag.get_text(strip=True)
                if len(text) > 20 and text not in headlines:
                    headlines.append(text)

        # IGN India
        elif site_name == "IGN India":
            blacklist = ["Follow IGN India"]

            for tag in soup.select("h3"):
                text = tag.get_text(strip=True)

                if (
                    len(text) > 15
                    and text not in headlines
                    and text not in blacklist
                ):
                    headlines.append(text)

        # Custom website
        else:
            for tag in soup.find_all(["h1", "h2", "h3"]):
                text = tag.get_text(strip=True)
                if len(text) > 15 and text not in headlines:
                    headlines.append(text)

        return headlines[:20]

    except Exception as e:
        print("Error:", e)
        return []

print("\nChoose a news site to scrape top headlines:")
print("1. CNN")
print("2. BBC")
print("3. NBC News")
print("4. IGN India")
print("5. Custom URL")

choice = input("\nEnter your choice (1-5): ")

if choice in NEWS_SITES:
    site_name, url = NEWS_SITES[choice]
elif choice == "5":
    site_name = "Custom Site"
    url = input("Enter website URL: ")
else:
    print("Invalid choice!")
    exit()

print(f"\nScraping headlines from {site_name}...")

headlines = scrape_headlines(url, site_name)

if headlines:
    filename = "headlines.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"Top Headlines from {site_name}\n")
        file.write("=" * 40 + "\n\n")

        for i, headline in enumerate(headlines, start=1):
            print(f"{i}. {headline}")
            file.write(f"{i}. {headline}\n")

    print(f"\nHeadlines saved to {filename}")
else:
    print("No headlines found.")