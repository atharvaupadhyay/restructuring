from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    Response,
    send_file,
    abort
)

from flask_limiter import Limiter
from flask_wtf.csrf import CSRFProtect

from datetime import datetime, UTC
import requests
import os
import re
import ipaddress

try:
    from dotenv import load_dotenv
    dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    load_dotenv(dotenv_path=dotenv_path, override=True)
except ImportError:
    pass

# Initialize Flask app, pointing template and static directories to the root folders
app = Flask(
    __name__,
    template_folder='../templates',
    static_folder='../public/static'
)

app.secret_key = os.environ.get("SECRET_KEY", os.urandom(24))

# CSRF Protection
csrf = CSRFProtect(app)

@app.context_processor
def inject_mandala_opacities():
    return {
        'mandala_light_opacity': os.environ.get('MANDALA_LIGHT_OPACITY', '0.05'),
        'mandala_dark_opacity': os.environ.get('MANDALA_DARK_OPACITY', '0.025')
    }


# Rate Limiting helper
def real_ip():
    # try Cloudflare first
    ip = request.headers.get("CF-Connecting-IP")
    if ip:
        return ip

    # try Vercel / proxy
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.remote_addr or "0.0.0.0"

storage_uri = os.environ.get("REDIS_URL") or "memory://"
limiter = Limiter(
    key_func=real_ip,
    storage_uri=storage_uri,
    app=app
)

# Helper functions
def parse_user_agent(ua_string):
    if not ua_string:
        return "Unknown", "Unknown", "Unknown", "Unknown"
    ua_lower = ua_string.lower()
    
    # Platform / OS
    if "windows" in ua_lower:
        os_name = "Windows"
    elif "android" in ua_lower:
        os_name = "Android"
    elif "iphone" in ua_lower:
        os_name = "iOS (iPhone)"
    elif "ipad" in ua_lower:
        os_name = "iOS (iPad)"
    elif "macintosh" in ua_lower or "mac os" in ua_lower:
        os_name = "macOS"
    elif "linux" in ua_lower:
        os_name = "Linux"
    else:
        os_name = "Unknown"
        
    # Browser and Version
    browser = "Unknown"
    version = "Unknown"
    
    if "edg/" in ua_lower:
        browser = "Edge"
        match = re.search(r'edg/([0-9\.]+)', ua_lower)
        if match: version = match.group(1)
    elif "opr/" in ua_lower or "opera" in ua_lower:
        browser = "Opera"
        match = re.search(r'(?:opr|opera)/([0-9\.]+)', ua_lower)
        if match: version = match.group(1)
    elif "chrome" in ua_lower or "crios" in ua_lower:
        browser = "Chrome"
        match = re.search(r'(?:chrome|crios)/([0-9\.]+)', ua_lower)
        if match: version = match.group(1)
    elif "firefox" in ua_lower or "fxios" in ua_lower:
        browser = "Firefox"
        match = re.search(r'(?:firefox|fxios)/([0-9\.]+)', ua_lower)
        if match: version = match.group(1)
    elif "safari" in ua_lower:
        browser = "Safari"
        match = re.search(r'version/([0-9\.]+)', ua_lower)
        if match: version = match.group(1)
        
    # Device Type
    if "mobi" in ua_lower:
        device = "Mobile"
    elif "ipad" in ua_lower or "tablet" in ua_lower:
        device = "Tablet"
    else:
        device = "Desktop"
        
    return browser, version, os_name, device

def get_country_from_ip(ip):
    try:
        if ip == "localhost":
            return "Localhost / Private Network"

        if ipaddress.ip_address(ip).is_private:
            return "Localhost / Private Network"

    except ValueError:
        return "Unknown"

    try:
        res = requests.get(f"http://ip-api.com/json/{ip}", timeout=1)

        if res.status_code == 200:
            data = res.json()

            if data.get("status") == "success":
                return data.get("country") or "Unknown"

    except Exception:
        pass

    return "Unknown"

# Routes
@app.route('/')
def index():
    return render_template('index.html', active_page='base')

# PROJECTS_LIST = [
#     {
#         "slug": "sample-project",
#         "title": "Sample Project",
#         "description": "This is a sample project to showcase how separate project pages work. You can copy its HTML file and customize it for other projects.",
#         "tech_stack": ["Python", "PyTorch", "Flask", "HTML5 Canvas"]
#     }
# ]

@app.route('/projects')
def projects():
    return render_template('projects.html', active_page='projects')

# @app.route('/projects/<path:slug>')
# def project_detail(slug):
#     # Sanitize the slug to prevent directory traversal
#     safe_slug = re.sub(r'[^a-zA-Z0-9\-_]', '', slug)
#     if not safe_slug or safe_slug != slug:
#         abort(404)
#     try:
#         return render_template(f'projects/{safe_slug}.html', active_page='projects')
#     except Exception:
#         abort(404)

# @app.route('/achievements')
# def achievements():
#     return render_template('achievements.html', active_page='achievements')

