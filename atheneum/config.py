import os


class Config:
    """
       This function stores all the required configurations to run the application 

    """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db' # os.environ.get('SQLALCHEMY_DATABASE_URI') 'sqlite:///site.db'