# route-check

An empty Python project scaffold.

## Setup Instructions for macOS (Apple Silicon M1/M2/M3)

### 1. Install Python 3 (if not already installed)
macOS comes with Python 3, but you can install the latest version via Homebrew:

```bash
brew install python
```

### 2. (Recommended) Upgrade pip
```bash
python3 -m pip install --upgrade pip
```

### 3. Install required Python packages
Install the dependencies (including OR-Tools and requests):

```bash
python3 -m pip install --break-system-packages ortools requests
```

- The `--break-system-packages` flag is needed for Homebrew-managed Python on recent macOS versions.
- If you prefer, you can use a virtual environment instead (see Python docs).

### 4. Get an OpenRouteService API key
- Sign up at [openrouteservice.org](https://openrouteservice.org/sign-up/) and get your API key.
- The script is already set up to use your API key (replace it in the code if needed).

## How to Run the Route Optimizer

From the project root, run:

```bash
python3 route_inputs.py
```

You will be prompted to enter 5 coordinates (latitude, longitude).

The script will:
- Query OpenRouteService for travel times
- Solve the optimal route
- Print the route and a Google Maps URL to visualize it

---

If you encounter any issues with installation or running the script, please check your Python version and ensure all dependencies are installed as above. 