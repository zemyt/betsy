# This file contains sample data


class ProductData:
    def __init__(
        self,
        name: str,
        description: str,
        price_per_unit,
        quantity: int = 1,
        tags: list = ["unknown"],
    ):
        if not isinstance(name, str):
            raise ValueError("Product name must be a string.")
        if not isinstance(description, str):
            raise ValueError("Product description must be a string.")
        if not (isinstance(price_per_unit, (int, float)) and price_per_unit > 0):
            raise ValueError("Product price_in_unit needs to be a positive number.")
        if not (isinstance(quantity, int) and quantity > 0):
            raise ValueError("Product quantity needs to be a postive integer.")
        if not isinstance(tags, (list, tuple)):
            raise ValueError("Product tags must be in a list format(or tuple).")

        self.name = name
        self.description = description
        self.price_per_unit = price_per_unit
        self.quantity = quantity
        self.tags = tags


blue_backack = ProductData(
    "Blue Backpack",
    "A spacious and durable backpack for all your adventures.",
    40,
    10,
    ("Travel", "Outdoor"),
)

wireless_earbuds = ProductData(
    "Wireless Earbuds",
    "High-quality wireless earbuds with noise-cancelling feature.",
    80,
    15,
    ("Electronics", "Audio"),
)

gourmet_coffee_beans = ProductData(
    "Gourmet Coffee Beans",
    "Premium Arabica coffee beans for the perfect cup of coffee.",
    12.99,
    50,
    ("Beverages", "Coffee"),
)

user_data = [
    (
        ("Anna Adams"),
        ("123 Main Street", "Anytown", "Astate", "12345", "United States"),
        ("1234567890", "2050-12-12"),
        [
            (
                "Laptop",
                "High-performance laptop with SSD storage",
                999.9999,
                10,
                ["electronics", "computers"],
            ),
            (
                "Coffee Maker",
                "Automatic coffee maker with built-in grinder",
                80.66666,
                5,
                ["appliances", "kitchen"],
            ),
        ],
    ),
    (
        ("Benjamin Bond"),
        ("123 Birch Street", "Brooklyn", "NY", "11201", "United States"),
        ("0987654321", "2050-12-12"),
        [
            (
                "Backpack",
                "Durable backpack with multiple compartments",
                50,
                12,
                ["outdoor", "travel"],
            ),
            (
                "Guitar",
                "Acoustic guitar with a beautiful wooden finish",
                300,
                3,
                ["music", "instruments"],
            ),
        ],
    ),
    (
        ("Catherine Clark"),
        ("456 Cedar Avenue", "Chicago", "IL", "60601", "United States"),
        ("5432109876", "2030-12-12"),
        [
            (
                "Hiking Boots",
                "Waterproof hiking boots for outdoor adventures",
                129.95,
                20,
                ["footwear", "outdoor"],
            ),
            (
                "Yoga Mat",
                "Non-slip yoga mat for home workouts",
                19.99,
                25,
                ["fitness", "health"],
            ),
        ],
    ),
    (
        ("David Davis"),
        ("1234 Dover Street", "Denver", "CO", "80202", "United States"),
        ("2109854376", "2090-12-12"),
        [
            (
                "Dumbbells",
                "Set of adjustable dumbbells for strength training",
                149.00,
                18,
                ["fitness", "exercise"],
            ),
            (
                "Cookbook",
                "Bestselling cookbook with a variety of recipes",
                24.95,
                40,
                ["books", "cooking"],
            ),
        ],
    ),
    (
        ("Emily Evans"),
        ("5678 Oak Avenue", "Eugene", "OR", "97401", "United States"),
        ("2105498376", "2030-11-11"),
        [
            (
                "Smartphone",
                "Latest smartphone with a high-resolution camera",
                699.00,
                30,
                ["electronics", "phones"],
            ),
            (
                "Bluetooth Speaker",
                "Portable Bluetooth speaker with deep bass",
                59.95,
                22,
                ["electronics", "audio"],
            ),
        ],
    ),
]


tag_data = [
    "Electronics",
    "Computers",
    "Clothing",
    "Sports",
    "Books",
    "Toys",
    "Shoes",
    "Beauty",
    "Audio",
]
