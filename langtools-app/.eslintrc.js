module.exports = {
  extends: ['expo'],
  rules: {
    // General rules
    'no-console': 'warn',
    'prefer-const': 'error',
    'no-var': 'error',
    // Disable problematic import rules
    'import/namespace': 'off',
    'import/no-unresolved': 'off',
  },
  ignorePatterns: [
    'node_modules/',
    'dist/',
    'build/',
    '.expo/',
    'convex/_generated/',
  ],
};