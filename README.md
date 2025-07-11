# AttendanceTrack - Système de Suivi de Présence

## Description du Projet

**AttendanceTrack** est une application FastAPI pour la gestion de présence dans les institutions éducatives. Elle permet de :

- Gérer les étudiants et leurs profils
- Créer et organiser des sessions de cours
- Suivre la présence des étudiants par session
- Authentification sécurisée avec Firebase
- Intégration des paiements via Stripe
- Liens de paiement et checkout Stripe

**Technologies :** FastAPI, Firebase, Stripe, Docker

## Déploiement Docker

### 1. Configuration

```bash
# Copier le fichier d'environnement
cp env.example .env

# Configurer les variables dans .env
FIREBASE_SERVICE_ACCOUNT_KEY={"type":"service_account",...}
FIREBASE_CONFIG={"apiKey":"...","authDomain":"...",...}
STRIPE_SK=sk_test_votre_cle_stripe
STRIPE_WEBHOOK_SECRET=whsec_votre_secret
```

### 2. Déploiement Local

```bash
# Construire et démarrer
docker compose up --build

# Accès : http://localhost:8001/docs
```

### 3. Déploiement sur Docker Hub

```bash
# Construire l'image
docker build -t attendancetrack .

# Tagger pour Docker Hub
docker tag attendancetrack votre-username/attendancetrack:latest

# Publier sur Docker Hub
docker login
docker push votre-username/attendancetrack:latest

# Déployer depuis Docker Hub
docker pull votre-username/attendancetrack:latest
docker run -p 8001:8001 --env-file .env votre-username/attendancetrack:latest
```

## Tests

### Tests Automatisés

```bash
# Dans le conteneur
docker compose exec attendancetrack pytest

# Avec couverture
docker compose exec attendancetrack pytest --cov=.
```

### Tests Manuels

```bash
# Test de santé
curl http://localhost:8001/docs

# Créer un étudiant
curl -X POST "http://localhost:8001/students/" \
     -H "Content-Type: application/json" \
     -d '{"name": "Test Student"}'

# Créer un compte
curl -X POST "http://localhost:8001/auth/signup" \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "password": "password123"}'

# Accéder au checkout Stripe
curl http://localhost:8001/stripe/checkout

# Vérifier l'utilisation du compte (avec token)
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8001/stripe/usage

### Endpoints Principaux

- `GET /students/` - Liste des étudiants
- `POST /students/` - Créer un étudiant
- `GET /sessions/` - Liste des sessions
- `POST /attendances/` - Créer une présence
- `POST /auth/signup` - Inscription
- `POST /auth/login` - Connexion
- `GET /stripe/checkout` - Lien de paiement Stripe
- `GET /stripe/success` - Page de succès après paiement
- `POST /stripe/webhook` - Webhook Stripe pour les événements
- `GET /stripe/usage` - Suivi de l'utilisation du compte 
