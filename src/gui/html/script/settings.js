// Définition de la langue courante
let currentLang = localStorage.getItem("lang") || "fr";

// Applique la traduction sur toute la page
function initTranslation() {
    translatePage(); // depuis translations.js

    // Initialisation du select langue
    const langSelect = document.getElementById("language");
    if(langSelect){
        langSelect.value = currentLang;
        langSelect.addEventListener("change", (e) => {
            currentLang = e.target.value;
            localStorage.setItem("lang", currentLang);
            translatePage();
        });
    }
}

// Sauvegarde des paramètres
function saveSettings() {
    const ip = document.getElementById('serverIp').value;
    const name = document.getElementById('machineName').value;
    const lang = document.getElementById('language').value;

    console.log(`IP: ${ip}, Machine: ${name}, Lang: ${lang}`);
    alert(translations[currentLang].save + " !");
}

// Initialisation à l'affichage
document.addEventListener("DOMContentLoaded", () => {
    initTranslation();
});
