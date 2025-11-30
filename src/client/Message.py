# On met ici les protocoles / messages attendus par le serveur pour la communication.

import re
from datetime import datetime


class Message:
    """Encapsule la construction, l'analyse et la validation des données des messages"""

    @staticmethod
    def build_action_cmd(action: str, terminal_name: str) -> str:
        """Construit une commande d'action (ex: ADD A001)"""
        return f"{action} {terminal_name}"

    @staticmethod
    def build_param_cmd(params: dict) -> str:
        """Convertit un dictionnaire de paramètres en chaîne (ex: "-code PKG777 -fragile true")"""
        return " ".join([f"-{k} {v}" for k, v in params.items()])

    @staticmethod
    def parse_response(response: str) -> tuple[str, str]:
        """Analyse la réponse du serveur : retourne le statut (OK/ERROR/UNKNOWN) et le contenu"""
        if response.startswith("OK:"):
            return "OK", response[4:].strip()
        elif response.startswith("ERROR:"):
            return "ERROR", response[7:].strip()
        else:
            return "UNKNOWN", response.strip()

    @staticmethod
    def validate_data(data: dict, action: str) -> tuple[bool, str]:
        """Validation unifiée du format et de l'intégrité des données"""
        # Définir les règles de validation
        rules = {
            "ADD": {
                "required": ["code", "weight", "spacecode"],
                "format": {
                    "code": r"^PKG[A-Z0-9]+$",  # Format du code colis (PKG+lettres/chiffres)
                    "weight": r"^\d+(\.\d+)?$",  # Poids (entier/décimal)
                    "estimated_delivery": r"^\d{4}-\d{2}-\d{2}$",  # Format date
                    "fragile": r"^true|false$",  # Valeur booléenne
                    "refrigerated": r"^true|false$",
                    "source": r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",  # Email
                    "destination": r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
                },
                "range": {
                    "weight": (0.1, 1000)  # Plage de poids (0.1-1000kg)
                }
            },
            "MODIFY": {
                "required": ["code"],
                "format": {
                    "code": r"^PKG[A-Z0-9]+$",
                    "weight": r"^\d+(\.\d+)?$",
                    "status": r"^in_storage|picked_up|delivered$"  # Énumération des statuts
                }
            },
            "READ": {
                "required": ["code"],
                "format": {
                    "code": r"^PKG[A-Z0-9]+$"
                }
            },
            "DELETE": {
                "required": ["code"],
                "format": {
                    "code": r"^PKG[A-Z0-9]+$"
                }
            }
        }

        # Pas de règles = validation automatique
        if action not in rules:
            return True, "Aucune règle de validation"

        current_rules = rules[action]
        errors = []

        # 1. Vérification des champs obligatoires
        if "required" in current_rules:
            for field in current_rules["required"]:
                if field not in data or not str(data[field]).strip():
                    errors.append(f"Champ obligatoire : {field}")

        # 2. Vérification du format
        if "format" in current_rules:
            for field, pattern in current_rules["format"].items():
                if field in data and str(data[field]).strip():
                    if not re.match(pattern, str(data[field]).strip()):
                        errors.append(f"Format incorrect : {field} (valeur : {data[field]})")

        # 3. Vérification de la plage
        if "range" in current_rules:
            for field, (min_val, max_val) in current_rules["range"].items():
                if field in data and str(data[field]).strip():
                    try:
                        value = float(data[field])
                        if not (min_val <= value <= max_val):
                            errors.append(f"Hors plage : {field} (doit être entre {min_val} et {max_val})")
                    except ValueError:
                        pass  # Déjà couvert par la vérification de format

        # 4. Vérification de la validité de la date
        if "estimated_delivery" in data and str(data["estimated_delivery"]).strip():
            try:
                datetime.strptime(data["estimated_delivery"], "%Y-%m-%d")
            except ValueError:
                errors.append(f"Date invalide : {data['estimated_delivery']}")

        if errors:
            return False, " ; ".join(errors)
        return True, "Validation réussie"
