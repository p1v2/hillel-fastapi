# Request with basic auth
import json

import requests

# response = requests.get("http://localhost:8000/books")
# print(response.json())

# # Create a book
# response = requests.post(
#     "http://localhost:8000/books",
#     json={
#         "title": "The Great Gatsby",
#         "author": "F. Scott Fitzgerald",
#     },
# )
# print(response.json())

# Update a book
data = {'title': 'New Title', "author": "New Author"}
response = requests.patch(
    "http://localhost:8000/books/2",
    json=data
)
print(response.status_code)
print(response.text)

# Delete a book
# response = requests.delete('http://localhost:8000/books/3')
# print(response.status_code)
# print(response.text)

# Find a book
# response = requests.get('http://localhost:8000/books/2')
# print(response.status_code)
# print(response.text)
