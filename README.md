# 🚀 Fastdev Stack – Fullstack Starter Template

A modern fullstack starter project with:

- ⚛️ React + Vite + TailwindCSS + Shadcn UI
- 🔐 Supabase (Auth + Postgres + RLS)
- 🐍 FastAPI backend (deployed to Render)
- 🌐 Frontend deployed to Vercel
- 🧪 Template-ready `.env` setup
- 💡 Works out of the box for prototyping, SaaS, internal tools, or solo projects

## 🧱 Folder Structure

```
fastdev/
├── frontend/        # React + Vite + Supabase Client
├── backend/         # FastAPI (Python) API server
└── README.md
```

## 🧑‍💻 Local Setup

### 1. Clone the template

```bash
git clone https://github.com/YOUR_USERNAME/fastdev.git
cd fastdev
```

## ⚛️ Frontend Setup (Vite + Supabase)

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

📝 Fill in `.env` with your Supabase + backend URL:

```env
VITE_SUPABASE_URL=https://xyz.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key
VITE_BACKEND_API_URL=https://your-api.onrender.com
```

## 🐍 Backend Setup (FastAPI + Poetry)

```bash
cd backend
cp .env.example .env
poetry install
poetry run uvicorn multiplier_backend.main:app --reload --app-dir src
```

### 🛜 Environment Variables (`backend/.env.example`)

```env
PORT=8000
```

## ☁️ Deployment

### ✅ Frontend (Vercel)
- Import `/frontend` folder into [vercel.com](https://vercel.com)
- Add the environment variables from `.env`
- Vercel auto-deploys on push

### ✅ Backend (Render)
- Create new **Web Service** on [render.com](https://render.com)
- Connect `/backend` folder
- Set build command: `poetry install`
- Start command: `poetry run uvicorn multiplier_backend.main:app --host 0.0.0.0 --port 10000 --app-dir src`
- Add environment variables

## ✅ Features

- 🔐 Email/password signup with Supabase Auth
- 🧮 Input form that calls a FastAPI endpoint
- 📝 Logged-in users see their input + result history (with RLS)
- 🔁 Clean loading states, error handling, and deployable out of the box

## 🔧 Tech Stack

| Layer         | Tech                                  |
|---------------|----------------------------------------|
| Frontend      | React, Vite, Tailwind, Shadcn UI       |
| Backend       | FastAPI, Python, Poetry                |
| Auth / DB     | Supabase (PostgreSQL + RLS)            |
| Deployment    | Vercel (frontend), Render (backend)    |
| Dev Tools     | GitHub, `.env`, monorepo               |

## 🧪 Dev Tips

- Env variables are managed via `.env` (local) and Vercel/Render (deploy)
- Supabase's RLS ensures each user only sees their own data
- You can easily extend this into a full SaaS by adding Stripe, analytics, etc.

## 📦 Reuse This Template

1. Click **"Use this template"** on GitHub
2. Set up `.env` files
3. Deploy + ship fast 🚀

## 📄 License

MIT — use it for anything. Credit appreciated 💛

## ✌️ Built by Yange – Enjoy & Build Fast