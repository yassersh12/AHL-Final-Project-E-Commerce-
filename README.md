# Final-Project---Team-3

## Setup Instructions

### 1. Set up a Virtual Environment

Create a virtual environment using Python’s `venv` module.

```bash
python3 -m venv venv
```

### 2. Activate the Virtual Environment

Activate the virtual environment:

- On macOS/Linux:

  ```bash
  source venv/bin/activate
  ```

- On Windows:
  ```bash
  .\venv\Scripts\activate
  ```

### 3. Install Dependencies

Install the required Python packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

## How to Run the App

To run the FastAPI app, use the following command:

```bash
fastapi dev app/main.py
```

## Environment Variables

The following environment variables should be set in the `.env` file:

- `POSTGRES_USER`: PostgreSQL username (default: `default_user`)
- `POSTGRES_PASSWORD`: PostgreSQL password (default: `default_password`)
- `POSTGRES_DB`: PostgreSQL database name (default: `default_db`)
- `POSTGRES_HOST`: PostgreSQL host (default: `localhost`)
- `POSTGRES_PORT`: PostgreSQL port (default: `5433`)

You can create a `.env` file in the project root:
