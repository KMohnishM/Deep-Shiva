@echo off
echo 🚀 Indian Tourism Chatbot Deployment Script
echo ==========================================

REM Check if git is initialized
if not exist ".git" (
    echo 📁 Initializing git repository...
    git init
    git add .
    git commit -m "Initial commit"
)

REM Check if Heroku CLI is installed
heroku --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Heroku CLI not found. Please install it first:
    echo    Windows: winget install --id=Heroku.HerokuCLI
    pause
    exit /b 1
)

REM Check if user is logged in to Heroku
heroku auth:whoami >nul 2>&1
if errorlevel 1 (
    echo 🔐 Please login to Heroku first:
    heroku login
)

REM Get app name
set /p app_name="Enter your Heroku app name (or press Enter to auto-generate): "

if "%app_name%"=="" (
    echo 🏗️  Creating Heroku app...
    heroku create
) else (
    echo 🏗️  Creating Heroku app: %app_name%
    heroku create %app_name%
)

REM Get Azure OpenAI credentials
echo 🔑 Setting up Azure OpenAI credentials...
set /p api_key="Enter your Azure OpenAI API Key: "
set /p endpoint="Enter your Azure OpenAI Endpoint: "
set /p deployment_name="Enter your GPT-4 Deployment Name: "

REM Generate a secure secret key
for /f %%i in ('python -c "import secrets; print(secrets.token_hex(24))"') do set secret_key=%%i

REM Set environment variables
echo ⚙️  Setting environment variables...
heroku config:set OPENAI_API_VERSION=2024-02-15-preview
heroku config:set AZURE_GPT_DEPLOYMENT=%deployment_name%
heroku config:set AZURE_OPENAI_ENDPOINT=%endpoint%
heroku config:set AZURE_OPENAI_API_KEY=%api_key%
heroku config:set FLASK_SECRET_KEY=%secret_key%

REM Deploy
echo 🚀 Deploying to Heroku...
git add .
git commit -m "Deploy to Heroku"
git push heroku main

REM Open the app
echo 🌐 Opening your app...
heroku open

echo ✅ Deployment complete!
echo 🔗 Your app URL: 
heroku info -s | findstr web_url
echo 📊 View logs: heroku logs --tail
pause 