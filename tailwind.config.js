/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '**/*.{html,js}',
    './vsi_business/settings.py',
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