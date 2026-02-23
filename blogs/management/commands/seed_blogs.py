"""
Management command: python manage.py seed_blogs
Creates 4 sample categories + 4 blog posts using the first superuser.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from blogs.models import Blog, Category


CATEGORIES = [
    "Technology",
    "Programming",
    "Web Development",
    "Artificial Intelligence",
]

POSTS = [
    {
        "title": "The Future of Artificial Intelligence in Everyday Life",
        "category": "Artificial Intelligence",
        "is_featured": True,
        "short_description": (
            "Artificial Intelligence is no longer a futuristic concept — it is woven into "
            "the fabric of our daily routines. From voice assistants and recommendation engines "
            "to self-driving cars and medical diagnosis, AI is reshaping how we live, work, and interact."
        ),
        "blog_body": """Artificial Intelligence (AI) has moved far beyond the realm of science fiction. Today, it powers the smartphone in your pocket, the streaming platform you watch, and even the hospital equipment diagnosing diseases with pinpoint accuracy.

What Is AI?

At its core, AI refers to machines or software that can perform tasks that typically require human intelligence — understanding language, recognising images, making decisions, and learning from experience.

AI in Your Daily Life

1. Smart Assistants: Tools like Siri, Google Assistant, and Alexa understand your speech and respond in real time.

2. Personalised Recommendations: Netflix, Spotify, and YouTube use AI algorithms to suggest content tailored specifically to your preferences.

3. Healthcare: AI models now detect certain cancers from medical scans with accuracy rivalling experienced radiologists.

4. Finance: Banks use AI fraud-detection systems to flag suspicious transactions instantly.

The Road Ahead

The next decade will see AI become even more embedded in infrastructure, education, and creative industries. Large Language Models (LLMs) like ChatGPT are already changing how people write, code, and research.

Challenges remain — bias in algorithms, job displacement fears, and data privacy concerns — but the consensus among experts is that AI, when responsibly developed, holds enormous promise for solving humanity's greatest challenges.

The future is AI-augmented, not AI-replaced. Humans and machines will collaborate, each amplifying the strengths of the other.""",
        "status": "Published",
    },
    {
        "title": "10 Python Tips Every Developer Should Know in 2024",
        "category": "Programming",
        "is_featured": True,
        "short_description": (
            "Python continues to dominate as one of the most popular programming languages in the world. "
            "Whether you are a beginner or a seasoned developer, these 10 practical tips will sharpen "
            "your Python skills and help you write cleaner, faster, and more Pythonic code."
        ),
        "blog_body": """Python's simplicity is deceptive — beneath its clean syntax lies a rich set of features that many developers never fully explore. Here are 10 tips to level up your Python game.

1. Use f-Strings for Formatting

Instead of messy string concatenation, use f-strings:
    name = "Alice"
    print(f"Hello, {name}!")

2. List Comprehensions

Replace verbose for-loops with concise comprehensions:
    squares = [x**2 for x in range(10)]

3. The Walrus Operator (:=)

Assign and test in a single expression:
    if (n := len(data)) > 10:
        print(f"Too long: {n}")

4. Unpacking with *

Unpack iterables cleanly:
    first, *middle, last = [1, 2, 3, 4, 5]

5. defaultdict for Cleaner Code

Avoid KeyError when building dictionaries:
    from collections import defaultdict
    counts = defaultdict(int)

6. Use enumerate() Instead of range(len())

    for i, item in enumerate(my_list):
        print(i, item)

7. Context Managers (with)

Always use with for file and resource management to ensure proper cleanup.

8. Type Hints

Type hints improve code readability and catch bugs early with tools like mypy:
    def greet(name: str) -> str:
        return f"Hello, {name}"

9. dataclasses for Clean Data Models

    from dataclasses import dataclass
    @dataclass
    class Point:
        x: float
        y: float

10. Profile Before Optimising

Use cProfile or line_profiler to identify real bottlenecks before rewriting code.

Mastering these patterns will make your Python code more readable, efficient, and enjoyable to maintain.""",
        "status": "Published",
    },
    {
        "title": "Building Modern Web Apps with Django and Bootstrap 5",
        "category": "Web Development",
        "is_featured": False,
        "short_description": (
            "Django is a powerful Python web framework that encourages rapid development and clean, pragmatic design. "
            "Combined with Bootstrap 5, you can build beautiful, responsive web applications in a fraction of the time "
            "it would take with other stacks."
        ),
        "blog_body": """Django is often described as "the web framework for perfectionists with deadlines" — and for good reason. It comes batteries-included with an ORM, authentication, admin panel, and templating engine right out of the box.

Why Django?

- Rapid development: Django's convention-over-configuration philosophy means less boilerplate.
- Security: Built-in protection against SQL injection, XSS, CSRF, and clickjacking.
- Scalability: Powers high-traffic sites like Instagram, Pinterest, and Disqus.
- Huge ecosystem: Thousands of third-party packages available on PyPI.

