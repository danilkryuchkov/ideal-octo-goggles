import requests
from bs4 import BeautifulSoup


food_url = 'https://tarkov-market.com/tag/food'
drink_url = 'https://tarkov-market.com/tag/drinks'
# URL to be scraped
food_page = requests.get(food_url)
drink_page = requests.get(drink_url)


food_soup = BeautifulSoup(food_page.content, 'html.parser')
drink_soup = BeautifulSoup(drink_page.content, 'html.parser')

