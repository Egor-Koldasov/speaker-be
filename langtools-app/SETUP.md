# Langtools App Setup Guide

This guide will help you set up and run the Langtools React Native mobile application.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js 18+** and npm
- **Expo CLI**: `npm install -g @expo/cli`
- **EAS CLI**: `npm install -g @expo/eas-cli`
- **Git** for version control

### Mobile Development Environment

#### For iOS Development:
- **macOS** (required for iOS development)
- **Xcode** (latest version from App Store)
- **iOS Simulator** (included with Xcode)

#### For Android Development:
- **Android Studio** with Android SDK
- **Android Virtual Device (AVD)** or physical Android device
- **Java Development Kit (JDK) 11+**

## Quick Start

### 1. Install Dependencies

```bash
cd langtools-app
npm install
```

### 2. Set Up Environment Variables

Copy the environment template and configure:

```bash
cp .env.example .env.local
```

Edit `.env.local` and add your Convex deployment URL:

```
EXPO_PUBLIC_CONVEX_URL=https://your-convex-deployment.convex.cloud
```

### 3. Set Up Convex Backend

#### Install Convex CLI:
```bash
npm install -g convex
```

#### Initialize Convex:
```bash
npx convex dev
```

This will:
- Create a new Convex project (if needed)
- Generate the `convex/_generated` directory
- Start the Convex development server

#### Configure Authentication:
1. Go to your Convex dashboard
2. Navigate to "Authentication" settings
3. Enable email/password authentication
4. Configure any additional auth providers if desired

### 4. Add Required Assets

Add the following image files to the `assets/` directory:
- `icon.png` (1024x1024) - App icon
- `adaptive-icon.png` (1024x1024) - Android adaptive icon
- `splash.png` (1284x2778) - Splash screen
- `favicon.png` (48x48) - Web favicon

You can use placeholder images initially or generate proper assets using design tools.

### 5. Start Development Server

```bash
npm start
```

This will start the Expo development server. You can then:
- Press `i` to open iOS Simulator
- Press `a` to open Android Emulator
- Scan QR code with Expo Go app on physical device

## Development Workflow

### Running Quality Checks

```bash
# Run all quality checks (linting, type checking, tests)
./scripts/lint.sh

# Run individual checks
npm run lint          # ESLint
npm run type-check    # TypeScript
npm test             # Jest tests
```

### Development Commands

```bash
# Start development server
npm start

# Start on specific platform
npm run android       # Android
npm run ios          # iOS
npm run web          # Web

# Clear cache and restart
npx expo start --clear
```

### Building the App

#### Development Builds
```bash
# Configure EAS Build
eas build:configure

# Build for development
eas build --profile development
```

#### Production Builds
```bash
# Build for app stores
eas build --profile production --platform all
```

## Project Structure Overview

```
langtools-app/
├── app/                    # Expo Router file-based routing
│   ├── (auth)/            # Authentication screens
│   ├── (tabs)/            # Main app navigation
│   └── _layout.tsx        # Root layout with providers
├── components/            # Reusable UI components
├── hooks/                 # Custom React hooks
├── services/              # API and business logic
├── types/                 # TypeScript type definitions
├── constants/             # App constants and colors
├── convex/                # Convex backend configuration
├── assets/                # Images and static assets
├── scripts/               # Build and development scripts
└── tests/                 # Test files
```

## Authentication Flow

1. **Unauthenticated**: User sees login screen
2. **Login/Register**: User enters credentials
3. **Convex Auth**: Handles authentication with secure tokens
4. **Authenticated**: User accesses main app with tabs navigation
5. **Logout**: Returns to authentication flow

## Troubleshooting

### Common Issues

#### Metro bundler problems:
```bash
npx expo start --clear
```

#### TypeScript errors:
```bash
npm run type-check
```

#### Convex connection issues:
- Verify `EXPO_PUBLIC_CONVEX_URL` in `.env.local`
- Ensure Convex development server is running: `npx convex dev`
- Check Convex dashboard for deployment status

#### Build failures:
- Check EAS build logs in terminal or Expo dashboard
- Verify all required environment variables are set
- Ensure all dependencies are properly installed

### Getting Help

1. Check the [Expo Documentation](https://docs.expo.dev/)
2. Review [Convex Documentation](https://docs.convex.dev/)
3. Check [React Navigation Documentation](https://reactnavigation.org/)
4. Search GitHub issues in the repository

## Next Steps

After setting up the app, you can:

1. **Customize the UI** - Modify colors, fonts, and components
2. **Add Features** - Implement language learning functionality
3. **Configure Push Notifications** - Set up Expo Notifications
4. **Add Analytics** - Integrate analytics tracking
5. **Set Up CI/CD** - Configure automated builds and deployments

## Production Deployment

### App Store Submission

1. **Configure app metadata** in `app.json`
2. **Build production version**: `eas build --profile production`
3. **Submit to stores**: `eas submit --platform all`

### Environment Configuration

- **Development**: Local development with hot reload
- **Preview**: Internal testing and staging
- **Production**: App store distribution

Each environment can have different Convex deployments and configuration settings.

---

For more detailed information, see the main [README.md](./README.md) file.