# Python Visual Audit POC

A standalone Python automation proof-of-concept designed to execute browser flows and automatically capture layout screenshots and video recordings for visual auditing. The project connects to a local Dockerized Selenium Grid and organizes outputs into dedicated local directories.

---

## Project Structure

```text
python-visual-audit-poc/
├── README.md
├── docker-compose.yml       
├── requirements.txt         
├── .gitignore               
├── videos/                  
├── test_runs/              
├── config/
│   ├── __init__.py
│   └── driver_setup.py     
└── tests/
    ├── __init__.py
    └── test_visual_login.py
```

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/)
- Python 3.x
- Git

---

## Setup & Installation

### 1. Prepare the Output Directories

Because the Selenium Docker containers run as an isolated user, you must grant write permissions to your local video output folder so the container can save `.mp4` files.

```bash
mkdir videos
sudo chmod 777 videos
```

### 2. Start the Infrastructure

Spin up the local Selenium Grid (Hub and Firefox Node with native video recording) using Docker Compose (you can scale to it multiple nodes as shown):

```bash
# For single node
docker-compose up -d

# For multiple nodes
docker-compose up -d --scale firefox-node=5
```

Verify the grid is running by navigating to `http://localhost:4444` in your browser.

### 3. Configure the Python Environment

It is recommended to use a virtual environment to manage project dependencies.

```bash
# Create the virtual environment
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Execution

With the Docker grid running and your virtual environment active, execute the visual audit test script:

```bash
python tests/test_visual_login.py
```

---

## Output

This POC generates two types of visual logs:

| Type | Location | Description |
|---|---|---|
| **Static Screenshots** | `test_runs/run_YYYY-MM-DD_HH-MM-SS/` | Timestamped directory created automatically per run |
| **Video Recordings** | `videos/*.mp4` | Recorded by the Selenium Node and extracted on session end |

> **Note:** The browser runs in non-headless mode intentionally so the container's VNC stream can capture the UI for video recording.

---

## Teardown

When testing is complete, stop the Docker containers to free up system resources:

```bash
docker-compose down
```