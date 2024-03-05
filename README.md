## playgroundAPI - One stop solution for managing your sports inventory


![pexels-pixabay-248547](https://github.com/vidhi-kumar/playgroundAPI/assets/55309127/b9359bbd-cf88-4e52-bf25-eef6e5e12526)


Welcome to the Playground APIs repository!<br>
This project provides a set of authenticated APIs for testing and experimenting with various features.<br> 
Each registered user receives an isolated dashboard to manage their inventory.
The APIs are connected to relational database and containerized, allowing easy deployment and testing locally.<br>
The project is designed to be flexible, with mounted volumes for making changes and a convenient script for interacting with the APIs.

## Getting Started

Follow these steps to set up and run the Playground APIs on your local machine:

1. **Clone the Repository**

2. **Generate secret hex key:**
    ```python
      import secrets
      # taking 10 bytes
      secrets.token_hex(10)
    ```

3.  **Add secret key in .env file:**
     ```env
     secret=XXXXXXXXXXXX
     ```

4. **Build and Run the Container:**
    ```bash
     $ docker compose up --build
    ```

5. **Explore the APIs:**
  The APIs will now be available locally at http://localhost:8000

6. **Visit Swagger Documentation for APIs:**
   Explore and test APIs at http://localhost:8000/docs

7. **Open docker interactive shell while container is running in another:**
   ```bash
   $ docker exec -it playground-container bash
   ```
   
8. **Start using the APIs once inside interactive shell:**
   ```bash
   $ python playground-api-playground.py
   ```

With the mounted volumes, feel free to test changes while the container is hosting the APIs.

## Under the hood
**Programming Language used:**
Python<br>
**Database used:**
Sqlalchemy ORM on top of in-memory sqlite3 relational database<br>
**API Development:**
FastAPI<br>
**Documentation using:**
Swagger.io<br>
**Containerized by:**
Dockers<br>
**Authentication using:**
JWT Tokens<br>
