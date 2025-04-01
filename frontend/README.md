# ⚛️ FastDev Frontend – Vite + React + Supabase

This is the frontend for the **FastDev** fullstack template, built with **React**, **Vite**, **Tailwind CSS**, and **Shadcn UI**.  
It handles user authentication, input, result display, and history using Supabase as the backend-as-a-service.

---

## 🗂 Project Structure

```
fastdev/frontend/
├── public/
├── src/
│   ├── components/          # UI components (shadcn/ui)
│   ├── lib/                 # API, Supabase, utils
│   ├── App.tsx              # Main component
│   ├── main.tsx             # Entry point
│   └── index.css            # Tailwind styles
├── vite.config.ts
├── tailwind.config.js
├── tsconfig*.json
└── .env.example             # Template for env variables
```

---

## 🚀 Getting Started (Local Dev)

### 1. Install dependencies

```bash
npm install
```

### 2. Set up your `.env`

```bash
cp .env.example .env
```

Fill in:

```env
VITE_SUPABASE_URL=https://xyz.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
VITE_BACKEND_API_URL=https://your-api.onrender.com
```

### 3. Run the dev server

```bash
npm run dev
```

Visit: [http://localhost:5173](http://localhost:5173)

---

## ☁️ Deployment (Vercel)

1. Push to GitHub
2. Go to [Vercel](https://vercel.com) → New Project
3. Select `frontend/` as the root folder
4. Add the environment variables:
   - `VITE_SUPABASE_URL`
   - `VITE_SUPABASE_ANON_KEY`
   - `VITE_BACKEND_API_URL`

✅ Vercel handles auto-deploys, preview URLs, and environment scopes

---

## ✅ Features

- ✨ Auth: Sign up, login, logout (email/password via Supabase)
- ➕ Input: Number input form with validation
- ⚙️ API: Sends requests to FastAPI backend
- 🧠 History: Fetches user-specific history from Supabase
- 🎨 Clean UI: Tailwind + Shadcn pre-built components
- 🧪 Ready for React Query or TanStack if needed

---

## 📄 License

MIT — Use it freely, share it, and build your next idea faster 🚀

---

## ✨ Part of the FastDev Fullstack Template