import time
from bs4 import BeautifulSoup as BS
import csv
import json
import aiohttp
import asyncio
from math import ceil

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/111.0.0.0 Safari/537.36 OPR/97.0.0.0'
}
url = 'https://av.by'


async def get_list_car_brands(url=url):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers=headers)
        soup = BS(await response.text(), 'lxml')
        list_brands = soup.findAll('span', class_="catalog__title")
        inter_list = [i.text for i in list_brands]
        result_list = list()
        for i in range(len(inter_list)):
            result_list.append(f'{i + 1}: {inter_list[i]} ')

        return result_list


async def get_link_brand(brand, url=url):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers=headers)
        soup = BS(await response.text(), 'lxml')
        link_brand = soup.find('a', class_="catalog__link", title=brand).get('href')
        soup_count = soup.find('a', class_="catalog__link", title=brand)
        count = soup_count.find('span', class_="catalog__count").text
        return [link_brand, count]


# <a class="catalog__link" title="Logo" href="/honda/logo">flex

# <span class="catalog__count">308</span>

async def parse_button_link(link):  # inf, count
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=link, headers=headers)
        soup = BS(await response.text(), 'lxml')
        url_pages = soup.find('a', class_="button button--default", role='button').get('href')
        button_link = 'https://cars.av.by' + url_pages
        button_link = button_link.replace('brands%5B0%5D%5Bbrand%5D', 'brands[0][brand]').replace('%5B0%5D%5Bmodel%5D',
                                                                                                  '[0][model]') \
            .replace('price_currency=2&', '')
    return button_link


async def parse_ads(link):  # inf, count
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=link, headers=headers)
        soup = BS(await response.text(), 'lxml')
        ads_links = soup.findAll('a', class_="listing-item__link")
        links = list()
        for i in ads_links:
            links.append(i.get('href'))
        return links


# <div class="listing-item__priceusd">≈&nbsp;22&thinsp;800&nbsp;$</div>
async def parse_price_ads(link):  # inf, count
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=link, headers=headers)
        soup = BS(await response.text(), 'lxml')
        ads_links = soup.findAll('div', class_="listing-item__priceusd")
        links = list()
        for i in ads_links:
            links.append(int(i.text.encode('ascii', errors='ignore')
                                                      .decode('UTF-8').replace('$', '')))
        return links


async def full_soup_parser(link, count):
    '''объект должен содержать несколько страниц'''
    url_button = await parse_button_link(link)
    tasks = list()
    res_list = list()
    async with aiohttp.ClientSession() as session:
        counter = 2
        for i in range(1, ceil(count / 25) + 1):
            url_button = url_button.replace(f'page={counter}', f'page={i}')
            counter = i

            async def tasks_funk(url):
                link = await parse_ads(url)
                price = await parse_price_ads(url)
                res_list.append([link, price])

            task = asyncio.create_task(tasks_funk(url_button))
            tasks.append(task)
        await asyncio.gather(*tasks)

        result_list = list()
        for i in res_list:
            for g in range(len(i)):
                result_list.append([i[0][g], i[1][g]])
        print(result_list)


        # response = await session.get(url=url_button, headers=headers)
        # soup = BS(await response.text(), 'lxml')


if __name__ == '__main__':
    a = asyncio.run(
        full_soup_parser('https://cars.av.by/honda/civic', 353))

    # https: // cars.av.by / volkswagen / passat

# /filter?brands%5B0%5D%5Bbrand%5D=43&brands%5B0%5D%5Bmodel%5D=181&price_currency=2&page=2
# https://cars.av.by/citroen/c5
# https://cars.av.by/citroen/c5/filter?brands%5B0%5D%5Bbrand%5D=43&brands%5B0%5D%5Bmodel%5D=181&price_currency=2&page=2
# https://cars.av.by/filter?brands[0][brand]=43&brands[0][model]=181&page=2
