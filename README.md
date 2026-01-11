# Personal Bookmark Manager API

A REST API for managing personal bookmarks with Google OAuth 2.0 authentication, built with Django and Django REST Framework.

## Features

- 🔐 **Google OAuth 2.0 Authentication** - No traditional username/password needed
- 📚 **Bookmark Management** - Create, read, and delete bookmarks
- 🔒 **User Isolation** - Users can only access their own bookmarks
- 🚀 **Production Ready** - Configured for Railway/Render deployment

## Tech Stack

- Django 5.0+
- Django REST Framework
- django-allauth (OAuth)
- dj-rest-auth
- SQLite (development) / PostgreSQL (production)

## Quick Start

### Prerequisites

- Python 3.11+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd bookmark_manager
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser (for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Configure Google OAuth**
   ```bash
   python manage.py runserver
   # Go to http://localhost:8000/admin
   # Add a Site (example.com -> localhost:8000)
   # Add a Social Application for Google with your OAuth credentials
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/auth/google/redirect/` | Get Google OAuth URL |
| POST | `/api/auth/google/` | Exchange OAuth code for token |
| GET | `/api/auth/google/callback/` | OAuth callback handler |
| GET | `/api/auth/user/` | Get current user info |
| POST | `/api/auth/logout/` | Logout (delete token) |

### Bookmarks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/bookmarks/` | List all user's bookmarks |
| POST | `/api/bookmarks/` | Create a new bookmark |
| GET | `/api/bookmarks/{id}/` | Get a specific bookmark |
| DELETE | `/api/bookmarks/{id}/` | Delete a bookmark |

## Testing the OAuth Flow

### Step 1: Set Up Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Create a new project or select an existing one
3. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client IDs"
4. Select "Web application"
5. Add authorized redirect URIs:
   - `http://localhost:8000/api/auth/google/callback/`
   - `http://localhost:8000/accounts/google/login/callback/`
   - Your production URL (e.g., `https://your-app.railway.app/api/auth/google/callback/`)
6. Copy the Client ID and Client Secret

### Step 2: Configure Django

1. Run the Django server and go to `/admin`
2. Go to "Sites" and change the default site to match your domain
3. Go to "Social Applications" → "Add"
4. Select Provider: Google
5. Enter your Client ID and Client Secret
6. Select the site you configured
7. Save

### Step 3: Test the Flow

1. **Get the OAuth URL:**
   ```bash
   curl http://localhost:8000/api/auth/google/redirect/
   ```

2. **Open the `auth_url` in a browser** - You'll be redirected to Google login

3. **After login, you'll receive an authorization code** - Use it to get your token:
   ```bash
   curl -X POST http://localhost:8000/api/auth/google/ \
     -H "Content-Type: application/json" \
     -d '{"code": "YOUR_AUTH_CODE"}'
   ```

4. **You'll receive an auth token** - Use it for all subsequent requests

## cURL Examples

### Using Authentication

All bookmark endpoints require the `Authorization` header:

```bash
# Replace YOUR_TOKEN with your actual token
AUTH="Authorization: Token YOUR_TOKEN"
```

### List All Bookmarks

```bash
curl -H "$AUTH" http://localhost:8000/api/bookmarks/
```

### Create a Bookmark

```bash
curl -X POST http://localhost:8000/api/bookmarks/ \
  -H "$AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://github.com",
    "title": "GitHub",
    "description": "Where the world builds software"
  }'
```

### Get a Specific Bookmark

```bash
curl -H "$AUTH" http://localhost:8000/api/bookmarks/1/
```

### Delete a Bookmark

```bash
curl -X DELETE -H "$AUTH" http://localhost:8000/api/bookmarks/1/
```

### Get User Profile

```bash
curl -H "$AUTH" http://localhost:8000/api/auth/user/
```

### Logout

```bash
curl -X POST -H "$AUTH" http://localhost:8000/api/auth/logout/
```

## Deployment Options

### Option 1: Render.com (Recommended for Free Tier)

As per requirements, Render.com is a valid backend host. It is often more reliable for initial free deployments.

1. Go to [Render.com](https://render.com) and create a new **Web Service**.
2. Connect your GitHub repository: `AryaP-1243/personal-bookmark-manager-api`
3. Set **Build Command**: `pip install -r requirements.txt`
4. Set **Start Command**: `gunicorn bookmark_manager.wsgi`
5. Add Environment Variables in the "Env" tab:
   - `SECRET_KEY`: (any random string)
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `*`
6. Click **Deploy**.

### Option 2: Railway.app

1. Go to [Railway](https://railway.app)
2. Create a new project → **Deploy from GitHub repo**
3. Select your repository.
4. Set the following **Environment Variables**:
   - `SECRET_KEY`: (generate a secure key)
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `*`
5. Note: New Railway accounts may require GitHub verification at [railway.com/verify](https://railway.com/verify) to unlock code deployments.

### 3. Configure OAuth for Production

Update your Google OAuth credentials to include your Railway URL in authorized redirect URIs.

## Project Structure

```
bookmark_manager/
├── manage.py
├── requirements.txt
├── Procfile
├── runtime.txt
├── .env.example
├── README.md
├── bookmark_manager/       # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/               # OAuth & user management
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
└── bookmarks/              # Bookmark CRUD API
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── permissions.py
    └── urls.py
```

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK` - Success
- `201 Created` - Resource created
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Access denied (not owner)
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

Example error response:
```json
{
  "error": "Error message",
  "detail": "Detailed description"
}
```

## License

MIT License
