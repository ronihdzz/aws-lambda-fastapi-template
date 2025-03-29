import unittest
from fastapi.testclient import TestClient
from main import app
from api.v1.endpoints import books_db, counter_id

class TestBooksAPI(unittest.TestCase):
    def setUp(self):
        # Reset global state before each test
        global books_db, counter_id
        books_db.clear()
        counter_id = 0
        self.client = TestClient(app)
    
    def test_read_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Books API 📚"})
    
    def test_get_books_empty(self):
        response = self.client.get("/books")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
    
    def test_create_book(self):
        payload = {"title": "Test Book", "author": "Author A", "year": 2020}
        response = self.client.post("/books", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["title"], payload["title"])
        self.assertEqual(data["author"], payload["author"])
        self.assertEqual(data["year"], payload["year"])
    
    def test_get_book(self):
        # First create a book
        payload = {"title": "Test Book", "author": "Author A", "year": 2020}
        create_response = self.client.post("/books", json=payload)
        book_id = create_response.json()["id"]
        
        # Retrieve the created book
        response = self.client.get(f"/books/{book_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], book_id)
        self.assertEqual(data["title"], payload["title"])
    
    def test_update_book(self):
        # Create a book
        payload = {"title": "Old Title", "author": "Author A", "year": 2020}
        create_response = self.client.post("/books", json=payload)
        book_id = create_response.json()["id"]
        
        # Update the book
        updated_payload = {"title": "New Title", "author": "Author B", "year": 2021}
        response = self.client.put(f"/books/{book_id}", json=updated_payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], book_id)
        self.assertEqual(data["title"], updated_payload["title"])
        self.assertEqual(data["author"], updated_payload["author"])
        self.assertEqual(data["year"], updated_payload["year"])
    
    def test_delete_book(self):
        # Create a book to delete later
        payload = {"title": "Delete Me", "author": "Author A", "year": 2020}
        create_response = self.client.post("/books", json=payload)
        book_id = create_response.json()["id"]
        
        # Delete the book
        response = self.client.delete(f"/books/{book_id}")
        self.assertEqual(response.status_code, 204)
        
        # Verify the book no longer exists
        get_response = self.client.get(f"/books/{book_id}")
        self.assertEqual(get_response.status_code, 404)
        self.assertEqual(get_response.json()["detail"], "Book not found")
    
    def test_get_nonexistent_book(self):
        response = self.client.get("/books/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Book not found")
    
    def test_update_nonexistent_book(self):
        updated_payload = {"title": "New Title", "author": "Author B", "year": 2021}
        response = self.client.put("/books/999", json=updated_payload)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Book not found")
    
    def test_delete_nonexistent_book(self):
        response = self.client.delete("/books/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Book not found")
    
    def test_openapi_schema(self):
        response = self.client.get("/openapi.json")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Verify that the openapi version is the forced one
        self.assertEqual(data["openapi"], "3.0.3")
        self.assertEqual(data["info"]["title"], "Books API")
        self.assertEqual(data["info"]["version"], "1.0.0")
