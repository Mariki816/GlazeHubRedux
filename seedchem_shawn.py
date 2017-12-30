# from pprint import pprint
import model_shawn
import csv
from model_shawn import connect_to_db, db, Chem, User, Component, Recipe
from glazehub_shawn import app


def load_chems():

    for i, row in enumerate(open('chemlist121114b.csv')):
        row = row.rstrip()
        chem_name, quarter, half, onelb, fivelb, tenlb, twentyfivelb, fiftylb, onehundlb, fivehundlb = row.split(',')

        chem = Chem(chem_name = chem_name,
                    quarter = quarter,
                    half = half,
                    onelb = onelb,
                    fivelb = fivelb,
                    tenlb = tenlb,
                    twentyfivelb = twentyfivelb,
                    fiftylb = fiftylb,
                    onehundlb = onehundlb,
                    fivehundlb = fivehundlb)
        db.session.add(chem)

    db.session.commit()


def load_recipes():
    for i, row in enumerate(open('testfiles/recipes.csv')):
        row = row.rstrip()
        recipe_name, user_id, user_notes = row.split(',')

        recipe = Recipe(recipe_name = recipe_name,
                        user_id = user_id,
                        user_notes = user_notes)
        db.session.add(recipe)
    db.session.commit()


def load_users():
    for i, row in enumerate(open('testfiles/usertest.csv')):
        row = row.rstrip()
        user_name, email, password = row.split(',')

        user = User(user_name = user_name,
                    email = email,
                    password = password)
        db.session.add(user)
    db.session.commit()


def load_components():
    for i, row in enumerate(open('testfiles/components.csv')):
        row = row.rstrip()
        chem_id, recipe_id, percentage = row.split(',')

        component = Component(chem_id = chem_id,
                              recipe_id = recipe_id,
                              percentage = percentage)
        db.session.add(component)
    db.session.commit()




if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_chems()