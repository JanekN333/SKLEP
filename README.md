# SKLEP

Sklep z generowaniem wideo produktów przez **Seedance 2.5** (ByteDance, API ModelArk).

## Start

```bash
cp .env.example .env   # wpisz ARK_API_KEY i dokładne SEEDANCE_MODEL z konsoli ModelArk
npm start              # http://localhost:3000
```

Wymaga Node 22+. Bez zależności zewnętrznych.

## API

- `POST /api/video` – `{ prompt, imageUrl?, resolution?, duration?, ratio? }` → `{ id }`
- `GET /api/video/:id` – `{ status, videoUrl?, error? }`

Klucz API zostaje na serwerze (`.env`, ignorowany przez git) i nie trafia do przeglądarki.
