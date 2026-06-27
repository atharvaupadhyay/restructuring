# Atharva Upadhyay Portfolio Website

A modern Flask-based portfolio website showcasing projects, contact form integration, and achievement tracking. Features include real-time form validation, Discord webhook integration, rate limiting, and a customizable dark/light theme with environmental configuration.

## Project Overview

This is a personal portfolio website built with Flask that demonstrates:
- Professional contact form with spam protection (honeypot technique) and Discord webhook notifications
- Project showcase with individual project detail pages
- Achievement/tracking section
- Environment-based configuration for theme customization
- Rate limiting to prevent abuse
- Responsive design with custom fonts and styling

## Project Structure

```
restructuring/
├── api/
│   ├── __pycache__/
│   └── index.py          # Main Flask application with routes and logic
├── design/               # Design assets (empty)
├── public/               # Static assets
│   ├── fonts/
│   ├── static/           # CSS, JS, images
│   ├── favicon.ico
│   ├── favicon.svg
│   ├── robots.txt
│   └── sitemap.xml
├── templates/            # HTML templates
│   ├── 404.html
│   ├── 429.html
│   ├── achievements.html
│   ├── contact.html
│   ├── index.html
│   ├── layout.html       # Base layout with theme toggle
│   ├── projects.html
│   ├── success.html
│   └── project/
│       ├── projects.html
│       └── sample-project.html  # Template for individual project pages
├── .env                  # Environment variables (not tracked)
├── .env.example          # Template for environment variables
├── .gitattributes
├── .gitignore
├── .mailmap
├── main.py               # Application entry point
├── requirements.txt      # Python dependencies
├── test.cxx              # Test file (C++)
└── vercel.json           # Vercel deployment configuration
```

## Key Features

### Core Functionality
- **Contact Form**: Secure form with honeypot spam protection, client-side and server-side validation, and Discord webhook integration
- **Project Showcase**: Displays projects with individual detail pages (currently under construction)
- **Achievements Section**: Shows professional accomplishments
- **Theme System**: Customizable dark/light theme with CSS variables controlled via environment variables
- **Rate Limiting**: Flask-Limiter integration to prevent abuse (5 contact submissions per hour)
- **SEO Friendly**: Includes robots.txt and sitemap.xml

### Technical Implementation
- **Flask 3.0.3**: Web framework with Blueprint-like structure
- **Environment Configuration**: Uses python-dotenv for managing configuration
- **Static Asset Serving**: Serves CSS, JS, images, and fonts from public directory
- **Client-Side Interactivity**: Theme toggle with localStorage persistence
- **Analytics**: Integrated Vercel Speed Insights and Web Analytics

## Dependencies

### Python Packages
- `Flask==3.0.3` - Core web framework
- `Flask-Limiter==3.8.0` - Rate limiting for abuse prevention
- `Flask-WTF==1.2.1` - Form handling and validation
- `requests==2.32.3` - HTTP client for Discord webhook calls
- `redis==5.0.8` - Backend for rate limiting storage
- `python-dotenv==1.0.1` - Environment variable management

### Frontend Technologies
- HTML5 with Jinja2 templating
- CSS3 with custom properties (CSS variables)
- Vanilla JavaScript for theme toggle
- Inter font from Google Fonts
- Cormorant Garamond for project pages

## Installation & Setup

### Prerequisites
- Python 3.7+ installed
- Redis server running (for production rate limiting) OR configure to use in-memory storage

### Local Development
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd restructuring
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your values:
   # - SECRET_KEY: Flask secret key (generate with: python -c "import secrets; print(secrets.token_hex(24))")
   # - DISCORD_WEBHOOK_URL: Your Discord webhook URL for contact form notifications
   # - REDIS_URL: Redis connection string (default: "memory://" for development)
   # - MANDALA_LIGHT_OPACITY: Opacity for light theme mandala (default: 0.05)
   # - MANDALA_DARK_OPACITY: Opacity for dark theme mandala (default: 0.025)
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Visit** `http://localhost:5000` in your browser

### Production Deployment (Vercel)
The project includes `vercel.json` for easy deployment to Vercel:
- All routes are rewritten to the Flask API endpoint
- Static assets are served with proper caching headers
- Environment variables must be set in Vercel dashboard

## Configuration Options

All configurable options are set via environment variables in `.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask session secret key | Randomly generated |
| `DISCORD_WEBHOOK_URL` | Discord webhook for contact notifications | (Required for production) |
| `REDIS_URL` | Redis connection for rate limiting | `memory://` (in-memory) |
| `MANDALA_LIGHT_OPACITY` | Opacity of mandala pattern in light theme | `0.05` |
| `MANDALA_DARK_OPACITY` | Opacity of mandala pattern in dark theme | `0.025` |

## Potential Issues & Considerations

### Known Limitations
1. **Redis Requirement**: For production use with multiple instances, a proper Redis server is required. The in-memory storage (`memory://`) works for single-instance development but won't share rate limits across processes.

2. **Discord Webhook**: Contact form requires a configured Discord webhook URL. Without it, form submissions will log to console but won't send notifications.

3. **Rate Limiting Scope**: Current implementation uses IP-based rate limiting which may affect users behind NAT/shared networks. Consider implementing user-agent or account-based limiting for stricter controls.

4. **Security Considerations**:
   - Contact form uses basic validation (could benefit from additional CSRF protection beyond Flask-WTF)
   - File upload endpoints are not implemented (reduces attack surface)
   - Consider adding CSP headers for enhanced security

5. **Development Features**:
   - The application watches `.env` for changes and reloads automatically (convenient for dev, not ideal for production)
   - Debug mode is enabled by default in `main.py`

6. **Missing Content**:
   - Projects section currently shows "Under Construction" message
   - Individual project pages need to be populated with actual project data
   - Achievements page exists but may need content updates

### Deployment Notes
- When deploying to platforms like Heroku, AWS, or Docker, ensure Redis is properly configured
- Set appropriate `SECRET_KEY` in production environment
- Consider disabling debug mode in production by modifying `main.py`
- Monitor Discord webhook delivery and implement fallback notifications if needed

## Future Improvements

1. **Content Population**: Fill in actual project details and achievements
2. **Enhanced Security**: Add additional security headers and validation
3. **Database Integration**: Consider adding a database for persistent storage of contact messages or project metadata
4. **CI/CD Pipeline**: Set up automated testing and deployment
5. **Accessibility**: Improve ARIA labels and keyboard navigation
6. **Performance**: Optimize asset delivery and consider implementing caching strategies

## License

This project is for personal portfolio use. Feel free to adapt and modify for your own use case.

---

*Last updated: June 2026*