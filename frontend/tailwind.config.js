/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                primary: '#0A0302', // Based on PWA_APP_THEME_COLOR
                secondary: '#ffffff',
            }
        },
    },
    plugins: [],
}
