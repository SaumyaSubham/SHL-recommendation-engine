import requests
from bs4 import BeautifulSoup

def get_length(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        text_element = soup.select_one("body > main > div.product-catalogue.module > div > div:nth-child(2) > div.col-12.col-md-8 > div > div:nth-child(4) > p")
        if text_element:
            text = text_element.text
            return int("".join(filter(lambda x: x.isdigit(), text)).replace(" ", ""))
        else:
            return None  # Or some other indicator that length couldn't be found
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        return None

def do_stuff(file, soup):
    table = soup.find("table")
    if table is None:
        print("No table found on this page")
        return

    for job in table.find_all("tr"):
        if job is None:
            continue

        job_cols = job.find_all("td")

        if len(job_cols) == 4:  # Ensure there are exactly 4 data columns
            try:
                name = job_cols[0].text.strip()
                link_tag = job_cols[0].find("a")
                link = "https://www.shl.com" + link_tag.get("href") if link_tag and link_tag.get("href") else ""
                remote = job_cols[1].find("span", {"class": "-yes"}) is not None
                irt = job_cols[2].find("span", {"class": "-yes"}) is not None
                ttype = job_cols[3].text.strip().replace("\n", "").lower()
                length = get_length(link)

                file.write(f"{name}, {remote}, {irt}, {ttype}, {link}, {length}\n")
            except Exception as e:
                print(f"Error processing row: {job_cols} - {e}")

def extract():
    with open("updated_file.csv", "w", encoding="utf-8") as file:
        # Write the header row
        file.write("Name,Remote,IRT,Type,Link,Duration\n")

        for pageNo in range(0, 12):
            print(f"Processing page :{pageNo}")
            try:
                response = requests.get(f"https://www.shl.com/solutions/products/product-catalog/?start={pageNo*12}")
                response.raise_for_status() # Raise an exception for HTTP errors
                soup = BeautifulSoup(response.text, 'html.parser')
                do_stuff(file, soup)
            except requests.exceptions.RequestException as e:
                print(f"Error fetching page {pageNo}: {e}")
            except Exception as e:
                print(f"Error processing page {pageNo}: {e}")

extract()