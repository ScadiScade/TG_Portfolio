# Deploy Guide: Hosting Your Bots 🚀

To make your portfolio accessible, you should host your bots so potential clients can "play" with them 24/7.

Here are the best ways to deploy your Telegram bots for free or very cheap:

## 1. Render.com (Free Tier)
Great for simple bots without databases or bots using external databases.
1. Push your code to GitHub.
2. Sign up on [Render.com](https://render.com/).
3. Create a new "Web Service" or "Background Worker".
4. Connect your GitHub repository.
5. Set the Start Command to `python bot.py` (or whatever your entry point is).
6. Add your `BOT_TOKEN` in the Environment Variables tab.

*Note: Free tier sleeps after 15 minutes of inactivity. For Web Services, you can use a pinging service to keep it alive.*

## 2. PythonAnywhere (Free Tier)
Good for simple Python scripts.
1. Sign up on [PythonAnywhere](https://www.pythonanywhere.com/).
2. Open a bash console.
3. Clone your GitHub repo.
4. Create a virtual environment and install requirements.
5. Create a `.env` file and put your token.
6. Go to the "Web" tab or run it in an "Always-on task" (Requires paid plan, but you can run it manually in console for testing).

## 3. Cheap VPS (Recommended for Freelancers)
If you start getting clients, you should have a cheap Linux server (Ubuntu) to host multiple bots. Providers like Aeza, Timeweb, or Hetzner cost $2-4/month.

### Steps to deploy on a VPS:
1. Connect via SSH: `ssh root@your_server_ip`
2. Update packages: `apt update && apt upgrade -y`
3. Install Python & Git: `apt install python3 python3-venv git -y`
4. Clone your repo: `git clone https://github.com/yourusername/portfolio.git`
5. Go to the bot folder: `cd portfolio/bot_shop`
6. Create VENV: `python3 -m venv venv && source venv/bin/activate`
7. Install deps: `pip install -r requirements.txt`
8. Set up `systemd` or `pm2` to keep the bot running in the background.

Example using PM2:
```bash
apt install npm -y
npm install pm2 -g
pm2 start "python3 bot.py" --name "shop_bot"
pm2 save
```

Happy freelancing! 🎉