@app.route("/mandala-monochrome")
def image():
    return send_file("../public/static/images/mandala-monochrome.png", mimetype="image/png")

@app.route('/contact', methods=['GET', 'POST'])
@limiter.limit("5 per hour", methods=["POST"])
def contact():
    if request.method == 'POST':
        # Honeypot check
        if request.form.get('comment'):
            # Silent redirect for spam bots
            return redirect(url_for('contact_success'))

        # Form fields
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        body = request.form.get('body', '').strip()

        # Input validations
        if not name or not email or not subject or not body:
            flash('All form fields are required.', 'danger')
            return redirect(url_for('contact'))
        
        if len(subject) > 200:
            flash('Subject is too long.', 'danger')
            return redirect(url_for('contact'))

        if len(body) > 2000:
            flash('Message is too long.', 'danger')
            return redirect(url_for('contact'))

        # Email validation pattern
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            flash('Please enter a valid email address.', 'danger')
            return redirect(url_for('contact'))

        # Collected metadata
        ip = real_ip()
        country = get_country_from_ip(ip)
        
        user_agent_str = request.headers.get("User-Agent") or "Unknown"
        browser, version, os_name, device = parse_user_agent(user_agent_str)
        
        accept_lang = request.headers.get("Accept-Language")
        lang = accept_lang.split(",")[0].strip() if accept_lang else "Unknown"
        
        screen_res = request.form.get("screen_resolution") or "Unknown"
        timezone = request.form.get("timezone") or "Unknown"
        referrer = request.form.get("referrer") or request.referrer or "Direct"
        
        collected_at = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")

        webhook_url = os.getenv('DISCORD_WEBHOOK_URL')

        if not webhook_url:
            flash('Webhook URL is not configured. (Fallback: Message logged)', 'warning')
            print(f"FALLBACK: Name: {name}, Email: {email}, Subject: {subject}, Body: {body}")
            return redirect(url_for('contact_success'))

        data = {
            "content": f"**New Contact Form Submission** <@692994823928741918>",
            "embeds": [
                {
                    "title": f"Subject: {subject}",
                    "description": body,
                    "color": 12745742,
                    "fields": [
                        {"name": "Name", "value": name, "inline": True},
                        {"name": "Email", "value": email, "inline": True},
                        {"name": "IP Address", "value": ip, "inline": True},
                        {"name": "Country", "value": country, "inline": True},
                        {"name": "Browser", "value": f"{browser} (v{version})", "inline": True},
                        {"name": "Operating System", "value": os_name, "inline": True},
                        {"name": "Device Type", "value": device, "inline": True},
                        {"name": "Language", "value": lang, "inline": True},
                        {"name": "Screen Resolution", "value": screen_res, "inline": True},
                        {"name": "Timezone", "value": timezone, "inline": True},
                        {"name": "Referrer", "value": referrer, "inline": True},
                        {"name": "Submitted At (UTC)", "value": collected_at, "inline": True},
                        {"name": "User Agent", "value": user_agent_str, "inline": False}
                    ]
                }
            ]
        }

        try:
            result = requests.post(webhook_url, json=data)
            result.raise_for_status()
            return redirect(url_for('contact_success'))
        except requests.exceptions.RequestException:
            flash('An error occurred while sending your message. Please try again later.', 'danger')
            return redirect(url_for('contact'))

    return render_template('contact.html')

@app.route('/contact/success')
def contact_success():
    return render_template('success.html')

@app.route('/robots.txt')
@limiter.exempt
def robots():
    content = "User-agent: *\nAllow: /\n\nSitemap: https://atharvaupadhyay.com/sitemap.xml"
    return Response(content, mimetype="text/plain")

@app.route('/sitemap.xml')
@limiter.exempt
def sitemap():
    urls = [
        {"loc": "https://atharvaupadhyay.com/", "changefreq": "weekly", "priority": "1.0"},
        {"loc": "https://atharvaupadhyay.com/contact", "changefreq": "monthly", "priority": "0.8"},
        {"loc": "https://atharvaupadhyay.com/projects", "changefreq": "monthly", "priority": "0.8"},
        {"loc": "https://atharvaupadhyay.com/achievements", "changefreq": "monthly", "priority": "0.8"},
    ]
    
    xml_items = []
    for item in urls:
        xml_items.append(
            f"  <url>\n    <loc>{item['loc']}</loc>\n    <changefreq>{item['changefreq']}</changefreq>\n    <priority>{item['priority']}</priority>\n  </url>"
        )
    
    xml_content = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{chr(10).join(xml_items)}\n"
        '</urlset>'
    )
    return Response(xml_content, mimetype="application/xml")

# 429 Page (Rate limit)
@app.errorhandler(429)
def ratelimit_handler(e):
    if request.path == '/contact':
        flash("You are sending messages too fast. Please wait a bit and try again.", "danger")
        return redirect(url_for('contact'))
    return render_template('429.html'), 429

# 404 Page (Not Found)
@app.errorhandler(404)
def not_found_handler(e):
    return render_template('404.html'), 404
