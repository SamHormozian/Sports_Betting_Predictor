import os
import subprocess
import time

# Docker-related configurations
DOCKER_IMAGE_NAME = "sports-betting-predictor"
DOCKER_CONTAINER_NAME = "sports-betting-app"
DOCKER_PORT = 8080

def build_docker_image():
    """
    Build the Docker image for the project.
    """
    print("\nBuilding Docker image...")
    result = subprocess.run(
        ["docker", "build", "-t", DOCKER_IMAGE_NAME, "."],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("Docker image built successfully!\n")
    else:
        print(f"Error building Docker image:\n{result.stderr}")
        exit(1)

def run_docker_container():
    """
    Run the Docker container for the project.
    """
    print(f"\nStarting Docker container on port {DOCKER_PORT}...")
    subprocess.run(["docker", "rm", "-f", DOCKER_CONTAINER_NAME], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # Remove any existing container
    result = subprocess.run(
        [
            "docker", "run", "-d",
            "-p", f"{DOCKER_PORT}:5000",
            "--name", DOCKER_CONTAINER_NAME,
            DOCKER_IMAGE_NAME
        ],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"Docker container started successfully!\n")
        print(f"Access the application at: http://127.0.0.1:{DOCKER_PORT}")
    else:
        print(f"Error starting Docker container:\n{result.stderr}")
        exit(1)

def stop_docker_container():
    """
    Stop the running Docker container.
    """
    print("\nStopping Docker container...")
    result = subprocess.run(
        ["docker", "stop", DOCKER_CONTAINER_NAME],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("Docker container stopped successfully!")
    else:
        print(f"Error stopping Docker container:\n{result.stderr}")

def main():
    while True:
        print("\nOptions:")
        print("1. Build and run the application")
        print("2. Stop the application")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            build_docker_image()
            run_docker_container()
        elif choice == "2":
            stop_docker_container()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
