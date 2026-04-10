# 🚀 Deploy SchoolMind on Render.com

This guide will help you deploy SchoolMind to Render.com for free cloud hosting.

## 📋 Prerequisites

1. **Render.com Account** - Sign up at https://render.com
2. **GitHub Repository** - Already available at: https://github.com/e91707-spec/SchoolMind
3. **Ollama Service** - Note: Render.com deployment uses mock AI responses unless you have Ollama running elsewhere

## 🎯 Quick Deployment (Recommended)

### Step 1: Connect GitHub to Render
1. Log in to [Render.com](https://render.com)
2. Click **"New +"** → **"Web Service"**
3. Select **"Connect a repository"**
4. Choose **GitHub** and authorize
5. Select the **SchoolMind** repository

### Step 2: Configure Deployment
1. **Name**: `schoolmind-ui`
2. **Environment**: `Python 3`
3. **Branch**: `master`
4. **Root Directory**: `./` (leave empty)
5. **Build Command**: `pip install -r requirements.txt`
6. **Start Command**: `python ui_server.py`
7. **Instance Type**: `Free` (or choose paid tier for better performance)

### Step 3: Environment Variables
Add these environment variables:
- `PORT`: `10000` (Render provides this automatically)
- `PYTHON_VERSION`: `3.9.0`

### Step 4: Deploy
1. Click **"Create Web Service"**
2. Wait for deployment (2-5 minutes)
3. Your app will be available at: `https://schoolmind-ui.onrender.com`

## 🔧 Advanced Deployment (Manual Configuration)

### Option 1: Using render.yaml
The repository includes `render.yaml` for automatic deployment:

1. Fork the repository to your GitHub
2. In Render, go to **"Dashboard"** → **"New +"** → **"Blueprint"**
3. Select the repository
4. Render will automatically detect and deploy both services

### Option 2: Multi-Service Setup
Deploy both UI and Search servers separately:

**Main UI Service:**
- Name: `schoolmind-ui`
- Port: `10000`
- Start: `python ui_server.py`

**Search Service:**
- Name: `schoolmind-search`  
- Port: `10001`
- Start: `python search-server.py`

## ⚙️ Configuration Options

### Free Tier Limitations
- **RAM**: 512MB
- **CPU**: Shared
- **Build Time**: 15 minutes
- **Sleeps**: After 15 minutes inactivity

### Paid Tiers (Recommended for Production)
- **Starter**: $7/month - 1GB RAM, better performance
- **Standard**: $25/month - 2GB RAM, dedicated CPU

### Environment Variables
```bash
PORT=10000                    # Provided by Render
PYTHON_VERSION=3.9.0         # Python version
OLLAMA_URL=your-ollama-url   # Optional: External Ollama
```

## 🔗 Connecting Services

### Local Development Setup
For full AI functionality, run locally:

```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Start search server  
python search-server.py

# Terminal 3: Start desktop app
python schoolmind_desktop.py
```

### Production Limitations
- **No Ollama**: Render doesn't support GPU models
- **Mock Responses**: Consider adding fallback responses
- **Web Search**: DuckDuckGo integration works

## 🛠️ Customization for Production

### Add Mock AI Responses
```python
# In ui_server.py, add fallback:
async def generate_mock_response(user_message, model):
    responses = {
        "default": "I'm SchoolMind! This is a demo response. For full AI functionality, run locally with Ollama."
    }
    return responses.get("default", responses["default"])
```

### Environment-Specific Config
```python
import os
IS_PRODUCTION = os.environ.get("RENDER") == "true"

if IS_PRODUCTION:
    # Production settings
    OLLAMA_URL = "https://your-ollama-instance.com"
else:
    # Local development
    OLLAMA_URL = "http://localhost:11434"
```

## 📊 Monitoring & Logs

### View Logs
1. Go to Render Dashboard
2. Click on your service
3. View **"Logs"** tab for real-time output
4. Check **"Metrics"** for performance data

### Health Checks
- **UI Health**: `https://your-app.onrender.com/health`
- **Search Health**: `https://your-search.onrender.com/health`

## 🔄 Continuous Deployment

### Automatic Updates
1. Enable **"Auto-deploy"** in Render settings
2. Push to GitHub → Automatic deployment
3. Changes are live within minutes

### Manual Deploy
1. Push changes to GitHub
2. In Render, click **"Manual Deploy"**
3. Select the latest commit

## 🚨 Troubleshooting

### Common Issues

**"Build Failed"**
- Check requirements.txt for valid packages
- Verify Python version compatibility
- Review build logs in Render dashboard

**"Service Not Responding"**
- Check start command: `python ui_server.py`
- Verify PORT environment variable
- Review service logs

**"502 Bad Gateway"**
- Service still starting (wait 2-5 minutes)
- Check if port binding is correct
- Verify health endpoint

**"Memory Limit Exceeded"**
- Free tier has 512MB limit
- Upgrade to paid tier for production use
- Optimize code memory usage

### Debug Steps
1. **Check Logs**: First place to look for errors
2. **Local Test**: Run `python ui_server.py` locally
3. **Dependencies**: Verify all packages in requirements.txt
4. **Environment**: Check all environment variables

## 🌐 Custom Domain (Optional)

### Setup Custom Domain
1. In Render service settings, click **"Custom Domains"**
2. Add your domain: `schoolmind.yourdomain.com`
3. Update DNS records as instructed
4. Enable SSL certificate (automatic)

## 📈 Scaling

### Horizontal Scaling
- **Multiple Instances**: Add more web services
- **Load Balancer**: Use Render's built-in load balancing
- **Database**: Add Redis for caching

### Performance Optimization
- **Caching**: Implement response caching
- **CDN**: Use CloudFlare with custom domain
- **Compression**: Enable gzip compression

## 🔐 Security

### Environment Variables
- Never commit secrets to git
- Use Render's encrypted environment variables
- Rotate API keys regularly

### HTTPS
- Render provides automatic SSL certificates
- All traffic is encrypted by default
- No additional configuration needed

## 💡 Pro Tips

### Reduce Build Time
- Use `.dockerignore` to exclude unnecessary files
- Cache dependencies with Docker layers
- Minimize requirements.txt

### Optimize Performance
- Use async/await for I/O operations
- Implement connection pooling
- Add response caching

### Monitor Usage
- Set up alerts for high error rates
- Track response times
- Monitor memory usage

## 📞 Support

### Render Support
- **Documentation**: https://render.com/docs
- **Status Page**: https://status.render.com
- **Support**: support@render.com

### SchoolMind Support
- **GitHub Issues**: https://github.com/e91707-spec/SchoolMind/issues
- **Documentation**: Check README.md
- **Community**: Join discussions in GitHub

---

**🎓 Your SchoolMind is now live on Render.com!**
