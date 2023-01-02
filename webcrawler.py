import csv
import json
import urllib3
import re
import requests
from bs4 import BeautifulSoup


def main():
    brand = 'dell'
    # create an HTTP connection pool
    http = urllib3.PoolManager()

    # make a GET request to the website

    user = input('enter url: ')

    try:
        response = http.request('GET',user)

    except Exception as e:
        print(e)
        main()

    # Parse the HTML of the website
    soup = BeautifulSoup(response.data, 'html.parser')



    #section find
    section = soup.find(id='hero_section')
    h1 = section.find('h1')
    span = h1.find('span')
    text = span.text
    parts = text.split("-")
    name = parts[-1].strip()


    #section find
    section = soup.find(id='hero-tech-spec')


    diagonal_size_div = section.find('div', {'id': 'T0000236'})
    diagonal_size = diagonal_size_div.find('p').text

    resolution_refresh_rate_div = section.find('div', {'id': 'T0002261'})
    resolution_refresh_rate = resolution_refresh_rate_div.find('p').text
    #




    resolution_match = re.search(r"\d+ x \d+", resolution_refresh_rate)
    if resolution_match:
        resolution = resolution_match.group(0)
        resolution = resolution.replace(" ","")

    refresh_rate_match = re.search(r"\d+ Hz", resolution_refresh_rate)
    if refresh_rate_match:
        refresh_rate = refresh_rate_match.group(0).lower()

    diagonal_size = diagonal_size[:-1] + ' in'
    # push
    print(f"\n{name}\n{diagonal_size}\n{resolution}\n{refresh_rate}\n")

    try:
        response = requests.post(f'http://127.0.0.1:5000/monitors?guid=0&name={name}&rate={refresh_rate}&resolution={resolution}&dimensions={diagonal_size}&brand={brand}')
        print(response)
        print('added to csv')

    except Exception as e:
        print(e)

    main()
try:
    main()
except Exception as e:
    print(e)


