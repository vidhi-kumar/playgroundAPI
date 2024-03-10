from fastapi.testclient import TestClient
from main import app
from fastapi import status


client = TestClient(app)

def setup_function():
    # Clear the database or perform any setup needed
    print("Cleared Database")
    
def test_hello_world():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Proceed to /docs url for api documentation"}


# def test_get_all_equipments():
#     headers = {'accept: application/json', f'Authorization: Bearer {test_token}'}
    
#     print(headers)
    
#     response = client.get("/equipments", headers=headers)
#     print(response.json())
    
#     # Print the response status code and text for debugging
#     print(response.status_code)
#     print(response.text)

#     assert response.status_code == status.HTTP_200_OK  # Update to the expected status code
#     assert response.json() == {"message": "No equipments found"}

# Run the test
