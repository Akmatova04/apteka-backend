// static/menu/main.js (же static/js/main.js, эгер ошол жерде болсо)

document.addEventListener('DOMContentLoaded', function() {

    // --- Мобилдик менюну ачуу/жабуу ---
    // Бул үчүн HTML'де .menu-toggle жана .main-navigation класстары болушу керек.
    // Биздин base.html'де Bootstrap'тын navbar-toggler жана collapse класстары колдонулат,
    // алар Bootstrap'тын өзүнүн JS'и менен иштейт, андыктан бул бөлүк азыркы base.html үчүн
    // милдеттүү эмес, бирок калтырсак зыяны жок.
    const menuToggle = document.querySelector('.navbar-toggler'); // Bootstrap класс
    const mainNav = document.querySelector('#navbarNavMain'); // Bootstrap ID

    if (menuToggle && mainNav) {
        // Bootstrap муну өзү жасайт, бирок кошумча класс кошкуңуз келсе:
        // menuToggle.addEventListener('click', function() {
        //     mainNav.classList.toggle('custom-is-open');
        //     menuToggle.classList.toggle('custom-is-active');
        // });
    }

    // --- Django messages жабуу (Bootstrap муну өзү жасайт, бирок бул кошумча) ---
    const closeButtons = document.querySelectorAll('.alert .close'); // Bootstrap класстары
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Bootstrap муну data-dismiss="alert" аркылуу жасайт.
            // Эгер ал иштебесе, бул код жардам бериши мүмкүн.
            // this.parentElement.style.display = 'none';
        });
    });

    // --- Экрандын өлчөмү өзгөргөндө ---
    // Bootstrap'тын navbar'ы муну автоматтык түрдө жасайт.
    // window.addEventListener('resize', function() {
    //     if (window.innerWidth > 992) { // Bootstrap'тын lg breakpoint'и
    //         if (mainNav && mainNav.classList.contains('show')) { // Bootstrap'тын 'show' классы
    //             // Bootstrap муну өзү жабат.
    //         }
    //     }
    // });

    console.log("Apteka KG: Негизги JavaScript файлы жүктөлдү.");
    // Бул жерге башка жөнөкөй JS функцияларын кошсоңуз болот.

}); // DOMContentLoaded аягы