from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from . import models
from requests.compat import quote_plus
""" quote_plus will add + sign automatically in between the searched query, i.e. if we have made search for computer of the week
then it will quote_plus will convert it as computer+of+the+week """


BASE_CRAIGSLIST_URL ='https://delhi.craigslist.org/search/hhh?query={}'
BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

# Create your views here.
def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    """The below line will go to the Search model in the models.py and create a Search object where the argument is search.
    It will ad all the searches to the search database which can be seen by the admin by
    clicking on Searches in http://127.0.0.1:8000/admin/"""
    models.Search.objects.create(search=search)
    #print(quote_plus(search))
    """ the below code line will add the searched item in the BASE_CRAIGSLIST_URL and convert it into the authenticated url,
    for example if we searched for "Computer of the week" then it will add it to the BASE_CRAIGSLIST_URL as
    https://ahmedabad.craigslist.org/search/jjj?computer=puppy+of+the+week
    that is it will concatenate the BASE_CRAIGSLIST_URL link and the search """
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    #print(final_url)
    # getting the webpage, creating a response object
    response = requests.get(final_url)
    #Extracting the source code of the page
    data = response.text
    #print(data)

    #Passing the source code to BeautifulSoup to create a BeautifulSoup object fr it
    soup = BeautifulSoup(data, features='html.parser')

    #Extracting all the <li> tags whose class name is 'result-row' into a list named post_listings
    # so basically we are saying that fing all the links form the source page where class is result-row
    post_listings = soup.find_all('li', {'class': 'result-row'})

    final_postings = []

    # now for each item ie link in the post_listings, we will find its title,url and price
    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        if post.find(class_='result-image').get('data-ids'):
            post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
            post_image_url = BASE_IMAGE_URL.format(post_image_id)
            print(post_image_url)
        else:
            post_image_url = 'https://craigslist.org/images/peace.jpg'

        final_postings.append((post_title, post_url, post_price, post_image_url))


    # prints the zeroth link from the post_titles list
    #print(post_titles[0].get('href'))

        # prints the text of the zeroth link from the post_titles list
        #print(post_titles[0].text)



    stuff_for_frontend = {'search': search,
                'final_postings': final_postings,}

    return render(request, 'myapp/new_search.html',stuff_for_frontend)
