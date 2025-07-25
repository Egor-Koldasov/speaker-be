import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
  Alert,
} from 'react-native';
import { Link, router } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useAuth } from '@/hooks/useAuth';
import Button from '@/components/ui/Button';
import TextInput from '@/components/ui/TextInput';
import { Colors } from '@/constants/Colors';
import type { RegisterForm } from '@/types/auth';

export default function RegisterScreen(): JSX.Element {
  const { signUp, isSubmitting, error, clearError } = useAuth();
  const [formData, setFormData] = useState<RegisterForm>({
    email: '',
    password: '',
    confirmPassword: '',
    name: '',
  });
  const [formErrors, setFormErrors] = useState<Partial<RegisterForm>>({});

  const validateForm = (): boolean => {
    const errors: Partial<RegisterForm> = {};

    if (!formData.email.trim()) {
      errors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      errors.email = 'Please enter a valid email address';
    }

    if (!formData.password) {
      errors.password = 'Password is required';
    } else if (formData.password.length < 8) {
      errors.password = 'Password must be at least 8 characters';
    } else if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(formData.password)) {
      errors.password = 'Password must contain uppercase, lowercase, and number';
    }

    if (!formData.confirmPassword) {
      errors.confirmPassword = 'Please confirm your password';
    } else if (formData.password !== formData.confirmPassword) {
      errors.confirmPassword = 'Passwords do not match';
    }

    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (): Promise<void> => {
    clearError();
    
    if (!validateForm()) {
      return;
    }

    // Attempting to sign up with the provided credentials
    const success = await signUp(formData);
    
    if (success) {
      // Sign up successful, auth state should update
      
      // Force navigation to home after successful signup
      setTimeout(() => {
        // Force navigating to main app
        router.replace('/(tabs)');
      }, 1000);
    } else if (error) {
      // Sign up failed with error
      Alert.alert('Sign Up Error', error.message);
    }
  };

  const updateFormData = (field: keyof RegisterForm, value: string): void => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Clear field error when user starts typing
    if (formErrors[field]) {
      setFormErrors(prev => ({ ...prev, [field]: undefined }));
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.keyboardAvoidingView}
      >
        <ScrollView
          contentContainerStyle={styles.scrollContainer}
          keyboardShouldPersistTaps="handled"
        >
          <View style={styles.header}>
            <Text style={styles.title}>Create Account</Text>
            <Text style={styles.subtitle}>
              Join us to start your language learning adventure
            </Text>
          </View>

          <View style={styles.form}>
            <TextInput
              label="Name (Optional)"
              value={formData.name}
              onChangeText={(text) => updateFormData('name', text)}
              placeholder="Enter your name"
              autoCapitalize="words"
              autoComplete="name"
              textContentType="name"
            />

            <TextInput
              label="Email"
              value={formData.email}
              onChangeText={(text) => updateFormData('email', text)}
              error={formErrors.email}
              placeholder="Enter your email"
              keyboardType="email-address"
              autoCapitalize="none"
              autoComplete="email"
              textContentType="emailAddress"
            />

            <TextInput
              label="Password"
              value={formData.password}
              onChangeText={(text) => updateFormData('password', text)}
              error={formErrors.password}
              placeholder="Create a password"
              secureTextEntry
              autoComplete="new-password"
              textContentType="newPassword"
            />

            <TextInput
              label="Confirm Password"
              value={formData.confirmPassword}
              onChangeText={(text) => updateFormData('confirmPassword', text)}
              error={formErrors.confirmPassword}
              placeholder="Confirm your password"
              secureTextEntry
              autoComplete="new-password"
              textContentType="newPassword"
            />

            <View style={styles.passwordRequirements}>
              <Text style={styles.requirementsTitle}>Password Requirements:</Text>
              <Text style={styles.requirementItem}>• At least 8 characters</Text>
              <Text style={styles.requirementItem}>• One uppercase letter</Text>
              <Text style={styles.requirementItem}>• One lowercase letter</Text>
              <Text style={styles.requirementItem}>• One number</Text>
            </View>

            <Button
              title="Create Account"
              onPress={handleSubmit}
              loading={isSubmitting}
              disabled={isSubmitting}
              style={styles.signUpButton}
            />
          </View>

          <View style={styles.footer}>
            <Text style={styles.footerText}>Already have an account? </Text>
            <Link href="/(auth)/login" asChild>
              <Text style={styles.signInLink}>Sign In</Text>
            </Link>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.systemBackground,
  },
  keyboardAvoidingView: {
    flex: 1,
  },
  scrollContainer: {
    flexGrow: 1,
    padding: 24,
    justifyContent: 'center',
  },
  header: {
    alignItems: 'center',
    marginBottom: 32,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: Colors.label,
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: Colors.secondaryLabel,
    textAlign: 'center',
    lineHeight: 22,
  },
  form: {
    marginBottom: 24,
  },
  passwordRequirements: {
    backgroundColor: Colors.secondarySystemBackground,
    padding: 16,
    borderRadius: 8,
    marginBottom: 16,
  },
  requirementsTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: Colors.label,
    marginBottom: 8,
  },
  requirementItem: {
    fontSize: 13,
    color: Colors.secondaryLabel,
    marginBottom: 2,
  },
  signUpButton: {
    marginTop: 8,
  },
  footer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
  },
  footerText: {
    fontSize: 16,
    color: Colors.secondaryLabel,
  },
  signInLink: {
    fontSize: 16,
    color: Colors.link,
    fontWeight: '600',
  },
});