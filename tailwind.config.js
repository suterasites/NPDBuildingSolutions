/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./**/*.html'],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: '#E8710A',
          dark: '#CC6010',
          light: '#F09A4E',
          50: '#FEF5EC',
          100: '#FDEBD4',
        },
      },
      fontFamily: {
        display: ['"Barlow Condensed"', 'Arial Narrow', 'sans-serif'],
        body: ['"Inter"', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
