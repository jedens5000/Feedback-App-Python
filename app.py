from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail


app = Flask(__name__)
##############TEST******************
# app = Flask(__name__)

# with app.app_context():
    # within this block, current_app points to app.
  # print(current_app.name)

#############################
# def create_app():
#   app = Flask(__name__)
  
#   with app.app_context():
#     init_db()
  
#   return app  
##############TEST******************
############THIS CONNECTS DB*****************
ENV = "dev"

if ENV == "dev":
  app.debug = True
  app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///postgres:Zacapa23@localhost/lexus"
else:
  app.debug = True
  app.config["SQLALCHEMY_DATABASE_URI"] = ""

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
############END DB CONNECT*******************
############THIS CREATES DB MODEL/TABLE***************
class Feedback(db.Model):
  __tablename__ = "feedback"
  id = db.Column(db.Integer, primary_key=True)
  customer = db.Column(db.String(200))
  dealer = db.Column(db.String(200))
  rating = db.Column(db.Integer)
  comments = db.Column(db.Text())
  # This is constructor/initializer
  def __init__(self, customerid, customer, dealer, rating, comments):
    self.customer = customer
    self.dealer = dealer
    self.rating = rating
    self.comments = comments

# with app.app_context():
#   db.create_all()    
# db.create_all()


#KILL SERVER AND TYPE THIS IN TERMINAL:
#>>> python
#>>> from app import db
#>>> db.create_all()
#>>> exit()
#>>> python app.py <----This part just starts the server again

# >>> from project import app, db
# >>> app.app_context().push()
# >>> db.create_all()
############END CREATE DB MODEL/TABLE*****************

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
  if request.method == "POST":
    customer = request.form["customer"] # Needs to match field "Name" from input form
    dealer = request.form["dealer"]
    rating = request.form["rating"]
    comments = request.form["comments"]
    print(customer, dealer, rating, comments)
    if customer == "" or dealer == "":
      return render_template("index.html", message="Please enter required fields") # This triggers msg line 17-19 on index.html
    if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0: #This checks if customer exists in db
      data = Feedback(customer, dealer, rating, comments)
      db.session.add(data)
      db.session.commit()
      send_mail(customer, dealer, rating, comments)
      return render_template("success.html") # This tells it what page to render/load after submitting the form
    return render_template("index.html", message="You have already submtted feedback") # This triggers msg line 17-19 on index.html


if __name__ == "__main__":
    app.run()
