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
    extend: {
      fontFamily: {
        header: ['Bree Serif', 'serif'],
        body: ['Rubik', 'sans-serif'],
      },
      colors: {
        primary: "#C51A4A",
        accent: "#A2157B",
        neutral: "#1B0E12",
        primary000: "#2d0611",
        primary100: "#510b1f",
        primary200: "#710f2a",
        primary300: "#ac1641",
        primary400: "#e22258",
        primary500: "#ea5d85",
        primary600: "#f193ad",
        primary700: "#f8c9d6",
        primary800: "#fce8ee",
        primary900: "#fef6f8",
        accent000: "#2d0622",
        accent100: "#510b3d",
        accent200: "#710f55",
        accent300: "#ac1681",
        accent400: "#e222ac",
        accent500: "#ea5dc2",
        accent600: "#f193d6",
        accent700: "#f8c9eb",
        accent800: "#fce8f7",
        accent900: "#fef6fc",
        neutral000: "#1b0e12",
        neutral100: "#4c333a",
        neutral200: "#766066",
        neutral300: "#907f84",
        neutral400: "#a7a0a2",
        neutral500: "#c7c2c3",
        neutral600: "#dfdddd",
        neutral700: "#ebeaea",
        neutral800: "#f8f7f7",
        neutral900: "#fcfcfc",
      }
    },
  },
  variants: {},
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
