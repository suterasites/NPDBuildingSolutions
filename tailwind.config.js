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
        ink: {
          DEFAULT: '#191919',
          soft: '#4c4c4c',
          muted: '#7f7f7f',
          line: '#e5e5e5',
          bg: '#f2f2f2',
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
