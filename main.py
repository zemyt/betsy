import peewee
import models
import logging
from models import *
from peewee import SqliteDatabase, IntegrityError
from fuzzywuzzy import fuzz
from datetime import datetime
from data import (
    ProductData,
    blue_backack,
    wireless_earbuds,
    gourmet_coffee_beans,
)

# Do not modify these lines
__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"


db = SqliteDatabase("database.db")
db.connect()
logging.basicConfig(
    filename="error.log",
    level=logging.ERROR,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


"""
Before running this code, make sure to install the required packages
using the following commands:
pip install fuzzywuzzy
pip install python-Levenshtein
"""


def main():
    # search("searchterm")

    # list_user_products(1)

    # list_products_per_tag(1)

    # add_product_to_catalog(1, gourmet_coffee_beans)

    # update_stock(1, 1)

    # purchase_product(2, 5, 1)

    # remove_product(20)

    # get_transaction(1)

    ...


# Search for products in catalog based on name/description
def search(searchterm: str):
    if not isinstance(searchterm, str):
        searchterm = str(searchterm)

    try:
        results = Product.select()
        matched_results = []

        for product in results:
            name_score = fuzz.token_set_ratio(searchterm.lower(), product.name.lower())
            description_score = fuzz.token_set_ratio(
                searchterm.lower(), product.description.lower()
            )
            if (
                name_score >= 65
                or description_score >= 65
                or (searchterm.lower() in product.name.lower() and len(searchterm) >= 3)
                or (
                    searchterm.lower() in product.description.lower()
                    and len(searchterm) >= 3
                )
            ):
                matched_results.append(product)
        if matched_results:
            print("Search results:")
            for product in matched_results:
                print(f"Product: {product.name}")
        else:
            print(f"No products found that match your search term.")
    except peewee.OperationalError as e:
        error_message = f"An error occurred: {str(e)}"
        logging.error(error_message, exc_info=True)
        print(error_message)


# View the products of a given user.
def list_user_products(user_id: int):
    if not isinstance(user_id, int):
        return print("user_id must be an integer.")

    try:
        user = User.get(User.id == user_id)
        query = user.inventory.select(  # Get the inventory for the user
            Product.name, Product.description, Product.price_per_unit, Product.quantity
        )
        products = list(query)  # Fetch the actual usable product data from the database
        if products:
            print(f"Product(s) from {user.name}:")
            for product in products:
                if product.quantity > 0:
                    print(f"Product Name: {product.name}")
                    print(f"Description: {product.description}")
                    print(f"Price: €{product.price_per_unit}")
                    print(f"Quantity: {product.quantity}")
        else:
            print(f"No products found for user {user.name}.")
    except User.DoesNotExist:
        error_message = f"User with ID [{user_id}] does not exist."
        logging.error(error_message, exc_info=True)
        print(error_message)


# View all products for a given tag.
def list_products_per_tag(tag_id: int):
    if not isinstance(tag_id, int):
        return print("tag_id must be an integer.")

    try:
        tag = Tag.get(Tag.id == tag_id)
        query = (
            Product.select().join(ProductTagThrough).join(Tag).where(Tag.id == tag_id)
        )  # Peewee query object that specifies the conditions and columns to select.
        products = list(
            query
        )  # Execute the query and fetch the actual product data from the database.
        if products:
            print(f"Products with tag: {tag.tag}")
            for product in products:
                if product.quantity > 0:
                    print(f"Product: {product.name} - Product ID:{product.id}")
        else:
            print(f"No products with tag: {tag.tag}.")
    except Tag.DoesNotExist:
        error_message = f"Tag with ID [{tag_id}] does not exist."
        logging.error(error_message, exc_info=True)
        print(error_message)


# Add product to a user. Takes in a product instance from ProductData and adds it to the database to the user
def add_product_to_catalog(user_id: int, product: ProductData):
    if not isinstance(user_id, int):
        return print("user_id must be an integer.")

    try:  # Check if user_id exits
        user = User.get(User.id == user_id)
    except User.DoesNotExist:
        error_message = f"User with ID [{user_id}] does not exist."
        logging.error(error_message, exc_info=True)
        print(error_message)
        return

    if not isinstance(product, ProductData):  # Check if data given is correct
        return print("Product should be an instance of ProductData")

    product.price_per_unit = round(product.price_per_unit, 2)
    # Check is the product already exists
    existing_product = user.inventory.filter(
        (Product.name == product.name)
        & (Product.description == product.description)
        & (Product.price_per_unit == product.price_per_unit)
    ).first()

    if existing_product:
        existing_product.quantity += product.quantity
        existing_product.save()
        return print(
            f"({product.name}) already exists in inventory, updated quantity from ({existing_product.quantity - product.quantity}) to ({existing_product.quantity})"
        )

    else:
        # Create Product instance
        product_model = models.Product.create(
            name=product.name,
            description=product.description,
            price_per_unit=product.price_per_unit,
            quantity=product.quantity,
        )

        # Insert records into the product_tag_through table
        if product.tags:
            for tag_name in product.tags:
                tag_name_lower = tag_name.lower()
                tag, created = models.Tag.get_or_create(tag=tag_name_lower)
                if tag not in product_model.tags:
                    product_model.tags.add(tag)

        # Add the product to user's inventory
        user.inventory.add(product_model)
        db.commit()
        return print(f"Successfully added ({product.name}) to inventory.")


# Update(set) the stock quantity of a product.
def update_stock(product_id: int, new_quantity: int):
    # check for int
    if not isinstance(product_id, int):
        return print("product_id should be an integer")
    if not isinstance(new_quantity, int):
        return print("new_quantity should be a integer")

    try:
        product = Product.get(Product.id == product_id)
        # print(f"Product: {product.name} - Product ID: {product.id}")
        # print(f"Old quantity: {product.quantity}")
        if new_quantity >= 0:
            print(f"Product: {product.name} - Product ID: {product.id}")
            print(f"Old quantity: {product.quantity}")
            print(f"New quantity: {new_quantity}")
            product.quantity = new_quantity
            product.save()
        else:
            print("New quantity must be a positive number or 0.")

    except Product.DoesNotExist:
        error_message = f"Product ID [{product_id}] does not exist."
        logging.error(error_message, exc_info=True)
        print(error_message)


# Handle a purchase between a buyer and a seller for a given product
def purchase_product(product_id: int, buyer_id: int, quantity: int):
    if not isinstance(product_id, int):
        return print("product_id should be an integer")
    if not isinstance(buyer_id, int):
        return print("buyer_id should be a integer")
    if not isinstance(quantity, int):
        return print("quantity should be a integer")

    try:
        product = Product.get(Product.id == product_id)
        buyer = User.get(User.id == buyer_id)
        seller = (
            User.select()
            .join(UserProductThrough)
            .where(UserProductThrough.product == product)
            .get()
        )
        if buyer == seller:
            return print(f"Buyer and seller are the same user.")

        if product.quantity >= quantity:
            Transaction.create(
                buyer=buyer,
                product=product,
                quantity=quantity,
                product_name=product.name,  # Add the product name as a backup for when product gets deleted
                date_of_purchase=datetime.now(),
            )
            product.quantity -= quantity
            product.save()
            print(f"Successfully purchased {product.name}.")
        else:
            print(f"Not enough quantity, current stock: {product.quantity}.")

    except Product.DoesNotExist:
        error_message = f"Product ID [{product_id}] does not exist."
        logging.error(error_message, exc_info=True)
        print(error_message)
    except User.DoesNotExist:
        error_message = "Invalid buyer or seller ID."
        logging.error(error_message, exc_info=True)
        print(error_message)


# Remove a product from a user.
def remove_product(product_id: int):
    if not isinstance(product_id, int):
        return print("product_id must be an integer.")

    try:
        product = Product.get(Product.id == product_id)
        if product:
            try:
                UserProductThrough.delete().where(
                    UserProductThrough.product == product
                ).execute()  # Also Delete the product from the UserProductThrough, avoiding duplicate IDs / errors

                product.delete_instance()
                print(f"Successfully deleted: {product.name}.")
            except IntegrityError as e:
                error_message = f"Failed to delete product: {product.name}."
                logging.error(error_message, exc_info=True)
                print(error_message)
    except Product.DoesNotExist:
        error_message = f"Product ID [{product_id}] does not exist."
        logging.error(error_message, exc_info=True)
        print(error_message)


def get_transaction(transaction_id: int):
    if not isinstance(transaction_id, int):
        return print("transaction_id must be an integer.")

    try:
        transaction = Transaction.get(Transaction.id == transaction_id)
        try:
            product = transaction.product
            if product:
                print(
                    f"Transaction ID: {transaction.id} - Bought by user ID: {transaction.buyer}"
                )
                print(
                    f"Date of purchase: {transaction.date_of_purchase.strftime('%Y-%m-%d')} - Product: {product.name} - Quantity: {transaction.quantity}"  # ADD PRICE?
                )
            else:
                print("Product no longer exists in the database")
        except Product.DoesNotExist:
            # When original product has beed deleted from the Product table in the database
            print(
                f"Transaction ID: {transaction.id} - Bought by user ID: {transaction.buyer}"
            )
            print(
                f"Date of purchase: {transaction.date_of_purchase.strftime('%Y-%m-%d')} - Product: {transaction.product_name} - Quantity: {transaction.quantity}"
            )
    except Transaction.DoesNotExist:
        error_message = f"Transaction with ID [{transaction_id}] does not exist."
        logging.error(error_message, exc_info=True)
        print(error_message)


if __name__ == "__main__":
    main()
