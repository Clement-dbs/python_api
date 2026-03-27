# Image de base
FROM python:3.11-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Répertoire de travail
WORKDIR /app

# Copier les dépendances
COPY requirements.txt .

# Installer les dépendances (sans cache)
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY scripts/ ./scripts/
COPY src/ ./src/
COPY models/ ./models/

# Exposer le port
EXPOSE 8000

# Lancer l'application avec uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]