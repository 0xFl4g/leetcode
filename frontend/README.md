# LeetCode Learning Tool - Frontend

Modern React application for browsing and learning LeetCode problem solutions.

## Overview

The frontend provides an intuitive interface for:
- Browsing LeetCode problems
- Viewing detailed solutions with multiple approaches
- Understanding time/space complexity
- Learning key insights and patterns
- Exploring similar problems

## Technology Stack

- **React 18** - UI library with hooks
- **React Router v6** - Client-side routing
- **Axios** - HTTP client for API requests
- **Tailwind CSS** - Utility-first CSS framework
- **Vite** - Fast build tool and dev server

## Project Structure

```
frontend/
├── src/
│   ├── components/       # React components
│   │   ├── ProblemList.jsx      # Problem browser
│   │   ├── ProblemDetail.jsx    # Solution viewer
│   │   ├── SearchBar.jsx        # Search functionality
│   │   ├── FilterBar.jsx        # Difficulty/topic filters
│   │   └── ErrorMessage.jsx     # Error handling
│   ├── services/         # API integration
│   │   └── api.js       # Axios API client
│   ├── App.jsx          # Main application component
│   ├── main.jsx         # React entry point
│   └── index.css        # Global styles + Tailwind
├── public/              # Static assets
├── dist/                # Production build output
├── index.html           # HTML template
├── vite.config.js       # Vite configuration
├── tailwind.config.js   # Tailwind configuration
└── package.json         # Dependencies and scripts
```

## Setup

### Prerequisites

- Bun (https://bun.sh)

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
bun install
```

### Development

Start the development server:
```bash
bun run dev
```

The application will be available at `http://localhost:5173`

Features in development mode:
- Hot module replacement (HMR)
- Fast refresh for React components
- Source maps for debugging

### Production Build

Create an optimized production build:
```bash
bun run build
```

Built files will be in the `dist/` directory.

Preview the production build:
```bash
bun run preview
```

## Environment Configuration

The frontend connects to the backend API at:
- Development: `http://localhost:8000`
- Production: Configure via `src/services/api.js`

To change the API URL, update the `baseURL` in `src/services/api.js`:
```javascript
const api = axios.create({
  baseURL: 'http://your-api-url:8000',
});
```

## Component Architecture

### App.jsx
Main application component that sets up routing and global state.

### ProblemList.jsx
Displays a list of problems with filtering and search capabilities.

Features:
- Difficulty filtering (Easy, Medium, Hard)
- Topic filtering
- Search by title or topic
- Responsive card layout

### ProblemDetail.jsx
Shows detailed solution information for a selected problem.

Features:
- Multiple solution approaches
- Syntax-highlighted code
- Complexity analysis
- Key insights
- Edge cases
- Similar problems

### SearchBar.jsx
Real-time search functionality with debouncing.

### FilterBar.jsx
Difficulty and topic filters with clear buttons.

### ErrorMessage.jsx
Displays user-friendly error messages.

## API Integration

The application uses Axios to communicate with the backend API.

### API Service (`src/services/api.js`)

```javascript
// Get all problems
api.get('/api/problems')

// Filter by difficulty
api.get('/api/problems?difficulty=Easy')

// Filter by topic
api.get('/api/problems?topic=Array')

// Search problems
api.get('/api/search?q=sum')

// Get specific problem
api.get('/api/problems/two-sum')

// Get by LeetCode URL
api.get('/api/problems/by-url?url=...')
```

## Styling

The application uses Tailwind CSS for styling.

### Tailwind Configuration

The `tailwind.config.js` file defines:
- Custom color palette
- Responsive breakpoints
- Custom utilities

### Custom Styles

Global styles are in `src/index.css`:
- Tailwind base, components, utilities
- Custom component styles
- Typography styles

### Responsive Design

The application is fully responsive:
- Mobile-first approach
- Breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px)
- Flexible grid layouts
- Responsive navigation

## State Management

Currently uses React's built-in state management:
- `useState` for component state
- `useEffect` for side effects
- `useParams` for route parameters

For larger applications, consider adding:
- React Context for global state
- Redux or Zustand for complex state management

## Routing

React Router v6 handles client-side routing:

```javascript
Routes:
  / - Home page with problem list
  /problems/:problemId - Problem detail view
```

## Performance Optimizations

- Code splitting via dynamic imports
- Lazy loading of components
- Memoization with `useMemo` and `useCallback`
- Image optimization
- Minification in production build
- Tree shaking for smaller bundle size

## Browser Support

Supports modern browsers:
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Development Guidelines

### Code Style

- Use functional components with hooks
- Follow React naming conventions
- Use descriptive variable names
- Add PropTypes or TypeScript for type checking
- Keep components small and focused

### File Naming

- Components: PascalCase (e.g., `ProblemList.jsx`)
- Utilities: camelCase (e.g., `api.js`)
- Styles: kebab-case (e.g., `custom-styles.css`)

### Component Structure

```javascript
// 1. Imports
import React, { useState, useEffect } from 'react';

// 2. Component definition
function ComponentName({ prop1, prop2 }) {
  // 3. State declarations
  const [state, setState] = useState(initialValue);

  // 4. Effects
  useEffect(() => {
    // effect logic
  }, [dependencies]);

  // 5. Event handlers
  const handleClick = () => {
    // handler logic
  };

  // 6. Render
  return (
    <div>
      {/* JSX */}
    </div>
  );
}

// 7. Export
export default ComponentName;
```

## Debugging

### React DevTools

Install React Developer Tools browser extension for:
- Component tree inspection
- Props and state inspection
- Performance profiling

### Console Logging

API responses are logged in development mode.

### Error Boundaries

Consider adding error boundaries for better error handling:
```javascript
class ErrorBoundary extends React.Component {
  // Error boundary implementation
}
```

## Testing (Future)

Recommended testing setup:
- **Vitest** - Unit testing
- **React Testing Library** - Component testing
- **Playwright** or **Cypress** - E2E testing

## Deployment

### Build for Production

```bash
npm run build
```

### Deployment Options

- **Vercel** - Zero-config deployment (recommended for Vite)
- **Netlify** - Easy static site hosting
- **AWS S3 + CloudFront** - Scalable cloud hosting
- **GitHub Pages** - Free hosting for static sites

### Deployment Configuration

Most platforms auto-detect Vite projects. If manual configuration is needed:
- Build command: `npm run build`
- Output directory: `dist`
- Install command: `npm install`

## Environment Variables

Vite uses `import.meta.env` for environment variables.

Create `.env` files for different environments:

**.env.development**
```
VITE_API_URL=http://localhost:8000
```

**.env.production**
```
VITE_API_URL=https://api.your-domain.com
```

Access in code:
```javascript
const apiUrl = import.meta.env.VITE_API_URL;
```

## Future Enhancements

- Add TypeScript for type safety
- Implement user authentication
- Add dark mode toggle
- Implement solution bookmarking
- Add code playground for testing solutions
- Mobile app (React Native)
- Progressive Web App (PWA) features
- Offline support with service workers
- Solution submission tracking
- Performance analytics

## Troubleshooting

### Port Already in Use

If port 5173 is already in use:
```bash
npm run dev -- --port 3000
```

### Module Not Found

Clear node_modules and reinstall:
```bash
rm -rf node_modules package-lock.json
npm install
```

### Build Errors

Clear Vite cache:
```bash
rm -rf node_modules/.vite
npm run build
```

## Resources

- [React Documentation](https://react.dev/)
- [React Router Documentation](https://reactrouter.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [Vite Documentation](https://vitejs.dev/)
- [Axios Documentation](https://axios-http.com/)
