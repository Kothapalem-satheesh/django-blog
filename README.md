# Django Blog Application

A full-featured blog application built with **Django**. It includes a public blog and an admin-style dashboard for managing posts, categories, comments, and users.

## Features

- **Blog posts**: create, edit, delete, feature, and publish posts (draft/published)
- **Categories**: organize posts and browse/filter by category
- **Comments**: add comments with a basic moderation workflow
- **Authentication**: register, login, logout (Django auth)
- **Dashboard**: manage posts, categories, comments, and users
- **Search**: search posts by title/content

## Screenshots

> These screenshots are embedded via GitHub image links.  
> If you prefer local screenshots, add them under a `screenshots/` folder and update the paths.

#### Home Page
<img width="958" height="573" alt="Home Page" src="https://github.com/user-attachments/assets/23186853-e92e-4ab4-9539-abe082242be8" />

#### Featured Posts
<img width="960" height="573" alt="Featured Posts" src="https://github.com/user-attachments/assets/34434963-3e55-4b38-ab96-7be4801fdb27" />

#### Login Page
<img width="960" height="573" alt="Login Page" src="https://github.com/user-attachments/assets/eb8d19c3-23ea-4def-9856-4c94001151ba" />

#### Registration Page
<img width="960" height="576" alt="Registration Page" src="https://github.com/user-attachments/assets/00234e9e-1f13-4bb9-b61e-d9476d63e6d1" />

#### Post Detail
<img width="960" height="569" alt="Post Detail" src="https://github.com/user-attachments/assets/655146c0-e570-488c-9f60-056b6c2d55a3" />

#### Blog Post with Comments
<img width="959" height="571" alt="Blog Post with Comments" src="https://github.com/user-attachments/assets/6024a7b6-fba1-42b7-a59b-0308b489c942" />

#### Dashboard Overview
<img width="960" height="575" alt="Dashboard Overview" src="https://github.com/user-attachments/assets/a724385e-881c-461a-a859-05883d305171" />

#### Categories Management
<img width="959" height="571" alt="Categories Management" src="https://github.com/user-attachments/assets/20aac721-f597-49de-9be0-33f5765ef3c8" />

## Tech Stack

- **Backend**: Django
- **Frontend**: Django templates, HTML, CSS
- **Database**: SQLite (default local configuration)
- **Forms/UI helpers**: `django-crispy-forms`, `crispy-bootstrap4`
- **Images**: `Pillow`

## Project Structure

- **`blog_main/`**: project configuration (settings, URLs, WSGI/ASGI)
- **`blogs/`**: core blog logic (models, views, URLs, context processors)
- **`dashboards/`**: admin-style dashboard for content management
- **`assignments/`**: additional app used within the project
- **`templates/`**: templates for the public site and dashboard
- **`static/`**: CSS/images and other static assets
- **`media/`**: uploaded media files (e.g., post images)

## Getting Started (Local)

#### 1) Create and activate a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python -m venv venv
source venv/bin/activate
```

#### 2) Install dependencies

```bash
pip install -r requirements.txt
```

#### 3) Apply migrations

```bash
python manage.py migrate
```

#### 4) Create a superuser (for dashboard access)

```bash
python manage.py createsuperuser
```

#### 5) Run the development server

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Usage

- **Public site**: browse posts, filter by category, search, and add comments
- **Dashboard**: log in as a staff/superuser to manage posts, categories, comments, and users

## Static & Media Files

- **Static files**: stored under `static/` (CSS, images, JS)
- **Media uploads**: stored under `media/`

## Running Tests

```bash
python manage.py test
```

