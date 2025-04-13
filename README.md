# MockPay Payment API

Une API REST simple en FastAPI pour simuler des paiements par carte bancaire ou mobile money, avec notification via webhook.

---

## 🚀 Fonctionnalités

- 💳 Paiement via carte bancaire ou mobile money
- 🔄 Traitement asynchrone simulé avec `asyncio`
- 📡 Envoi automatique de notifications webhook
- 🧾 Persistance des transactions en fichier JSON
- 🐳 Déploiement facile via Docker & GitHub Actions

---

## 📁 Structure du projet

```
.
├── app.py                # Code principal de l'API
├── Dockerfile            # Pour construire l'image Docker
├── requirements.txt      # Dépendances Python
├── transactions.json     # Historique des transactions
├── webhook_errors.log    # Log des erreurs webhook
└── .github/
    └── workflows/
        └── deploy.yml    # Déploiement automatique via GitHub Actions
```

---

## ⚙️ Installation locale

### 1. Cloner le dépôt

```bash
git clone https://github.com/<ton-utilisateur>/payment-api.git
cd payment-api
```

### 2. Créer un environnement virtuel

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Lancer l'API

```bash
uvicorn app:app --reload
```

L'API sera disponible sur : [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🧪 Exemple d'appel à l'API

### Endpoint : `POST /pay`

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

### Build et run local

```bash
docker build -t fastapi-app .
docker run -d -p 8000:8000 fastapi-app
```

---

## 🚀 Déploiement automatisé avec GitHub Actions + Docker Hub + DigitalOcean

### Secrets requis dans GitHub :

- `DOCKER_USERNAME` → Ton identifiant Docker Hub
- `DOCKER_PASSWORD` → Ton mot de passe Docker Hub (ou token)
- `DOCKER_IMAGE_NAME` → Exemple : `tonpseudo/fastapi-app`
- `DO_SSH_PRIVATE_KEY` → Clé SSH privée pour se connecter à ton serveur
- `DO_HOST` → IP de ton serveur DigitalOcean
- `DO_USER` → Utilisateur SSH (`root`, `ubuntu`, etc.)

Chaque `git push` sur `main` :
1. Build l’image Docker
2. Push l’image sur Docker Hub
3. Se connecte à ton serveur via SSH
4. Pull l’image
5. Redémarre le conteneur

---
