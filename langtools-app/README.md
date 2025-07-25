# Langtools App

React Native mobile application for language learning tools with Convex backend authentication.

## Overview

This package provides a mobile app interface for the langtools ecosystem, featuring:

- **Email/password authentication** with Convex backend
- **React Native + Expo** for cross-platform mobile development
- **TypeScript** for type safety
- **Expo Router** for file-based navigation
- **Modern authentication flows** with secure token storage

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- Expo CLI: `npm install -g @expo/cli`
- EAS CLI: `npm install -g @expo/eas-cli`

### Development Setup

```bash
# Install dependencies
npm install

# Start development server
npm start

# Run on specific platforms
npm run android  # Android
npm run ios      # iOS
npm run web      # Web
```

### Quality Assurance

```bash
# Run all quality checks
./scripts/lint.sh

# Run tests only
./scripts/test.sh

# Type checking
npm run type-check

# Linting
npm run lint
```

### Building

```bash
# Development build
./scripts/build.sh

# Platform-specific builds
./scripts/build.sh android
./scripts/build.sh ios
./scripts/build.sh all
```

## Architecture

### Authentication Flow

1. **Login/Register screens** for email/password input
2. **Convex authentication** handles user validation
3. **Secure token storage** via expo-secure-store
4. **Authenticated navigation** to main app screens

### Project Structure

```
langtools-app/
├── app/                    # Expo Router file-based routing
│   ├── (auth)/            # Authentication group routes
│   ├── (tabs)/            # Main app tab navigation
│   └── _layout.tsx        # Root layout with providers
├── components/            # Reusable UI components
├── hooks/                 # Custom React hooks
├── services/              # API and business logic
├── types/                 # TypeScript type definitions
├── constants/             # App constants
└── scripts/               # Build and quality scripts
```

### Key Dependencies

- **Expo SDK 52+** - React Native framework
- **Convex** - Real-time database and authentication
- **Expo Router** - Type-safe navigation
- **TypeScript** - Static type checking
- **ESLint** - Code linting

## Configuration

### Environment Variables

Create `.env.local` with:

```
EXPO_PUBLIC_CONVEX_URL=https://your-convex-deployment.convex.cloud
```

### Convex Setup

The app expects a Convex backend with email/password authentication configured. See the Convex documentation for setup instructions.

## Development Guidelines

### Code Quality

- **Strict TypeScript** configuration with comprehensive type checking
- **ESLint** rules for code consistency
- **Zero-error quality gates** for CI integration
- **Comprehensive testing** with Jest and React Native Testing Library

### Component Patterns

- Use functional components with hooks
- Implement proper TypeScript typing
- Follow React Native best practices
- Use Expo Router for navigation

### Authentication Integration

- Use `@convex-dev/auth` React hooks
- Implement secure token storage
- Handle authentication state properly
- Provide proper error handling

## Deployment

### EAS Build

```bash
# Configure build profiles
eas build:configure

# Build for app stores
eas build --platform all --profile production
```

### Environment Management

- **Development**: Local development with hot reload
- **Preview**: Internal testing builds
- **Production**: App store distribution

## Testing

```bash
# Run all tests
npm test

# Watch mode for development
npm run test:watch
```

## Troubleshooting

### Common Issues

1. **Metro bundler issues**: Clear cache with `npx expo start --clear`
2. **Type errors**: Run `npm run type-check` for detailed output
3. **Build failures**: Check EAS build logs for specific errors

### Quality Gate Failures

All code must pass:
- TypeScript type checking (`npm run type-check`)
- ESLint linting (`npm run lint`)
- Jest tests (`npm test`)

## Integration with Langtools Ecosystem

This package integrates with the broader langtools monorepo:

- **Independent authentication**: Uses Convex for mobile-specific auth
- **Consistent patterns**: Follows langtools code quality standards
- **Quality gates**: Maintains zero-error quality requirements
- **Deployment**: Uses modern mobile deployment practices

## Contributing

1. Follow the existing TypeScript and ESLint configuration
2. Ensure all quality checks pass: `./scripts/lint.sh`
3. Add tests for new functionality
4. Update documentation as needed