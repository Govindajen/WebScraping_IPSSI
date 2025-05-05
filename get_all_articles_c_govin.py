
from pymongo import MongoClient


def get_articles_by_category_or_subcategory(category=None, sub_category=None):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["ipssi-scrapping"]
    articles_collection = db["articles"]

    query = {}
    if category:
        query["category"] = category
    if sub_category:
        query["sub_category"] = sub_category

    articles = articles_collection.find(query)
    return list(articles)

category = "Marketing"
sub_category = None

articles = get_articles_by_category_or_subcategory(category=category, sub_category=sub_category)

for article in articles:
    print(f"Title: {article['title']}")
    print(f"Category: {article['category']}")
    print(f"Sub-category: {article['sub_category']}")
    print(f"Author: {article['author']}")
    print(f"Date: {article['date']}")
    print(f"Summary: {article['summary']}")
    print(f"Content: {article['content']}")
    print("-" * 80)
