import datetime
import os

from flask import Flask, render_template, redirect, url_for
from forms import ItemForm
from models import Items
from database import db_session

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

@app.route("/", methods=['GET', 'POST'])
def add_item():
    form = ItemForm()
    if form.validate_on_submit():
        #Through testing, I found this bit of code is what's causing the 504 error.
        #Took out the date_added variable to see if that was holding it up.
        #Added datetime back in. It didn't break anything. Still getting outputs like [,,].
        
        item = Items(name=form.name.data, quantity=form.quantity.data, description=form.description.data, date_added=datetime.datetime.now())

##        #Maybe item isn't being populated correctly. Try one attribute at a time.
##        #Still getting the same [,,,] type output.
##        item = Items()
##        item.name = form.name.data
##        item.quantity = form.quantity.data
##        item.description = form.description.data
##        item.date_added = datetime.datetime.now()
        
        #More testing shows the error 504 came from calling db_session.
        #This was because the postgres port was supposed to stay as 5432.
        #Output after submittion is a list of commas, so maybe item isn't getting
        #added correctly to the table.
        db_session.add(item)
        db_session.commit()
        return redirect(url_for('success'))
    return render_template('index.html', form=form)

@app.route("/success")
def success():
    #Testing to see if I can complete the redirect with a Hello World.
    #return "Hello, World!"

    #Try bipassing results = [] that might be giving empty entries. No change.
    #return str(db_session.query(Items).all())

##    #Trying a different way to get the Items table. Still get 504 error, so the syntax here
##    #doesn't seem at issue.
##    #This gives the same [,,] as the original code.
##    qry = Items.query.all()
##    return str(qry)

##    #Trying to just display one thing from the table with .get(1)
##    #This gave an empty page. This table is just filled with empty entries, but adding a new
##    #entry upon submission.
##    return str(Items.query.get(1))

##    #What happens when returning a query Items.query.all()?
##    #List isn't callable, so try str(Items.query.all()
##    #Still showing an additional comma with each submission.
##    #Try again with query defined in the class Items. That didn't work because database.py sets
##    #up query on Base with declarative.
##    return str(Items.query.all())
    
    

    #It seems that any call to db_session is causing 504 error.
    #After fixing the postgres port to 5432, this now returns [,] or [,,] etc.
    results = []
    qry = db_session.query(Items)
    results = qry.all()

    return str(results)

 

#This command didn't specify a port, so I made it look like it does in the docker documentation.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

###From source flask.pocoo.org, need to remove database session at end of request. This might be causing the 504 error.
###This code didn't affect the [,,] output.
##@app.teardown_appcontext
##def shutdown_session(exception=None):
##    db_session.remove()
