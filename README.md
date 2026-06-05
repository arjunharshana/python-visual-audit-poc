# Python Visual Audit POC

A standalone Python automation proof-of-concept designed to execute headless browser flows and automatically capture layout screenshots for visual auditing. The project connects to a local Dockerized Selenium Grid and organizes outputs into timestamped directories.

## Project Structure

```text
python-visual-audit-poc/
├── README.md
├── docker-compose.yml      
├── requirements.txt       
├── .gitignore              
├── config/
│   ├── __init__.py
│   └── driver_setup.py 
└── tests/
    ├── __init__.py
    └── test_visual_login.py 
```
## Prerequisites

- Docker and Docker Compose
- Python 3.x
- Git

## Setup & Installation

### 1. Start the Infrastructure

Spin up the local Selenium Grid (Hub and Firefox Node) using Docker Compose:

```bash
docker-compose up -d
```

> You can verify the grid is running by navigating to `http://localhost:4444` in your browser.

### 2. Configure the Python Environment

It is highly recommended to use a virtual environment to manage project dependencies.

```bash
# Create the virtual environment
python -m venv venv

# Activate the virtual environment (Linux/macOS)
source venv/bin/activate

# Activate the virtual environment (Windows)
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Execution

With the Docker grid running and your virtual environment active, execute the visual audit test script:

```bash
python tests/test_visual_login.py
```

## Output

The execution engine automatically handles directory management. Upon completion, a new `test_runs/` folder will be generated in the project root containing a timestamped directory (e.g., `run_YYYY-MM-DD_HH-MM-SS`) with the automated screenshots inside.

## Teardown

When testing is complete, stop the Docker containers to free up system resources:

```bash
docker-compose down
```