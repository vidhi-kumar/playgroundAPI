"""

This script interacts with a Playground Inventory Portal API using curl commands. 

It enables users to add equipment, update quantities, and view inventory through HTTP requests to the Playground Inventory Portal API using the curl command-line tool. 

The application also allows periodic saving of information on sports equipment with zero quantities in JSON format, providing a record of such equipment over a set duration.

"""

import subprocess
import getpass
import sys
import os
import requests
import json
import time
from datetime import datetime


BASE_URL = "http://127.0.0.1:8000"
access_token = None


# creating new equipment in database using playground api
def create_item():
    try:
        item = input("\nEnter the item name: ")
        quantity = int(input("Enter the item quantity: "))
        
        command_create_item = f"""
        curl -X 'POST' \
        'http://localhost:8000/equipments' \
        -H 'accept: application/json' \
        -H 'Authorization: Bearer {{   "access_token": "{access_token}" }}' \
        -H 'Content-Type: application/json' \
        -d '{{
        "item": "{item}",
        "quantity": {quantity}
        }}'
        """
        try:
            result = subprocess.run(command_create_item, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            response_json = json.loads(result.stdout)
            if 'message' in response_json and response_json['message'] == 'Equipment has been added':
                print("\nEquipment has been added")
            else:
                print("\nSomething went wrong")
        except Exception as e:
            print(e)
    except ValueError as e:
        print("\nInvalid input. Please enter a valid integer.")
        
    
# updating quantity of equipment in database using playground api 
def update_quantity():
    try:
        item = input("Enter the item name: ")
        quantity = int(input("Enter the new quantity: "))
        
        command_update = f"""
        curl -X 'PUT' \
        'http://localhost:8000/equipments' \
        -H 'accept: application/json' \
        -H 'Authorization: Bearer {{   "access_token": "{access_token}" }}' \
        -H 'Content-Type: application/json' \
        -d '{{
        "item": "{item}",
        "quantity": {quantity}
        }}'
        """

        try:
            result = subprocess.run(command_update, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            response_json = json.loads(result.stdout)
            if 'message' in response_json and response_json['message'] == 'Quantity of equipment has been updated':
                print("\nQuantity of equipment has been updated")
            else:
                print("\nEquipement does not exist.")
        except Exception as e:
            print(e)
    except ValueError as e:
        print("\nInvalid input. Please enter a valid integer.")
    

# displaying inventory items using playgroud api
def show_items():
    command_all_items = f"""
    curl -X 'GET' \
    'http://localhost:8000/equipments' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer {{   "access_token": "{access_token}" }}'
    """
    result = subprocess.run(command_all_items, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    try:
        response_json = json.loads(result.stdout)
        if 'message' in response_json and response_json['message'] == 'No equipments found':
            print("\nNo equipments found")
        else:
            print("\nFollowing are all sports equipments:")
            for equipment in response_json['equipments']:
                print(f"{equipment['quantity']} units of {equipment['item']}")

    except Exception as e:
        print(e)
 
    
# displaying inventory items with zero quantity using playground api
def get_items_with_no_quantity():
    command_out_of_stock = f"""
    curl -X 'GET' \
    'http://localhost:8000/equipments/outofstock/' \
    -H 'accept: application/json' \
    -H 'Authorization: Bearer {{   "access_token": "{access_token}" }}'
    """
    result = subprocess.run(command_out_of_stock, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    try:
        response_json = json.loads(result.stdout)
        if 'message' in response_json and response_json['message'] == 'No equipments found':
            print("\nNo equipments found with zero quantity")
        else:
            print("\nFollowing sports equipments have 0 quantity:")
            for equipment in response_json['equipments']:
                print(f"{equipment['item']}")

    except Exception as e:
        print(e)


# signing up user and storing details in database using playground api
def signup():
    global access_token
    name = input("\nEnter your name: ")
    email = input("Enter your email: ")
    password = getpass.getpass("Enter your password: ")
    
    command_signup = f"""
    curl -X 'POST' \
    'http://localhost:8000/user/signup' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d ' {{
        "name": "{name}",
        "email": "{email}",
        "password": "{password}"
    }}'
    """
    
    result = subprocess.run(command_signup, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    try:
        response_json = json.loads(result.stdout)
        access_token = response_json.get('access_token')

        if access_token:
            print("Sign up successful. Logged in")
        else:
            print("Sign up failed.")
    except json.JSONDecodeError:
        print("Error decoding JSON response.")


# logging in users who have been registered using playgroud api
def login():
    global access_token  
    email = input("\nEnter your email: ")
    password = getpass.getpass("Enter your password: ")

    command_login = f"""
    curl -X 'POST' \
    'http://localhost:8000/user/login' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{{
        "email": "{email}",
        "password": "{password}"
    }}'
    """
    
    result = subprocess.run(command_login, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    try:
        response_json = json.loads(result.stdout)
        access_token = response_json.get('access_token')
        # print(access_token)

        if access_token:
            print("\nLogin succesful")
        else:
            print("\nLogin failed")
    except json.JSONDecodeError:
        print("\nError decoding JSON response.")
        

'''periodic saving of information on sports equipment with zero quantities in JSON format, providing a record of such equipment over a set duration.
'''
def save_items_with_no_quantity():
    try:
        num_minutes = int(input("\nEnter number of minutes you want to save zero quantity items for: "))

        log_directory = "/app/ZeroQuantityLogs"
        os.makedirs(log_directory, exist_ok=True)

        for _ in range(int(num_minutes)):
            command_out_of_stock = f"""
            curl -X 'GET' \
            'http://localhost:8000/equipments/outofstock/' \
            -H 'accept: application/json' \
            -H 'Authorization: Bearer {{   "access_token": "{access_token}" }}'
            """

            result = subprocess.run(command_out_of_stock, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            try:
                response_json = json.loads(result.stdout)
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                file_name = f"{log_directory}/empty_equipments_{timestamp}.json"

                with open(file_name, 'w') as json_file:
                    log_data = {
                        "timestamp": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                        "data": {}
                    }
                    if 'message' in response_json and response_json['message'] == 'No equipments found':
                        log_data["data"]["message"] = "No equipments found with zero quantity"
                        json.dump(log_data, json_file, indent=2)
                        print("\nNo equipments found with zero quantity")
                    else:
                        equipment_list = [{"item": equipment['item']} for equipment in response_json['equipments']]
                        log_data["data"]["equipments"] = equipment_list
                        json.dump(log_data, json_file, indent=2)
                        print("\nFollowing sports equipments have 0 quantity:")
                        for equipment in response_json['equipments']:
                            print(f"{equipment['item']}")
            except json.JSONDecodeError:
                print("\nError decoding JSON response.")

            time.sleep(60)
    except ValueError:
        print("\nInvalid input. Please enter a valid number.")

 


def main_menu():
    print("\nPlayground Inventory Portal")
    if access_token:
        print("\n1. Show my inventory")
        print("2. Add an equipment")
        print("3. Update Sports Equipement Quantity")
        print("4. Display Sports Equipments with Zero Quantity")
        print("5. Save Zero quantity Equipments json each minute for next n minutes")
    else:
        print("\n6. Signup")
        print("7. Login")
    
    print("8. Exit")



if __name__ == "__main__":
    while True:
        main_menu()
        choice = input("\nEnter your choice: ")

        if choice == "1":
            show_items()
        elif choice == "2":
            create_item()
        elif choice == "3":
            update_quantity()
        elif choice == "4":
            get_items_with_no_quantity()
        elif choice == "5":
            save_items_with_no_quantity()
        elif choice == "6" and access_token is None:
            signup()
        elif choice == "7" and access_token is None:
            login()
        elif choice == "8":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")
