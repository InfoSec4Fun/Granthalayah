# standard imports

# external imports
from flask import request
import requests
from random import randint

# internal imports


# Helper Functions


def is_alphabets(s : str):
    """
        This function check's if passed variable is string and returns a Boolean value
    """
    return ''.join(s.split()).isalpha()



def remove_spaces(s : str):
    """
        This function removes unnecessary space between characters 
    """
    return ' '.join(s.split())



def make_API_call():
    """
       This function makes a call to the API to fetch book records  and returns a proper response  
    """

    # This is The Base Url from which we will make the imports
    BASE_URL = 'https://frappe.io/api/method/frappe-library?'

    title = remove_spaces(request.form['title'])                # Removing inconsistency in spaces
    authors = remove_spaces(request.form['authors'])             # Removing inconsistency in spaces
    publisher = remove_spaces(request.form['publisher'])        # Removing inconsistency in spaces
    isbn = request.form['isbn']

    end = ''

    if title or authors or isbn or publisher:   # if proper inputs are passed 
        end = f'title={title}&authors={authors}&isbn={isbn}publisher={publisher}'
        response = requests.get(BASE_URL + end).json()['message']
    
    else:  # if no parameters are passed this condition checked 
        # No parameters passed for searching so we will search at random pages between 1 - 200
        response = requests.get(BASE_URL + f'page={randint(1,200)}').json()['message']

    return response