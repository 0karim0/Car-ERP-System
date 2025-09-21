# Frontend Requirements - Car ERP System

## 📋 System Requirements

### Minimum System Requirements
- **Node.js**: Version 16.0.0 or higher
- **npm**: Version 7.0.0 or higher (comes with Node.js)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space
- **Browser**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+

### Recommended System Requirements
- **Node.js**: Version 18.0.0 or higher
- **npm**: Version 9.0.0 or higher
- **RAM**: 8GB or higher
- **Storage**: 5GB free space
- **Browser**: Latest version of Chrome, Firefox, or Safari

## 📦 Dependencies

### Core Dependencies

#### React Framework
```json
{
  "react": "^18.2.0",
  "react-dom": "^18.2.0",
  "react-scripts": "5.0.1"
}
```

#### Routing & Navigation
```json
{
  "react-router-dom": "^6.8.1"
}
```

#### HTTP Client & API Communication
```json
{
  "axios": "^1.6.2"
}
```

#### State Management & Data Fetching
```json
{
  "react-query": "^3.39.3"
}
```

#### Form Handling
```json
{
  "react-hook-form": "^7.48.2"
}
```

#### UI Components & Icons
```json
{
  "lucide-react": "^0.294.0",
  "react-hot-toast": "^2.4.1"
}
```

#### Data Visualization
```json
{
  "recharts": "^2.8.0"
}
```

#### Utility Libraries
```json
{
  "date-fns": "^2.30.0",
  "web-vitals": "^2.1.4"
}
```

### Development Dependencies

#### CSS Framework & Styling
```json
{
  "tailwindcss": "^3.3.6",
  "autoprefixer": "^10.4.16",
  "postcss": "^8.4.32"
}
```

#### Testing
```json
{
  "@testing-library/jest-dom": "^5.17.0",
  "@testing-library/react": "^13.4.0",
  "@testing-library/user-event": "^13.5.0"
}
```

## 🛠️ Installation Commands

### Install All Dependencies
```bash
cd frontend
npm install
```

### Install Individual Packages
```bash
# Core React dependencies
npm install react@^18.2.0 react-dom@^18.2.0 react-scripts@5.0.1

# Routing
npm install react-router-dom@^6.8.1

# HTTP client
npm install axios@^1.6.2

# State management
npm install react-query@^3.39.3

# Form handling
npm install react-hook-form@^7.48.2

# UI components
npm install lucide-react@^0.294.0 react-hot-toast@^2.4.1

# Data visualization
npm install recharts@^2.8.0

# Utilities
npm install date-fns@^2.30.0 web-vitals@^2.1.4

# Development dependencies
npm install --save-dev tailwindcss@^3.3.6 autoprefixer@^10.4.16 postcss@^8.4.32

# Testing dependencies
npm install --save-dev @testing-library/jest-dom@^5.17.0 @testing-library/react@^13.4.0 @testing-library/user-event@^13.5.0
```

## 🔧 Development Setup

### 1. Install Node.js
Download and install Node.js from [nodejs.org](https://nodejs.org/)
- Recommended: LTS version (18.x or higher)
- npm comes bundled with Node.js

### 2. Verify Installation
```bash
node --version
npm --version
```

### 3. Install Project Dependencies
```bash
cd frontend
npm install
```

### 4. Start Development Server
```bash
npm start
```

The application will be available at: http://localhost:3000

## 📁 Package Structure

```
frontend/
├── package.json              # Dependencies and scripts
├── package-lock.json         # Locked dependency versions
├── public/                   # Static assets
│   ├── index.html           # HTML template
│   └── manifest.json        # PWA manifest
├── src/                     # Source code
│   ├── components/          # Reusable components
│   ├── pages/              # Page components
│   ├── services/           # API services
│   ├── contexts/           # React contexts
│   ├── utils/              # Utility functions
│   ├── App.js              # Main app component
│   └── index.js            # Entry point
├── tailwind.config.js       # Tailwind CSS configuration
├── postcss.config.js        # PostCSS configuration
└── Dockerfile              # Docker configuration
```

## 🚀 Build Commands

### Development
```bash
npm start                    # Start development server
npm run build               # Build for production
npm test                    # Run tests
npm run eject              # Eject from Create React App
```

### Production Build
```bash
npm run build
```
Creates optimized build in `build/` directory

## 🌐 Browser Support

### Supported Browsers
- **Chrome**: 90+
- **Firefox**: 88+
- **Safari**: 14+
- **Edge**: 90+

### Polyfills Included
- ES6+ features
- Fetch API
- Promise support
- Array methods

## 📱 Responsive Design

### Breakpoints
- **Mobile**: < 640px
- **Tablet**: 640px - 1024px
- **Desktop**: > 1024px

### CSS Framework
- **Tailwind CSS**: Utility-first CSS framework
- **Responsive**: Mobile-first design approach
- **Custom Components**: Reusable UI components

## 🔒 Security Features

### Content Security Policy
- XSS protection
- Secure headers
- HTTPS enforcement

### Authentication
- JWT token handling
- Secure API communication
- Role-based access control

## 📊 Performance Optimization

### Code Splitting
- Route-based splitting
- Component lazy loading
- Bundle optimization

### Caching
- Browser caching
- API response caching
- Static asset caching

## 🧪 Testing

### Test Framework
- **Jest**: JavaScript testing framework
- **React Testing Library**: Component testing
- **User Event**: User interaction testing

### Test Commands
```bash
npm test                    # Run tests in watch mode
npm test -- --coverage     # Run tests with coverage
npm test -- --watchAll=false  # Run tests once
```

## 🔧 Configuration Files

### Tailwind CSS Configuration
```javascript
// tailwind.config.js
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: {
          // Custom color palette
        }
      }
    }
  },
  plugins: []
}
```

### PostCSS Configuration
```javascript
// postcss.config.js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {}
  }
}
```

## 🐳 Docker Support

### Dockerfile
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

### Docker Commands
```bash
# Build Docker image
docker build -t car-erp-frontend .

# Run container
docker run -p 3000:3000 car-erp-frontend

# With docker-compose
docker-compose up frontend
```

## 🔄 Environment Variables

### Required Variables
```env
REACT_APP_API_URL=http://localhost:8000
```

### Optional Variables
```env
REACT_APP_ENVIRONMENT=development
REACT_APP_VERSION=1.0.0
```

## 📈 Performance Metrics

### Bundle Size
- **Initial Bundle**: ~500KB (gzipped)
- **Vendor Bundle**: ~200KB (gzipped)
- **Total Bundle**: ~700KB (gzipped)

### Loading Performance
- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Time to Interactive**: < 3.5s

## 🛠️ Troubleshooting

### Common Issues

#### Node Version Issues
```bash
# Check Node version
node --version

# Use nvm to switch versions
nvm use 18
```

#### Dependency Issues
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### Port Already in Use
```bash
# Kill process on port 3000
npx kill-port 3000

# Or use different port
PORT=3001 npm start
```

### Performance Issues
```bash
# Analyze bundle size
npm run build
npx serve -s build
```

## 📚 Additional Resources

### Documentation
- [React Documentation](https://reactjs.org/docs)
- [React Router Documentation](https://reactrouter.com/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [React Query Documentation](https://tanstack.com/query/latest)

### Tools
- [React Developer Tools](https://chrome.google.com/webstore/detail/react-developer-tools)
- [Redux DevTools](https://chrome.google.com/webstore/detail/redux-devtools)
- [Lighthouse](https://developers.google.com/web/tools/lighthouse)

---

**Note**: This frontend application is designed to work with the Car ERP System backend API. Ensure the backend is running on the configured API URL for full functionality.
