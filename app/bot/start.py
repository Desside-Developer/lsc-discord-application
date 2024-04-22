# import subprocess

# def install_requirements(file_path):
#     subprocess.run(["pip", "install", "--upgrade", "pip"])
#     subprocess.run(["pip", "install", "--no-cache-dir", "--upgrade", "-r", file_path])

# def run_fastapi():
#     subprocess.run(["uvicorn", "api.fastapi:app", "--host", "0.0.0.0", "--port", "3537", "--reload"])

# def run_bot():
#     subprocess.run(["python", "app/bots/main.py"])

# if __name__ == "__main__":
#     install_requirements("requirements-fastapi.txt")
#     run_fastapi()
#     install_requirements("requirements.txt")
#     run_bot()