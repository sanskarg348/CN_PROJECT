import time
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
amazon_data = []
flipkart_data = []
myntra_data = []


def amazon_scraper(url, driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    dic = {}
    dic['title'] = soup.find(id='productTitle').get_text().strip()
    try:
        dic['rating'] = soup.find(id='acrPopover').attrs['title'].split()[0]
    except:
        dic['rating'] = ''
    try:
        dic['num_rating'] = soup.find(id='acrCustomerReviewText').get_text().split()[0]
    except:
        dic['num_rating'] = ''
    dic['url'] = 'https://www.amazon.in' + url
    dic['price'] = soup.find('span', {'class': 'a-price-whole'}).get_text()
    dic['description'] = " + ".join(
        [i.find('span').get_text() for i in soup.find(id='feature-bullets').find('ul').find_all('li')])

    return dic


def flipkart_scrapper(url, driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    dic = {}
    dic['title'] = soup.find('h1', {'class': 'yhB1nd'}).get_text()
    try:
        dic['rating'] = soup.find('div', {'class': '_3LWZlK'}).get_text()
    except:
        dic['rating'] = ''
    try:
        dic['num_rating'] = soup.find('span', {'class': '_2_R_DZ'}).find('span').find('span').get_text()
    except:
        dic['num_rating'] = ''
    dic['url'] = 'https://www.flipkart.com' + url
    dic['price'] = soup.find('div', {'class': '_30jeq3'}).get_text()
    dic['description'] = ''

    return dic


def myntra_scrapper(url, driver):

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    dic = {}
    dic['title'] = soup.find('h1', {'class': 'pdp-title'}).get_text() + ' ' + soup.find('h1', {'class': 'pdp-name'}).get_text()
    try:
        dic['rating'] = soup.find('div', {'class': 'index-overallRating'}).find('div').find('div').get_text()
    except:
        dic['rating'] = ''
    try:
        dic['num_rating'] = soup.find('div', {'class': 'index-ratingsCount'}).get_text()
    except:
        dic['num_rating'] = ''
    dic['url'] = 'https://www.myntra.com' + url
    dic['price'] = soup.find('span', {'class': 'pdp-price'}).get_text()
    dic['description'] = soup.find('p', {'class': 'pdp-product-description-content'}).get_text()
    return dic


def get_data(keywords, limit: int):
    driver = webdriver.Chrome()
    global amazon_data, flipkart_data, myntra_data
    fin_amazon_url = f'https://www.amazon.in/s?k={"+".join(keywords.split())}&ref=nb_sb_noss'
    fin_flipkart_url = f'https://www.flipkart.com/search?q={"%20".join(keywords.split())}&as-show=on&as=off'
    fin_myntra_url = f'https://www.myntra.com/{"-".join(keywords.split())}'

    driver.get(fin_amazon_url)
    amazon_soup = BeautifulSoup(driver.page_source, 'html.parser')
    amazons_urls = [i.find('div', {'class': 's-product-image-container'}).find('a').attrs['href']
                    for i in amazon_soup.find_all('div', {'data-component-type': "s-search-result"})[:limit]]
    s = 'Amazon \n'
    inn = 1
    for i in amazons_urls:
        driver.get('https://www.amazon.in' + i)
        amazon_data.append(amazon_scraper(i, driver))
        s += f'Product {inn} \n'
        s += 'URL ' + amazon_data[-1]['url'] + '\n Price ' + amazon_data[-1]['price'] + '\n Rating ' + amazon_data[-1]['rating'] + '\n'
        time.sleep(1)
        inn += 1
    print(pd.DataFrame(amazon_data))

    driver.get(fin_flipkart_url)
    flipkart_soup = BeautifulSoup(driver.page_source, 'html.parser')
    flipkart_urls = [i.find('a').attrs['href'] for i in flipkart_soup.find_all('div', {'class': '_1AtVbE'})[3:limit+3]]
    s1 = 'Flipkart \n'
    inn = 1
    for i in flipkart_urls:
        driver.get('https://www.flipkart.com' + i)
        flipkart_data.append(flipkart_scrapper(i, driver))
        s1 += f'Product {inn} \n'
        s1 += 'URL ' + flipkart_data[-1]['url'] + '\n Price ' + flipkart_data[-1]['price'] + '\n Rating' + flipkart_data[-1]['rating'] + '\n'
        time.sleep(1)
        inn += 1
    print(pd.DataFrame(flipkart_data))
    s2 = 'Myntra \n'
    driver.get(fin_myntra_url)
    myntra_soup = BeautifulSoup(driver.page_source, 'html.parser')
    myntra_urls = [i.find('a').attrs['href'] for i in myntra_soup.find_all('li', {'class': 'product-base'})[:limit]]
    inn = 1
    for i in myntra_urls:
        driver.get('https://www.myntra.com/' + i)
        myntra_data.append(myntra_scrapper(i, driver))
        s2 += f'Product {inn} \n'
        s2 += 'URL ' + myntra_data[-1]['url'] + '\n Price ' + myntra_data[-1]['price'] + '\n Rating' + myntra_data[-1]['rating'] + '\n'
        time.sleep(1)
        inn += 1

    print(pd.DataFrame(myntra_data))
    return s,s1,s2
