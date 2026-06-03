
import os
import django
import random

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'config.settings'
)

django.setup()

from django.contrib.auth.models import User
from store.models import Category, Product, Review


# CLEAN OLD DATA

Review.objects.all().delete()
Product.objects.all().delete()
Category.objects.all().delete()


# CATEGORIES

categories = [
    "Electronics",
    "Fashion",
    "Home & Kitchen",
    "Beauty",
    "Sports",
    "Books",
    "Gaming",
    "Accessories"
]

category_objects = {}

for category_name in categories:

    category = Category.objects.create(
        name=category_name,
        image=f"https://picsum.photos/300/200?random={random.randint(1,1000)}"
    )

    category_objects[category_name] = category


# PRODUCTS

products_data = {

    "Electronics": [
        "iPhone 15 Pro",
        "Samsung Galaxy S25",
        "OnePlus 13",
        "Sony Headphones",
        "MacBook Air M4",
        "Dell XPS Laptop",
        "Apple Watch",
        "Bluetooth Speaker",
        "Gaming Monitor",
        "Wireless Earbuds"
    ],

    "Fashion": [
        "Men T-Shirt",
        "Women Hoodie",
        "Denim Jacket",
        "Sports Shoes",
        "Sneakers",
        "Formal Shirt",
        "Leather Belt",
        "Cargo Pants",
        "Summer Dress",
        "Track Suit"
    ],

    "Home & Kitchen": [
        "Mixer Grinder",
        "Coffee Machine",
        "Air Fryer",
        "Dinner Set",
        "Vacuum Cleaner",
        "Electric Kettle",
        "Water Purifier",
        "Rice Cooker",
        "Microwave Oven",
        "Kitchen Knife Set"
    ],

    "Beauty": [
        "Face Wash",
        "Hair Dryer",
        "Lipstick",
        "Skin Serum",
        "Body Lotion",
        "Perfume",
        "Face Cream",
        "Beard Oil",
        "Hair Straightener",
        "Sunscreen"
    ],

    "Sports": [
        "Cricket Bat",
        "Football",
        "Basketball",
        "Gym Gloves",
        "Yoga Mat",
        "Dumbbell Set",
        "Tennis Racket",
        "Cycling Helmet",
        "Sports Bottle",
        "Running Shoes"
    ],

    "Books": [
        "Atomic Habits",
        "Rich Dad Poor Dad",
        "Think And Grow Rich",
        "Deep Work",
        "Python Programming",
        "Clean Code",
        "The Psychology Of Money",
        "The Alchemist",
        "Ikigai",
        "Power Of Habit"
    ],

    "Gaming": [
        "PlayStation 5",
        "Xbox Series X",
        "Gaming Mouse",
        "Gaming Keyboard",
        "Gaming Chair",
        "Graphics Card",
        "VR Headset",
        "Gaming Controller",
        "Mechanical Keyboard",
        "Gaming Desk"
    ],

    "Accessories": [
        "Leather Wallet",
        "Travel Bag",
        "Laptop Sleeve",
        "Power Bank",
        "Phone Cover",
        "Smart Backpack",
        "Sunglasses",
        "Watch Strap",
        "USB Hub",
        "Portable SSD"
    ]
}


brands = [
    "Apple",
    "Samsung",
    "Sony",
    "Nike",
    "Adidas",
    "Puma",
    "OnePlus",
    "Dell",
    "HP",
    "Lenovo"
]


all_products = []

for category_name, items in products_data.items():

    category = category_objects[category_name]

    for item in items:

        product = Product.objects.create(

            category=category,

            name=item,

            brand=random.choice(brands),

            description=f"""
Premium quality {item}.

High performance.
Best seller product.
Trusted by thousands of customers.
Perfect choice for daily use.
""",

            price=random.randint(5000, 100000),

            discount=random.randint(5, 50),

            stock=random.randint(10, 250),

            rating=round(
                random.uniform(3.5, 5.0),
                1
            ),

            featured=random.choice(
                [True, False]
            ),

            image=f"https://picsum.photos/600/600?random={random.randint(1,9999)}"
        )

        all_products.append(product)


# REVIEWS

users = list(User.objects.all())

if users:

    comments = [

        "Amazing product.",
        "Worth the money.",
        "Highly recommended.",
        "Very good quality.",
        "Excellent purchase.",
        "Fast delivery.",
        "Best product in this range.",
        "Satisfied with quality.",
        "Looks premium.",
        "Will buy again."
    ]

    for product in random.sample(
        all_products,
        min(25, len(all_products))
    ):

        for _ in range(
            random.randint(1, 4)
        ):

            Review.objects.create(

                product=product,

                user=random.choice(users),

                rating=random.randint(3, 5),

                comment=random.choice(comments)
            )


print("=" * 50)
print("SUCCESS")
print(f"Categories: {Category.objects.count()}")
print(f"Products: {Product.objects.count()}")
print(f"Reviews: {Review.objects.count()}")
print("=" * 50)
