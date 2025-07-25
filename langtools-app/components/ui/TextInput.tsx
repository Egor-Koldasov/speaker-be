import React, { useState } from 'react';
import {
  TextInput as RNTextInput,
  View,
  Text,
  StyleSheet,
  TextInputProps,
  ViewStyle,
  TextStyle,
} from 'react-native';
import { Colors } from '@/constants/Colors';

interface CustomTextInputProps extends TextInputProps {
  label?: string;
  error?: string | undefined;
  containerStyle?: ViewStyle;
  inputStyle?: TextStyle;
  labelStyle?: TextStyle;
  errorStyle?: TextStyle;
}

export default function TextInput({
  label,
  error,
  containerStyle,
  inputStyle,
  labelStyle,
  errorStyle,
  onFocus,
  onBlur,
  ...props
}: CustomTextInputProps): JSX.Element {
  const [isFocused, setIsFocused] = useState(false);

  const handleFocus = (e: any): void => {
    setIsFocused(true);
    onFocus?.(e);
  };

  const handleBlur = (e: any): void => {
    setIsFocused(false);
    onBlur?.(e);
  };

  const inputContainerStyle = [
    styles.inputContainer,
    isFocused && styles.inputContainerFocused,
    error && styles.inputContainerError,
  ];

  const textInputStyle = [
    styles.input,
    inputStyle,
  ];

  return (
    <View style={[styles.container, containerStyle]}>
      {label && (
        <Text style={[styles.label, labelStyle]}>
          {label}
        </Text>
      )}
      <View style={inputContainerStyle}>
        <RNTextInput
          style={textInputStyle}
          onFocus={handleFocus}
          onBlur={handleBlur}
          placeholderTextColor={Colors.tertiaryLabel}
          {...props}
        />
      </View>
      {error && (
        <Text style={[styles.error, errorStyle]}>
          {error}
        </Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginBottom: 16,
  },
  label: {
    fontSize: 16,
    fontWeight: '500',
    color: Colors.label,
    marginBottom: 8,
  },
  inputContainer: {
    borderWidth: 1,
    borderColor: Colors.inputBorder,
    borderRadius: 8,
    backgroundColor: Colors.inputBackground,
    paddingHorizontal: 12,
    minHeight: 44,
    justifyContent: 'center',
  },
  inputContainerFocused: {
    borderColor: Colors.inputBorderFocused,
    backgroundColor: Colors.systemBackground,
  },
  inputContainerError: {
    borderColor: Colors.error,
  },
  input: {
    fontSize: 16,
    color: Colors.label,
    padding: 0,
    margin: 0,
  },
  error: {
    fontSize: 14,
    color: Colors.error,
    marginTop: 4,
  },
});