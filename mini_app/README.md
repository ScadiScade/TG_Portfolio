# Telegram Mini App (TMA) 📱

A portfolio project demonstrating the creation of a **Telegram Web App** (Mini App) using **TypeScript**, **HTML**, and **Vite**.

## Features
- **Native Telegram UI Integration**: Seamlessly pulls color variables from the user's current Telegram theme (`--tg-theme-bg-color`, etc.).
- **User Data Extraction**: Extracts user info (ID, Username, Premium Status) via `Telegram.WebApp.initDataUnsafe`.
- **Native Interactions**: Uses native Telegram popups (`showConfirm`, `showAlert`) and the native Main Button (`tg.MainButton`).
- **Data Transfer**: Sends JSON data back to the Telegram bot when executed inside a Keyboard button context (`tg.sendData()`).

## Tech Stack
- **TypeScript** (Vanilla, No heavy frameworks)
- **Vite** (Fast dev server and bundler)
- **Telegram WebApp API**

## How to run
1. Clone this repository.
2. Ensure you have Node.js installed.
3. Install dependencies:
   ```bash
   npm install
   ```
4. Start the development server:
   ```bash
   npm run dev
   ```

## How to deploy for your bot
To connect this app to a Telegram bot, you must host it online with HTTPS:
1. Build the project: `npm run build`
2. Deploy the `dist` folder to GitHub Pages, Netlify, Render, or any static host.
3. Use BotFather (`/setmenubutton` or `/newapp`) to connect your app URL.

*Created to demonstrate frontend Web App skills for freelance clients.*
