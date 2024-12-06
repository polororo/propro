import re
import requests
import hashlib
import secrets
import string

def password_verification(mdp):
    if len(mdp) < 8:
        return (False, "Le mot de passe doit contenir au moins 8 caractères")
    elif not re.search(r'[A-Z]', mdp):
        return (False, "Le mot de passe doit contenir au moins une majuscule")
    elif not re.search(r'\d', mdp):
        return (False, "Le mot de passe doit contenir au moins un chiffre")
    else: 
        return (True, "Mot de passe valide")
    
def hibp_verification(mdp):
    sha1_mdp = hashlib.sha1(mdp.encode('UTF-8')).hexdigest().upper()
    prefix = sha1_mdp[:5]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    
    response = requests.get(url)

    if response.status_code == 200:
        hashes = response.text.splitlines()
        for hash_entry in hashes: 
            hash_suffix, count = hash_entry.split(':')
            if hash_suffix == sha1_mdp[5:]:
                return (True, "Ce mot de passe a été trouvé dans des fuites de données. Veuillez en choisir un autre.")
    return (False, "Le mot de passe n'a pas été compromis")

def check_password_security(password):
    # Vérification des critères de base
    is_valid, message = password_verification(password)
    if not is_valid:
        return False, message
    
    # Vérification si le mot de passe a été compromis
    is_compromised, message = hibp_verification(password)
    if is_compromised:
        return False, message
    
    return True, "Mot de passe sécurisé"

def generate_password():
    alphabet = string.ascii_letters + string.digits

    password = ''.join(secrets.choice(alphabet) for i in range(16))
    if (any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and any(c.isdigit() for c in password)):
        return password
