## Django Blog Application

This is a full‑featured blog application built with Django. It includes public blog pages and an admin dashboard for managing posts, categories, and users.

### Features

- **Blog posts**
  - Create, edit, delete, and publish posts
  - Post detail pages with featured images
  - Status handling for drafts and published posts
- **Categories**
  - Organize posts into categories
  - View posts filtered by category
- **Comments**
  - Add comments on blog posts
  - Basic moderation workflow
- **User authentication**
  - User registration and login
  - Secure password hashing via Django auth
- **Dashboard**
  - Admin-style dashboard for managing:
    - Posts
    - Categories
    - Users
- **Search**
  - Search blog posts by title or content
- **Responsive UI**
  - Basic responsive layout using Django templates and custom CSS

### Screenshots

#### Home Page
<img src="screenshots/home.png" alt="Home Page" width="800"/>

#### Featured Posts
<img src="screenshots/featured-posts.png" alt="Featured Posts" width="800"/>

#### Login Page
<img src="screenshots/login.png" alt="Login Page" width="800"/>

#### Registration Page
<img src="screenshots/register.png" alt="Registration Page" width="800"/>

#### Post Detail
<img src="screenshots/post-detail.png" alt="Post Detail" width="800"/>

#### Blog Post with Comments
<img src="screenshots/post-comments.png" alt="Blog Post with Comments" width="800"/>

#### Dashboard Overview
<img src="screenshots/dashboard.png" alt="Dashboard Overview" width="800"/>

#### Categories Management
<img src="screenshots/categories.png" alt="Categories Management" width="800"/>

### Tech Stack

- **Backend**: Django
- **Frontend**: Django templates, HTML, CSS
- **Database**: SQLite (default Django configuration)
- **Forms & UI helpers**:
  - `django-crispy-forms`
  - `crispy-bootstrap4`
- **Images**: `Pillow` for image handling

### Project Structure (Key Apps)

- **`blog_main`**: Main project configuration (settings, URLs, WSGI/ASGI).
- **`blogs`**: Core blog logic (models, views, URLs, context processors).
- **`dashboards`**: Admin-style dashboard for managing content.
- **`assignments`**: Additional app used within the project (e.g., extra content or examples).
- **`templates`**: Shared templates for the public site and dashboard.
- **`static` / `blog_main/static`**: CSS, images, and other static assets.
- **`media`**: Uploaded media files (such as post images).

### Getting Started

#### 1. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

On Linux/macOS:

```bash
python -m venv venv
source venv/bin/activate
```

#### 2. Install dependencies

```bash
pip install -r requirements.txt
```

#### 3. Apply database migrations

```bash
python manage.py migrate
```

#### 4. Create a superuser (for dashboard access)

```bash
python manage.py createsuperuser
```

#### 5. Run the development server

```bash
python manage.py runserver
```

Then open your browser at `http://127.0.0.1:8000/`.

### Usage

- **Public site**: View posts, browse by category, search, and comment.
- **Dashboard**: Log in as a staff/superuser to add and manage posts, categories, and users.

### Static and Media Files

- **Static files** (CSS, images, JS) live under `static/` and may also be collected into `staticfiles/`.
- **Media files** uploaded through the admin or dashboard are stored in the `media/` directory.

### Running Tests

```bash
python manage.py test
```

This will run tests defined inside the app `tests.py` files.

