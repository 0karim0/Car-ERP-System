#!/bin/bash

# Frontend Installation Script for Car ERP System
echo "🚗 Installing Car ERP Frontend dependencies..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ from https://nodejs.org/"
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 16 ]; then
    echo "❌ Node.js version 16+ is required. Current version: $(node --version)"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm."
    exit 1
fi

echo "✅ Node.js version: $(node --version)"
echo "✅ npm version: $(npm --version)"

# Install dependencies
echo "📦 Installing dependencies..."
npm install

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
    echo ""
    echo "🚀 To start the development server:"
    echo "   npm start"
    echo ""
    echo "🏗️  To build for production:"
    echo "   npm run build"
    echo ""
    echo "🧪 To run tests:"
    echo "   npm test"
    echo ""
    echo "📖 For more information, see requirements.md"
else
    echo "❌ Failed to install dependencies. Please check the error messages above."
    exit 1
fi
