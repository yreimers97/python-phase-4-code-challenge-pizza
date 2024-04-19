from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    # add relationship
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates = 'restaurant', cascade='all')

    # add serialization rules
    # serialize_rules = ('-restaurantpizzas.restaurant',)

    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # add relationship
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates = 'pizza', cascade='all')

    # add serialization rules
    # serialize_rules = ('-restaurantpizzas.pizza',)

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))

    # add relationships
    restaurant = db.relationship('Restaurant', back_populates = 'restaurant_pizzas')
    pizza = db.relationship('Pizza', back_populates = 'restaurant_pizzas')

    # add serialization rules
    # serialize_rules = ('-restaurant.restaurantpizzas', '-pizza.restaurantpizzas',)

    # add validation
    @validates('price')
    def validate_price(self, attr, value):
        if not value or not(1 <= value <= 30):
            raise ValueError(f'{attr} must be between 1 and 30')
        else:
            return value

    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"