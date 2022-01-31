# standard import
from datetime import datetime


# external import
from flask import render_template, request, Blueprint
from flask import render_template, request, redirect, flash
from flask.helpers import url_for



# internal
from atheneum.models import Members, Transactions, Books 
from atheneum import db
from .helper_fun import *



requisite     = Blueprint('requisite', __name__)


@requisite.route("/")
@requisite.route("/home")
def home():
    """
    
       This route will take you to home page of the web application  

    """
    available_books = Books.query.all()
    return render_template("home.html",  title="Library", books = available_books )

@requisite.route("/about")
def about():
    """

       This route will take you to about page of the application 
    
    """
    return render_template("about.html", title="About")


@requisite.route('/members', methods = ["POST" , "GET"])
def members():
    """
       This function  register's new members and records data to the database
    
    """

    if request.method == "POST":

        user_name = request.form['user_name']     # getting the user Name
        balance_amount = request.form['balance']  # getting the amount the user wants to add initially

        if not is_alphabets(user_name): 
            # This means the Librarian has entered wrong data
            message = "Please enter correct User-Name"
            return render_template('error.html', message = message, page = "members")
        
        if not balance_amount.isnumeric():
            # This means the Librarian has entered wrong balance
            message = "Please enter correct balence"
            return render_template('error.html',
                                    message = message,
                                    page = "members"
                                    )
        
        # Every Thing is Correct
        try:
            
            # Creating record
            member = Members(
                            member_name=user_name,
                            balance_amount = float(balance_amount)
                            ) 
                            
            db.session.add(member)  # adding in the DB 
            db.session.commit()     # commiting changes
            
        except:

            return render_template('error.html', message = "Unexpected Error, Cannot add Member")

    # no matter if the method is GET or POST we need to render the available member list.
    members = Members.query.all()                               # Getting all the members
    return render_template('members.html', members = members)   # rendering the page for members

# this function loads all the transactons
@requisite.route('/transactions')
def transactions():
    """
       This function sort the transactions in order from recent to old .
    
    """

    transactions = Transactions.query.order_by(Transactions.time.desc()).all() 
    return render_template('transactions.html', transactions = transactions)


# Renders Analytics Page
@requisite.route('/analytics')
def analytics():
    """
        This function audit's and returns top 5 books and top 5 members with maxmium transaction amount
    
    """

    # This query takes the top 5 popular Books which were issued most number of times
    popular_books = Books.query.order_by(Books.times_issued.desc()).limit(5).all()

    # This query takes the top 5 people who have spent the most
    top_spenders  = Members.query.order_by(Members.paid_for_borrowed_books.desc()).limit(5).all()

    return render_template('analytics.html', books = popular_books , people = top_spenders)



@requisite.route('/rent_out/<int:book_ID>', methods = ["POST" , "GET"])
def rent_out(book_ID):
    """
        This function work's on the logic of renting out of books 
    
    """
    all_members = Members.query.filter(
                            Members.borrowed == False
                            ).all()
    print('here your getting error 1')

    if request.method == "POST":

        # getting the id of the member.
        id_of_the_member = request.form['id']
        print('here your getting error 2')

        # if The entered member ID is invalid.
        if not id_of_the_member.isnumeric():
            return render_template('error.html', message = "Enter valid Id")
        print('here your getting error 3')

        # Get the member from the form data.
        member = Members.query.get(int(id_of_the_member))
        print('here your getting error 4')
        
        # check if member is present or not:
        if member == None:
            return render_template('error.html', message = "Not A valid Member!")
        print('here your getting error 5')

        if member.balance_amount < -500:
            # Users Balance is less Than 500

            message = f'The balance of {member.member_name} is {member.balance_amount} \
            which is less than -500 so please add money to your wallet before taking books.'

            return render_template('error.html', message = message)
        print('here your getting error 6')
        
        if member.borrowed==True:
            # User has already borrowed a book.

            message = 'The User has already Taken Books'
            return render_template('error.html' , message= message)
        print('here your getting error 7')

        try:

            member.borrowed = True   # Member has borrowed a book.
            member.balance_amount -= 500    # members balance Should Decrease by 500.
            member.paid_for_borrowed_books += 500    # Member paid 500 rs to the Library.

            book = Books.query.get(book_ID)         # Get the book from the book_ID.
            print('here your getting error 8')
            if book == None:
                return render_template('error.html', message = "Unexpected Error Occured")
            print('here your getting error 9')
            
            book.quantity = 0   # Book's quantity is decreased.
            book.times_issued += 1  # books Times issued is increased by 1.
            book.borrower = member.id_    # Books borrower is set to the id of member's id.

            # New transaction is registered and added to transactions.
            trans = Transactions(
                                book_title = book.book_title,
                                member_name = member.member_name,
                                direction = False
                                )
            print('here your getting error 10')

            db.session.add(trans)
            print('here your getting error 11')
            db.session.commit()
            print('here your getting error 12')
            # return redirect(url_for('home'))
            return redirect('/')
            

        except:
            print('here your getting error 13')

            return render_template(
                                'error.html',
                                message = "Unexpected Error Occured"
                                )
        
    return render_template(
                        'rent_out.html',
                        id = book_ID,
                        members = all_members
                        )



