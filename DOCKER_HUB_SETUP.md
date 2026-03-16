# Docker Hub Publishing Setup

This guide explains how to enable Docker Hub publishing for your CI/CD pipeline.

## Overview

The pipeline is configured to build and publish Docker images to Docker Hub, but requires credentials to be configured first.

**Docker Hub Repository:** `tdesai2705/unify-python-app`

**Image Tags:**
- `latest` - Always points to the most recent build
- `<commit-sha>` - Specific version tied to git commit (first 8 characters)

## Prerequisites

1. **Docker Hub Account**
   - Sign up at https://hub.docker.com if you don't have an account
   - Verify your email address

2. **Docker Hub Repository**
   - Create a repository: `unify-python-app`
   - Make it public or private (your choice)

3. **Docker Hub Access Token** (Recommended over password)
   - Go to: Account Settings > Security > New Access Token
   - Name: `CloudBees-Unify-Pipeline`
   - Permissions: Read & Write
   - Copy the token (you won't see it again!)

## Setup Instructions

### Step 1: Add Secrets to CloudBees Unify

1. **Navigate to your organization/project settings** in CloudBees Unify
2. **Go to Secrets or Credentials section**
3. **Add the following secrets:**

   | Secret Name       | Value                          |
   |-------------------|--------------------------------|
   | `DOCKER_USERNAME` | Your Docker Hub username       |
   | `DOCKER_PASSWORD` | Your Docker Hub access token   |

### Step 2: Enable the Publishing Step

1. **Open the pipeline file:**
   `.cloudbees/workflows/ci-cd-pipeline.yaml`

2. **Uncomment the "Publish to Docker Hub" step** (around line 75)

   Change this:
   ```yaml
   # - name: Publish to Docker Hub
   #   uses: docker://gcr.io/kaniko-project/executor:latest
   ```

   To this:
   ```yaml
   - name: Publish to Docker Hub
     uses: docker://gcr.io/kaniko-project/executor:latest
   ```

3. **Remove the `#` from all lines** in that step

4. **Commit and push:**
   ```bash
   git add .cloudbees/workflows/ci-cd-pipeline.yaml
   git commit -m "Enable Docker Hub publishing"
   git push origin main
   ```

### Step 3: Verify Publishing

1. **Trigger the pipeline** (push to main or trigger manually)
2. **Check the logs** for "Publish to Docker Hub" step
3. **Verify on Docker Hub:**
   - Visit: https://hub.docker.com/r/tdesai2705/unify-python-app
   - You should see your image with tags

## Using the Published Image

Once published, anyone can pull and run your Docker image:

```bash
# Pull the latest version
docker pull tdesai2705/unify-python-app:latest

# Pull a specific version
docker pull tdesai2705/unify-python-app:a1b2c3d4

# Run the container
docker run -p 5000:5000 tdesai2705/unify-python-app:latest
```

Access the app at: http://localhost:5000

## Troubleshooting

### Issue: "unauthorized: authentication required"

**Solution:** Check that your secrets are correctly configured in CloudBees Unify

### Issue: "repository does not exist"

**Solution:** Create the repository on Docker Hub first: https://hub.docker.com/repository/create

### Issue: Kaniko build fails

**Solution:** Verify your Dockerfile is valid by building locally:
```bash
docker build -t test-image .
```

## Alternative: GitHub Container Registry

If you prefer GitHub Container Registry over Docker Hub:

1. **Change the destination:**
   ```yaml
   --destination=ghcr.io/tdesai2705/unify-python-app:latest
   ```

2. **Use GitHub token:**
   - Secret: `GITHUB_TOKEN` (GitHub Personal Access Token)
   - Permissions: write:packages

## Security Best Practices

✅ **DO:**
- Use access tokens instead of passwords
- Limit token permissions to read/write only
- Rotate tokens periodically
- Use secrets management in CloudBees

❌ **DON'T:**
- Commit credentials to git
- Use your account password
- Give tokens unnecessary permissions
- Share tokens with others

## Support

For issues with:
- **CloudBees Unify:** Contact your CloudBees administrator
- **Docker Hub:** Visit https://hub.docker.com/support
- **This Pipeline:** Check logs in CloudBees Unify or create an issue in GitHub

---

**Last Updated:** 2026-03-17
**Maintained by:** TEJAS DESAI (tdesai@cloudbees.com)
