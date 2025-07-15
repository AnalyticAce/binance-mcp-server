#!/usr/bin/env bash
# deploy-package.sh
# This script automates the deployment process for the binance-mcp-server package
# using the UV package manager for Python projects.

set -e  # Exit immediately if a command exits with a non-zero status

# Display banner
echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║           🚀 Binance MCP Server Deployment 🚀          ║"
echo "╠════════════════════════════════════════════════════════╣"
echo "║   Automating build & publish with UV package manager   ║"
echo "╚════════════════════════════════════════════════════════╝"

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${PROJECT_DIR}/.venv"
DIST_DIR="${PROJECT_DIR}/dist"
PYTHON_VERSION="3.10"  # Set your required Python version

# Utility function for logging
log() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') - $1"
}

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    log "ERROR: UV package manager is not installed"
    log "Please install it first: pip install uv"
    exit 1
fi

log "Starting deployment process..."

# Clean up previous builds
log "Cleaning previous build artifacts..."
rm -rf "${DIST_DIR:?}" build *.egg-info
mkdir -p "$DIST_DIR"

# Create/update virtual environment
log "Setting up virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    log "Creating new virtual environment with Python $PYTHON_VERSION..."
    uv venv "$VENV_DIR" --python="$PYTHON_VERSION"
else
    log "Virtual environment already exists"
fi

# Activate virtual environment
log "Activating virtual environment..."
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate" || { log "Failed to activate virtual environment"; exit 1; }

# Update dependencies
log "Updating project dependencies..."
uv pip install -e ".[dev,test]"

# Run tests
# log "Running tests..."
# if command -v pytest &> /dev/null; then
#     pytest -xvs tests/ || { log "Tests failed"; exit 1; }
# else
#     log "WARNING: pytest not found, skipping tests"
# fi

# Build package using uv build
log "Building package..."
uv build

# Publish package using uv publish
log "Deploying package..."
if [ -n "${PYPI_TOKEN:-}" ]; then
    set +e  # Allow uv publish to fail without exiting the script
    PUBLISH_OUTPUT=$(uv publish --token "$PYPI_TOKEN" dist/* 2>&1)
    PUBLISH_EXIT_CODE=$?
    set -e

    if [[ $PUBLISH_EXIT_CODE -eq 0 ]]; then
        log "Package published successfully."
    elif echo "$PUBLISH_OUTPUT" | grep -qi "File already exists"; then
        log "Package version already published on PyPI. Exiting gracefully."
        exit 0
    else
        log "uv publish failed:"
        echo "$PUBLISH_OUTPUT"
        exit $PUBLISH_EXIT_CODE
    fi
else
    log "PYPI_TOKEN not found. Cannot deploy to PyPI."
    log "To deploy, set the PYPI_TOKEN environment variable:"
    log "export PYPI_TOKEN=your_pypi_token"
fi

# Display success message
log "Deployment process completed."
log "Package files are available in: $DIST_DIR"

# Deactivate virtual environment
deactivate

exit 0
