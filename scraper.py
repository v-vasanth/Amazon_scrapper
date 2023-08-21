import requests
from bs4 import BeautifulSoup
import csv

def get_title(soup):
    try:
        title = soup.find("span", attrs={"id": 'productTitle'})
        title_value = title.get_text(strip=True)
        title_string = title_value.strip()
    except AttributeError:
        title_string = ""
    return title_string

def get_price(soup):
    try:
        price = soup.find("span", attrs={'id': 'priceblock_ourprice'}).get_text(strip=True)
    except AttributeError:
        price = ""
    return price


def get_rating(soup):
    try:
        rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).get_text(strip=True)
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class': 'a-icon-alt'}).get_text(strip=True)
        except:
            rating = ""
    return rating


def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id': 'acrCustomerReviewText'}).get_text(strip=True)
    except AttributeError:
        review_count = ""
    return review_count

if __name__ == '__main__':
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5'}


    csv_filename = "amazon_scrapped_details(p1).csv"
    csv_columns = ["Product URL", "Product Name", "Product Price", "Rating", "Number of Reviews"]
    csv_data = []


    for page_num in range(1, 21):
        url = f"https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{page_num}"

        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, "html.parser")


        links = soup.find_all("a", class_="a-link-normal s-no-outline")
        product_links = [link.get("href") for link in links]

 
        for link in product_links:
            product_url = "https://www.amazon.in" + link

            product_page = requests.get(product_url, headers=HEADERS)
            product_soup = BeautifulSoup(product_page.content, "html.parser")

            product_name = get_title(product_soup)
            product_price = get_price(product_soup)
            rating = get_rating(product_soup)
            review_count = get_review_count(product_soup)

            csv_data.append([product_url, product_name, product_price, rating, review_count])

    with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(csv_columns)
        writer.writerows(csv_data)

    print("Completed.")
