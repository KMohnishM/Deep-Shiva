#!/bin/bash

echo "🚀 Indian Tourism Chatbot Deployment Script"
echo "=========================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit"
fi

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Please install it first:"
    echo "   Windows: winget install --id=Heroku.HerokuCLI"
    echo "   macOS: brew tap heroku/brew && brew install heroku"
    echo "   Linux: curl https://cli-assets.heroku.com/install.sh | sh"
    exit 1
fi

# Check if user is logged in to Heroku
if ! heroku auth:whoami &> /dev/null; then
    echo "🔐 Please login to Heroku first:"
    heroku login
fi

# Get app name
read -p "Enter your Heroku app name (or press Enter to auto-generate): " app_name

if [ -z "$app_name" ]; then
    echo "🏗️  Creating Heroku app..."
    heroku create
else
    echo "🏗️  Creating Heroku app: $app_name"
    heroku create $app_name
fi

# Get Azure OpenAI credentials
echo "🔑 Setting up Azure OpenAI credentials..."
read -p "Enter your Azure OpenAI API Key: " api_key
read -p "Enter your Azure OpenAI Endpoint: " endpoint
read -p "Enter your GPT-4 Deployment Name: " deployment_name

# Generate a secure secret key
secret_key=$(python -c "import secrets; print(secrets.token_hex(24))")

# Set environment variables
echo "⚙️  Setting environment variables..."
heroku config:set OPENAI_API_VERSION=2024-02-15-preview
heroku config:set AZURE_GPT_DEPLOYMENT=$deployment_name
heroku config:set AZURE_OPENAI_ENDPOINT=$endpoint
heroku config:set AZURE_OPENAI_API_KEY=$api_key
heroku config:set FLASK_SECRET_KEY=$secret_key

# Deploy
echo "🚀 Deploying to Heroku..."
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Open the app
echo "🌐 Opening your app..."
heroku open

echo "✅ Deployment complete!"
echo "🔗 Your app URL: $(heroku info -s | grep web_url | cut -d= -f2)"
echo "📊 View logs: heroku logs --tail" 