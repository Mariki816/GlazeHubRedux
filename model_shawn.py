from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy import Column, Float, String, Integer
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import relationship, backref
from flask_sqlalchemy import SQLAlchemy

# import model

# ENGINE = None
# Session = None

db = SQLAlchemy()
# engine = create_engine("sqlite:///glazehub.db", echo=False)
# session = scoped_session(sessionmaker(bind=engine, autocommit=False,
#                          autoflush=False))


# Base = declarative_base()
# Base.query = session.query_property()


#Class declarations
#This is the CP chemical database and a few functions for the class itself
class Chem(db.Model):
    __tablename__ = "chemicals"
    id = Column(Integer, primary_key=True)
    chem_name = Column(String(120), unique=True)
    quarter = Column(Float)
    half = Column(Float)
    onelb = Column(Float)
    fivelb = Column(Float)
    tenlb = Column(Float)
    twentyfivelb = Column(Float)
    fiftylb = Column(Float)
    onehundlb = Column(Float)
    fivehundlb = Column(Float)

    @classmethod
    def getAllChemicals(cls):
        return db.session.query(Chem).all()

    @classmethod
    def getChemNameByID(cls, chemID):
        return db.session.query(Chem).get(chemID).chem_name

    @classmethod
    def getChemIDByName(cls, chemNAME):
        return db.session.query(Chem).filter_by(chem_name=chemNAME).first().id

    @classmethod
    def getChemPriceByName(cls, id, weight):
        if (weight <= 0.5):
            price = db.session.query(Chem).filter_by(id=id).first().quarter
        elif (weight >= 0.5 and weight < 1.0):
            price = db.session.query(Chem).filter_by(id=id).first().half
        elif (weight >= 1 and weight < 5):
            price = db.session.query(Chem).filter_by(id=id).first().onelb
        elif (weight >= 5 and weight < 10):
            price = db.session.query(Chem).filter_by(id=id).first().fivelb
        elif (weight >= 10 and weight < 25):
            price = db.session.query(Chem).filter_by(id=id).first().tenlb
        elif (weight >= 25 and weight < 50):
            price = db.session.query(Chem).filter_by(id=id).first().twentyfivelb
        elif (weight >= 50 and weight < 100):
            price = db.session.query(Chem).filter_by(id=id).first().fiftylb
        elif (weight >= 100 and weight < 500):
            price = db.session.query(Chem).filter_by(id=id).first().onehundlb
        else:
            price = db.session.query(Chem).filter_by(id=id).first().fivehundlb
        return price


#This is the table of users
class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    user_name = Column(String(64), nullable=False)
    email = Column(String(64), nullable=False)
    password = Column(String(64), nullable=False)

    @classmethod
    def getUserID(cls):
        return db.session.query(User).get(id)

    @classmethod
    def getUserByEmail(cls, email):
        return db.session.query(User).filter_by(email=email).first()

    @classmethod
    def getUserNameByID(cls, id):
        return db.session.query(User).filter_by(id=id).first()

    @classmethod
    def getUserPasswordByEmail(cls, email):
        return db.session.query(User).filter_by(email=email).first().password


#This is the table of recipes.
class Recipe(db.Model):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True)
    recipe_name = Column(String(120))
    user_id = Column(Integer, ForeignKey('users.id'))
    user_notes = Column(String(3000), nullable=True)

    user = relationship("User", backref=backref("recipes", order_by=id))

    @classmethod
    def getRecipeName(cls, recipe_name):
        return db.session.query(Recipe).filter_by(recipe_name=recipe_name).first()

    @classmethod
    def getRecipeNamesByUserID(cls, user_id):
        return db.session.query(Recipe).filter_by(user_id=user_id).all()

    @classmethod
    def getRecipeIDByName(cls, recipe_name, user_id):
        return db.session.query(Recipe).\
            filter_by(recipe_name=recipe_name).\
            filter_by(user_id=user_id).first()


#This is the table of Components
class Component(db.Model):
    __tablename__ = "components"
    id = Column(Integer, primary_key=True)
    chem_id = Column(Integer, ForeignKey('chemicals.id'), nullable=False)
    recipe_id = Column(Integer, ForeignKey('recipes.id'), nullable=False)
    percentage = Column(Float, nullable=False)

    chem = relationship("Chem", backref=backref("components", order_by=id))
    recipe = relationship("Recipe", backref=backref("components", order_by=id))

    @classmethod
    def getComponentsByRecipeID(cls, recipe_id):
        return db.session.query(Component).filter_by(recipe_id=recipe_id).all()


# def connect():
#     global ENGINE

#     ENGINE = create_engine("sqlite:///chemicals.db", echo=True)
#     Session = sessionmaker(bind=ENGINE)

#     return Session()


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///glazehub.db'
#    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


def main():
    """In case we need this"""
    pass


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from glazehub_shawn import app
    connect_to_db(app)
    print "Connected to DB."
