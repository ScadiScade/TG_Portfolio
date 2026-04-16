import './style.css';

// Initialize Telegram Web App
const tg = window.Telegram.WebApp;
tg.expand();
tg.ready();

const app = document.querySelector<HTMLDivElement>('#app')!;
const user = tg.initDataUnsafe?.user;
const lang = user?.language_code === 'ru' ? 'ru' : 'en';

const i18n = {
  en: {
    welcome: 'Welcome, {name}!',
    subtitle: 'Select the service you want to order:',
    services: [
      { id: 'bot_basic', title: 'Basic Telegram Bot', desc: 'Simple bot with basic logic and menus', price: '$100' },
      { id: 'bot_shop', title: 'E-commerce Bot', desc: 'Full shop with cart and database', price: '$300' },
      { id: 'tma', title: 'Telegram Mini App', desc: 'Interactive Web App inside Telegram', price: '$500' },
      { id: 'web_landing', title: 'Landing Page', desc: 'Modern responsive single page website', price: '$400' },
      { id: 'web_full', title: 'Fullstack Website', desc: 'Complex site with backend & DB', price: '$1000+' }
    ],
    orderBtn: 'Order Selected',
    confirm: 'Do you want to order "{service}"?',
    selectFirst: 'Please select a service first!'
  },
  ru: {
    welcome: 'Добро пожаловать, {name}!',
    subtitle: 'Выберите услугу для заказа:',
    services: [
      { id: 'bot_basic', title: 'Базовый Telegram Бот', desc: 'Простой бот с меню и логикой', price: 'от 5000 ₽' },
      { id: 'bot_shop', title: 'Бот-Магазин', desc: 'Полноценный магазин с корзиной и БД', price: 'от 15000 ₽' },
      { id: 'tma', title: 'Telegram Mini App', desc: 'Интерактивное Web-приложение в Telegram', price: 'от 25000 ₽' },
      { id: 'web_landing', title: 'Landing Page (Сайт)', desc: 'Современный одностраничный сайт', price: 'от 20000 ₽' },
      { id: 'web_full', title: 'Fullstack Сайт', desc: 'Сложный сайт с бэкендом и базами данных', price: 'от 50000 ₽' }
    ],
    orderBtn: 'Заказать выбранное',
    confirm: 'Вы хотите заказать "{service}"?',
    selectFirst: 'Пожалуйста, выберите услугу!'
  }
};

const t = i18n[lang];
const userName = user?.first_name || (lang === 'ru' ? 'Гость' : 'Guest');

let selectedService: string | null = null;
let selectedTitle: string | null = null;

const renderApp = () => {
  app.innerHTML = `
    <div class="container">
      <div class="header">
        <h1>${t.welcome.replace('{name}', userName)}</h1>
        <p class="subtitle">${t.subtitle}</p>
      </div>
      
      <div class="services-list">
        ${t.services.map(s => `
          <div class="service-card" data-id="${s.id}" data-title="${s.title}">
            <div class="service-info">
              <h3>${s.title}</h3>
              <p>${s.desc}</p>
            </div>
            <div class="service-price">${s.price}</div>
          </div>
        `).join('')}
      </div>
    </div>
  `;

  // Attach click events
  document.querySelectorAll('.service-card').forEach(card => {
    card.addEventListener('click', (e) => {
      // Remove selected from all
      document.querySelectorAll('.service-card').forEach(c => c.classList.remove('selected'));
      // Add selected to clicked
      const target = e.currentTarget as HTMLDivElement;
      target.classList.add('selected');
      
      selectedService = target.dataset.id || null;
      selectedTitle = target.dataset.title || null;

      // Update Main Button
      if (selectedService) {
        tg.MainButton.setText(t.orderBtn);
        tg.MainButton.show();
      }
    });
  });
};

renderApp();

// Handle Main Button Click
tg.MainButton.onClick(() => {
  if (!selectedService || !selectedTitle) {
    tg.showAlert(t.selectFirst);
    return;
  }

  tg.showConfirm(t.confirm.replace('{service}', selectedTitle), (confirmed) => {
    if (confirmed) {
      // Send data to Telegram Bot
      tg.sendData(JSON.stringify({ 
        action: 'order_service', 
        service_id: selectedService,
        service_title: selectedTitle
      }));
    }
  });
});
