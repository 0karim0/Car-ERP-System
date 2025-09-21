@echo off
REM Frontend Installation Script for Car ERP System (Windows)
echo 🚗 Installing Car ERP Frontend dependencies...

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js 16+ from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if npm is installed
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm is not installed. Please install npm.
    pause
    exit /b 1
)

echo ✅ Node.js version:
node --version
echo ✅ npm version:
npm --version

REM Install dependencies
echo 📦 Installing dependencies...
npm install

if %errorlevel% equ 0 (
    echo ✅ Dependencies installed successfully!
    echo.
    echo 🚀 To start the development server:
    echo    npm start
    echo.
    echo 🏗️  To build for production:
    echo    npm run build
    echo.
    echo 🧪 To run tests:
    echo    npm test
    echo.
    echo 📖 For more information, see requirements.md
) else (
    echo ❌ Failed to install dependencies. Please check the error messages above.
)

pause
