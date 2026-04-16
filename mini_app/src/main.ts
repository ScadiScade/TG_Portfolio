import './style.css';

// Initialize Telegram Web App
const tg = window.Telegram.WebApp;

// Expand to full height
tg.expand();

// Tell Telegram that the Mini App is ready
tg.ready();

const app = document.querySelector<HTMLDivElement>('#app')!;
const user = tg.initDataUnsafe?.user;

const lang = user?.language_code === 'ru' ? 'ru' : 'en';

const i18n = {
  en: {
    welcome: 'Welcome, {name}! 🚀',
    guest: 'Guest',
    subtitle: 'This is a portfolio Telegram Mini App (TMA) built with TypeScript.',
    profile: 'Your Telegram Profile',
    unknown: 'Unknown',
    yes: 'Yes ⭐',
    no: 'No',
    btnSend: 'Send Data back to Bot',
    btnTheme: 'Check Current Theme',
    confirmSend: 'Do you want to send action data to the bot?',
    alertTheme: 'You are using {theme} theme!',
    mainBtn: 'NATIVE MAIN BUTTON',
    alertMainBtn: 'Native MainButton clicked!'
  },
  ru: {
    welcome: 'Добро пожаловать, {name}! 🚀',
    guest: 'Гость',
    subtitle: 'Это портфолио Telegram Mini App (TMA), написанное на TypeScript.',
    profile: 'Ваш профиль Telegram',
    unknown: 'Неизвестно',
    yes: 'Да ⭐',
    no: 'Нет',
    btnSend: 'Отправить данные боту',
    btnTheme: 'Проверить текущую тему',
    confirmSend: 'Вы хотите отправить данные боту?',
    alertTheme: 'Вы используете тему: {theme}!',
    mainBtn: 'НАТИВНАЯ КНОПКА',
    alertMainBtn: 'Нативная кнопка была нажата!'
  }
};

const t = i18n[lang];
const userName = user?.first_name || t.guest;

app.innerHTML = `
  <div class="container">
    <div class="header">
      <h1>${t.welcome.replace('{name}', userName)}</h1>
      <p class="subtitle">${t.subtitle}</p>
    </div>
    
    <div class="card">
      <h3>${t.profile}</h3>
      <ul>
        <li><strong>ID:</strong> ${user?.id || t.unknown}</li>
        <li><strong>Username:</strong> ${user?.username ? '@' + user.username : t.unknown}</li>
        <li><strong>Language:</strong> ${user?.language_code || t.unknown}</li>
        <li><strong>Premium:</strong> ${user?.is_premium ? t.yes : t.no}</li>
      </ul>
    </div>

    <div class="actions">
      <button id="main-btn" class="btn primary">${t.btnSend}</button>
      <button id="theme-btn" class="btn secondary">${t.btnTheme}</button>
    </div>
  </div>
`;

// Setup Event Listeners
const mainBtn = document.querySelector<HTMLButtonElement>('#main-btn');
mainBtn?.addEventListener('click', () => {
  // Show Telegram native confirmation
  tg.showConfirm(t.confirmSend, (confirmed) => {
    if (confirmed) {
      // Send data back to the bot (only works if opened via keyboard button)
      tg.sendData(JSON.stringify({ action: 'checkout', status: 'success' }));
    }
  });
});

const themeBtn = document.querySelector<HTMLButtonElement>('#theme-btn');
themeBtn?.addEventListener('click', () => {
  tg.showAlert(t.alertTheme.replace('{theme}', tg.colorScheme));
});

// Use MainButton from Telegram UI
tg.MainButton.setText(t.mainBtn);
tg.MainButton.onClick(() => {
  tg.showAlert(t.alertMainBtn);
});
tg.MainButton.show();
