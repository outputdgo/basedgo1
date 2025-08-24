# Deployment Automation Scripts

This project includes several scripts to automate the deployment process and server management. All scripts pull the latest changes from your GitHub repository and restart the server automatically.

## Available Scripts

### 1. `./deploy.sh` - Full Deployment Script
**When to use:** For complete deployments with potential database changes, new dependencies, or major updates.

**What it does:**
- ✅ Pulls latest changes from the `production` branch
- ✅ Checks for uncommitted changes (with warning)
- ✅ Activates virtual environment
- ✅ Installs/updates Python dependencies
- ✅ Checks for and applies database migrations
- ✅ Collects static files
- ✅ Stops and restarts Gunicorn server
- ✅ Validates server startup
- ✅ Comprehensive logging with colored output

**Usage:**
```bash
./deploy.sh
```

### 2. `./quick-deploy.sh` - Quick Update Script
**When to use:** For minor code changes when you know there are no new migrations or dependencies.

**What it does:**
- ✅ Pulls latest changes from the `production` branch
- ✅ Activates virtual environment
- ✅ Collects static files
- ✅ Stops and restarts Gunicorn server
- ✅ Validates server startup

**Usage:**
```bash
./quick-deploy.sh
```

### 3. `./restart-server.sh` - Server Restart Only
**When to use:** When you just need to restart the server without pulling changes.

**What it does:**
- ✅ Stops all existing Gunicorn processes
- ✅ Starts Gunicorn with proper configuration
- ✅ Validates server startup

**Usage:**
```bash
./restart-server.sh
```

## Server Configuration

All scripts start Gunicorn with the following optimized configuration:
- **Bind:** `0.0.0.0:8000`
- **Workers:** 3 (can handle multiple requests)
- **Worker Class:** `gthread` (for better performance)
- **Threads per worker:** 2
- **Worker connections:** 1000
- **Max requests per worker:** 1000 (with jitter)
- **Timeout:** 60 seconds
- **Keep-alive:** 5 seconds

## Workflow for Development

1. **Make changes on your development branch**
2. **Test locally**
3. **Merge to production branch:**
   ```bash
   git checkout production
   git merge development
   git push origin production
   ```
4. **Deploy on server:**
   - For major changes: `./deploy.sh`
   - For minor changes: `./quick-deploy.sh`
   - Just restart: `./restart-server.sh`

## Script Features

### Security
- ✅ Comprehensive CSP headers for security
- ✅ Video embed compatibility (YouTube, Vimeo)
- ✅ XSS protection and content type sniffing prevention

### Error Handling
- ✅ Scripts exit on any error (`set -e`)
- ✅ Graceful process termination
- ✅ Server validation after startup
- ✅ Clear error messages

### Logging
- ✅ Colored output for better readability
- ✅ Timestamps on full deployment script
- ✅ Progress indicators
- ✅ Process status validation

## Troubleshooting

### If deployment fails:
1. Check the error message in the script output
2. Manually run each step to identify the issue
3. Ensure you're on the production branch
4. Verify virtual environment is working

### If server won't start:
1. Check for syntax errors in your code
2. Verify database migrations are applied
3. Check static files are collected
4. Use `./restart-server.sh` for a clean restart

### To check server status:
```bash
ps aux | grep gunicorn
curl -I http://localhost:8000
```

## Best Practices

1. **Always test locally first** before deploying to production
2. **Use the full deploy script** when unsure about migrations
3. **Keep your production branch clean** - only merge tested code
4. **Monitor the server** after deployment to ensure everything works
5. **Check logs** if you encounter issues

## File Locations

- Scripts: `/home/ubuntu/basedgo1/`
- Virtual Environment: `/home/ubuntu/basedgo1/venv312/`
- Static Files: `/home/ubuntu/basedgo1/staticfiles/`
- Project Root: `/home/ubuntu/basedgo1/`

These scripts make deployment safe, consistent, and automated while giving you full control over the process!
