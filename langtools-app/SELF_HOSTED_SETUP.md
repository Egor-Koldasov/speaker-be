# Self-Hosted Convex Setup Guide

Perfect! You can run Convex completely self-hosted without using their cloud dashboard. Here's how:

## 🚀 Quick Setup

### 1. Generate Your AUTH_SECRET

```bash
# Generate a secure secret
openssl rand -hex 32
```

### 2. Your Environment is Already Set Up!

I've created `.env.local` with:
- `EXPO_PUBLIC_CONVEX_URL=http://localhost:3210` (local Convex server)
- `AUTH_SECRET=<generated-secret>` (required for auth)

### 3. Start Local Convex Development Server

```bash
cd langtools-app

# This starts a local Convex server (no cloud required)
npx convex dev --url http://localhost:3210
```

### 4. Start Your React Native App

```bash
npm start
```

## 🔧 How This Works

### Self-Hosted Architecture

```
React Native App (Expo) 
    ↓ 
Local Convex Server (localhost:3210)
    ↓
Local Database (SQLite/File-based)
```

### Environment Variables

- **`AUTH_SECRET`**: Set locally in `.env.local` (no dashboard needed)
- **`EXPO_PUBLIC_CONVEX_URL`**: Points to your local server
- **No cloud dependencies**: Everything runs on your machine

### Authentication Flow

1. User enters email/password in React Native app
2. Convex Auth validates credentials using local AUTH_SECRET
3. User data stored in local database
4. JWT tokens managed locally

## 🛠️ Self-Hosted Benefits

- ✅ **No external dependencies**: Runs completely offline
- ✅ **Full data control**: Your data never leaves your machine
- ✅ **No accounts required**: No Convex cloud signup needed
- ✅ **Fast development**: No network latency
- ✅ **Privacy**: All authentication happens locally

## 📁 Local Data Storage

Your user data will be stored locally in:
```
langtools-app/convex/_storage/
```

This includes:
- User accounts and profiles
- Authentication sessions
- Any app data you create

## 🔄 Alternative: Pure Local Development

If you want even simpler local development, you can skip Convex entirely and use mock data:

1. **Edit `app/index.tsx`**:
   ```typescript
   // Skip authentication completely
   return <Redirect href="/(tabs)" />;
   ```

2. **Use mock data in components** instead of Convex queries

But with the self-hosted Convex setup above, you get real authentication without any cloud dependencies!

## 🚨 Troubleshooting

**Error: "Cannot connect to localhost:3210"**
- Make sure `npx convex dev --url http://localhost:3210` is running
- Check that port 3210 is not blocked by firewall

**Error: "AUTH_SECRET not found"**
- Verify `.env.local` exists and contains AUTH_SECRET
- Restart both Convex dev server and Expo app

**Auth still not working**
- Check Convex dev server logs for errors
- Verify your `.env.local` file is in the correct location
- Try regenerating AUTH_SECRET with a new random value

## 🎯 Next Steps

Once this is working:
- All authentication will work normally
- You can create users, sign in/out
- Add more Convex functions for your app features
- Scale to cloud Convex later if needed (optional)

Your app now runs completely self-hosted! 🎉