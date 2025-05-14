# Étape 1 : Utiliser une image légère de Python
FROM python:3.11-slim

# Étape 2 : Empêcher l'interactivité et configurer les variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Étape 3 : Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libffi-dev \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Étape 4 : Définir le répertoire de travail
WORKDIR /app

# Étape 5 : Copier uniquement les fichiers nécessaires pour installer les deps d'abord
COPY requirements.txt .

# Étape 6 : Installer les dépendances Python
RUN pip install --upgrade pip && pip install -r requirements.txt

# Étape 7 : Copier le reste des fichiers
COPY . .

# Étape 8 : Exposer le port utilisé par Uvicorn
EXPOSE 8000

# Étape 9 : Démarrer l’application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

