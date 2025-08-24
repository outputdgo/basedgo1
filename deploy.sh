#!/bin/bash

# Automated deployment script for basedgo1
# This script pulls changes, applies migrations, collects static files, and restarts the server

set -e  # Exit on any error

# Configuration
PROJECT_DIR="/home/ubuntu/basedgo1"
VENV_PATH="$PROJECT_DIR/venv312"
BRANCH="production"
GUNICORN_CONFIG="base.wsgi:application"
BIND_ADDRESS=""  # Using gunicorn.conf.py for configuration

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

# Change to project directory
cd "$PROJECT_DIR"

log "Starting deployment process..."

# Check if git repo is clean
if ! git diff-index --quiet HEAD --; then
    warn "Working directory has uncommitted changes"
    git status --porcelain
fi

# Pull latest changes
log "Pulling latest changes from $BRANCH branch..."
git fetch origin
git checkout "$BRANCH"
git pull origin "$BRANCH"

# Activate virtual environment
log "Activating virtual environment..."
source "$VENV_PATH/bin/activate"

# Install/update dependencies
log "Installing/updating dependencies..."
pip install -r requirements.txt

# Check for new migrations
log "Checking for database migrations..."
if python manage.py showmigrations --plan | grep -q "\[ \]"; then
    log "Applying database migrations..."
    python manage.py migrate
else
    log "No new migrations to apply"
fi

# Collect static files
log "Collecting static files..."
python manage.py collectstatic --noinput

# Stop existing Gunicorn processes
log "Stopping existing Gunicorn processes..."
pkill -f gunicorn || true  # Don't fail if no processes found

# Wait a moment for processes to stop
sleep 2

# Start Gunicorn in background
log "Starting Gunicorn server..."
gunicorn "$GUNICORN_CONFIG" -c gunicorn.conf.py --daemon

# Wait a moment and check if server started successfully
sleep 3

if pgrep -f gunicorn > /dev/null; then
    log "Deployment completed successfully! Server is running."
    log "Gunicorn processes:"
    ps aux | grep gunicorn | grep -v grep
else
    error "Failed to start Gunicorn server!"
    exit 1
fi

log "Deployment script finished at $(date)"
