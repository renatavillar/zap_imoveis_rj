import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

data_dict = {'Rent': [], 'Address': [], 'Street': [], 'Neighborhood': [], 'Area': [], 'Rooms': [], 'Bathrooms': [], 'Parking': []}


for i in range(1, 289):

    url = 'https://www.zapimoveis.com.br/aluguel/imoveis/rj+rio-de-janeiro/?pagina=i&onde=,Rio%20de%20Janeiro,Rio%20de%20Janeiro,,,,BR%3ERio%20de%20Janeiro%3ENULL%3ERio%20de%20Janeiro,-29.9477228,-51.1021166&transacao=Aluguel&tipo=Im%C3%B3vel%20usado'
    user_agent = {'User-agent': 'Mozilla/5.0'}
    response = requests.get(url, headers = user_agent)
    soup = BeautifulSoup(response.text, 'html.parser')

    for element in soup.find_all('div', class_="box--display-flex box--flex-column gutter-top-double gutter-left-double gutter-right-double gutter-bottom-double simple-card__box"):

        if element.find('div', class_="simple-card__prices simple-card__listing-prices") is not None:

            data_dict['Rent'].append(element.find('div', class_="simple-card__prices simple-card__listing-prices").find('p', class_="simple-card__price js-price heading-regular heading-regular__bolder align-left").find('strong').text)

        if element.find('div', class_="simple-card__actions") is not None:

        	data_dict['Area'].append(element.find('div', class_="simple-card__actions").find('ul',
        		class_="feature__container simple-card__amenities").find('li', class_=
        		"feature__item text-small js-areas").find_all('span')[1].text)

        if element.find('div', class_="simple-card__actions") is not None:

        	data_dict['Address'].append(element.find('div', class_="simple-card__actions").find('p',
        		attrs={'class':"color-dark text-regular simple-card__address", 'ellipsis':"true",
        		'ellipsis-lines':"1"}).text)

        if element.find('div', class_="simple-card__actions").find('ul',
        	class_="feature__container simple-card__amenities").find('li', class_=
        		"feature__item text-small js-bedrooms") is not None:

        	data_dict['Rooms'].append(element.find('div', class_="simple-card__actions").find('ul',
        	    class_="feature__container simple-card__amenities").find('li', class_=
        	    "feature__item text-small js-bedrooms").find_all('span')[1].text)

        else:

        	data_dict['Rooms'].append(0)

        if element.find('div', class_="simple-card__actions").find('ul',
        	class_="feature__container simple-card__amenities").find('li', class_=
        		"feature__item text-small js-bathrooms") is not None:

        	data_dict['Bathrooms'].append(element.find('div', class_="simple-card__actions").find('ul',
        	    class_="feature__container simple-card__amenities").find('li', class_=
        	    "feature__item text-small js-bathrooms").find_all('span')[1].text)

        else:

        	data_dict['Bathrooms'].append(0)

        if element.find('div', class_="simple-card__actions").find('ul',
        	class_="feature__container simple-card__amenities").find('li', class_=
        		"feature__item text-small js-parking-spaces") is not None:

        	data_dict['Parking'].append(element.find('div', class_="simple-card__actions").find('ul',
        	    class_="feature__container simple-card__amenities").find('li', class_=
        	    "feature__item text-small js-parking-spaces").find_all('span')[1].text)

        else:

        	data_dict['Parking'].append(0)

for i in range(0, len(data_dict['Address'])):
	data_dict['Street'].append(data_dict['Address'][i].rsplit(',', 1)[0])

for i in range(0, len(data_dict['Address'])):
	data_dict['Neighborhood'].append(data_dict['Address'][i].rsplit(',', 1)[1])

zap = pd.DataFrame(data_dict)

filepath = 'YOUR_PATH'

with open(filepath+'GIVE_A_NAME.csv', 'a') as f:
	zap.to_csv(f, quoting=csv.QUOTE_NONNUMERIC, sep='|', decimal='.', header=data_dict.keys(), index=False)