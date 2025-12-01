# Granian vs Hypercorn comparison

This repository hosts a minimal Quart application packaged with two ASGI servers (Granian and Hypercorn) and an nginx proxy that allows you to compare their behaviour and response times under identical traffic.

Requirements

- Python >=3.13.9 with the UV package manager
- Docker with Docker Compose

## Quick start
1. Clone the repository:
    ```powershell
    git clone https://github.com/Cybernetic-Ransomware/Granian_Quart_ASGI_Compare.git
    ```
   
2. Set up the `.env` file based on the provided template.

3. Build and start the containers:
   ```powershell
   docker compose -f docker/docker-compose.yml up -d --build
   ```
   This launches the Granian app, the Hypercorn app, and the nginx proxy that exposes comparison endpoints on `http://localhost:8080`.
 
4. Install UV:
    ```powershell
    pip install uv
    ```

5. Install the development dependencies:
   ```powershell
   uv sync --group dev
   ```

6. Run the tests:
   ```powershell
   uv run pytest
   ```
   The suite includes a load-test scenario that can be enabled by setting `RUN_LOAD_TESTS=1` inside `.env`.
