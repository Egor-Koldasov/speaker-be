/**
 * Authentication-related TypeScript types
 */

export interface AuthUser {
  id: string;
  email: string;
  name?: string;
  createdAt: number;
}

export interface LoginForm {
  email: string;
  password: string;
}

export interface RegisterForm {
  email: string;
  password: string;
  confirmPassword: string;
  name?: string;
}

export interface ForgotPasswordForm {
  email: string;
}

export interface AuthError {
  code: string;
  message: string;
}

export interface AuthState {
  user: AuthUser | null;
  isLoading: boolean;
  error: AuthError | null;
}