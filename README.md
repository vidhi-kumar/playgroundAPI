# playgroundAPI - One stop solution for your sports inventory


![pexels-pixabay-248547](https://github.com/vidhi-kumar/playgroundAPI/assets/55309127/b9359bbd-cf88-4e52-bf25-eef6e5e12526)


Welcome to the Playground APIs repository! This project provides a set of authenticated APIs for testing and experimenting with various features. 
The APIs are containerized, allowing easy deployment and testing locally. 
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
     secret=<your-hex-secret-key>
     ```

4. **Build and Run the Container:**
    ```bash
     $ docker compose up --build
    ```

5. **Explore the APIs:**
  The APIs will then be available at http://localhost:8000

6. **Visit built-in Swagger API Documentation for APIs:**
   Explore and test APIs at http://localhost:8000/docs

7. **Open container's interactive shell from another terminal and start using the APIs:**
   ```bash
   $ docker exec -it playground-container bash
   ```
