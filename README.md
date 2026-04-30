# Django REST API Blog

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Django](https://img.shields.io/badge/Django-6.0-green?logo=django)
![DRF](https://img.shields.io/badge/Django%20REST%20Framework-3.17.1-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

A secure and scalable blog REST API built with **Django REST Framework**, featuring token-based authentication, object-level permissions, and optimized database queries.

---

## 📸 Screenshots

| Posts List | Create Post | Login | Post Detail |
|---|---|---|---|
| ![Posts List](screenshots/posts-list.png) | ![Create Post](screenshots/create-post.png) | ![Login](screenshots/login.png) | 

---

## ✨ Features

- 🔐 Token-based authentication
- 🛡️ Object-level permissions (users can only edit/delete their own posts)
- ⚡ Optimized database queries with `select_related()`
- 📊 Proper HTTP status codes
- 🔄 Full CRUD operations on posts
- 🏗️ Clean, maintainable project architecture

---

## 📂 Project Structure

```
blog_api/
├── posts/
│   ├── models.py          # Database models
│   ├── serializers.py     # JSON serialization/deserialization
│   ├── views.py           # Business logic & API views
│   └── urls.py            # URL routing
├── config/
│   ├── settings.py
│   └── urls.py
└── requirements.txt
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.11 | Programming language |
| Django 6.0 | Web framework |
| Django REST Framework | API layer |
| SQLite | Database (development) |
| Token Authentication | Auth mechanism |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/Dev-Mostafa-Mohamed/django-rest-blog.git
cd django-rest-blog
```

**2. Create and activate a virtual environment**

```bash
python -m venv blog_api_env
blog_api_env\Scripts\activate       # On Windows: venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Apply migrations**

```bash
python manage.py migrate
```

**5. Create a superuser (optional)**

```bash
python manage.py createsuperuser
```

**6. Run the development server**

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

---

## 📡 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `POST` | `/api/register/` | Register a new user | No |
| `POST` | `/api/login/` | Log in and receive a token | No |

### Posts

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/api/posts/` | List all posts | No |
| `POST` | `/api/posts/` | Create a new post | ✅ Yes |
| `GET` | `/api/posts/<id>/` | Retrieve a single post | No |
| `PUT` | `/api/posts/<id>/` | Update a post (owner only) | ✅ Yes |
| `PATCH` | `/api/posts/<id>/` | Partially update a post (owner only) | ✅ Yes |
| `DELETE` | `/api/posts/<id>/` | Delete a post (owner only) | ✅ Yes |

---

## 🔐 Authentication Usage

Include the token in the `Authorization` header for protected endpoints:

```
Authorization: Token <your_token_here>
```

**Example — Login:**

```bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_user", "password": "your_password"}'
```

**Response:**

```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

**Example — Create Post:**

```bash
curl -X POST http://127.0.0.1:8000/api/posts/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{"title": "My First Post", "content": "Hello, World!"}'
```

---

## 🔒 Security Details

**Author auto-assignment** — The server automatically assigns the authenticated user as the post author, preventing impersonation:

```python
serializer.save(author=request.user)
```

**Object-level permissions** — Only the post owner can modify or delete their content:

```python
if post.author != request.user:
    return Response(
        {'error': 'Permission denied'},
        status=status.HTTP_403_FORBIDDEN
    )
```

---

## ⚡ Performance

Database queries are optimized using `select_related()` to fetch the author in a single SQL query, avoiding the N+1 problem:

```python
posts = Post.objects.select_related('author').all()
```

---

## 📊 HTTP Status Codes

| Code | Meaning |
|---|---|
| `200 OK` | Successful GET / PUT / PATCH |
| `201 Created` | Resource successfully created |
| `204 No Content` | Resource successfully deleted |
| `400 Bad Request` | Validation error |
| `401 Unauthorized` | Missing or invalid token |
| `403 Forbidden` | Authenticated but not the owner |
| `404 Not Found` | Resource does not exist |

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to your branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
