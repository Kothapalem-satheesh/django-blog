"""
Management command: python manage.py seed_blogs
Clears all existing blog posts and creates 10 fresh ones with images.
"""
import os
import urllib.request
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.conf import settings
from blogs.models import Blog, Category


CATEGORIES = [
    "Technology",
    "Programming",
    "Web Development",
    "Artificial Intelligence",
    "Sports",
    "Politics",
    "Health",
    "Entertainment",
    "Science",
]

# Unsplash direct CDN images (no API key required)
IMAGES = {
    "ai_future":     "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=900&q=80&fm=jpg",
    "python_tips":   "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=900&q=80&fm=jpg",
    "django_web":    "https://images.unsplash.com/photo-1547658719-da2b51169166?w=900&q=80&fm=jpg",
    "cloud":         "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=900&q=80&fm=jpg",
    "ml_beginners":  "https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=900&q=80&fm=jpg",
    "js_vs_python":  "https://images.unsplash.com/photo-1579468118864-1b9ea3c0db4a?w=900&q=80&fm=jpg",
    "rest_api":      "https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=900&q=80&fm=jpg",
    "cybersecurity": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=900&q=80&fm=jpg",
    "chatgpt":       "https://images.unsplash.com/photo-1676573401423-f3e29c0e9b5a?w=900&q=80&fm=jpg",
    "git_github":    "https://images.unsplash.com/photo-1556075798-4825dfaaf498?w=900&q=80&fm=jpg",
    # Sports, Politics, Health, Entertainment, Science
    "cricket":       "https://images.unsplash.com/photo-1531415074968-036ba1b575da?w=900&q=80&fm=jpg",
    "football":      "https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=900&q=80&fm=jpg",
    "olympics":      "https://images.unsplash.com/photo-1461896836934-4a1e5d2ccef2?w=900&q=80&fm=jpg",
    "fitness":       "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=900&q=80&fm=jpg",
    "politics":      "https://images.unsplash.com/photo-1540914124281-342587941389?w=900&q=80&fm=jpg",
    "election":      "https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=900&q=80&fm=jpg",
    "democracy":     "https://images.unsplash.com/photo-1589994965851-a8f479c573a9?w=900&q=80&fm=jpg",
    "health":        "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=900&q=80&fm=jpg",
    "mental_health": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=900&q=80&fm=jpg",
    "movies":        "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=900&q=80&fm=jpg",
    "music":         "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=900&q=80&fm=jpg",
    "climate":       "https://images.unsplash.com/photo-1611273426858-450d8e3c9fce?w=900&q=80&fm=jpg",
    "space":         "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=900&q=80&fm=jpg",
}

