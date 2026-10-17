# DastarPlan

AI-powered meal planning iOS application with computer vision inventory scanning, personalized recipe generation, and an admin panel for content moderation.

---

## Overview

DastarPlan helps users plan their meals based on what they already have at home. Users scan their fridge or pantry with the camera, the app recognizes the products, and an AI generates personalized recipes based on the inventory, user goals, and dietary preferences. A React admin panel provides moderation tools, analytics, and user management.

> Bachelor's thesis project, Kazakh-British Technical University (2026). Supervisor: A. Myrzakanurov.
> This repository contains the **Django backend**. The iOS client lives in [yelzhana/dastarplan](https://github.com/yelzhana/dastarplan).

**Demo videos:** [Short demo 1](https://youtube.com/shorts/_iC_jnuVxLA) · [Short demo 2](https://youtube.com/shorts/ypjwW0PsHJk) · [Full demo](https://youtu.be/EVKJm5PvHpE)

**Thesis summary:** [PDF](DastarPlan%20—%20Technical%20Thesis%20Summary.pdf)
    

---

## Team

| Member | Role |
|---|---|
| Yelzhana Gizatova | Backend developer — computer-vision pipeline |
| Diyas Tolegenov | Backend developer — AI recipe generation |
| Dilnaz Koishybekova | UX/UI designer, project manager |
| Dilnaz Zhussipbekova | iOS developer |

---

## Recognising Cyrillic product labels

Most packaging in Kazakhstan mixes Cyrillic and Latin text, and general-purpose OCR handles Cyrillic less reliably. Open Food Facts also covers few local brands. The pipeline in `myapp/cv_service.py` therefore uses several layers:

1. One Google Cloud Vision request with four features: object localisation, logo detection, document OCR and labels.
2. **Packaged goods:** OCR paragraphs and logos are assigned to the nearest detected object, and a product name is built from the strongest text block plus brand.
3. **Fresh produce:** Vision labels are mapped to localised names (`apple → яблоко`).
4. **Keyword fallback:** if fewer than five products are found, all OCR text, logos and object names are matched against a curated keyword dictionary.
5. **GPT-3.5 normalisation:** noisy or mixed-script strings are turned into a clean product name and category (e.g. `MAXEER Руcckar` → `горчица`, Sauces).
6. **Open Food Facts enrichment:** verified calories and macronutrients where a match exists.

Known limitations: heavily stylised Cyrillic fonts, small or occluded items, and local products missing from Open Food Facts.

---

## Tech Stack

| Layer | Technology |
|---|---|
| iOS | Swift, SwiftUI |
| Backend | Django, Django REST Framework, PostgreSQL |
| AI | OpenAI GPT-3.5-turbo |
| Computer Vision | Google Cloud Vision API |
| Product Data | OpenFoodFacts API |
| Image Search | DuckDuckGo Images |
| Infrastructure | Docker, ngrok |
| Admin Panel | React, TypeScript, Vite, Tailwind CSS, Recharts |

---

## Features

**iOS App**
- Email/password authentication with onboarding flow
- Camera scan to detect fresh produce and packaged goods
- AI-generated recipes based on inventory and user profile
- Meal plan calendar with breakfast / lunch / dinner slots
- Shopping list with 2-hour auto-expiry timer
- Ingredient availability check per recipe
- Goal tracking: weight loss, maintenance, muscle gain

**Computer Vision Pipeline**
1. Image conversion to JPEG (HEIC supported)
2. Google Vision API — labels, objects, logos, OCR
3. Object-anchored OCR for packaged goods
4. Label detection for fresh produce
5. Keyword fallback across all annotation text
6. GPT normalization → OpenFoodFacts enrichment → PostgreSQL

**Admin Panel**
- Dashboard with real-time platform stats
- Analytics with 7 / 30 / 90 day / all-time filter
- AI Moderation queue with risk score and violation details
- Approve / reject recipes
- User, product, and recipe management
- Admin action logs

---

## Project Structure

```
dastarplan/
├── dastarhan/              # iOS app (Swift / SwiftUI)
├── dastarplan_app/         # Django backend
│   ├── myapp/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── views_auth.py
│   │   ├── serializers.py
│   │   ├── services.py
│   │   ├── cv_service.py
│   │   ├── urls.py
│   │   └── admin.py
│   ├── config/
│   │   └── settings.py
│   ├── docker-compose.yml
│   └── Dockerfile
└── admin_panel/            # React / TypeScript admin panel
    └── src/app/
        ├── api.ts
        ├── pages/
        │   ├── Dashboard.tsx
        │   ├── Analytics.tsx
        │   ├── Recipes.tsx
        │   ├── AIModerationPage.tsx
        │   ├── Users.tsx
        │   ├── Products.tsx
        │   └── Logs.tsx
        └── components/
```

---

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Node.js 18+
- Xcode 15+
- ngrok account
- OpenAI API key
- Google Cloud Vision API credentials

### Backend

```bash
cd dastarplan_app
docker-compose up --build
```

The API will be available at `http://localhost:8000`.

### ngrok tunnel (required for iOS)

```bash
ngrok http 8000
```

Copy the generated URL and update `dastarhan/APIConfig.swift`:

```swift
static let baseURL = "https://your-ngrok-url.ngrok-free.dev"
```

### Admin Panel

```bash
cd admin_panel
npm install
npm run dev
```

Open `http://localhost:5173`.

### iOS

Open `dastarhan/` in Xcode and press **Run**.

---

## Environment Variables

Create a `.env` file in `dastarplan_app/` with the following:

```env
OPENAI_API_KEY=your_openai_key
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
SECRET_KEY=your_django_secret_key
DEBUG=True
```

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register/` | Register a new user |
| POST | `/api/auth/login/` | Login and receive token |
| GET | `/api/auth/me/` | Get current user profile |
| POST | `/api/auth/profile/` | Save onboarding profile |
| POST | `/api/auth/logout/` | Invalidate token |
| GET/POST | `/api/inventory/` | User inventory |
| GET/POST | `/api/scans/` | CV image scans |
| GET/POST | `/api/meal-plans/` | Meal plans |
| GET/POST | `/api/meal-plan-items/` | Meal plan slots |
| PATCH | `/api/meal-plan-items/{id}/` | Update meal plan slot |
| POST | `/api/generate-recipe/` | AI recipe generation |
| GET | `/api/shopping-list/calculate/` | Missing ingredients |
| GET | `/api/recipes/` | Approved recipes |
| GET | `/api/recipes/pending/` | Recipes awaiting moderation |
| POST | `/api/recipes/{id}/approve/` | Approve recipe |
| DELETE | `/api/recipes/{id}/reject/` | Reject and delete recipe |
| GET | `/api/dashboard/stats/?days=7` | Platform analytics |

---

## Admin Panel Token

Generate an admin token via the Django shell:

```bash
docker-compose exec web python -c "
import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
user = User.objects.filter(is_superuser=True).first()
token, _ = Token.objects.get_or_create(user=user)
print('TOKEN:', token.key)
"
```

Paste the token into `admin_panel/src/app/api.ts`.

---

## Useful Docker Commands

```bash
# View backend logs
docker-compose logs web --tail=30

# Restart backend
docker-compose restart web

# Run database migrations
docker-compose exec web python manage.py migrate

# Access PostgreSQL
docker-compose exec db psql -U postgres
```

---

## Repositories

- iOS: [github.com/yelzhana/dastarplan](https://github.com/yelzhana/dastarplan)
- Backend: [github.com/yelzhana/dastarplan_app](https://github.com/yelzhana/dastarplan_app)
