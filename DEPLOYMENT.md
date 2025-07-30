# 🚀 Deployment Guide for Indian Tourism Chatbot

## 📋 Prerequisites

1. **Azure OpenAI Account** - You need an Azure OpenAI service with GPT-4 deployment
2. **Git** - For version control
3. **Python 3.12** - For local development

## 🔧 Setup Azure OpenAI

1. Go to [Azure Portal](https://portal.azure.com)
2. Create an Azure OpenAI resource
3. Deploy a GPT-4 model
4. Get your API key and endpoint

## 🌐 Deployment Options

### Option 1: Heroku (Recommended for beginners)

#### Step 1: Install Heroku CLI
```bash
# Windows
winget install --id=Heroku.HerokuCLI

# macOS
brew tap heroku/brew && brew install heroku

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

#### Step 2: Login to Heroku
```bash
heroku login
```

#### Step 3: Create Heroku App
```bash
# Navigate to your project directory
cd Indian-Tourism-Chatbot

# Initialize git if not already done
git init
git add .
git commit -m "Initial commit"

# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set OPENAI_API_VERSION=2024-02-15-preview
heroku config:set AZURE_GPT_DEPLOYMENT=your-gpt4-deployment-name
heroku config:set AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
heroku config:set AZURE_OPENAI_API_KEY=your-api-key
heroku config:set FLASK_SECRET_KEY=your-secure-secret-key-here

# Deploy
git push heroku main
```

#### Step 4: Open Your App
```bash
heroku open
```

### Option 2: Railway

#### Step 1: Install Railway CLI
```bash
npm install -g @railway/cli
```

#### Step 2: Deploy
```bash
# Login to Railway
railway login

# Initialize project
railway init

# Set environment variables
railway variables set OPENAI_API_VERSION=2024-02-15-preview
railway variables set AZURE_GPT_DEPLOYMENT=your-gpt4-deployment-name
railway variables set AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
railway variables set AZURE_OPENAI_API_KEY=your-api-key
railway variables set FLASK_SECRET_KEY=your-secure-secret-key-here

# Deploy
railway up
```

### Option 3: Render

#### Step 1: Connect GitHub
1. Go to [Render](https://render.com)
2. Connect your GitHub account
3. Import your repository

#### Step 2: Configure Service
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`
- **Environment**: Python 3

#### Step 3: Set Environment Variables
Add these in Render dashboard:
- `OPENAI_API_VERSION=2024-02-15-preview`
- `AZURE_GPT_DEPLOYMENT=your-gpt4-deployment-name`
- `AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/`
- `AZURE_OPENAI_API_KEY=your-api-key`
- `FLASK_SECRET_KEY=your-secure-secret-key-here`

### Option 4: Vercel

#### Step 1: Create vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

#### Step 2: Deploy
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

## 🔐 Environment Variables

Make sure to set these environment variables in your deployment platform:

```bash
OPENAI_API_VERSION=2024-02-15-preview
AZURE_GPT_DEPLOYMENT=your-gpt4-deployment-name
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
FLASK_SECRET_KEY=your-secure-secret-key-here
```

## 🐛 Troubleshooting

### Common Issues:

1. **Import Errors**: Make sure all dependencies are in `requirements.txt`
2. **API Errors**: Verify your Azure OpenAI credentials
3. **Port Issues**: Use `PORT` environment variable for cloud platforms
4. **Memory Issues**: Some platforms have memory limits

### Debug Commands:

```bash
# Check logs (Heroku)
heroku logs --tail

# Check logs (Railway)
railway logs

# Check environment variables
heroku config
```

## 📊 Monitoring

- **Heroku**: Use Heroku Dashboard for monitoring
- **Railway**: Built-in monitoring in dashboard
- **Render**: Automatic monitoring and alerts
- **Vercel**: Analytics in dashboard

## 🔄 Continuous Deployment

Set up GitHub Actions for automatic deployment:

```yaml
name: Deploy to Heroku
on:
  push:
    branches: [ main ]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - uses: akhileshns/heroku-deploy@v3.12.12
      with:
        heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
        heroku_app_name: ${{ secrets.HEROKU_APP_NAME }}
        heroku_email: ${{ secrets.HEROKU_EMAIL }}
```

## 🎉 Success!

Your Indian Tourism Chatbot is now live! Share the URL with users and start helping them explore India's rich culture and spirituality. 