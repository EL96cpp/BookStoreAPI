from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from reviews.models import Review
from books.models import Book
from customers.models import Customer


class ReviewsTestView(APITestCase):

    def setUp(self):
        customer1 = Customer.objects.create(username="user1", password="qwerty1234qwerty",
                                            first_name="Joe", last_name="Simpson")
        customer2 = Customer.objects.create(username="user2", password="qwerty1234qwerty",
                                            first_name="Dan", last_name="Cooper")
    
        self.token_customer1 = Token.objects.create(user=customer1)
        self.token_customer2 = Token.objects.create(user=customer2)

        self.book1 = Book.objects.create(author="D.B.Cooper", title="Example title", price=2400.00, discount=0)
        self.book2 = Book.objects.create(author="N.B.Siemens", title="Example title2", price=1200.00, discount=50)


    def test_unauthorized_get_reviews(self):
        response = self.client.get(reverse("reviews"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    
    def test_authorized_get_empty_reviews(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_customer1.key)
        response = self.client.get(reverse("reviews"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)
    

    def test_authorized_create_reviews(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_customer1.key)
        response_book1 = self.client.post("/api/v1/add-review/1", {"review": "Great book!", "rating": 5})
        response_book2 = self.client.post("/api/v1/add-review/2", {"review": "Good book!", "rating": 4})

        self.assertEqual(response_book1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_book2.status_code, status.HTTP_201_CREATED)


    def test_authorized_get_reviews(self):
        # Make 2 reviews on books with id 1 and 2 as customer1
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_customer1.key)
        response_book1 = self.client.post("/api/v1/add-review/1", {"review": "Great book!", "rating": 5})
        response_book2 = self.client.post("/api/v1/add-review/2", {"review": "Good book!", "rating": 4})
        self.assertEqual(response_book1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_book2.status_code, status.HTTP_201_CREATED)

        # Check reviews as customer2
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_customer2.key)
        response_reviews1 = self.client.get("/api/v1/book-reviews/1")
        response_reviews2 = self.client.get("/api/v1/book-reviews/2")
        self.assertEqual(response_reviews1.status_code, status.HTTP_200_OK)
        self.assertEqual(response_reviews2.status_code, status.HTTP_200_OK)
        self.assertEqual(response_reviews1.data["results"][0]["customer"], 1)
        self.assertEqual(response_reviews2.data["results"][0]["customer"], 1)
        self.assertEqual(response_reviews1.data["results"][0]["rating"], 5)
        self.assertEqual(response_reviews2.data["results"][0]["rating"], 4)
        self.assertEqual(response_reviews1.data["results"][0]["review"], "Great book!")
        self.assertEqual(response_reviews2.data["results"][0]["review"], "Good book!")
        self.assertEqual(response_reviews1.data["results"][0]["book"], 1)
        self.assertEqual(response_reviews2.data["results"][0]["book"], 2)

        response_my_reviews = self.client.get(reverse("reviews"))
        self.assertEqual(len(response_my_reviews.data["results"]), 0)

    
    def test_only_one_review_per_book(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_customer1.key)
        response_book1 = self.client.post("/api/v1/add-review/1", {"review": "Great book!", "rating": 5})
        response_book2 = self.client.post("/api/v1/add-review/1", {"review": "Good book!", "rating": 4})
        self.assertEqual(response_book1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_book2.status_code, status.HTTP_403_FORBIDDEN)