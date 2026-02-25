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
<img width="958" height="510" alt="image" src="https://github.com/user-attachments/assets/63a764af-3b46-4acf-b778-b12751f9c2ff" />


#### Featured Posts
<img width="955" height="572" alt="image" src="https://github.com/user-attachments/assets/1f9f0d7f-9d04-4384-9164-b7c59339fa3d" />


#### Login Page
<img width="960" height="573" alt="Login Page" src="https://github.com/user-attachments/assets/eb8d19c3-23ea-4def-9856-4c94001151ba" />

#### Registration Page
<img width="960" height="576" alt="Registration Page" src="https://github.com/user-attachments/assets/00234e9e-1f13-4bb9-b61e-d9476d63e6d1" />

#### Post Detail
<img width="960" height="567" alt="image" src="https://github.com/user-attachments/assets/0a081e32-8730-43cc-a1f2-35fa6da4cd12" />


#### Blog Post with Comments
<img width="960" height="506" alt="image" src="https://github.com/user-attachments/assets/b342543b-3bab-487b-97b1-a37ae0ebb59b" />


#### Dashboard Overview
<img width="960" height="572" alt="image" src="https://github.com/user-attachments/assets/0958f6fd-16e7-4edc-a250-b4b86c8a1796" />


#### Categories Management
<img width="960" height="514" alt="image" src="https://github.com/user-attachments/assets/4badba30-bc82-4cee-84cc-a2f496eedde5" />


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

