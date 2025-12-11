# Granian vs Hypercorn Comparison

![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![Quart](https://img.shields.io/badge/Quart-Latest-green.svg)
![Granian](https://img.shields.io/badge/Granian-Rust_ASGI-orange.svg)
![Hypercorn](https://img.shields.io/badge/Hypercorn-ASGI-yellow.svg)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)
![Nginx](https://img.shields.io/badge/Nginx-Proxy-green.svg)

This repository hosts a minimal **Quart** application packaged with two different ASGI servers—**Granian** (Rust-based) and **Hypercorn**—along with an **Nginx** proxy. Ideally suited for performance benchmarking, it allows you to compare behavior, throughput, and latency under identical traffic conditions.

## 🏗️ Architecture

The project runs three containerized services via Docker Compose:

1.  **Granian Service**: Runs the Quart app using the Granian ASGI server.
2.  **Hypercorn Service**: Runs the exact same Quart app using the Hypercorn ASGI server.
3.  **Nginx Proxy**: Routes traffic to the backend services and handles **traffic mirroring**.

### 🌟 Key Features

*   **Identical Workload**: The application simulates a consistent async workload (50ms non-blocking sleep) on a `/hello` endpoint, ensuring fair comparison.
*   **Traffic Mirroring**: Requests to the main `/hello` endpoint are handled by Granian but transparently **mirrored** to Hypercorn by Nginx. This allows you to load test one endpoint and see how both servers behave under the same real-time pressure.
*   **Direct Access**: Dedicated endpoints (`/granian` and `/hypercorn`) allow for isolated testing of each server.
*   **Automated Benchmarking**: Includes a `pytest` suite with `httpx` to run reproducible load tests (RPS, Latency p95, etc.).

## 🚀 Quick Start

### Prerequisites

*   **Python >= 3.13** (managed via `uv`)
*   **Docker** & **Docker Compose**
*   **UV** (Python package manager)

### Installation & Setup

1.  **Clone the repository:**
    ```powershell
    git clone https://github.com/Cybernetic-Ransomware/Granian_Quart_ASGI_Compare.git
    cd Granian_Quart_ASGI_Compare
    ```

2.  **Configure Environment:**
    Set up the `.env` file based on the provided template.
    ```powershell
    cp .env.template .env
    ```

3.  **Launch Services:**
    Build and start the Docker containers.
    ```powershell
    docker compose -f docker/docker-compose.yml up -d --build
    ```
    *Note: If you change the number of workers, restart Nginx:*
    ```powershell
    docker compose -f docker/docker-compose.yml restart nginx
    ```

4.  **Install Local Dependencies:**
    Install `uv` and the project dependencies for running tests.
    ```powershell
    pip install uv
    uv sync --group dev
    ```

## 🧪 Usage & Testing

### API Endpoints (via Nginx on Port 8080)

*   `http://localhost:8080/hello` - **Mirrored Endpoint**. Responded to by Granian; shadowed to Hypercorn.
*   `http://localhost:8080/granian` - Direct route to Granian.
*   `http://localhost:8080/hypercorn` - Direct route to Hypercorn.

### Running Load Tests

The project includes a performance test suite.

```powershell
# Run the standard test suite
uv run pytest

# Enable heavy load tests (configure RUN_LOAD_TESTS=1 in .env first)
uv run pytest
```

The load test (`tests/test_load.py`) measures:
*   Requests Per Second (RPS)
*   Average Latency
*   95th Percentile Latency (p95)

### Local Development

You can run the app locally without Docker for development or debugging.

1.  **Run Granian locally:**
    ```powershell
    uv run granian --interface asgi --workers 2 --host 0.0.0.0 --port 8000 src.app.main:app
    ```

2.  **View Documentation (Swagger UI):**
    Open your browser to:
    ```
    http://0.0.0.0:8000/docs
    ```