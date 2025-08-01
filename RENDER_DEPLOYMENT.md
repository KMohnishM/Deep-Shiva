# Deploying Deep-Shiva on Render

This guide explains how to deploy the Deep-Shiva application on Render's free tier.

## Prerequisites

1. A [Render](https://render.com/) account
2. Azure OpenAI API credentials

## Deployment Steps

### 1. Fork or Clone the Repository

Make sure you have your own copy of the repository.

### 2. Create a New Web Service on Render

1. Log in to your Render account
2. Click on "New +" and select "Web Service"
3. Connect your GitHub/GitLab repository or use the "Public Git repository" option
4. Enter the repository URL
5. Configure the service:
   - **Name**: deep-shiva (or your preferred name)
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free

### 3. Set Environment Variables

Add the following environment variables in the Render dashboard:

- `OPENAI_API_VERSION`: Your Azure OpenAI API version (e.g., 2024-02-15-preview)
- `AZURE_GPT_DEPLOYMENT`: Your Azure OpenAI deployment name
- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL
- `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key
- `FLASK_SECRET_KEY`: A secure random string for Flask sessions

### 4. Deploy

Click "Create Web Service" and wait for the deployment to complete.

## Alternative: Deploy with render.yaml

If you have the `render.yaml` file in your repository, you can use Render's Blueprint feature:

1. Log in to your Render account
2. Click on "New +" and select "Blueprint"
3. Connect your repository
4. Render will automatically detect the `render.yaml` file and configure the services
5. You'll still need to set up the environment variables manually in the Render dashboard

## Troubleshooting

- Check the logs in the Render dashboard for any errors
- Verify that all environment variables are correctly set
- Ensure your Azure OpenAI API key has sufficient credits