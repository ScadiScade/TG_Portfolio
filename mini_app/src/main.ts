import './style.css';

// Initialize Telegram Web App
const tg = window.Telegram.WebApp;

// Expand to full height
tg.expand();

// Tell Telegram that the Mini App is ready
tg.ready();

const app = document.querySelector<HTMLDivElement>('#app')!;
const user = tg.initDataUnsafe?.user;

app.innerHTML = `
  <div class="container">
    <div class="header">
      <h1>Welcome, ${user?.first_name || 'Guest'}! 🚀</h1>
      <p class="subtitle">This is a portfolio Telegram Mini App (TMA) built with TypeScript.</p>
    </div>
    
    <div class="card">
      <h3>Your Telegram Profile</h3>
      <ul>
        <li><strong>ID:</strong> ${user?.id || 'Unknown'}</li>
        <li><strong>Username:</strong> ${user?.username ? '@' + user.username : 'Unknown'}</li>
        <li><strong>Language:</strong> ${user?.language_code || 'Unknown'}</li>
        <li><strong>Premium:</strong> ${user?.is_premium ? 'Yes ⭐' : 'No'}</li>
      </ul>
    </div>

    <div class="actions">
      <button id="main-btn" class="btn primary">Send Data back to Bot</button>
      <button id="theme-btn" class="btn secondary">Check Current Theme</button>
    </div>
  </div>
`;

// Setup Event Listeners
const mainBtn = document.querySelector<HTMLButtonElement>('#main-btn');
mainBtn?.addEventListener('click', () => {
  // Show Telegram native confirmation
  tg.showConfirm('Do you want to send action data to the bot?', (confirmed) => {
    if (confirmed) {
      // Send data back to the bot (only works if opened via keyboard button)
      tg.sendData(JSON.stringify({ action: 'checkout', status: 'success' }));
    }
  });
});

const themeBtn = document.querySelector<HTMLButtonElement>('#theme-btn');
themeBtn?.addEventListener('click', () => {
  tg.showAlert(`You are using ${tg.colorScheme} theme!`);
});

// Use MainButton from Telegram UI
tg.MainButton.setText('NATIVE MAIN BUTTON');
tg.MainButton.onClick(() => {
  tg.showAlert('Native MainButton clicked!');
});
tg.MainButton.show();
