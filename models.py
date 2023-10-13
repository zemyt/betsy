# This file defines the database models using the Peewee ORM
import peewee
from peewee import SQL


db = peewee.SqliteDatabase("database.db")


class Tag(peewee.Model):
    tag = peewee.CharField(unique=True)

    class Meta:
        database = db


class Product(peewee.Model):
    name = peewee.CharField(null=False)
    description = peewee.CharField(null=False)
    price_per_unit = peewee.DecimalField(max_digits=10, decimal_places=2, null=False)
    quantity = peewee.IntegerField(null=False)
    tags = peewee.ManyToManyField(Tag, backref="products")

    class Meta:
        database = db


class Address(peewee.Model):
    street = peewee.CharField(null=False)
    city = peewee.CharField(null=False)
    state = peewee.CharField(null=False)
    postal_code = peewee.CharField(null=False)
    country = peewee.CharField(null=False)

    class Meta:
        database = db


class BillingInformation(peewee.Model):
    card_number = peewee.CharField()
    expiration_date = peewee.DateField()
    billing_address = peewee.ForeignKeyField(Address)

    class Meta:
        database = db


class User(peewee.Model):
    name = peewee.CharField(null=False)
    address = peewee.ForeignKeyField(Address, null=False)
    billing_information = peewee.ForeignKeyField(BillingInformation)
    inventory = peewee.ManyToManyField(Product)

    class Meta:
        database = db


class Transaction(peewee.Model):
    buyer = peewee.ForeignKeyField(User)
    product = peewee.ForeignKeyField(Product)
    quantity = peewee.IntegerField()
    product_name = peewee.CharField()
    date_of_purchase = peewee.DateTimeField(
        constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")]
    )

    class Meta:
        database = db


ProductTagThrough = Product.tags.get_through_model()
UserProductThrough = User.inventory.get_through_model()
