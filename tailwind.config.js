// tailwind.config.js
module.exports = {
  purge: {
    content: [
      './choralcat_core/**/*.html',
      './choralcat_web/**/*.html',
    ],
  },
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {},
  },
  variants: {},
  plugins: [],
}