@requisite.route('/addBooks', methods = ["POST" , "GET"])
def addBooks():
    """
        This function adds books records which are fetched from  API call and redirects to the home page of the application 
    
    """



    if request.method == "POST":

        # GET the data from the API.
        # pass the data in LMS and then redirect to root page.
        # render the data recieved.

        # Gets the data from The API.
        response = make_API_call()

        # going through data.
        for data in response:

            # getting the book ID from the form.
            book_ID = int(data["bookID"])

            # Checking if the same data exists in the data base or not.
            to_find = Books.query.get(book_ID)

            if to_find == None:

                # If book is not found in the data base then add it in the data base.
                book = Books (
                            book_ID = book_ID,
                            book_title = data["title"],
                            authors = data["authors"],
                            publisher =data["publisher"],
                            isbn = data["isbn"]
                            
                            )

                db.session.add(book)
                db.session.commit()
            
        # rendering page using jinja and then redirect.
        return redirect(url_for('requisite.home'))

    else:

        return render_template('add_books.html')


@requisite.route('/addCustomBooks', methods=["POST"])
def add_custom_books():
    if request.method == "POST":
        book_ID = request.form['book_ID']
        book_title = request.form['book_title']
        authors = request.form['authors']
        publisher = request.form['publisher']
        isbn = request.form['isbn'] or 404

        # checking for if book_ID already exists or not and values are valid
        
        if not book_ID.isnumeric():
            return render_template(
                                'error.html',
                                message = "Please enter a valid book ID"
                                )
        
        book_ID = int(book_ID)
        if Books.query.get(book_ID) != None:
            return render_template('error.html', message = "Book Id already Exists in DB")

        # every thing is valid 
        try:
            book = Books(
                        book_ID = book_ID,
                        book_title = book_title,
                        authors = authors,
                        publisher = publisher,
                        isbn = isbn
                        )

            db.session.add(book)
            db.session.commit()
            return redirect('/')

        except:
            return render_template('error.html', message = "Unexpected Error")
        

    else:
        return render_template('error.html', message = "NOT AUTHORIZED")




@requisite.route('/return_book')
def return_book():
    """
       This function returns records of rented books 
    
    
    """
    books = Books.query.filter(
                        Books.quantity == 0     # render only those books which have been issued
                        ).all()

    return render_template(
                        'return_book.html',
                        books = books
                        )



@requisite.route('/summary/<int:id_>')
def summary(id_):
    """
       This is the function which reverts the data to its initial stage
    """

    book = Books.query.get(id_)                  # get The book.
    book.quantity = 1                           # set its quantity to 1 again.
    member = Members.query.get(book.borrower)   # get the member using borrower column.

    # get the old transaction to get the time at which the book was issued.
    old_trans = Transactions.query.filter(
        Transactions.book_title == book.book_title
        ).first()

    # create a new transaction for the return of book
    trans = Transactions(
                        book_title = book.book_title,
                        member_name = member.member_name,
                        direction = True
                        )

    db.session.add(trans)   # Add it to the session.
    book.borrower = -1  # set the borrower to -1 again as it has no borrower now.

    # Calculate the balance of member by the formula => 10 * number of days for which the book was borrowed
    charges = (datetime.utcnow() - old_trans.time).days * 10

    # deduct the amount from the members wallet
    member.balance_amount -= charges

    # add the amount deducted by the user wallet to the library profits
    member.paid_for_borrowed_books += charges
    
    member.borrowed = False  # set this property to False as the member has not borrowed a book.
    db.session.commit()     # commit changes.

    return render_template('summary.html', member = member)


@requisite.route('/delete_member/<int:id_>')
def delete(id_):
    """
         This function deletes a registered member records
    """
    try:

        task_to_delete =  Members.query.get(id_)
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/members')

    except:

        return render_template('error.html', message = "Unexpected Error Occured")


@requisite.route('/update/<int:id_>', methods = ["POST", "GET"])
def update(id_):
    """
       This function adds amount to the members id 
    """
    if request.method == "POST":
        try:

            user = Members.query.get(id_)
            user.balance_amount += float(request.form['amount'])
            db.session.commit()
            return redirect('/members')

        except:

            return render_template('error.html', message = "Unexpected Error Occured")
    else:
        return render_template('update.html', id = id_)