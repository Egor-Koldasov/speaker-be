# Convex Authentication Setup

The "Create Account" button is not working because Convex authentication needs to be properly initialized. Here's how to fix it:

## Quick Fix

You're getting the error `Could not find public function for 'auth:signIn'` because the Convex backend isn't running. When you click "Create Account", you should now see a more helpful error message that says:

> "Authentication backend is not set up. Please run 'npx convex dev' first. See CONVEX_SETUP.md for instructions."

Here's how to fix it:

### 1. Initialize Convex (Required)

```bash
cd langtools-app
npx convex dev
```

This command will:
- Create a new Convex project interactively
- Generate the proper API types
- Start the development server
- Deploy your auth functions

### 2. Set Required Environment Variables

#### A. Set AUTH_SECRET in Convex Dashboard

You'll see an error about `AUTH_SECRET`. This is required for Convex Auth security:

1. **Go to the Convex Dashboard**: https://dashboard.convex.dev/d/anonymous-langtools-convex/settings/environment-variables?var=AUTH_SECRET
2. **Generate a secret**: Run this command to generate a secure secret:
   ```bash
   openssl rand -hex 32
   ```
3. **Set the variable**: In the Convex dashboard, set `AUTH_SECRET` to the generated value

#### B. Update Your Local Environment

After running `npx convex dev`, you'll get a Convex URL. Add it to your `.env.local`:

```bash
# Create .env.local file
cp .env.example .env.local

# Edit .env.local and add your Convex URL
EXPO_PUBLIC_CONVEX_URL=https://your-actual-convex-deployment.convex.cloud
```

### 3. Enable Real Authentication

Once AUTH_SECRET is set, replace the placeholder auth with the real configuration:

```bash
# Replace convex/auth.ts with the real config
cp convex/auth.config.ts convex/auth.ts
```

### 4. Restart Your Expo App

```bash
npm start
```

## What Was Wrong

The authentication functions in `convex/auth.ts` are properly configured, but they need to be deployed to Convex to work. The `npx convex dev` command:

1. **Deploys your functions** - Makes `auth:signIn`, `auth:signOut`, and `users:getCurrentUser` available
2. **Generates proper types** - Updates `convex/_generated/api.js` with your actual functions
3. **Starts the dev server** - Enables real-time sync between your app and Convex

## Verify It's Working

After running `npx convex dev`:

1. Try creating an account in the app
2. Check the Convex dashboard at https://dashboard.convex.dev
3. You should see your user data in the database

## What's Working Now

The app now handles the missing Convex setup gracefully:

- ✅ **UI Navigation**: All screens and navigation work perfectly
- ✅ **Form Validation**: Login/register forms validate input properly
- ✅ **Error Handling**: Clear error messages guide you to the solution
- ✅ **TypeScript**: Full type safety and compilation

The only thing missing is the actual authentication backend, which requires the Convex setup above.

## Alternative: Mock Authentication (For Development Only)

If you want to test the authenticated screens without setting up Convex, you can temporarily modify `app/index.tsx`:

```typescript
// Replace the authentication check with:
return <Redirect href="/(tabs)" />; // Skip auth, go directly to main app
```

But for real authentication, you need the Convex setup above.

## Troubleshooting

**Error: "Environment variable AUTH_SECRET is used in auth config file but its value was not set"**
- This is the error you're seeing! Follow step 2A above to set the AUTH_SECRET in your Convex dashboard
- Generate the secret with: `openssl rand -hex 32`
- Set it in the Convex dashboard environment variables section

**Error: "Cannot find module '@convex-dev/auth/providers/Password'"**
- Run `npm install` to ensure all dependencies are installed
- Make sure you're using the latest version of `@convex-dev/auth`

**Error: "Project not found"**
- Run `npx convex dev` again and create a new project when prompted
- Make sure you're logged into Convex CLI with `npx convex login`

**Auth still not working**
- Check that your `.env.local` has the correct `EXPO_PUBLIC_CONVEX_URL`
- Verify that `AUTH_SECRET` is set in the Convex dashboard
- Restart your Expo development server with `npm start`
- Check the Convex logs for any deployment errors