/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '**/*.{html,js}',
    './healthy_herbs/settings.py',
    './application_processors/*.py',
    '**/tables.py'
  ],
  plugins: [
    require('flowbite/plugin'),
  ],
  safelist: [
    'info',
    'success',
    'warning',
    'error',
  ],
}