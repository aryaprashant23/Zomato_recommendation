# Deployment Plan: Railway (Backend) & Vercel (Frontend)

To deploy the Zomato Recommendation Engine across two separate services (Railway for the Python backend and Vercel for the static frontend), we need to slightly adjust the architecture so they can communicate seamlessly.

## 1. Backend Deployment (Railway)

Railway is excellent for hosting the FastAPI backend because it automatically builds from the `requirements.txt` and manages Python environments efficiently.

### Steps to Deploy:
1. **Create a `Procfile`**: 
   - Create a `Procfile` in the root directory to explicitly tell Railway how to start the FastAPI server:
     ```text
     web: uvicorn app.api.main:app --host 0.0.0.0 --port $PORT
     ```
2. **Connect GitHub to Railway**:
   - Go to [Railway.app](https://railway.app), create a new project, and select "Deploy from GitHub repo".
   - Select your repository: `aryaprashant23/Zomato_recommendation`.
3. **Configure Environment Variables**:
   - In your Railway project variables, add your `GROQ_API_KEY`.
   - Add `DATASET_CACHE_PATH` as `data/zomato_cache.parquet`.
4. **Deploy & Get URL**:
   - Once deployed, Railway will generate a public domain (e.g., `https://zomato-backend-production.up.railway.app`). You will need this URL for the frontend.

## 2. Frontend Deployment (Vercel)

Vercel is perfect for serving the static HTML/JS/CSS. To avoid Cross-Origin Resource Sharing (CORS) errors when the frontend talks to the backend, we will use Vercel's rewrite rules to proxy `/api` requests directly to Railway.

### Steps to Deploy:
1. **Rename the HTML File**:
   - Rename `frontend/code.html` to `frontend/index.html` so Vercel automatically serves it as the root page.
2. **Create `vercel.json`**:
   - Create a `vercel.json` file inside the `frontend/` directory with the following rewrite rule. This makes requests like `fetch('/api/recommend')` route securely to your new Railway backend:
     ```json
     {
       "rewrites": [
         {
           "source": "/api/:match*",
           "destination": "https://<YOUR_RAILWAY_URL>/api/:match*"
         }
       ]
     }
     ```
3. **Connect GitHub to Vercel**:
   - Go to [Vercel.com](https://vercel.com), add a new project, and select your GitHub repository.
4. **Configure Root Directory**:
   - **Crucial Step**: In the Vercel project settings during import, change the **Root Directory** from the default (`./`) to `frontend`.
5. **Deploy**:
   - Click deploy! Vercel will instantly host your blazing-fast UI.

---

> [!NOTE]  
> **Would you like me to automatically create the `Procfile`, rename the `code.html` file to `index.html`, and set up the `vercel.json` proxy template for you right now so it's ready to be pushed to GitHub?**