POSTS = [
    # ── ARTIFICIAL INTELLIGENCE ──────────────────────────────────────────
    {
        "title": "The Future of Artificial Intelligence in 2025",
        "category": "Artificial Intelligence",
        "is_featured": True,
        "image_key": "ai_future",
        "short_description": (
            "Artificial Intelligence is no longer a futuristic concept — it is woven into the fabric "
            "of our daily lives. From voice assistants and recommendation engines to self-driving cars "
            "and medical diagnosis, AI is reshaping how we live, work, and interact with the world."
        ),
        "blog_body": """Artificial Intelligence (AI) has moved far beyond the realm of science fiction. Today, it powers the smartphone in your pocket, the streaming service you watch every evening, and even the medical equipment diagnosing diseases with remarkable accuracy.

What Is Artificial Intelligence?

At its core, AI refers to machines or software capable of performing tasks that typically require human intelligence — understanding natural language, recognising images, making decisions, and learning from experience.

AI in Your Daily Life

1. Smart Assistants — Tools like Siri, Google Assistant, and Alexa understand speech and respond in real time, learning your preferences over time.

2. Personalised Recommendations — Netflix, Spotify, and YouTube use sophisticated AI algorithms to suggest content specifically tailored to your taste.

3. Healthcare — AI models now detect certain cancers from medical scans with accuracy rivalling experienced radiologists, reducing diagnostic errors significantly.

4. Finance — Banks deploy AI fraud-detection systems that flag suspicious transactions within milliseconds, protecting millions of customers every day.

5. Transportation — Tesla's Autopilot and Waymo's self-driving technology represent years of machine learning training on billions of miles of road data.

Large Language Models (LLMs)

2024 and 2025 have been transformational years for LLMs. Models like GPT-4, Claude, and Gemini are changing how people write, code, research, and create. Businesses are integrating these tools into customer service, content generation, and software development workflows.

Challenges Ahead

Despite the excitement, significant challenges remain:
- Algorithmic bias that can reinforce societal inequalities
- Job displacement concerns across multiple industries
- Data privacy and security vulnerabilities
- Energy consumption of large AI training runs

The Road Ahead

The consensus among experts is that AI, when responsibly developed, holds enormous promise for solving humanity's greatest challenges — from climate change to disease. The future is AI-augmented, not AI-replaced. Humans and machines will collaborate, each amplifying the strengths of the other.""",
        "status": "Published",
    },
    {
        "title": "How ChatGPT and Large Language Models Actually Work",
        "category": "Artificial Intelligence",
        "is_featured": False,
        "image_key": "chatgpt",
        "short_description": (
            "ChatGPT took the world by storm, but how does it actually work under the hood? "
            "This article breaks down the transformer architecture, training process, and "
            "the concept of attention mechanisms that make LLMs so remarkably capable."
        ),
        "blog_body": """In November 2022, ChatGPT was released to the public and reached one million users in just five days. But what is actually happening inside these powerful language models?

The Transformer Architecture

Modern LLMs are built on the Transformer architecture, introduced in the landmark 2017 paper "Attention Is All You Need" by Google researchers. Before transformers, AI used recurrent neural networks (RNNs) that processed text sequentially — word by word — which was slow and struggled with long-range dependencies.

Transformers process entire sequences simultaneously using a mechanism called self-attention, which allows the model to weigh the importance of every word in relation to every other word in the input.

How Attention Works

Imagine reading the sentence: "The trophy did not fit in the suitcase because it was too big."
What does "it" refer to — the trophy or the suitcase? Humans resolve this instantly. Self-attention allows the model to do the same by computing relationships between every token.

Training Process

LLMs are trained in two main stages:

1. Pre-training — The model is exposed to hundreds of billions of tokens from the internet, books, and code. It learns to predict the next word in a sequence. This is unsupervised learning at a massive scale.

2. Fine-tuning with RLHF — Reinforcement Learning from Human Feedback (RLHF) is then used to make the model helpful, harmless, and honest. Human raters rank model outputs, and the model is rewarded for better responses.

Why Are They So Capable?

Scale is the key insight. Researchers discovered that as you increase the number of parameters (GPT-4 is estimated to have over 1 trillion parameters) and the training data, models develop emergent abilities — capabilities that were not explicitly trained for, such as reasoning, coding, and creative writing.

The Future of LLMs

Multimodal models (like GPT-4V and Gemini) can now understand images, audio, and video alongside text. Smaller, efficient models (like Llama 3 and Mistral) are making LLMs accessible on personal devices without internet connectivity.

Understanding the basics of how these models work gives you a significant advantage in a world where AI is becoming as fundamental as the internet itself.""",
        "status": "Published",
    },
    {
        "title": "Machine Learning for Beginners: Getting Started with Scikit-Learn",
        "category": "Artificial Intelligence",
        "is_featured": False,
        "image_key": "ml_beginners",
        "short_description": (
            "Machine learning can feel overwhelming at first, but with Python and Scikit-Learn, "
            "you can train your first model in under 30 minutes. This beginner-friendly guide walks "
            "you through the core concepts, algorithms, and your first hands-on ML project."
        ),
        "blog_body": """Machine learning (ML) is the science of getting computers to learn from data without being explicitly programmed. If you know Python, you already have everything you need to get started.

Core Concepts

Before writing any code, understand these three concepts:

1. Features — The input variables (columns) your model learns from. For a house price predictor, features might include size, location, and number of bedrooms.

2. Labels — The output your model predicts. In the house example, the label is the sale price.

3. Training vs Testing — You split your data into a training set (the model learns from this) and a test set (used to evaluate how well the model generalised).

Installing Scikit-Learn

    pip install scikit-learn pandas numpy matplotlib

Your First Model: Linear Regression

    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_squared_error

    # Load dataset
    df = pd.read_csv('housing.csv')
    X = df[['size', 'bedrooms', 'age']]
    y = df['price']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Train model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Evaluate
    predictions = model.predict(X_test)
    print(f"MSE: {mean_squared_error(y_test, predictions):.2f}")

Popular Algorithms in Scikit-Learn

- Linear/Logistic Regression — Great starting point for regression and classification
- Decision Trees — Easy to visualise and interpret
- Random Forest — Powerful ensemble method that combines multiple trees
- Support Vector Machine (SVM) — Excellent for high-dimensional data
- K-Nearest Neighbours (KNN) — Simple, intuitive, and surprisingly effective

Tips for Beginners

1. Start with clean, small datasets — Kaggle has hundreds of beginner-friendly datasets.
2. Always visualise your data before training — Use matplotlib or seaborn to understand distributions and correlations.
3. Normalise features — Many algorithms perform much better when features are on the same scale.
4. Cross-validation — Use k-fold cross-validation instead of a single train/test split for more reliable accuracy estimates.

The journey from zero to machine learning practitioner is shorter than you think. Start small, build intuition, and gradually tackle more complex problems.""",
        "status": "Published",
    },

    # ── PROGRAMMING ──────────────────────────────────────────────────────
    {
        "title": "10 Python Tips Every Developer Should Know in 2025",
        "category": "Programming",
        "is_featured": True,
        "image_key": "python_tips",
        "short_description": (
            "Python continues to dominate as one of the most popular programming languages worldwide. "
            "Whether you are a beginner or a seasoned developer, these 10 practical tips will sharpen "
            "your Python skills and help you write cleaner, faster, and more Pythonic code."
        ),
        "blog_body": """Python's simplicity is deceptive — beneath its clean syntax lies a rich set of features that many developers never fully explore. Here are 10 tips to level up your Python skills immediately.

1. Use f-Strings for Formatting

Instead of messy string concatenation or old-style % formatting, use f-strings (Python 3.6+):

    name = "Satheesh"
    score = 98.5
    print(f"Hello, {name}! Your score is {score:.1f}%")

2. List Comprehensions

Replace verbose for-loops with concise comprehensions:

    # Old way
    squares = []
    for x in range(10):
        squares.append(x**2)

    # Pythonic way
    squares = [x**2 for x in range(10)]

3. The Walrus Operator (:=)

Assign and test in a single expression (Python 3.8+):

    if (n := len(data)) > 10:
        print(f"List too long: {n} items")

4. Unpacking with *

    first, *middle, last = [1, 2, 3, 4, 5]
    # first=1, middle=[2,3,4], last=5

5. defaultdict for Cleaner Code

    from collections import defaultdict
    word_count = defaultdict(int)
    for word in text.split():
        word_count[word] += 1

6. Use enumerate() Instead of range(len())

    for i, item in enumerate(my_list, start=1):
        print(f"{i}. {item}")

7. Context Managers (with)

Always use with for file and resource management to ensure proper cleanup even if an exception occurs.

8. Type Hints

    def calculate_area(radius: float) -> float:
        return 3.14159 * radius ** 2

9. dataclasses for Clean Data Models

    from dataclasses import dataclass, field

    @dataclass
    class BlogPost:
        title: str
        author: str
        tags: list = field(default_factory=list)

10. Profile Before Optimising

Use cProfile or line_profiler to identify real bottlenecks before rewriting code. Premature optimisation is the root of all evil.

Bonus: Use pathlib Instead of os.path

    from pathlib import Path
    base = Path(__file__).parent
    config_file = base / "config" / "settings.json"

Mastering these patterns will transform your Python code into something elegant, readable, and efficient.""",
        "status": "Published",
    },
    {
        "title": "JavaScript vs Python: Which Language Should You Learn First?",
        "category": "Programming",
        "is_featured": False,
        "image_key": "js_vs_python",
        "short_description": (
            "Two of the world's most popular programming languages — but which should you pick first? "
            "This honest comparison covers syntax, job market, use cases, learning curve, and community "
            "to help you make the right decision for your goals."
        ),
        "blog_body": """The first programming language you learn shapes how you think about code. JavaScript and Python are both excellent choices — but they excel in different areas. Let's compare them honestly.

The Short Answer

- Learn Python if you are interested in data science, AI/ML, automation, backend development, or academic research.
- Learn JavaScript if you want to build interactive websites, become a full-stack developer, or get hired as quickly as possible.

Python: Strengths and Use Cases

Python reads almost like English, making it the most beginner-friendly language available today.

Strengths:
- Clean, readable syntax with forced indentation
- Dominant in data science, machine learning, and AI (NumPy, Pandas, TensorFlow, PyTorch)
- Excellent for scripting and automation
- Strong in backend web development (Django, FastAPI, Flask)
- Huge standard library

Use cases: Data analysis, ML models, automation scripts, web scraping, backend APIs, scientific computing.

JavaScript: Strengths and Use Cases

JavaScript is the only language that runs natively in every web browser, making it essential for frontend development.

Strengths:
- Runs in the browser (frontend) and on servers (Node.js)
- Instant visual feedback when building web interfaces
- Massive npm ecosystem (over 2 million packages)
- React, Vue, and Angular for building powerful SPAs
- Full-stack development possible with one language

Use cases: Web frontends, Node.js backends, mobile apps (React Native), desktop apps (Electron).

Salary and Job Market (2025)

Both languages command excellent salaries. JavaScript developers are in higher demand due to the volume of web projects. Python developers often earn more in specialised fields like AI and data engineering.

Learning Curve

Python: Lower — less syntax noise, fewer concepts needed to build something useful.
JavaScript: Moderate — asynchronous programming (callbacks, Promises, async/await) can be confusing initially.

My Recommendation

For absolute beginners: Start with Python. The simpler syntax lets you focus on programming logic without fighting the language.

For those who know their goal is web development: Go straight to JavaScript.

The good news? Once you learn one language well, picking up the other takes a fraction of the time.""",
        "status": "Published",
    },
    {
        "title": "Git and GitHub: The Complete Developer Workflow Guide",
        "category": "Programming",
        "is_featured": False,
        "image_key": "git_github",
        "short_description": (
            "Git is the most important tool in every developer's toolkit — yet many developers only scratch "
            "the surface of what it can do. This guide covers everything from basic commits to branching "
            "strategies, pull requests, and professional team workflows."
        ),
        "blog_body": """Every professional developer uses Git. It is not optional — it is as fundamental as knowing how to type. Let's go from the basics to the workflow used by professional engineering teams.

What Is Git?

Git is a distributed version control system that tracks every change you make to your codebase. It lets you:
- Revert to any previous state of your project
- Work on multiple features simultaneously using branches
- Collaborate with other developers without overwriting each other's work

Essential Git Commands

    # Start tracking a project
    git init

    # Check what has changed
    git status
    git diff

    # Stage and commit changes
    git add .
    git commit -m "Add user authentication feature"

    # View history
    git log --oneline --graph

Branching Strategy

Professional teams never commit directly to main. Instead:

    # Create a feature branch
    git checkout -b feature/bookmark-system

    # Do your work, then push
    git push origin feature/bookmark-system

    # Create a Pull Request on GitHub for code review

The GitHub Flow (Used by Most Teams)

1. Create a branch from main
2. Add commits to your branch
3. Open a Pull Request
4. Discuss and review the code
5. Merge to main after approval
6. Deploy

Writing Good Commit Messages

Bad: "fix stuff", "update", "changes"
Good: "Fix bookmark toggle returning 405 on GET requests"

Follow this format:
    <type>: <short summary>

    Types: feat, fix, docs, style, refactor, test, chore

Undoing Mistakes

    # Undo last commit (keep changes)
    git reset --soft HEAD~1

    # Discard all local changes
    git checkout -- .

    # Remove a file from staging
    git restore --staged filename.py

.gitignore — What to Never Commit

Always add these to .gitignore:
- env/ or venv/ (virtual environments)
- .env (secret keys and passwords)
- __pycache__/ and *.pyc
- db.sqlite3 (local database)
- media/ (user uploads)

Mastering Git is one of the highest-ROI investments you can make as a developer. It protects your work, enables collaboration, and is expected in every professional environment.""",
        "status": "Published",
    },

    # ── WEB DEVELOPMENT ──────────────────────────────────────────────────
    {
        "title": "Building Modern Web Apps with Django and Bootstrap 5",
        "category": "Web Development",
        "is_featured": True,
        "image_key": "django_web",
        "short_description": (
            "Django is a powerful Python web framework that encourages rapid development and clean, "
            "pragmatic design. Combined with Bootstrap 5, you can build beautiful, responsive web "
            "applications in a fraction of the time it would take with other stacks."
        ),
        "blog_body": """Django is often described as "the web framework for perfectionists with deadlines" — and for good reason. It comes batteries-included with an ORM, authentication, admin panel, and templating engine right out of the box.

Why Choose Django in 2025?

- Rapid development: Convention-over-configuration means less boilerplate and more productivity.
- Security: Built-in protection against SQL injection, XSS, CSRF, and clickjacking out of the box.
- Scalability: Powers high-traffic platforms like Instagram, Pinterest, Disqus, and Eventbrite.
- ORM: Write Python instead of SQL — Django translates it for you.
- Huge ecosystem: Thousands of third-party packages on PyPI.

Project Setup

    pip install django
    django-admin startproject myproject
    cd myproject
    python manage.py startapp myapp
    python manage.py migrate
    python manage.py runserver

Django MVT Architecture

Django follows the Model-View-Template pattern:
- Model: Defines your data structure (maps to database tables)
- View: Contains the business logic (processes requests and returns responses)
- Template: HTML files that display data to the user

Integrating Bootstrap 5

Add Bootstrap 5 to your base template:

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

Use Django template inheritance for DRY HTML:

    <!-- base.html -->
    <!DOCTYPE html>
    <html>
    <body>
        {% include 'navbar.html' %}
        {% block content %}{% endblock %}
    </body>
    </html>

Key Patterns

1. Forms with Crispy Forms: pip install django-crispy-forms gives you Bootstrap-styled forms automatically.
2. Messages Framework: Map Django's messages to Bootstrap alert colours for clean user feedback.
3. Custom 404/500 Pages: Define handler404 and handler500 in urls.py for professional error pages.

Deployment Checklist

- Set DEBUG = False in production
- Use WhiteNoise for static files
- Store secrets in environment variables (.env file)
- Use Gunicorn as your WSGI server
- Put Nginx in front of Gunicorn as a reverse proxy
- Use PostgreSQL instead of SQLite in production

Django + Bootstrap 5 is one of the most productive stacks available today. You can go from idea to a fully deployed, professional-looking web application in days — not months.""",
        "status": "Published",
    },
    {
        "title": "REST API Design Best Practices with Django REST Framework",
        "category": "Web Development",
        "is_featured": False,
        "image_key": "rest_api",
        "short_description": (
            "Building a REST API is easy. Building a great REST API is an art. This guide covers the "
            "principles of RESTful design, HTTP methods, status codes, authentication, versioning, "
            "and how to implement all of it cleanly using Django REST Framework."
        ),
        "blog_body": """REST (Representational State Transfer) APIs are the backbone of modern web applications. Every mobile app, single-page application, and third-party integration relies on well-designed APIs.

Installing Django REST Framework

    pip install djangorestframework
    # Add to INSTALLED_APPS:
    'rest_framework',

Core REST Principles

1. Resources over Actions: URLs should represent resources (nouns), not actions (verbs).
   Good:   GET /api/posts/
   Bad:    GET /api/getPosts/

2. Use HTTP Methods Correctly:
   - GET:    Retrieve data (never modify state)
   - POST:   Create a new resource
   - PUT:    Replace an existing resource completely
   - PATCH:  Partially update a resource
   - DELETE: Remove a resource

3. Meaningful Status Codes:
   - 200 OK: Successful GET, PUT, PATCH
   - 201 Created: Successful POST
   - 204 No Content: Successful DELETE
   - 400 Bad Request: Invalid input from client
   - 401 Unauthorized: Authentication required
   - 403 Forbidden: Authenticated but no permission
   - 404 Not Found: Resource does not exist
   - 500 Internal Server Error: Server-side bug

Serializers in DRF

    from rest_framework import serializers
    from .models import Blog

    class BlogSerializer(serializers.ModelSerializer):
        class Meta:
            model = Blog
            fields = ['id', 'title', 'slug', 'short_description', 'status', 'created_at']
            read_only_fields = ['id', 'slug', 'created_at']

ViewSets and Routers

    from rest_framework import viewsets
    from rest_framework.permissions import IsAuthenticatedOrReadOnly

    class BlogViewSet(viewsets.ModelViewSet):
        queryset = Blog.objects.filter(status='Published')
        serializer_class = BlogSerializer
        permission_classes = [IsAuthenticatedOrReadOnly]

    # In urls.py
    from rest_framework.routers import DefaultRouter
    router = DefaultRouter()
    router.register('posts', BlogViewSet)

Authentication Options

- Session Authentication: Good for same-domain browser clients
- Token Authentication: Simple, stateless, good for mobile apps
- JWT (JSON Web Tokens): Industry standard for modern SPAs and mobile apps

API Versioning

Always version your API from day one:
    /api/v1/posts/
    /api/v2/posts/

This allows you to introduce breaking changes in v2 without affecting existing v1 clients.

A well-designed API is a product. Treat it with the same care you give your frontend — your API consumers will thank you.""",
        "status": "Published",
    },

    # ── TECHNOLOGY ───────────────────────────────────────────────────────
    {
        "title": "Why Every Developer Should Learn Cloud Computing in 2025",
        "category": "Technology",
        "is_featured": False,
        "image_key": "cloud",
        "short_description": (
            "Cloud computing has fundamentally transformed how software is built, deployed, and scaled. "
            "From startups to Fortune 500 companies, the cloud is the backbone of modern technology. "
            "Here is why every developer — regardless of specialisation — should understand cloud fundamentals."
        ),
        "blog_body": """The cloud is no longer just an IT buzzword. It is the infrastructure layer underpinning almost every application you use today — from the apps on your phone to enterprise systems managing millions of transactions per second.

What Is Cloud Computing?

Cloud computing is the delivery of computing services — servers, storage, databases, networking, software, and analytics — over the internet on a pay-as-you-go basis. Instead of buying and maintaining physical hardware, you rent capacity from a cloud provider.

The Three Major Providers (2025)

1. Amazon Web Services (AWS): The market leader with the broadest service catalogue. If it exists in computing, AWS probably has a managed service for it.

2. Microsoft Azure: Dominant in enterprise environments, especially those already invested in the Microsoft ecosystem (Office 365, Active Directory).

3. Google Cloud Platform (GCP): Known for data analytics, machine learning infrastructure, and Kubernetes (which Google originally developed).

Key Services Every Developer Should Know

Compute:
- EC2 (AWS) / Compute Engine (GCP) — Virtual machines on demand
- Lambda / Cloud Functions — Serverless, run code without managing servers
- EKS / GKE — Managed Kubernetes for container orchestration

Storage:
- S3 (AWS) / Cloud Storage (GCP) — Object storage for files, images, backups
- RDS / Cloud SQL — Managed relational databases (no patching, automatic backups)

Networking:
- CloudFront / Cloud CDN — Content delivery networks for fast global performance
- VPC — Virtual Private Cloud for network isolation

Why Developers Need This Knowledge

Modern job descriptions increasingly list cloud skills alongside programming languages. Understanding how to:
- Deploy a containerised application to Kubernetes
- Set up a CI/CD pipeline with GitHub Actions and cloud deployment
- Configure auto-scaling and load balancing
- Use managed databases instead of self-hosted servers

...separates senior developers from junior ones.

Getting Started for Free

Both AWS Free Tier and GCP Free Tier offer generous always-free resources. Start by deploying a simple Django application to a cloud VM, then gradually explore managed services.

AWS Certified Solutions Architect and Google Associate Cloud Engineer certifications are among the most valued in the technology industry today.""",
        "status": "Published",
    },
    {
        "title": "Cybersecurity Essentials Every Developer Must Know",
        "category": "Technology",
        "is_featured": False,
        "image_key": "cybersecurity",
        "short_description": (
            "Security is not the responsibility of a separate team — it is every developer's job. "
            "From SQL injection and XSS to HTTPS, hashing passwords, and OWASP Top 10, "
            "this guide covers the security fundamentals that every developer must understand and practice."
        ),
        "blog_body": """In 2024, the average cost of a data breach reached $4.88 million. Security vulnerabilities are almost always caused by developers who did not know better — not by sophisticated nation-state hackers breaking unbreakable encryption. Here is what every developer needs to know.

The OWASP Top 10

The Open Web Application Security Project (OWASP) publishes the 10 most critical web application security risks. Every developer should know these:

1. Broken Access Control — Users can access resources or perform actions they should not be allowed to.
2. Cryptographic Failures — Sensitive data transmitted or stored without proper encryption.
3. Injection — SQL injection, command injection, and template injection attacks.
4. Insecure Design — Security not considered during the design phase.
5. Security Misconfiguration — Default passwords, unnecessary features enabled, verbose error messages.
6. Vulnerable Components — Using outdated libraries with known security vulnerabilities.
7. Authentication Failures — Weak passwords, missing rate limiting, insecure session management.
8. Integrity Failures — Unsigned software updates, insecure deserialization.
9. Logging Failures — Not logging security events, making breach detection impossible.
10. Server-Side Request Forgery (SSRF) — Tricking the server into making requests to internal systems.

SQL Injection — Still the Most Common Attack

Never build SQL queries with string concatenation:

    # DANGEROUS — never do this
    query = f"SELECT * FROM users WHERE username = '{username}'"

    # SAFE — use parameterised queries (Django ORM does this automatically)
    user = User.objects.get(username=username)

Password Storage — Always Hash

    # WRONG — never store plain text passwords
    user.password = "mysecretpassword"

    # RIGHT — Django handles this automatically with PBKDF2
    user.set_password("mysecretpassword")

HTTPS Everywhere

Never transmit sensitive data over plain HTTP. In development, use Django's SECURE_SSL_REDIRECT = True when deploying.

Cross-Site Scripting (XSS)

Django templates auto-escape HTML by default, protecting against XSS. Never use mark_safe() or |safe without careful review.

Django Security Settings for Production

    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_CONTENT_TYPE_NOSNIFF = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True

Security is a mindset, not a feature. Build it in from the first line of code, not as an afterthought before launch.""",
        "status": "Published",
    },

    # ── SPORTS ───────────────────────────────────────────────────────────
    {
        "title": "Why Cricket Is More Than Just a Sport in India",
        "category": "Sports",
        "is_featured": True,
        "image_key": "cricket",
        "short_description": (
            "Cricket in India is a religion, a unifier, and a source of national pride. "
            "From the IPL to Test matches, the sport has shaped culture, economy, and "
            "millions of dreams. Here is why cricket holds a special place in every Indian heart."
        ),
        "blog_body": """In India, cricket is not just a game — it is an emotion that cuts across regions, languages, and generations. When the Indian team plays, streets go quiet and screens light up in every corner of the country.

The Rise of Cricket in India

Cricket was introduced during the British era but truly captured the nation's imagination after the 1983 World Cup victory. Kapil Dev lifting the trophy at Lord's changed the way India looked at the sport forever. Since then, legends like Sachin Tendulkar, MS Dhoni, and Virat Kohli have become household names.

The IPL Revolution

The Indian Premier League (IPL), launched in 2008, transformed cricket into a year-round spectacle. It brought together international stars, young talent, and massive viewership. The league has created thousands of jobs, from players and coaches to analysts and content creators.

Cricket and National Identity

Major matches, especially against Pakistan or in World Cups, see the entire country rally behind the Men in Blue. Wins are celebrated with fireworks; losses are mourned. Cricket has the power to pause the nation — a rare feat for any sport.

The Future

With the growth of women's cricket and the continued success of the national team, cricket in India is only getting stronger. The sport will remain a cornerstone of Indian culture for generations to come.""",
        "status": "Published",
    },
    {
        "title": "The Evolution of Football: From Local Pitches to Global Phenomenon",
        "category": "Sports",
        "is_featured": False,
        "image_key": "football",
        "short_description": (
            "Football is the world's most popular sport, with over 4 billion fans. "
            "From its origins in England to the FIFA World Cup and Champions League, "
            "this is how the beautiful game conquered the globe."
        ),
        "blog_body": """Football, or soccer as it is known in some countries, is the universal language of sport. No other game commands such a massive global following or such passionate loyalty from fans.

A Brief History

Modern football took shape in England in the 19th century, with the formation of the Football Association in 1863. Rules were standardised, and the game spread rapidly through British colonies and trade routes. Today, almost every country has a professional league and a national team.

The World Cup and Global Icons

The FIFA World Cup, held every four years, is the most-watched sporting event on the planet. Legends like Pelé, Maradona, Zidane, and Messi have become cultural icons far beyond their home nations. The UEFA Champions League brings together the best club teams in Europe and attracts billions of viewers.

Why Football Unites

Football is simple to understand and play — all you need is a ball and some space. It thrives in crowded cities and remote villages alike. It gives people a shared identity, something to celebrate and debate. Whether you are in Brazil, Nigeria, or Japan, the love for the game is the same.

The future of football will see more women's leagues, technology like VAR, and perhaps even new formats. But the core — 22 players, one ball, and endless passion — will remain unchanged.""",
        "status": "Published",
    },
    {
        "title": "Olympics 2024: What Made Paris Unforgettable",
        "category": "Sports",
        "is_featured": False,
        "image_key": "olympics",
        "short_description": (
            "The Paris 2024 Olympics brought the world together for two weeks of "
            "incredible athletic achievement, record-breaking performances, and "
            "unforgettable moments. A look back at the games that defined 2024."
        ),
        "blog_body": """The Olympic Games represent the pinnacle of human athletic achievement. Every four years, the world tunes in to watch athletes push the limits of what the human body can do. Paris 2024 was no exception.

The Spirit of the Olympics

The Olympics are unique because they bring together nations that might otherwise rarely interact. Athletes compete under their flags but also under the shared ideals of excellence, friendship, and respect. The opening and closing ceremonies celebrate both national pride and global unity.

Memorable Moments from Paris 2024

From swimming to athletics, gymnastics to cycling, Paris delivered drama and glory. New world records were set, underdogs triumphed, and veterans said goodbye in style. The city itself — with events held at iconic venues like the Eiffel Tower and along the Seine — provided a stunning backdrop.

The Road to the Next Olympics

Los Angeles 2028 is already on the horizon. For athletes, the cycle of training, qualification, and competition never stops. For fans, the Olympics remain a reminder of what humanity can achieve when we come together in peace and competition.""",
        "status": "Published",
    },
    {
        "title": "How Sports Build Discipline and Leadership in Young People",
        "category": "Sports",
        "is_featured": False,
        "image_key": "fitness",
        "short_description": (
            "Sports do more than keep us fit — they teach discipline, teamwork, "
            "resilience, and leadership. Here is why every young person should "
            "have a sport in their life, whether competitively or just for fun."
        ),
        "blog_body": """Parents and educators have long argued that sports build character. Science and experience both back this up. Whether it is cricket, football, swimming, or martial arts, sports offer lessons that last a lifetime.

Discipline and Routine

Athletes learn to show up every day, follow a schedule, and prioritise rest and nutrition. This discipline often carries over into academics and later into careers. There are no shortcuts in sport — you get out what you put in.

Teamwork and Communication

Team sports teach you how to work with others, communicate under pressure, and put the group's success ahead of individual glory. These skills are invaluable in any workplace or community.

Resilience and Handling Failure

Every athlete loses at some point. Learning to accept defeat, analyse what went wrong, and come back stronger is one of the most important life skills. Sports provide a safe space to fail and try again.

Leadership

Captains and senior players learn to lead by example, motivate others, and make decisions under pressure. Many business leaders and public figures credit their sporting background for their success.

Encouraging young people to play sports — at any level — is one of the best investments we can make in their future.""",
        "status": "Published",
    },

    # ── POLITICS ──────────────────────────────────────────────────────────
    {
        "title": "Why Young People Must Engage with Politics",
        "category": "Politics",
        "is_featured": True,
        "image_key": "politics",
        "short_description": (
            "Politics shapes everything from the economy to education, health, and the environment. "
            "When young people stay away from politics, decisions are made without their voice. "
            "Here is why your vote and your voice matter more than ever."
        ),
        "blog_body": """Politics is often seen as something for older people or for those in power. But the truth is: politics affects every aspect of your life — from the cost of education and healthcare to job opportunities and climate policy. If you do not engage, others will decide for you.

What Is Politics, Really?

Politics is how we make collective decisions as a society. It is about who gets what, when, and how. It decides how taxes are spent, which laws are passed, and how the country responds to challenges like pandemics, inflation, and climate change.

Why Youth Participation Matters

Young people are the largest demographic in many countries, yet they often vote at lower rates than older generations. When young people vote and participate — through elections, protests, or community organising — leaders are forced to pay attention to issues like climate action, employment, and digital rights.

How to Get Started

You do not need to run for office tomorrow. Start by:
- Registering to vote and voting in every election
- Reading about local and national issues from reliable sources
- Discussing politics with family and friends in a respectful way
- Supporting causes and candidates that align with your values

Politics can feel messy and frustrating, but disengaging only makes it worse. Your voice matters. Use it.""",
        "status": "Published",
    },
    {
        "title": "Understanding Elections: How Democracy Works in Practice",
        "category": "Politics",
        "is_featured": False,
        "image_key": "election",
        "short_description": (
            "Elections are the cornerstone of democracy — but how do they actually work? "
            "From voter registration to counting and forming governments, this guide "
            "explains the process and why every vote counts."
        ),
        "blog_body": """In a democracy, elections are the moment when power passes from the people to their representatives. Understanding how elections work helps you participate meaningfully and hold leaders accountable.

The Electoral Process

Elections typically involve several steps: voter registration, campaigning, voting (often in person or by postal ballot), counting, and the declaration of results. In many countries, independent bodies oversee the process to ensure fairness and transparency.

First-Past-the-Post vs Proportional Representation

Different countries use different systems. First-past-the-post (e.g. in India, UK, USA for some bodies) means the candidate with the most votes wins. Proportional representation (e.g. in many European countries) allocates seats based on the share of votes each party receives. Each system has pros and cons.

Why Your Vote Matters

It is easy to think one vote does not matter. But elections are often decided by thin margins. In addition, high turnout sends a signal that citizens care, which influences how governments behave. Low turnout can lead to policies that ignore the needs of those who stayed home.

Staying Informed

Before voting, learn about the candidates and their positions. Use reliable news sources and fact-check claims. Democracy works best when citizens are informed and engaged.""",
        "status": "Published",
    },
    {
        "title": "Democracy in the Digital Age: Challenges and Opportunities",
        "category": "Politics",
        "is_featured": False,
        "image_key": "democracy",
        "short_description": (
            "Social media and the internet have changed how we discuss politics, spread information, "
            "and hold leaders accountable. But they also bring misinformation and polarisation. "
            "How can we protect democracy in the digital age?"
        ),
        "blog_body": """The internet was supposed to make democracy stronger — more information, more participation, more transparency. In many ways it has. But it has also created new challenges that we are still learning to address.

The Good: More Access to Information and Participation

Citizens can now follow debates, read policy documents, and contact representatives with a few clicks. Social movements have used digital tools to organise and demand change. Whistleblowers and journalists can share information that might once have been suppressed.

The Bad: Misinformation and Echo Chambers

False information spreads faster than the truth online. Algorithms often show us content that reinforces what we already believe, creating echo chambers. Foreign actors and bad actors can manipulate public opinion through coordinated campaigns.

What Can We Do?

- Media literacy: Learn to spot fake news and check sources before sharing.
- Support quality journalism: Subscribe to reliable outlets that do fact-based reporting.
- Regulate with care: Governments and platforms must balance free speech with the need to curb harmful content.
- Engage respectfully: Avoid spreading hate or unverified claims; encourage civil debate.

Democracy in the digital age will only work if we use technology wisely and stay vigilant.""",
        "status": "Published",
    },

    # ── HEALTH ────────────────────────────────────────────────────────────
    {
        "title": "Simple Habits for a Healthier Life in 2025",
        "category": "Health",
        "is_featured": False,
        "image_key": "health",
        "short_description": (
            "You do not need a drastic overhaul to feel better — small, consistent habits "
            "can transform your health. Sleep, movement, nutrition, and mindfulness: "
            "a practical guide to building a healthier daily routine."
        ),
        "blog_body": """Health is not about perfection; it is about consistency. A few small habits, practised daily, can improve your energy, mood, and long-term well-being more than any short-term crash diet or fitness fad.

Sleep: The Foundation of Health

Most adults need 7–8 hours of sleep per night. Poor sleep affects your immune system, concentration, and mood. Try to go to bed and wake up at roughly the same time every day, limit screens before bed, and keep your room cool and dark.

Move More, Sit Less

You do not need a gym membership. Walking, cycling, dancing, or even stretching for 20–30 minutes a day can make a big difference. The goal is to move regularly and reduce long periods of sitting.

Eat Whole Foods Most of the Time

Focus on vegetables, fruits, whole grains, lean protein, and healthy fats. You do not have to give up treats entirely — balance is key. Drink plenty of water and limit sugary drinks and highly processed foods.

Mental Health Matters

Stress, anxiety, and loneliness affect physical health too. Stay connected with people you care about, take breaks, and consider practices like meditation or journaling. If you are struggling, talking to a professional is a sign of strength, not weakness.

Start with one or two habits and build from there. Sustainable change is slow change.""",
        "status": "Published",
    },
    {
        "title": "Why Mental Health Is Just as Important as Physical Health",
        "category": "Health",
        "is_featured": False,
        "image_key": "mental_health",
        "short_description": (
            "Mental health affects how we think, feel, and act. It influences our relationships, "
            "work, and quality of life. Breaking the stigma and prioritising mental well-being "
            "is essential for a healthy, balanced life."
        ),
        "blog_body": """For too long, mental health was ignored or stigmatised. Today we know that mental and physical health are deeply connected — and that taking care of your mind is as important as taking care of your body.

What Is Mental Health?

Mental health includes our emotional, psychological, and social well-being. It affects how we handle stress, relate to others, and make choices. Good mental health does not mean never feeling sad or anxious; it means having the tools and support to cope with life's challenges.

Common Challenges

Anxiety, depression, and stress are among the most common mental health issues. They can be caused by genetics, life events, work pressure, or social isolation. The good news is that they are treatable — through therapy, medication, lifestyle changes, or a combination.

How to Support Your Mental Health

- Talk about it: Sharing with someone you trust can reduce the burden.
- Stay active: Exercise is one of the most effective ways to boost mood.
- Sleep well: Poor sleep worsens anxiety and depression.
- Limit social media: Compare less; connect more in real life.
- Seek help: Therapists and counsellors are trained to help. There is no shame in asking.

If you or someone you know is in crisis, reach out to a helpline or a professional. You are not alone.""",
        "status": "Published",
    },

    # ── ENTERTAINMENT ────────────────────────────────────────────────────
    {
        "title": "How Streaming Changed the Way We Watch Movies and Shows",
        "category": "Entertainment",
        "is_featured": False,
        "image_key": "movies",
        "short_description": (
            "Netflix, Disney+, Amazon Prime, and others have revolutionised entertainment. "
            "Binge-watching, original content, and the decline of the cinema — "
            "how streaming reshaped the film and TV industry forever."
        ),
        "blog_body": """Twenty years ago, watching a movie meant going to a theatre or waiting for it to air on TV. Today, we have thousands of films and series at our fingertips, anytime, anywhere. Streaming has changed not just how we watch, but what gets made.

The Rise of Streaming Giants

Netflix started as a DVD-by-mail service before pivoting to streaming. Today it competes with Disney+, Amazon Prime Video, Apple TV+, and regional players. These platforms invest billions in original content, from dramas and comedies to documentaries and reality shows.

Binge-Watching and the Serial Revolution

Streaming encouraged the release of full seasons at once, leading to binge-watching. Shows are now written with that in mind — cliffhangers, long arcs, and deep character development. The line between "TV" and "film" has blurred.

What Happens to Cinemas?

Cinemas have had to adapt. Big blockbusters still draw crowds, but smaller films often go straight to streaming. The pandemic accelerated this shift. The future may be a mix: event films in theatres, everything else at home.

The downside: too much choice can be overwhelming, and subscription costs add up. But for many, streaming has made great storytelling more accessible than ever.""",
        "status": "Published",
    },
    {
        "title": "The Power of Music: How It Shapes Our Mood and Memories",
        "category": "Entertainment",
        "is_featured": False,
        "image_key": "music",
        "short_description": (
            "Music can lift our mood, help us focus, or bring back vivid memories. "
            "From the science of why we love certain songs to the rise of streaming "
            "and playlists — the role of music in our daily lives."
        ),
        "blog_body": """Music is one of the few things that exists in every human culture. We use it to celebrate, mourn, work, and relax. Science is still uncovering why music has such a powerful effect on our brains and emotions.

Why Does Music Move Us?

Music activates multiple areas of the brain — those linked to emotion, memory, and reward. A familiar song can instantly transport us back to a specific moment. Upbeat music can boost energy; slow, calm music can reduce anxiety. We often use music to regulate our mood.

From Radio to Streaming

The way we listen has changed dramatically. Radio and CDs gave way to MP3s and iPods, and now streaming services like Spotify and Apple Music offer millions of songs on demand. Playlists and algorithms suggest new music based on our tastes, making discovery easier than ever.

Music and Identity

The music we love often becomes part of our identity. We bond with others over shared tastes, and we use music to express who we are. Whether you love classical, hip-hop, or indie, music connects us to ourselves and to others.

So the next time you put on your headphones, remember: you are not just listening — you are feeling, remembering, and sometimes healing.""",
        "status": "Published",
    },

    # ── SCIENCE ──────────────────────────────────────────────────────────
    {
        "title": "Climate Change: What We Know and What We Can Do",
        "category": "Science",
        "is_featured": False,
        "image_key": "climate",
        "short_description": (
            "Climate change is one of the defining challenges of our time. "
            "From rising temperatures and extreme weather to melting ice and ocean acidification — "
            "the science is clear. So is the path to action."
        ),
        "blog_body": """The evidence for climate change is overwhelming. Global temperatures are rising, ice sheets are melting, sea levels are rising, and extreme weather events are becoming more frequent. The main cause is human activity — especially the burning of fossil fuels and deforestation.

What the Science Says

Scientists have known for decades that greenhouse gases (like CO2) trap heat in the atmosphere. As we burn coal, oil, and gas, we add more of these gases, so the planet warms. The result: more heatwaves, floods, droughts, and stronger storms. The oceans absorb much of the extra heat and CO2, leading to warmer and more acidic waters, which harm marine life.

What We Can Do

Individual actions matter: reduce energy use, choose sustainable transport, eat less meat, and waste less. But the biggest impact will come from systemic change: shifting to renewable energy, protecting forests, and holding governments and corporations accountable.

Hope and Action

It is easy to feel hopeless, but we still have time to limit the damage. Every fraction of a degree matters. Young people around the world are demanding action, and many countries and companies are setting net-zero targets. The future depends on the choices we make today.""",
        "status": "Published",
    },
    {
        "title": "Space Exploration in 2025: Mars, Moon, and Beyond",
        "category": "Science",
        "is_featured": False,
        "image_key": "space",
        "short_description": (
            "Humans are once again aiming for the Moon and setting sights on Mars. "
            "With NASA, SpaceX, ISRO, and others leading the charge, space exploration "
            "is entering a new golden age. Here is what is happening and why it matters."
        ),
        "blog_body": """Space exploration has entered a new era. Government agencies and private companies are working together to return humans to the Moon, send astronauts to Mars, and push the boundaries of what we know about the universe.

Back to the Moon

NASA's Artemis programme aims to land the first woman and the next man on the Moon by the end of this decade. The goal is not just to visit but to stay — building a sustainable presence that can serve as a stepping stone to Mars. International partners and commercial players are involved.

Mars: The Next Frontier

Mars has long captured our imagination. SpaceX is developing Starship for crewed Mars missions. NASA is testing technologies for long-duration spaceflight and life support. Robotic missions continue to explore the Red Planet, searching for signs of past or present life.

Why It Matters

Space exploration drives innovation — from better materials and medical devices to improved communication and Earth observation. It inspires young people to study science and engineering. It also raises big questions: Are we alone? What is our place in the cosmos?

The next decade will likely see humans walk on the Moon again and perhaps take the first steps toward Mars. The sky is no longer the limit.""",
        "status": "Published",
    },
]


