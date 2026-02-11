/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        "lab-bg": "var(--color-bg)",
        "lab-surface": "var(--color-surface)",
        "lab-accent": "var(--color-accent)",
        "lab-accent-soft": "var(--color-accent-soft)",
        "lab-danger": "var(--color-danger)"
      },
      fontFamily: {
        serif: ["'Playfair Display'", "'Libre Baskerville'", "serif"],
        mono: ["'Space Mono'", "ui-monospace", "SFMono-Regular", "monospace"]
      }
    }
  },
  plugins: []
};

