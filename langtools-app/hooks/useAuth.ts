import { useAuthActions } from '@convex-dev/auth/react';
import { useConvexAuth } from 'convex/react';
import { useState } from 'react';
import type { AuthUser, AuthError, LoginForm, RegisterForm } from '@/types/auth';

/**
 * Custom hook for authentication functionality
 */
export function useAuth() {
  const { isLoading, isAuthenticated } = useConvexAuth();
  const { signIn, signOut } = useAuthActions();
  const [authError, setAuthError] = useState<AuthError | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Get current user data
  // Note: This would need to be implemented as a Convex query
  // const currentUser = useQuery(api.users.getCurrentUser);

  const handleSignIn = async (formData: LoginForm): Promise<boolean> => {
    setIsSubmitting(true);
    setAuthError(null);

    try {
      await signIn('password', {
        email: formData.email,
        password: formData.password,
        flow: 'signIn',
      });
      return true;
    } catch (error) {
      // Handle sign in error
      const errorMessage = error instanceof Error ? error.message : 'Failed to sign in';
      
      // Check if it's the Convex setup error
      if (errorMessage.includes('Convex auth not initialized')) {
        setAuthError({
          code: 'CONVEX_NOT_INITIALIZED',
          message: 'Authentication backend is not set up. Please run "npx convex dev" first. See CONVEX_SETUP.md for instructions.',
        });
      } else {
        setAuthError({
          code: 'SIGN_IN_ERROR',
          message: errorMessage,
        });
      }
      return false;
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleSignUp = async (formData: RegisterForm): Promise<boolean> => {
    setIsSubmitting(true);
    setAuthError(null);

    if (formData.password !== formData.confirmPassword) {
      setAuthError({
        code: 'PASSWORD_MISMATCH',
        message: 'Passwords do not match',
      });
      setIsSubmitting(false);
      return false;
    }

    try {
      // Starting sign up process
      await signIn('password', {
        email: formData.email,
        password: formData.password,
        flow: 'signUp',
      });
      // Sign up successful
      
      // Auth state should update automatically
      setTimeout(() => {
        // Auth state should be updated now
      }, 100);
      
      return true;
    } catch (error) {
      // Handle sign up error
      const errorMessage = error instanceof Error ? error.message : 'Failed to sign up';
      
      // Check if it's the Convex setup error
      if (errorMessage.includes('Convex auth not initialized')) {
        setAuthError({
          code: 'CONVEX_NOT_INITIALIZED',
          message: 'Authentication backend is not set up. Please run "npx convex dev" first. See CONVEX_SETUP.md for instructions.',
        });
      } else {
        setAuthError({
          code: 'SIGN_UP_ERROR',
          message: errorMessage,
        });
      }
      return false;
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleSignOut = async (): Promise<void> => {
    try {
      await signOut();
    } catch {
      // Handle sign out error
    }
  };

  const clearError = (): void => {
    setAuthError(null);
  };

  return {
    // Auth state
    isLoading,
    isAuthenticated,
    isSubmitting,
    user: null as AuthUser | null, // Would be populated from currentUser query
    error: authError,

    // Auth actions
    signIn: handleSignIn,
    signUp: handleSignUp,
    signOut: handleSignOut,
    clearError,
  };
}