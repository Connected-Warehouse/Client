// basic_include.js
async function includeHTML() {
    const includes = document.querySelectorAll('[data-include]');
    for (const el of includes) {
        const file = el.getAttribute('data-include');
        try {
            const res = await fetch(file);
            if (res.ok) {
                const html = await res.text();
                el.innerHTML = html;
            } else {
                el.innerHTML = `<p style="color:red">Impossible de charger ${file}</p>`;
            }
        } catch (e) {
            el.innerHTML = `<p style="color:red">Erreur: ${e}</p>`;
        }
    }

    // 🔹 Très important : traduction après l’inclusion
    if (typeof initTranslation === "function") {
        initTranslation();
    }
}

function goBack() {
    if (window.pywebview && window.pywebview.api) {
        // Appelle la déconnexion côté Python
        window.pywebview.api.safeDisconnect();
    }
    // Redirection vers le menu principal
    window.location.href = "/pages/index.html";
}

document.addEventListener('DOMContentLoaded', includeHTML);

function navigate(page) {
    window.location.href = page;
}
