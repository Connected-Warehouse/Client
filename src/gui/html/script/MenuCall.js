// Fonction qui appelle Python via PyWebView et gère la redirection
async function menuCall(command, href) {
    try {
        let result = "DENIED";

        switch(command) {
            case "ADD":
                result = await window.pywebview.api.loadAddMenu();
                break;
            case "DELETE":
                result = await window.pywebview.api.loadDeleteMenu();
                break;
            case "MODIFY":
                result = await window.pywebview.api.loadModifyMenu();
                break;
            case "SEARCH":
                result = await window.pywebview.api.loadSearchMenu();
                break;
            default:
                console.error("Commande inconnue :", command);
        }

        console.log("Python returned:", result);

        // Redirection si nécessaire
        if(href && result === "AUTHORIZED") {
            window.location.href = href;
        } else if(result === "DENIED") {
            alert("Accès refusé !");
        }


    } catch(e) {
        console.error("Erreur menuCall :", e);
        alert("Erreur lors de l'appel à Python");
    }
}

// Pour les boutons comme Options qui n'ont pas de commande Python
function navigate(href) {
    window.location.href = href;
}
