/** @type {import('postcss-load-config').Config} */
export default {
  plugins: {
    // CRITICAL FIX: The core 'tailwindcss' package no longer works directly here in v4.
    // It must use the separate '@tailwindcss/postcss' package once installed.
    '@tailwindcss/postcss': {},
    autoprefixer: {},
  },
}
