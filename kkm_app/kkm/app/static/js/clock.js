function updateClock() {
    const now = new Date();
    
    // Форматируем время
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    const timeString = `${hours}:${minutes}:${seconds}`;
    
    // Форматируем дату
    const day = String(now.getDate()).padStart(2, '0');
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const year = now.getFullYear();
    const dateString = `${day}.${month}.${year}`;
    
    // Обновляем DOM
    const timeElement = document.getElementById('time');
    const dateElement = document.getElementById('date');
    
    if (timeElement) timeElement.textContent = timeString;
    if (dateElement) dateElement.textContent = dateString;
}


// Автоматически обновляет данные с сервера каждую минуту

function autoRefresh() {
    // Первое обновление через 60 секунд
    setTimeout(() => {
        fetchTimeFromServer();
        // Устанавливаем интервал на каждую минуту
        setInterval(fetchTimeFromServer, 60000);
    }, calculateTimeToNextMinute());
}


// Запрашивает точное время с сервера
 
function fetchTimeFromServer() {
    fetch(window.location.href, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (response.ok) {
            return response.text();
        }
        throw new Error('Network response was not ok');
    })
    .then(html => {
        // Парсим HTML и извлекаем время
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const serverTime = doc.getElementById('time')?.textContent;
        const serverDate = doc.getElementById('date')?.textContent;
        
        if (serverTime) {
            document.getElementById('time').textContent = serverTime;
        }
        if (serverDate) {
            document.getElementById('date').textContent = serverDate;
        }
    })
    .catch(error => {
        console.log('Ошибка при обновлении времени:', error);
    });
}

// Инициализация часов

function initClock() {
    console.log('Часы инициализированы');
    
    // Обновляем время сразу при загрузке
    updateClock();
    
    // Обновляем время каждую секунду для плавного отображения
    setInterval(updateClock, 1000);
    
    // Запускаем автоматическое обновление с сервера каждую минуту
    autoRefresh();
    
    // Анимация появления
    animateAppearance();
}

// Анимация появления элементов

function animateAppearance() {
    const clockContainer = document.querySelector('.clock-container');
    if (clockContainer) {
        clockContainer.style.opacity = '0';
        clockContainer.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            clockContainer.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
            clockContainer.style.opacity = '1';
            clockContainer.style.transform = 'translateY(0)';
        }, 100);
    }
}

// Запускаем инициализацию после загрузки DOM
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initClock);
} else {
    initClock();
}