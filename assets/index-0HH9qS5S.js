(function(){const r=document.createElement("link").relList;if(r&&r.supports&&r.supports("modulepreload"))return;for(const t of document.querySelectorAll('link[rel="modulepreload"]'))u(t);new MutationObserver(t=>{for(const o of t)if(o.type==="childList")for(const s of o.addedNodes)s.tagName==="LINK"&&s.rel==="modulepreload"&&u(s)}).observe(document,{childList:!0,subtree:!0});function m(t){const o={};return t.integrity&&(o.integrity=t.integrity),t.referrerPolicy&&(o.referrerPolicy=t.referrerPolicy),t.crossOrigin==="use-credentials"?o.credentials="include":t.crossOrigin==="anonymous"?o.credentials="omit":o.credentials="same-origin",o}function u(t){if(t.ep)return;t.ep=!0;const o=m(t);fetch(t.href,o)}})();const i=window.Telegram.WebApp;i.expand();i.ready();const p=document.querySelector("#app");var d;const e=(d=i.initDataUnsafe)==null?void 0:d.user,f=(e==null?void 0:e.language_code)==="ru"?"ru":"en",g={en:{welcome:"Welcome, {name}! 🚀",guest:"Guest",subtitle:"This is a portfolio Telegram Mini App (TMA) built with TypeScript.",profile:"Your Telegram Profile",unknown:"Unknown",yes:"Yes ⭐",no:"No",btnSend:"Send Data back to Bot",btnTheme:"Check Current Theme",confirmSend:"Do you want to send action data to the bot?",alertTheme:"You are using {theme} theme!",mainBtn:"NATIVE MAIN BUTTON",alertMainBtn:"Native MainButton clicked!"},ru:{welcome:"Добро пожаловать, {name}! 🚀",guest:"Гость",subtitle:"Это портфолио Telegram Mini App (TMA), написанное на TypeScript.",profile:"Ваш профиль Telegram",unknown:"Неизвестно",yes:"Да ⭐",no:"Нет",btnSend:"Отправить данные боту",btnTheme:"Проверить текущую тему",confirmSend:"Вы хотите отправить данные боту?",alertTheme:"Вы используете тему: {theme}!",mainBtn:"НАТИВНАЯ КНОПКА",alertMainBtn:"Нативная кнопка была нажата!"}},n=g[f],h=(e==null?void 0:e.first_name)||n.guest;p.innerHTML=`
  <div class="container">
    <div class="header">
      <h1>${n.welcome.replace("{name}",h)}</h1>
      <p class="subtitle">${n.subtitle}</p>
    </div>
    
    <div class="card">
      <h3>${n.profile}</h3>
      <ul>
        <li><strong>ID:</strong> ${(e==null?void 0:e.id)||n.unknown}</li>
        <li><strong>Username:</strong> ${e!=null&&e.username?"@"+e.username:n.unknown}</li>
        <li><strong>Language:</strong> ${(e==null?void 0:e.language_code)||n.unknown}</li>
        <li><strong>Premium:</strong> ${e!=null&&e.is_premium?n.yes:n.no}</li>
      </ul>
    </div>

    <div class="actions">
      <button id="main-btn" class="btn primary">${n.btnSend}</button>
      <button id="theme-btn" class="btn secondary">${n.btnTheme}</button>
    </div>
  </div>
`;const a=document.querySelector("#main-btn");a==null||a.addEventListener("click",()=>{i.showConfirm(n.confirmSend,l=>{l&&i.sendData(JSON.stringify({action:"checkout",status:"success"}))})});const c=document.querySelector("#theme-btn");c==null||c.addEventListener("click",()=>{i.showAlert(n.alertTheme.replace("{theme}",i.colorScheme))});i.MainButton.setText(n.mainBtn);i.MainButton.onClick(()=>{i.showAlert(n.alertMainBtn)});i.MainButton.show();
