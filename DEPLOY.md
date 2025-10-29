# 🚀 Agora Deployment Guide

## Quick Deploy (5 minutes)

### Frontend (Already Done ✅)
**Live at:** https://frontend-bqhveg6tl-federico-de-pontes-projects.vercel.app

### Backend Deployment to Render

**Step 1:** Go to [Render Dashboard](https://dashboard.render.com/)

**Step 2:** Click "New +" → "Web Service"

**Step 3:** Connect your GitHub repository `SCAILE-it/agora`

**Step 4:** Configure the service:
- **Name:** `agora-backend`
- **Region:** Oregon (US West)
- **Branch:** `master`
- **Root Directory:** `backend`
- **Runtime:** Python 3
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Step 5:** Add Environment Variable:
- **Key:** `OPENAI_API_KEY`
- **Value:** Your OpenAI API key (starts with `sk-proj-...`)

**Step 6:** Click "Create Web Service"

**Step 7:** Wait for deployment (~2-3 minutes)

**Step 8:** Copy your backend URL (will be something like `https://agora-backend-xxxx.onrender.com`)

**Step 9:** Update Vercel Frontend Environment Variables:
```bash
# In your terminal
cd ~/agora/frontend
vercel env add NEXT_PUBLIC_API_URL production
# Paste: https://your-backend-url.onrender.com

vercel env add NEXT_PUBLIC_WS_URL production
# Paste: wss://your-backend-url.onrender.com/chat/ws

# Redeploy frontend
vercel --prod
```

## Alternative: Railway.app

1. Go to [Railway.app](https://railway.app)
2. "New Project" → "Deploy from GitHub repo"
3. Select `agora` repo
4. Add environment variable `OPENAI_API_KEY`
5. Railway will auto-detect Python and deploy

## Alternative: Local Docker

```bash
cd ~/agora
docker compose up
```
Visit http://localhost:3000

## Deployment Checklist

- [x] Frontend deployed to Vercel
- [ ] Backend deployed to Render/Railway
- [ ] Environment variables configured
- [ ] Frontend updated with backend URL
- [ ] Test the live application
- [ ] Agents responding correctly
- [ ] WebSocket streaming working

## Troubleshooting

### Frontend can't connect to backend
- Check that backend is deployed and running
- Verify CORS is allowing your frontend domain
- Check environment variables in Vercel

### WebSocket connection fails
- Ensure using `wss://` (not `ws://`) for production
- Check backend logs for errors
- Verify WebSocket endpoint `/chat/ws` is accessible

### Agents not responding
- Check OpenAI API key is set correctly
- Check backend logs for OpenAI API errors
- Verify you have OpenAI credits

## Support

- Backend issues: Check Render/Railway logs
- Frontend issues: Check Vercel deployment logs
- General: https://github.com/SCAILE-it/agora/issues
