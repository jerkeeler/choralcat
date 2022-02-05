module.exports = {
  plugins: [
    'postcss-preset-env',
    'autoprefixer',
    require('tailwindcss')('./frontend/tailwind.config.js'),
  ],
};
