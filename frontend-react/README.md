# AI Cold Email Generator - Setup Guide (Pure CSS)

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- **Node.js** (v16 or higher) - [Download here](https://nodejs.org/)
- **npm** or **yarn** (comes with Node.js)
- Your backend API running on `http://127.0.0.1:8000`

## 🚀 Setup Instructions

### Step 1: Create React App

Open your terminal and run:

```bash
npx create-react-app cold-email-generator
cd cold-email-generator
```

### Step 2: Install Required Dependencies

Only one dependency needed for icons:

```bash
npm install lucide-react
```

### Step 3: Replace App.js

1. Navigate to `src/App.js`
2. Delete all existing code
3. Copy the React component code from the artifact above and paste it into `src/App.js`

### Step 4: Clean Up CSS (Optional)

You can optionally clean up `src/index.css` to just have:

```css
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

### Step 5: Update API Endpoint (if needed)

If your backend API is running on a different port or address, update the `API` constant at the top of `App.js`:

```javascript
const API = 'http://127.0.0.1:8000'; // Change this to your backend URL
```

## 🏃‍♂️ Running the Application

### Start the Development Server

```bash
npm start
```

The app will open in your browser at `http://localhost:3000`

### Build for Production

```bash
npm run build
```

This creates an optimized production build in the `build` folder.

## 📁 Project Structure

```
frontend-react/
├── public/
│   ├── index.html
│   └── ...
├── src/
│   ├── App.js          # Main application (contains all components + CSS)
│   ├── index.css       # Optional base styles
│   ├── index.js        # React entry point
│   └── ...
├── package.json
└── README.md
```

## 🧩 Component Architecture

The app uses a single-file component structure with all CSS embedded:

**Components:**
- **Header** - Top banner with gradient background
- **InputField** - Reusable text input with icon
- **TextAreaField** - Reusable textarea with icon
- **SectionTitle** - Styled section headers with accent bar
- **FileUpload** - PDF file upload with preview
- **LoadingSpinner** - Animated loading indicator
- **App** - Main component with state management

**All CSS is included** in the `<style>` tag within the component - no external CSS files needed!

## 🔧 Configuration

### CORS Configuration

Make sure your backend API allows requests from `http://localhost:3000`. Add CORS headers:

**FastAPI Example:**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Express.js Example:**
```javascript
const cors = require('cors');
app.use(cors({
  origin: 'http://localhost:3000'
}));
```

## 🎨 Customization

### Changing Colors

All colors are defined in the CSS within the component. To change the purple theme:

1. Find the `<style>` tag in `App.js`
2. Replace color values:
   - `#667eea` → Your primary color
   - `#764ba2` → Your secondary color
   - Gradients: `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`

### Example Color Schemes:

**Blue Theme:**
```css
/* Replace #667eea with #3b82f6 */
/* Replace #764ba2 with #1d4ed8 */
```

**Green Theme:**
```css
/* Replace #667eea with #10b981 */
/* Replace #764ba2 with #059669 */
```

**Orange Theme:**
```css
/* Replace #667eea with #f59e0b */
/* Replace #764ba2 with #d97706 */
```

### Modifying the API Endpoints

Update these functions in `App.js`:

```javascript
// Email generation endpoint
const handleGenerateEmail = async (e) => {
  const response = await fetch(`${API}/generate-email`, { ... });
}

// Email sending endpoint
const handleSendEmail = async () => {
  await fetch(`${API}/send-email`, { ... });
}
```

## 🐛 Troubleshooting

### App won't start
```bash
# Check Node.js version
node --version

# Should be v16 or higher
# If issues persist, delete and reinstall:
rm -rf node_modules package-lock.json
npm install
```

### API Connection Issues
- ✅ Verify backend is running: `curl http://127.0.0.1:8000`
- ✅ Check browser console (F12) for CORS errors
- ✅ Ensure backend has proper CORS configuration
- ✅ Try using `http://localhost:8000` instead of `127.0.0.1`

### Icons not showing
```bash
# Reinstall lucide-react
npm uninstall lucide-react
npm install lucide-react
```

### Build errors
```bash
# Clear cache and rebuild
npm run build
# If errors, check console for specific issues
```

## 📦 Dependencies

**Required:**
- `react` (v18+) - UI library
- `lucide-react` - Icon library

**No CSS framework needed!** All styling is pure CSS embedded in the component.

## 🌐 Deployment

### Deploy to Vercel

```bash
npm install -g vercel
npm run build
vercel
```

### Deploy to Netlify

1. Run `npm run build`
2. Upload the `build` folder to Netlify
3. Or connect your GitHub repo for automatic deployments

### Deploy to GitHub Pages

```bash
npm install gh-pages --save-dev
```

Add to `package.json`:
```json
"homepage": "https://yourusername.github.io/cold-email-generator",
"scripts": {
  "predeploy": "npm run build",
  "deploy": "gh-pages -d build"
}
```

Then run:
```bash
npm run deploy
```

## 💡 Features

✅ **Pure CSS** - No Tailwind or other frameworks  
✅ **Component-based** - Reusable React components  
✅ **Responsive** - Works on mobile and desktop  
✅ **Animations** - Smooth transitions and effects  
✅ **File Upload** - PDF attachment support  
✅ **Loading States** - Visual feedback for users  
✅ **Modern Design** - Beautiful gradients and shadows  

## 📝 Quick Start Summary

```bash
# 1. Create app
npx create-react-app frontend-react
cd frontend-react

# 2. Install icons
npm install lucide-react

# 3. Replace src/App.js with the artifact code

# 4. Start the app
npm start

# 5. Open http://localhost:3000
```
