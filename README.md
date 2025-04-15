# 💸 MockPay – API de Paiement avec Webhook

Une API REST construite avec **FastAPI** pour simuler des paiements par **carte bancaire** ou **mobile money**, avec envoi automatique de notifications via **webhook**.

---

## 🚀 Fonctionnalités

- 💳 Paiement par carte ou mobile money  
- 🔁 Traitement asynchrone simulé avec `asyncio`  
- 📡 Notification automatique via webhook  
- 🧾 Sauvegarde des transactions dans un fichier JSON  
- 🐳 Déploiement simple avec Docker & GitHub Actions  

---

## 📁 Structure du projet

```
.
├── app.py                # Code principal de l'API
├── Dockerfile            # Image Docker de l'app
├── requirements.txt      # Dépendances Python
├── transactions.json     # Historique des paiements
├── webhook_errors.log    # Log des erreurs webhook
└── .github/
    └── workflows/
        └── deploy.yml    # Déploiement GitHub Actions
```

---

## ⚙️ Installation locale

### 1. Forker le dépôt

Commence par forker le projet depuis :

👉 https://github.com/troemmanuel/MockPay

### 2. Cloner ton fork

```bash
git clone https://github.com/<ton-utilisateur>/MockPay.git
cd MockPay
```

### 3. Créer un environnement virtuel

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 5. Lancer l'API

```bash
uvicorn app:app --reload
```

🔗 Accès local : [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🧪 Exemple d’appel API

### Endpoint : `POST /pay`

#### Paiement mobile money

```json
{
  "amount": 1500,
  "currency": "XOF",
  "method": "mobile_money",
  "customer_id": "client123",
  "webhook_url": "https://webhook.site/xxxx",
  "external_reference": "REF123456",
  "payment_data": {
    "phone_number": "+2250099000000",
    "provider": "mtn"
  }
}
```

#### Paiement carte bancaire

```json
{
  "amount": 2500,
  "currency": "XOF",
  "method": "debit_card",
  "customer_id": "client456",
  "webhook_url": "https://webhook.site/xxxx",
  "external_reference": "REF987654",
  "payment_data": {
    "card_number": "4111111111111111",
    "expiry_date": "12/25",
    "cvv": "123"
  }
}
```

---

## 📘 Endpoints disponibles

| Méthode | URL               | Description                        |
|---------|-------------------|------------------------------------|
| POST    | `/pay`            | Démarre un paiement                |
| GET     | `/webhook-errors` | Récupère les erreurs webhook       |

---

## 🐳 Déploiement avec Docker

### Build et exécution locale

```bash
docker build -t mockpay .
docker run -d -p 8000:8000 mockpay
```

---

## 🚀 Déploiement automatisé (GitHub Actions + Docker Hub + DigitalOcean)

### Secrets requis sur GitHub :

| Clé                  | Description                                      |
|----------------------|--------------------------------------------------|
| `DOCKER_USERNAME`     | Identifiant Docker Hub                          |
| `DOCKER_PASSWORD`     | Mot de passe ou token Docker Hub                |
| `DOCKER_IMAGE_NAME`   | Exemple : `tonpseudo/mockpay`                   |
| `DO_SSH_PRIVATE_KEY`  | Clé SSH privée pour se connecter au serveur     |
| `DO_HOST`             | IP publique du serveur DigitalOcean             |
| `DO_USER`             | Utilisateur SSH (`root`, `ubuntu`, etc.)        |

### Processus de déploiement (automatisé sur `main`) :

1. Build de l’image Docker  
2. Push vers Docker Hub  
3. Connexion SSH au serveur  
4. Pull de l’image  
5. Redémarrage du conteneur