def download_image(url, filename, dest_folder):
    """Download an image from a URL and save it to dest_folder."""
    os.makedirs(dest_folder, exist_ok=True)
    filepath = os.path.join(dest_folder, filename)
    if os.path.exists(filepath):
        return filepath
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            with open(filepath, 'wb') as f:
                f.write(response.read())
        return filepath
    except Exception as e:
        return None


class Command(BaseCommand):
    help = "Clear all existing blog posts and seed 22 posts (tech, sports, politics, health, entertainment, science) with author satheeshyadav."

    def handle(self, *args, **kwargs):
        # ── Get or create author: satheeshyadav ───────────────────────────
        author = User.objects.filter(username="satheeshyadav").first()
        if not author:
            author = User.objects.create_user(
                username="satheeshyadav",
                email="satheeshyadav85@gmail.com",
                password="satheesh_seed_2025",
                first_name="Satheesh",
                last_name="Yadav",
            )
            self.stdout.write(self.style.WARNING(
                "Created user 'satheeshyadav'. Change password after first login: python manage.py changepassword satheeshyadav"
            ))
        self.stdout.write(f"Author: {author.username}")

        # ── Delete all existing blog posts ──────────────────────────────
        count = Blog.objects.count()
        Blog.objects.all().delete()
        self.stdout.write(self.style.WARNING(f"Deleted {count} existing blog post(s)."))

        # ── Create categories ───────────────────────────────────────────
        cat_objects = {}
        for name in CATEGORIES:
            cat, created = Category.objects.get_or_create(category_name=name)
            cat_objects[name] = cat
            status = "Created" if created else "Exists"
            self.stdout.write(f"  [{status}] Category: {name}")

        # ── Image download folder ───────────────────────────────────────
        img_folder = os.path.join(settings.MEDIA_ROOT, 'uploads', 'blog_images')
        self.stdout.write(f"\nDownloading images to: {img_folder}")

        # ── Create posts ────────────────────────────────────────────────
        created_count = 0
        for data in POSTS:
            cat = cat_objects[data["category"]]
            slug_base = slugify(data["title"])
            image_field = ""

            # Download image
            img_key = data.get("image_key", "")
            img_url = IMAGES.get(img_key, "")
            if img_url:
                filename = f"{img_key}.jpg"
                local_path = download_image(img_url, filename, img_folder)
                if local_path:
                    # Store path relative to MEDIA_ROOT
                    image_field = f"uploads/blog_images/{filename}"
                    self.stdout.write(f"  [IMG] Downloaded: {filename}")
                else:
                    self.stdout.write(self.style.WARNING(f"  [IMG] Failed: {filename} (no internet?)"))

            post = Blog.objects.create(
                title=data["title"],
                category=cat,
                author=author,
                short_description=data["short_description"],
                blog_body=data["blog_body"],
                status=data["status"],
                is_featured=data["is_featured"],
                featured_image=image_field,
            )
            post.slug = f"{slug_base}-{post.id}"
            post.save()
            created_count += 1
            self.stdout.write(self.style.SUCCESS(
                f"  [OK] {data['category']}: {data['title'][:55]}"
            ))

        self.stdout.write(self.style.SUCCESS(
            f"\nDone! {created_count} posts created across {len(CATEGORIES)} categories."
        ))
