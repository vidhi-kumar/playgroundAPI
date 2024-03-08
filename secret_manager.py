import secrets
import os


env_file_path = ".env"
if os.path.isfile(env_file_path):
    with open(env_file_path, "r") as env_file:
        lines = env_file.readlines()

    with open(env_file_path, "w") as env_file:
        for line in lines:
            if not line.startswith("secret="):
                env_file.write(line)

# Generate a new secret key
secret_key = secrets.token_hex(16)


with open(env_file_path, "a") as env_file:
    env_file.write(f"secret={secret_key}\n")

print(f"Secret key added to {env_file_path}")