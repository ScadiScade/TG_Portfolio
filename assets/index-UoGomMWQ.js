(function(){const l=document.createElement("link").relList;if(l&&l.supports&&l.supports("modulepreload"))return;for(const e of document.querySelectorAll('link[rel="modulepreload"]'))o(e);new MutationObserver(e=>{for(const t of e)if(t.type==="childList")for(const u of t.addedNodes)u.tagName==="LINK"&&u.rel==="modulepreload"&&o(u)}).observe(document,{childList:!0,subtree:!0});function n(e){const t={};return e.integrity&&(t.integrity=e.integrity),e.referrerPolicy&&(t.referrerPolicy=e.referrerPolicy),e.crossOrigin==="use-credentials"?t.credentials="include":e.crossOrigin==="anonymous"?t.credentials="omit":t.credentials="same-origin",t}function o(e){if(e.ep)return;e.ep=!0;const t=n(e);fetch(e.href,t)}})();const r=window.Telegram.WebApp;r.expand();r.ready();const f=document.querySelector("#app");var p;const s=(p=r.initDataUnsafe)==null?void 0:p.user,m=(s==null?void 0:s.language_code)==="ru"?"ru":"en",v={en:{welcome:"Welcome, {name}!",subtitle:"Select the service you want to order:",services:[{id:"bot_basic",title:"Basic Telegram Bot",desc:"Simple bot with basic logic and menus",price:"$100"},{id:"bot_shop",title:"E-commerce Bot",desc:"Full shop with cart and database",price:"$300"},{id:"tma",title:"Telegram Mini App",desc:"Interactive Web App inside Telegram",price:"$500"},{id:"web_landing",title:"Landing Page",desc:"Modern responsive single page website",price:"$400"},{id:"web_full",title:"Fullstack Website",desc:"Complex site with backend & DB",price:"$1000+"}],orderBtn:"Order Selected",confirm:'Do you want to order "{service}"?',selectFirst:"Please select a service first!"},ru:{welcome:"Добро пожаловать, {name}!",subtitle:"Выберите услугу для заказа:",services:[{id:"bot_basic",title:"Базовый Telegram Бот",desc:"Простой бот с меню и логикой",price:"от 5000 ₽"},{id:"bot_shop",title:"Бот-Магазин",desc:"Полноценный магазин с корзиной и БД",price:"от 15000 ₽"},{id:"tma",title:"Telegram Mini App",desc:"Интерактивное Web-приложение в Telegram",price:"от 25000 ₽"},{id:"web_landing",title:"Landing Page (Сайт)",desc:"Современный одностраничный сайт",price:"от 20000 ₽"},{id:"web_full",title:"Fullstack Сайт",desc:"Сложный сайт с бэкендом и базами данных",price:"от 50000 ₽"}],orderBtn:"Заказать выбранное",confirm:'Вы хотите заказать "{service}"?',selectFirst:"Пожалуйста, выберите услугу!"}},c=v[m],g=(s==null?void 0:s.first_name)||(m==="ru"?"Гость":"Guest");let d=null,a=null;const b=()=>{f.innerHTML=`
    <div class="container">
      <div class="header">
        <h1>${c.welcome.replace("{name}",g)}</h1>
        <p class="subtitle">${c.subtitle}</p>
      </div>
      
      <div class="services-list">
        ${c.services.map(i=>`
          <div class="service-card" data-id="${i.id}" data-title="${i.title}">
            <div class="service-info">
              <h3>${i.title}</h3>
              <p>${i.desc}</p>
            </div>
            <div class="service-price">${i.price}</div>
          </div>
        `).join("")}
      </div>
    </div>
  `,document.querySelectorAll(".service-card").forEach(i=>{i.addEventListener("click",l=>{document.querySelectorAll(".service-card").forEach(o=>o.classList.remove("selected"));const n=l.currentTarget;n.classList.add("selected"),d=n.dataset.id||null,a=n.dataset.title||null,d&&(r.MainButton.setText(c.orderBtn),r.MainButton.show())})})};b();r.MainButton.onClick(()=>{if(!d||!a){r.showAlert(c.selectFirst);return}r.showConfirm(c.confirm.replace("{service}",a),i=>{i&&r.sendData(JSON.stringify({action:"order_service",service_id:d,service_title:a}))})});