Setting Up Your Project

    pip install django
    django-admin startproject myproject
    cd myproject
    python manage.py startapp myapp

Integrating Bootstrap 5

Add the Bootstrap 5 CDN to your base template:
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">

Use Django's template inheritance to keep your HTML DRY:
    <!-- base.html -->
    <body>{% block content %}{% endblock %}</body>

Key Django + Bootstrap Patterns

1. Forms: Use django-crispy-forms with the bootstrap5 pack for beautifully styled forms with zero extra CSS.
2. Messages: Map Django's message tags (success, error, warning) to Bootstrap alert classes.
3. Pagination: Django's Paginator class pairs perfectly with Bootstrap's pagination component.

Deployment Tips

- Use WhiteNoise to serve static files without a separate web server.
- Environment variables with python-decouple keep secrets out of your codebase.
- Gunicorn + Nginx is the standard production stack for Django applications.

With Django and Bootstrap 5, you have everything you need to go from idea to deployed product in days.""",
        "status": "Published",
    },
    {
        "title": "Why Every Developer Should Learn Cloud Computing in 2024",
        "category": "Technology",
        "is_featured": False,
        "short_description": (
            "Cloud computing has fundamentally transformed how software is built, deployed, and scaled. "
            "From startups to Fortune 500 companies, the cloud is the backbone of modern technology. "
            "Here is why every developer — regardless of specialisation — should understand cloud fundamentals."
        ),
        "blog_body": """The cloud is no longer just an IT buzzword. It is the infrastructure layer underpinning almost every application you use today — from the apps on your phone to enterprise software managing millions of transactions per second.

What Is Cloud Computing?

Cloud computing is the delivery of computing services — servers, storage, databases, networking, software, and analytics — over the internet ("the cloud") on a pay-as-you-go basis.

The Three Major Providers

1. Amazon Web Services (AWS): The market leader with the broadest service catalogue.
2. Microsoft Azure: Dominant in enterprise environments, especially those using Microsoft products.
3. Google Cloud Platform (GCP): Known for data analytics, machine learning, and Kubernetes (which Google invented).

Why Developers Need Cloud Knowledge

1. Serverless Functions: AWS Lambda, Azure Functions, and Google Cloud Functions let you run code without managing servers.

2. Containers & Kubernetes: Docker containers and Kubernetes orchestration are now standard deployment patterns. Cloud providers offer managed Kubernetes (EKS, AKS, GKE).

3. CI/CD Pipelines: GitHub Actions, AWS CodePipeline, and similar tools automate testing and deployment.

4. Databases as a Service: RDS, Firestore, Cosmos DB — managed databases mean no more server patching.

5. Scalability: Auto-scaling groups handle traffic spikes automatically, so your app stays fast under load.

Getting Started

- AWS Free Tier and GCP Free Tier both offer generous always-free resources to experiment with.
- Cloud certifications (AWS Solutions Architect, Google Associate Cloud Engineer) are highly valued by employers.
- Start with a simple project: deploy a Django app to a cloud VM, then explore managed services one by one.

The cloud is not optional anymore — it is the foundation of modern software development.""",
        "status": "Published",
    },
]


class Command(BaseCommand):
    help = "Seed the database with sample categories and blog posts."

    def handle(self, *args, **kwargs):
        # Get or create the first superuser
        author = User.objects.filter(is_superuser=True).first()
        if not author:
            author = User.objects.filter(is_staff=True).first()
        if not author:
            self.stderr.write("No superuser or staff user found. Create one with: python manage.py createsuperuser")
            return

        self.stdout.write(f"Using author: {author.username}")

        # Create categories
        cat_objects = {}
        for name in CATEGORIES:
            cat, created = Category.objects.get_or_create(category_name=name)
            cat_objects[name] = cat
            if created:
                self.stdout.write(f"  Created category: {name}")
            else:
                self.stdout.write(f"  Category already exists: {name}")

        # Create posts
        created_count = 0
        for data in POSTS:
            cat = cat_objects[data["category"]]
            slug_base = slugify(data["title"])

            if Blog.objects.filter(slug__startswith=slug_base).exists():
                self.stdout.write(f"  Post already exists: {data['title'][:50]}")
                continue

            post = Blog.objects.create(
                title=data["title"],
                category=cat,
                author=author,
                short_description=data["short_description"],
                blog_body=data["blog_body"],
                status=data["status"],
                is_featured=data["is_featured"],
                featured_image="",  # no image — placeholder
            )
            post.slug = f"{slug_base}-{post.id}"
            post.save()
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f"  [OK] Created post: {data['title'][:60]}"))

        self.stdout.write(self.style.SUCCESS(f"\nDone! {created_count} post(s) created."))
