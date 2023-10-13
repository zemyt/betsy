import models
import os
from data import user_data, tag_data


def main():
    delete_database()
    setup_test_database()
    populate_test_database()
    ...


def setup_test_database():
    models.db.connect()
    models.db.create_tables(
        [
            models.Tag,
            models.Product,
            models.Address,
            models.BillingInformation,
            models.Transaction,
            models.User,
            models.ProductTagThrough,
            models.UserProductThrough,
        ],
        safe=True,
    )


def populate_test_database():
    database_filename = "database.db"
    if not os.path.isfile(database_filename):
        print("Database file doesn't exist. Creating new database...")
        setup_test_database()

    # Fills the tag table with tags provided above.
    for tag_name in tag_data:
        tag_name_lower = tag_name.lower()
        tag, created = models.Tag.get_or_create(tag=tag_name_lower)

    # Fills database with data
    for user_info in user_data:
        user, address_info, billing_info, products_info = user_info

        # Create Address instance
        address = models.Address.create(
            street=address_info[0],
            city=address_info[1],
            state=address_info[2],
            postal_code=address_info[3],
            country=address_info[4],
        )

        # Create BillingInformation instance
        billing_information = models.BillingInformation.create(
            card_number=billing_info[0],
            expiration_date=billing_info[1],
            billing_address=address,
        )

        # Create User instance
        user_instance = models.User.create(
            name=user, address=address, billing_information=billing_information
        )
        # Create Products instances
        for product_info in products_info:
            (
                product_name,
                product_description,
                product_price,
                product_quantity,
                product_tags,
            ) = product_info

            product = models.Product.create(
                name=product_name,
                description=product_description,
                price_per_unit=product_price,
                quantity=product_quantity,
            )

            # Insert records into the product_tag_through table
            for tag_name in product_tags:
                tag_name_lower = tag_name.lower()
                tag, created = models.Tag.get_or_create(tag=tag_name_lower)
                if tag not in product.tags:
                    product.tags.add(tag)

            user_instance.inventory.add(product)


def delete_database():
    cwd = os.getcwd()
    database_path = os.path.join(cwd, "database.db")
    if os.path.exists(database_path):
        os.remove(database_path)


if __name__ == "__main__":
    main()
