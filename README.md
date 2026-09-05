# vpublication — Interactive Books, Not Flat PDFs

**vpub** is a modern platform that transforms static PDFs and manuscripts into living, responsive, interactive publications. Say goodbye to flat reading experiences and hello to dynamic, engaging digital books.

## 🎯 The Problem

Traditional PDFs are static, impersonal, and don't leverage modern web capabilities. Authors and publishers deserve better tools to share their work. Readers deserve better experiences.

## ✨ The Solution

vpub reimagines how books are published and consumed in the digital age:

- **Interactive & Responsive** — Books adapt beautifully to any device, from mobile to desktop
- **Engaging Experiences** — Embedded previews, dynamic content, and reader-friendly design
- **Author-Focused** — Simple workflows to publish and share your work
- **Reader Analytics** — Understand how your audience engages with your content
- **Beautiful by Default** — Modern design system with dark mode support

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd vpub
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env  # Create from template
   # Edit .env with your configuration
   ```

5. **Run the development server**
   ```bash
   python app/main.py
   ```

   Or use uvicorn directly:
   ```bash
   uvicorn app.main:app --reload
   ```

   The app will be available at `http://127.0.0.1:8000`

## 📁 Project Structure

```
vpub/
├── app/
│   ├── main.py              # FastAPI application
│   ├── templates/           # Jinja2 HTML templates
│   │   ├── base.html        # Base template with shared layout
│   │   ├── index.html       # Landing page
│   │   ├── 404.html         # 404 error page
│   │   ├── 500.html         # 500 error page
│   │   └── partials/        # Reusable template partials
│   └── static/              # Static assets (CSS, JS, images)
├── data/                    # Persistent data (e.g., subscribers)
├── tests/                   # Automated test suite
├── requirements.txt         # Python dependencies
├── task.md                  # Project tasks & checklist
└── README.md               # This file
```

## 🛠️ Tech Stack

- **Backend**: FastAPI with Uvicorn
- **Frontend**: Jinja2 templates, Tailwind CSS, HTMX
- **Styling**: Modern design tokens, dark mode support
- **Security**: Input validation, security headers, honeypot protection
- **Testing**: Pytest-based test suite

## ⚡ Key Features

### Frontend
- **Responsive Design** — Mobile-first approach with Tailwind CSS
- **Dark Mode** — Automatic detection with manual toggle, persistent across sessions
- **HTMX Integration** — Seamless form interactions without page reloads
- **Accessibility** — WCAG AA compliance, semantic HTML, proper heading hierarchy
- **Performance** — Optimized assets, lazy loading support

### Backend
- **Email Subscription** — Capture early access signups
- **Bot Protection** — Honeypot field + server-side validation
- **Security Headers** — XSS, clickjacking, and referrer policy protections
- **Error Handling** — Custom 404 and 500 pages with branded messaging
- **Data Persistence** — JSON-based subscriber storage

## 🧪 Testing

Run the automated test suite:

```bash
pytest tests/
```

Tests cover:
- Form submission (valid & invalid emails)
- Duplicate email handling
- Bot prevention (honeypot)
- Error page rendering

## 📋 Development Status

This project is actively in development. Check out `task.md` for the current roadmap and completed features.

### Completed
- ✅ Project setup & base templates
- ✅ Responsive landing page with HTMX integration
- ✅ Dark/light mode toggle
- ✅ Email subscription system
- ✅ Security features & hardening
- ✅ Automated test suite
- ✅ Accessibility compliance

### In Progress / Planned
- [ ] SEO enhancements (canonical URLs, structured data, sitemaps)
- [ ] Performance optimizations (self-hosted assets, lazy loading)
- [ ] Privacy-respecting analytics
- [ ] Cross-browser testing
- [ ] Admin dashboard for publishers

## 🔐 Security

vpub takes security seriously:

- **Input Validation** — Server-side email validation with regex
- **Bot Prevention** — Honeypot field + duplicate detection
- **Security Headers** — Comprehensive protection against common attacks
- **Environment Secrets** — All sensitive data in `.env` (never committed)
- **Semantic HTML** — Built with accessibility and proper structure

## 🌍 Accessibility

The entire platform is designed to be accessible:

- Logical heading hierarchy
- Alt text on all images
- Keyboard navigation support
- Focus-visible outlines
- Color contrast ≥ 4.5:1 (WCAG AA)
- Respects `prefers-reduced-motion`

## 📞 Support & Contributing

We're building vpub in the open. Contributions, bug reports, and feature requests are welcome!

## 📄 License

This project is licensed under the MIT License.

---

**Ready to transform how books are published?** Start exploring vpub today.
