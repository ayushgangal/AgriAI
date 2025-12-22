# AgriAI Frontend

A modern React-based frontend for the AgriAI agricultural advisory system, designed to provide farmers with AI-powered insights for weather, crops, finance, and farming practices.

## Features

### 🤖 AI Chat Interface
- **Text Queries**: Natural language processing for agricultural questions
- **Voice Input**: Speech-to-text conversion with multi-language support
- **Image Analysis**: Upload images for crop disease identification
- **Query History**: Track and review previous interactions
- **Feedback System**: Rate AI responses for continuous improvement

### 🌤️ Weather Intelligence
- **Real-time Weather**: Current conditions with detailed metrics
- **7-Day Forecast**: Extended weather predictions
- **Agricultural Alerts**: Weather-based farming recommendations
- **Location Services**: GPS integration for precise local data
- **Weather Recommendations**: Farming advice based on weather conditions

### 🌾 Crop Management
- **Smart Recommendations**: AI-powered crop suggestions based on location and weather
- **Suitability Scoring**: Detailed analysis of crop compatibility
- **Management Advice**: Growth stage-specific guidance
- **Disease & Pest Alerts**: Risk assessment and prevention tips
- **Seasonal Planning**: Optimal timing for planting and harvesting

### 💰 Financial Guidance
- **Credit Schemes**: Information about agricultural loans and subsidies
- **Market Trends**: Real-time crop price monitoring
- **Loan Calculator**: EMI calculations for agricultural financing
- **Financial Tips**: Best practices for farm economics
- **Government Schemes**: Latest agricultural support programs

### 🎤 Voice Interface
- **Multi-language Support**: 10+ Indian languages
- **Speech Recognition**: High-accuracy voice-to-text conversion
- **Text-to-Speech**: Audio responses for accessibility
- **Language Detection**: Automatic language identification
- **Voice Commands**: Quick access to common queries

## Technology Stack

- **React 18**: Modern React with hooks and functional components
- **React Query**: Server state management and caching
- **React Router**: Client-side routing
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client for API communication
- **React Hot Toast**: User notifications
- **Heroicons**: Beautiful SVG icons
- **Framer Motion**: Smooth animations

## API Integration

The frontend is fully integrated with the AgriAI backend API, providing:

### Core Endpoints
- `/api/v1/` - AI query processing
- `/api/v1/weather/*` - Weather data and forecasts
- `/api/v1/crops/*` - Crop recommendations and management
- `/api/v1/finance/*` - Financial information and calculations
- `/api/v1/voice/*` - Voice processing services

### Key Features
- **Real-time Data**: Live weather, market prices, and recommendations
- **Error Handling**: Graceful fallbacks and user-friendly error messages
- **Loading States**: Smooth loading indicators and skeleton screens
- **Caching**: Intelligent data caching for better performance
- **Offline Support**: Basic offline functionality with cached data

## Getting Started

### Prerequisites
- Node.js 16+ 
- npm or yarn
- AgriAI backend running on `http://localhost:8000`

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm start
   ```

4. **Open your browser**
   Navigate to `http://localhost:3000`

### Environment Configuration

The frontend is configured to proxy API requests to the backend. Ensure your backend is running on the correct port.

## Project Structure

```
src/
├── components/          # Reusable UI components
│   └── Navbar.js       # Navigation component
├── hooks/              # Custom React hooks
│   └── useAPI.js       # API integration hooks
├── pages/              # Page components
│   ├── Chat.js         # AI chat interface
│   ├── Weather.js      # Weather intelligence
│   ├── Crops.js        # Crop management
│   ├── Finance.js      # Financial guidance
│   ├── Voice.js        # Voice interface
│   └── Home.js         # Landing page
├── services/           # API services
│   └── api.js          # API client configuration
├── App.js              # Main application component
└── index.js            # Application entry point
```

## Key Components

### API Service Layer (`services/api.js`)
- Centralized API client with Axios
- Request/response interceptors
- Error handling and authentication
- FormData handling for file uploads

### Custom Hooks (`hooks/useAPI.js`)
- React Query integration for all API calls
- Optimistic updates and caching
- Loading and error states
- Toast notifications for user feedback

### Page Components
Each page component is designed to be:
- **Responsive**: Works on all device sizes
- **Accessible**: WCAG compliant with proper ARIA labels
- **Performant**: Optimized rendering and data fetching
- **User-friendly**: Intuitive interfaces with clear feedback

## Features in Detail

### AI Chat Interface
- **Multi-modal Input**: Text, voice, and image support
- **Context Awareness**: Remembers conversation history
- **Smart Suggestions**: Quick question buttons for common queries
- **Response Analysis**: Shows confidence scores and data sources
- **Feedback System**: Thumbs up/down for response quality

### Weather Intelligence
- **Location Services**: GPS integration with manual override
- **Real-time Updates**: Live weather data with refresh capability
- **Agricultural Context**: Weather interpreted for farming needs
- **Alert System**: Critical weather warnings and recommendations
- **Forecast Planning**: 7-day predictions for farm planning

### Crop Management
- **Location-based Recommendations**: Crops suited to local conditions
- **Weather Integration**: Recommendations adjusted for current weather
- **Growth Stage Support**: Specific advice for different crop phases
- **Risk Assessment**: Disease and pest risk indicators
- **Management Plans**: Detailed care instructions

### Financial Guidance
- **Scheme Information**: Government and bank agricultural schemes
- **Market Intelligence**: Real-time crop prices and trends
- **Loan Calculator**: EMI calculations with detailed breakdowns
- **Financial Planning**: Tips for farm economics
- **Documentation**: Required documents for various schemes

### Voice Interface
- **Multi-language Support**: 10+ Indian languages
- **Real-time Processing**: Live speech-to-text conversion
- **Audio Playback**: Text-to-speech for responses
- **Language Detection**: Automatic language identification
- **Voice Commands**: Quick access to common functions

## Performance Optimizations

- **React Query Caching**: Intelligent data caching and background updates
- **Code Splitting**: Lazy loading of page components
- **Image Optimization**: Efficient image handling and compression
- **Bundle Optimization**: Tree shaking and code splitting
- **Network Optimization**: Request deduplication and caching

## Accessibility Features

- **Keyboard Navigation**: Full keyboard accessibility
- **Screen Reader Support**: Proper ARIA labels and semantic HTML
- **Color Contrast**: WCAG AA compliant color schemes
- **Focus Management**: Clear focus indicators and logical tab order
- **Alternative Text**: Descriptive alt text for all images

## Browser Support

- **Chrome**: 90+
- **Firefox**: 88+
- **Safari**: 14+
- **Edge**: 90+

## Development

### Available Scripts

- `npm start` - Start development server
- `npm build` - Build for production
- `npm test` - Run tests
- `npm eject` - Eject from Create React App

### Code Style

The project follows:
- **ESLint**: Code linting and formatting
- **Prettier**: Code formatting
- **React Best Practices**: Functional components and hooks
- **TypeScript**: Type safety (optional)

## Deployment

### Production Build
```bash
npm run build
```

### Environment Variables
- `REACT_APP_API_URL`: Backend API URL (defaults to proxy)
- `REACT_APP_ENVIRONMENT`: Environment name (development/production)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

---

**AgriAI Frontend** - Empowering farmers with AI-driven agricultural intelligence. 