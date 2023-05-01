
# Request with basic auth
import requests

# response = requests.get("http://localhost:8000/books")
# print(response.json())

# Create a book
response = requests.post(
    "http://localhost:8000/books",
    json={
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
    },
)
print(response.json())

