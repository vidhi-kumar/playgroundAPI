from fastapi.testclient import TestClient
from main import app
from fastapi import status

# # This token has validity for 30 days from 4th April onwards
# test_token = {"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySUQiOiJ0ZXN0QHRlc3QuY29tIiwiZXhwaXJ5IjoxNzEwMTYwMDM1LjE3Njk3N30.JMpyNoKEuPK-VdfTA4CgmXuwwDRsn3Hdow-15iOChY0"}


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
