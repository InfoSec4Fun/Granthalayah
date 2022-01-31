from atheneum import create_app
""" atheneum means """
app  = create_app()
app.app_context().push()

if __name__  == '__main__':
    """
        This condition will start serving the application 
    
    """
    app.run(debug=True)