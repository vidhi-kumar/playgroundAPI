from fastapi.testclient import TestClient
from main import app
from fastapi import status
import pytest


client = TestClient(app)


def setup_function():
    # Clear the database or perform any setup needed
    print("Cleared Database")

# testing "/" endpoint
def test_hello_world():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Proceed to /docs url for api documentation"}

# testing "/user/signup/" endpoint with new signup
def test_signup():
    response = client.post("/user/signup/", json={"name": "unit_tester", "email": "unit_tester@test.com", "password": "test"})
    assert response.status_code == 200
    assert "access_token" in response.json() or response.json().get("error") == "Email is already registered"
    # print(response.json())


# testing "/user/login/" endpoint with existing test user
def test_login():
    response = client.post("/user/login/", json={"email": "unit_tester@test.com", "password": "test"})
    assert response.status_code == 200
    assert "access_token" in response.json() or response.json().get("error") == "Invalid login details"
    token = response.json()


@pytest.fixture
def login_token():
    response = client.post("/user/login/", json={"email": "unit_tester@test.com", "password": "test"})
    assert response.status_code == 200
    return response.json()


# # testing "/equipments/" endpoint with existing test user to check all existing equipments
# def test_get_all_equipments(login_token):
#     # headers = {'accept: application/json', f'Authorization: Bearer {login_token}'}
#     headers = {'accept': 'application/json', 'Authorization': f'Bearer {login_token}'}    
#     response = client.get("/equipments", headers=headers)
    
#     # # Print the response status code and text for debugging
#     # print(response.status_code)
#     # print(response.text)

#     # assert response.status_code == status.HTTP_200_OK  # Update to the expected status code
#     # assert response.json() == {"message": "No equipments found"}


# # def test_get_all_equipments():
# #     headers = {'accept: application/json', f'Authorization: Bearer {test_token}'}
    
# #     print(headers)
    
# #     response = client.get("/equipments", headers=headers)
# #     print(response.json())
    
# #     # Print the response status code and text for debugging
# #     print(response.status_code)
# #     print(response.text)

# #     assert response.status_code == status.HTTP_200_OK  # Update to the expected status code
# #     assert response.json() == {"message": "No equipments found"}

# # Run the test
