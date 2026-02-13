// static/js/script.js
document.addEventListener('DOMContentLoaded', function() {

    // Глобальное состояние расчета
    window.calculationState = {
        birthdayData: null,
    };
    
    // Элементы UI
    const uiElements = {
        birthdayInput: document.getElementById('birthdayInput'),
        birthdayResult: document.getElementById('birthdayResult'),
    };
    
    // Инициализация с передачей uiElements
    setupEventListeners(uiElements);
    
});



// --- НАСТРОЙКА ВСЕХ ОСНОВНЫХ ОБРАБОТЧИКОВ СОБЫТИЙ ---
function setupEventListeners(ui) {
    // 1. День рождения: Отправка по Enter
    ui.birthdayInput?.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            processBirthdayData(ui);
        }
    });
}

// --- ФУНКЦИЯ ОБРАБОТКИ ДНЯ РОЖДЕНИЯ ---
async function processBirthdayData(ui) {
    const birthday = ui.birthdayInput.value;
    
    if (!birthday) return;

    try {
        const response = await fetch(window.processBirthdayUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRFToken': window.csrfToken },
            body: JSON.stringify({ birthday })
        });
        const data = await response.json();
        console.log('data:', data);
        
        if (data.success) {
            window.calculationState.birthdayData = data;
            ui.birthdayResult.innerHTML = `<p>${data.cart_of_patient}</p>`;
        } else {
            alert('Ошибка (ДР): ' + data.error);
        }
    } catch (error) {
        alert('Произошла ошибка при отправке данных (ДР)');
    }
}


// --- ФУНКЦИЯ ДЛЯ ПЕРЕСЧЕТА МЕТОДА ПРИ ИЗМЕНЕНИИ ДАННЫХ ---
// function recalculateMethodIfNeeded(ui) {
    // Если метод уже выбран и есть все необходимые данные - пересчитываем
//     if (ui.methodSelect.value !== " " &&
//         window.calculationState.ourDateData && 
//         window.calculationState.cityData) {
        
//         console.log('Автоматический пересчет метода из-за изменения данных...');
//         processMethodData(ui);
//     }
// }