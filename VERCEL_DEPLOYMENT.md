# 🚀 Vercel Deployment Guide for Indian Tourism Chatbot

## 📋 Prerequisites

1. **Azure OpenAI Account** - You need an Azure OpenAI service with GPT-4 deployment
2. **GitHub Account** - For connecting to Vercel
3. **Vercel Account** - Sign up at [vercel.com](https://vercel.com)

## 🔧 Setup Azure OpenAI

1. Go to [Azure Portal](https://portal.azure.com)
2. Create an Azure OpenAI resource
3. Deploy a GPT-4 model
4. Get your API key and endpoint

## 🌐 Deploy to Vercel

### Method 1: Vercel Dashboard (Recommended)

#### Step 1: Prepare Your Repository
```bash
# Make sure your code is in a GitHub repository
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/indian-tourism-chatbot.git
git push -u origin main
```

#### Step 2: Connect to Vercel
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"New Project"**
3. Import your GitHub repository
4. Select the repository: `indian-tourism-chatbot`

#### Step 3: Configure Project
- **Framework Preset**: Other
- **Root Directory**: `./` (leave empty)
- **Build Command**: Leave empty (Vercel will auto-detect)
- **Output Directory**: Leave empty
- **Install Command**: `pip install -r requirements.txt`

#### Step 4: Set Environment Variables
Click on **"Environment Variables"** and add:

```
OPENAI_API_VERSION=2024-02-15-preview
AZURE_GPT_DEPLOYMENT=your-gpt4-deployment-name
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key
FLASK_SECRET_KEY=your-secure-secret-key-here
```

#### Step 5: Deploy
Click **"Deploy"** and wait for the build to complete!

### Method 2: Vercel CLI

#### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

#### Step 2: Login to Vercel
```bash
vercel login
```

#### Step 3: Deploy
```bash
# Navigate to your project directory
cd Indian-Tourism-Chatbot

# Deploy
vercel

# Follow the prompts:
# - Set up and deploy? Y
# - Which scope? Select your account
# - Link to existing project? N
# - What's your project's name? indian-tourism-chatbot
# - In which directory is your code located? ./
```

#### Step 4: Set Environment Variables
```bash
vercel env add OPENAI_API_VERSION
vercel env add AZURE_GPT_DEPLOYMENT
vercel env add AZURE_OPENAI_ENDPOINT
vercel env add AZURE_OPENAI_API_KEY
vercel env add FLASK_SECRET_KEY
```

#### Step 5: Deploy to Production
```bash
vercel --prod
```

## 🔐 Environment Variables

Make sure to set these in your Vercel project settings:

| Variable | Value |
|----------|-------|
| `OPENAI_API_VERSION` | `2024-02-15-preview` |
| `AZURE_GPT_DEPLOYMENT` | Your GPT-4 deployment name |
| `AZURE_OPENAI_ENDPOINT` | `https://your-resource-name.openai.azure.com/` |
| `AZURE_OPENAI_API_KEY` | Your Azure OpenAI API key |
| `FLASK_SECRET_KEY` | A secure random string |

## 🐛 Troubleshooting

### Common Issues:

1. **Build Failures**
   - Check that all dependencies are in `requirements.txt`
   - Ensure `vercel.json` is properly configured

2. **Import Errors**
   - Make sure `PYTHONPATH` is set to "."
   - Check that all files are in the correct directory

3. **API Errors**
   - Verify your Azure OpenAI credentials
   - Check environment variables are set correctly

4. **Runtime Errors**
   - Check Vercel function logs in dashboard
   - Ensure Flask app is properly configured

### Debug Commands:

```bash
# Check deployment status
vercel ls

# View logs
vercel logs

# Redeploy
vercel --prod

# Check environment variables
vercel env ls
```

## 📊 Monitoring

- **Vercel Dashboard**: Real-time analytics and monitoring
- **Function Logs**: View serverless function execution logs
- **Performance**: Automatic performance monitoring
- **Analytics**: Built-in analytics for your app

## 🔄 Continuous Deployment

Vercel automatically deploys when you push to your main branch:

```bash
# Make changes and push
git add .
git commit -m "Update chatbot"
git push origin main

# Vercel automatically deploys!
```

## 🎯 Custom Domain

1. Go to your project in Vercel Dashboard
2. Click **"Settings"** → **"Domains"**
3. Add your custom domain
4. Configure DNS settings

## 🚀 Performance Tips

- **Edge Functions**: Consider using Vercel Edge Functions for faster response times
- **Caching**: Implement proper caching for static assets
- **CDN**: Vercel automatically provides global CDN

## 🎉 Success!

Your Indian Tourism Chatbot is now live on Vercel! 

**Benefits of Vercel:**
- ⚡ **Lightning fast** global CDN
- 🔄 **Automatic deployments** from Git
- 📊 **Built-in analytics** and monitoring
- 🌍 **Global edge network**
- 💰 **Generous free tier**

Share your Vercel URL and start helping users explore India's rich culture! 🎉 