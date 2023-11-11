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
    themes: [
      {
        mytheme: {
          "primary": "#65c3c8",
          "secondary": "#ef9fbc",
          "accent": "#eeaf3a",
          "neutral": "#291334",
          "base-100": "#faf7f5",
          "info": "#3abff8",
          "success": "#36d399",
          "warning": "#fbbd23",
          "error": "#f87272",
        },
      },
    ],
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
    require('@tailwindcss/typography'),
    require('daisyui')
  ],
}

