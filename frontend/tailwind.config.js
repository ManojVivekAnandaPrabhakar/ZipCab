/** @type {import('tailwindcss').Config} */
export default {
  // CRITICAL: This content array tells Tailwind where to find your utility classes.
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}