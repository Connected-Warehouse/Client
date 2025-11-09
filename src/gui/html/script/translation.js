const translations = {
    fr: {
        // Header / menu
        app_name: "AbsolutWarehouse",
        menu_modify: "Modification",
        menu_add: "Ajout",
        menu_delete: "Suppression",
        menu_search: "Recherche",
        menu_options: "Options",
        footer_text: "2025 AbsolutWarehouse. Tous droits reserves.",
        back_button: "Retour au menu",

        // Page d'accueil
        home_welcome: "Bienvenue sur AbsolutWarehouse",
        home_instruction: "Utilisez les boutons du header pour naviguer entre les differentes pages.",

        // Page Supprimer
        delete_title: "Supprimer un element",
        delete_itemId_placeholder: "ID de l'element a supprimer",
        delete_button: "Supprimer",
        delete_error: "ID requis",
        delete_success: "Element {id} supprime avec succes !",

        // Page Ajouter
        add_title: "Ajouter un nouvel element",
        add_itemName_placeholder: "Nom de l'element",
        add_itemWeight_placeholder: "Poids",
        add_button: "Ajouter",
        add_error: "Tous les champs sont requis",
        add_success: "Element \"{name}\" ajoute avec succes !",

        // Page Modifier
        modify_title: "Modifier un element",
        modify_itemId_placeholder: "ID de l'element a modifier",
        modify_newValue_placeholder: "Nouvelle valeur",
        modify_button: "Modifier",
        modify_error: "Tous les champs sont requis",
        modify_success: "Element {id} modifie avec succes !",

        // Page Options
        settings_title: "Parametres",
        server_ip_label: "IP du serveur",
        server_ip_placeholder: "127.0.0.1",
        machine_name_label: "Nom de la machine",
        machine_name_placeholder: "Machine01",
        language_label: "Langue",
        lang_fr: "Francais",
        lang_en: "English",
        save_button: "Enregistrer",
        settings_saved_alert: "Parametres sauvegardes !\\nIP: {ip}, Machine: {name}, Lang: {lang}",

        // Page Search
        search_title: "Rechercher un element",
        search_query_placeholder: "ID ou nom de l'element",
        search_button: "Rechercher",
        search_error: "Champ requis",
        search_success: "Resultats pour \"{query}\" affiches ici !"
    },

    en: {
        // Header / menu
        app_name: "AbsolutWarehouse",
        menu_modify: "Modify",
        menu_add: "Add",
        menu_delete: "Delete",
        menu_search: "Search",
        menu_options: "Options",
        footer_text: "2025 AbsolutWarehouse. All rights reserved.",
        back_button: "Back to menu",

        // Home page
        home_welcome: "Welcome to AbsolutWarehouse",
        home_instruction: "Use the buttons in the header to navigate between different pages.",

        // Delete page
        delete_title: "Delete an item",
        delete_itemId_placeholder: "Item ID to delete",
        delete_button: "Delete",
        delete_error: "ID required",
        delete_success: "Item {id} deleted successfully!",

        // Add page
        add_title: "Add a new item",
        add_itemName_placeholder: "Item name",
        add_itemWeight_placeholder: "Weight",
        add_button: "Add",
        add_error: "All fields are required",
        add_success: "Item \"{name}\" added successfully!",

        // Modify page
        modify_title: "Modify an item",
        modify_itemId_placeholder: "Item ID to modify",
        modify_newValue_placeholder: "New value",
        modify_button: "Modify",
        modify_error: "All fields are required",
        modify_success: "Item {id} modified successfully!",

        // Options page
        settings_title: "Settings",
        server_ip_label: "Server IP",
        server_ip_placeholder: "127.0.0.1",
        machine_name_label: "Machine Name",
        machine_name_placeholder: "Machine01",
        language_label: "Language",
        lang_fr: "French",
        lang_en: "English",
        save_button: "Save",
        settings_saved_alert: "Settings saved!\nIP: {ip}, Machine: {name}, Lang: {lang}",

        // Search page
        search_title: "Search an item",
        search_query_placeholder: "Item ID or name",
        search_button: "Search",
        search_error: "Field required",
        search_success: "Results for \"{query}\" displayed here!"
    }
};

// -------------------------------
// Gestion de la langue
// -------------------------------
let currentLang = localStorage.getItem("lang") || "fr";

// Traduit tout le contenu visible
function translatePage() {
    document.querySelectorAll("[data-translate]").forEach(el => {
        const key = el.getAttribute("data-translate");
        if (translations[currentLang]?.[key]) {
            el.innerText = translations[currentLang][key];
        }
    });

    document.querySelectorAll("[data-translate-placeholder]").forEach(el => {
        const key = el.getAttribute("data-translate-placeholder");
        if (translations[currentLang]?.[key]) {
            el.placeholder = translations[currentLang][key];
        }
    });
}

// Initialise la traduction et écoute le changement de langue
function initTranslation() {
    translatePage();

    const langSelect = document.getElementById("language");
    if (langSelect) {
        langSelect.value = currentLang;
        langSelect.addEventListener("change", (e) => {
            currentLang = e.target.value;
            localStorage.setItem("lang", currentLang);
            translatePage();
        });
    }
}

// Permet d'obtenir une traduction dans le JS (pour les alert(), etc.)
function getTranslation(key) {
    return translations[currentLang]?.[key] || key;
}