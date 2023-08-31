/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '**/templates/**/*.html'
  ],
  theme: {
    fontFamily: {
      sans: ['Open Sans', 'sans-serif'],
    }
  },
  daisyui: {
    themes: ["corporate"],
    darkTheme: false,
    base: true,
    styled: true,
    utils: true,
    rtl: false,
    prefix: "",
    logs: true
  },
  plugins: [
    require('@tailwindcss/forms'),
    require("@tailwindcss/typography"),
    require('daisyui')
  ],
}

