/* eslint-env node */
require('@rushstack/eslint-patch/modern-module-resolution')

module.exports = {
  root: true,
  extends: [
    'plugin:vue/vue3-essential',
    'eslint:recommended',
    '@vue/eslint-config-typescript',
    // '@vue/eslint-config-prettier/skip-formatting'
  ],
  parserOptions: {
    ecmaVersion: 'latest',
  },
  rules: {
    'import/order': 'off',
    'vue/multi-word-component-names': 'off',
    'no-extra-semi': 'off',
  },
  overrides: [
    {
      files: ['src/**/*.ts', 'src/**/*.tsx'], // Your TypeScript files extension

      parserOptions: {
        project: [__dirname + '/tsconfig.vitest.json'], // Specify it only for TypeScript files
      },
      rules: {
        '@typescript-eslint/no-floating-promises': 'error',
        '@typescript-eslint/no-misused-promises': ['error', { checksVoidReturn: false }],
        'no-void': 'off',
      },
    },
  ],
}
