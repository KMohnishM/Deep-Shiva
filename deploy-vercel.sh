#!/bin/bash

echo "🚀 Vercel Deployment Script for Indian Tourism Chatbot"
echo "====================================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js first:"
    echo "   https://nodejs.org/"
    exit 1
fi

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

# Check if user is logged in to Vercel
if ! vercel whoami &> /dev/null; then
    echo "🔐 Please login to Vercel first:"
    vercel login
fi

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit"
fi

# Get Azure OpenAI credentials
echo "🔑 Setting up Azure OpenAI credentials..."
read -p "Enter your Azure OpenAI API Key: " api_key
read -p "Enter your Azure OpenAI Endpoint: " endpoint
read -p "Enter your GPT-4 Deployment Name: " deployment_name

# Generate a secure secret key
secret_key=$(python -c "import secrets; print(secrets.token_hex(24))")

# Deploy to Vercel
echo "🚀 Deploying to Vercel..."
vercel --yes

# Set environment variables
echo "⚙️  Setting environment variables..."
vercel env add OPENAI_API_VERSION
echo "2024-02-15-preview" | vercel env add OPENAI_API_VERSION

vercel env add AZURE_GPT_DEPLOYMENT
echo "$deployment_name" | vercel env add AZURE_GPT_DEPLOYMENT

vercel env add AZURE_OPENAI_ENDPOINT
echo "$endpoint" | vercel env add AZURE_OPENAI_ENDPOINT

vercel env add AZURE_OPENAI_API_KEY
echo "$api_key" | vercel env add AZURE_OPENAI_API_KEY

vercel env add FLASK_SECRET_KEY
echo "$secret_key" | vercel env add FLASK_SECRET_KEY

# Deploy to production
echo "🚀 Deploying to production..."
vercel --prod

echo "✅ Deployment complete!"
echo "🔗 Your app URL: $(vercel ls | grep indian-tourism-chatbot | awk '{print $2}')"
echo "📊 View logs: vercel logs" 