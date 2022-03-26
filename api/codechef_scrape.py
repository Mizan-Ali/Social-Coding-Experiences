from bs4 import BeautifulSoup
import requests


class CodechefUser:
    def __init__(self, username) -> None:
        self.__url = 'https://www.codechef.com/users/' + username
    
    def get_user_data(self):
        req = requests.get(self.__url)
        soup = BeautifulSoup(req.text, 'html.parser')

        try:
            soup.find('div', class_ = 'rating-number').text
        except Exception:
            return {'error' : 'Username not valid'}
        
        return_dict = dict()

        rating = soup.find('div', class_='rating-number').text
        solved = soup.find('section', class_ = 'rating-data-section problems-solved').find('div', class_='content').h5.text.split()[2][1:-1]
        country = soup.find('span', class_ = 'user-country-name').text
        ranks = soup.find('div', class_ = 'rating-ranks').find_all('a')
        global_rank = ranks[0].text
        country_rank = ranks[1].text
        highest_rating = soup.find('div', class_ = 'rating-header text-center').small.text.split()[2][:-1]
        num_stars = soup.find('span', class_ = 'rating')

        if num_stars:
            num_stars = num_stars.text[:-1]
            
        return_dict['rating'] = rating
        return_dict['solved'] = solved
        return_dict['global_rank'] = global_rank
        return_dict['country_rank'] = country_rank
        return_dict['highest_rating'] = highest_rating
        return_dict['num_stars'] = num_stars
        return_dict['country'] = country

        return return_dict