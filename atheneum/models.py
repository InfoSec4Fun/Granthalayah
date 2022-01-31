# standard imports
from datetime import datetime


# external imports
from flask import  render_template, request, redirect, flash
from flask.helpers import url_for
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.wrappers import response


# internal imports
from atheneum import db

# Tables Definition
class Books(db.Model):
    """
       This is a model class which defines structure of the table where book records will be stored 
    
    """
    # def __init__(self):
    #     self.name           = 'books'
    #     self.description    = """
    #                              This table stores books data
    #                           """

    book_ID                 = db.Column(db.Integer , primary_key = True) # book_id
    book_title               = db.Column(db.String(150))   # book_title
    authors                 = db.Column(db.String(75))    # authors
    # average_rating          = db.Column(db.Float(precision=), nullable)
    quantity                = db.Column(db.Integer , default = 1) # quantity                     
    borrower                = db.Column(db.Integer , default = -1)   # borrower         
    isbn                    = db.Column(db.String(15))             # isbn
    isbn13                    = db.Column(db.String(15))             # isbn13       
    times_issued            = db.Column(db.Integer , default = 0)  # times_issued            
    publisher               = db.Column(db.String(75))    # publisher
    

class Members(db.Model):
    """
       This is a model class which defines structure of the table where members records are stored 
    """
    id_ = db.Column(db.Integer , primary_key = True)   # member_id
    member_name = db.Column(db.String(150))  # member_name
    balance_amount = db.Column(db.Float , default = 1000) # member_balance
    borrowed = db.Column(db.Boolean, default = False) # member_borrowed
    paid_for_borrowed_books = db.Column(db.Float , default = 0) # library_fees_given


class Transactions(db.Model):
    """
       This is model class which defines structure of the table where transactions records are stored 
    
    """
    transaction_id = db.Column(db.Integer , primary_key = True) #_id
    book_title =  db.Column(db.String(150))
    member_name = db.Column(db.String(150))
    direction = db.Column(db.Boolean, default = True)
    time = db.Column(db.DateTime , default = datetime.utcnow)
