/**
 * App color constants following iOS design guidelines
 */

export const Colors = {
  // Primary colors
  primary: '#007AFF',
  primaryDark: '#0056CC',
  
  // Secondary colors
  secondary: '#5856D6',
  secondaryDark: '#3634A3',
  
  // System colors
  systemBlue: '#007AFF',
  systemGreen: '#34C759',
  systemRed: '#FF3B30',
  systemOrange: '#FF9500',
  systemYellow: '#FFCC00',
  systemPink: '#FF2D92',
  systemPurple: '#AF52DE',
  systemTeal: '#5AC8FA',
  systemIndigo: '#5856D6',
  
  // Gray scale
  label: '#000000',
  secondaryLabel: '#3C3C43',
  tertiaryLabel: '#3C3C43',
  quaternaryLabel: '#3C3C43',
  
  // Background colors
  systemBackground: '#FFFFFF',
  secondarySystemBackground: '#F2F2F7',
  tertiarySystemBackground: '#FFFFFF',
  
  // Grouped background colors
  systemGroupedBackground: '#F2F2F7',
  secondarySystemGroupedBackground: '#FFFFFF',
  tertiarySystemGroupedBackground: '#F2F2F7',
  
  // Fill colors
  systemFill: '#787880',
  secondarySystemFill: '#787880',
  tertiarySystemFill: '#767680',
  quaternarySystemFill: '#747480',
  
  // Separator colors
  separator: '#C6C6C8',
  opaqueSeparator: '#C6C6C8',
  
  // Link color
  link: '#007AFF',
  
  // Text colors
  text: '#000000',
  textSecondary: '#3C3C43',
  textTertiary: '#3C3C43',
  
  // Input colors
  inputBackground: '#F2F2F7',
  inputBorder: '#C7C7CC',
  inputBorderFocused: '#007AFF',
  
  // Error colors
  error: '#FF3B30',
  errorBackground: '#FFEBEE',
  
  // Success colors
  success: '#34C759',
  successBackground: '#E8F5E8',
  
  // Warning colors
  warning: '#FF9500',
  warningBackground: '#FFF3E0',
} as const;

export const lightColors = Colors;

export const darkColors = {
  ...Colors,
  // Override colors for dark mode
  label: '#FFFFFF',
  systemBackground: '#000000',
  secondarySystemBackground: '#1C1C1E',
  text: '#FFFFFF',
} as const;