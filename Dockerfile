# Dockerfile pour Railway - Alternative à Nixpacks
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . .

# Exposer le port (Railway utilise la variable PORT)
EXPOSE $PORT

# Commande de démarrage
CMD ["python", "app_production.py"]
