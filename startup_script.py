import subprocess

# Run secret manager
subprocess.run(["python", "secret_manager.py"])

# Run uvicorn in the background
uvicorn_cmd = ["uvicorn", "main:app", "--reload", "--host=0.0.0.0"]
subprocess.Popen(uvicorn_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Open an interactive shell
subprocess.run(["bash"])