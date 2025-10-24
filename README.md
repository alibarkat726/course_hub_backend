# E-Learning Platform

A modern, multi-tenant e-learning platform built with FastAPI, PostgreSQL, and SQLAlchemy. This platform supports course management, user authentication, payment processing, and organization-based multi-tenancy.

## 🚀 Features

- **Multi-tenant Architecture**: Support for multiple organizations with isolated data
- **User Management**: Student, instructor, and admin roles with JWT authentication
- **Course Management**: Create, manage, and publish courses with pricing
- **Payment Processing**: Integrated Stripe payment system
- **RESTful API**: Clean, well-documented API endpoints
- **Database**: PostgreSQL with async SQLAlchemy ORM
- **Security**: Password hashing with bcrypt, JWT tokens, and CORS support

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python 3.13+)
- **Database**: PostgreSQL with asyncpg driver
- **ORM**: SQLAlchemy 2.0 with async support
- **Authentication**: JWT tokens with refresh mechanism
- **Payments**: Stripe integration
- **Security**: Passlib with bcrypt hashing
- **Server**: Uvicorn ASGI server

## 📋 Prerequisites

- Python 3.13+
- PostgreSQL 12+
- pip (Python package manager)

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd E_learning_platform
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   ENVIRONMENT=development
   DEBUG=true
   DATABASE_URL=postgresql+asyncpg://postgres:user@localhost:5432/coursehub
   SECRET_KEY=your-secret-key-here
   STRIPE_SECRET_KEY=your-stripe-secret-key
   STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret
   ```

5. **Set up the database**
   - Ensure PostgreSQL is running
   - Create the database: `coursehub`
   - Run database migrations (if available)

## 🚀 Running the Application

1. **Start the development server**
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Access the application**
   - API Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## 📚 API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - User login
- `POST /auth/token` - OAuth2 token endpoint
- `POST /auth/refresh` - Refresh access token
- `GET /auth/me` - Get current user profile

### Organizations
- `GET /orgs/` - List organizations
- `POST /orgs/` - Create organization
- `GET /orgs/{org_id}` - Get organization details

### Courses
- `GET /courses/` - List courses
- `POST /courses/` - Create course
- `GET /courses/{course_id}` - Get course details
- `PUT /courses/{course_id}` - Update course
- `DELETE /courses/{course_id}` - Delete course

### Payments
- `POST /payments/create-checkout` - Create Stripe checkout session
- `POST /payments/webhook` - Stripe webhook handler

## 🏗️ Project Structure

```
E_learning_platform/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection and session
│   ├── dependencies.py     # FastAPI dependencies
│   ├── middleware/          # Custom middleware
│   │   └── tenant.py        # Multi-tenant middleware
│   ├── models/              # SQLAlchemy models
│   │   ├── core.py          # Core models (User, Organization, Course)
│   │   └── payments.py       # Payment models
│   ├── routers/             # API route handlers
│   │   ├── auth.py          # Authentication routes
│   │   ├── courses.py       # Course management routes
│   │   ├── organizations.py # Organization routes
│   │   └── payments.py      # Payment routes
│   ├── schemas/             # Pydantic models for API
│   │   ├── core.py          # Core schemas
│   │   └── payments.py      # Payment schemas
│   ├── services/            # Business logic services
│   └── utils/               # Utility functions
│       └── security.py      # Security utilities
├── requirements.txt         # Python dependencies
├── .env                    # Environment variables
└── README.md              # This file
```

## 🔐 Security Features

- **Password Hashing**: bcrypt with salt rounds
- **JWT Authentication**: Secure token-based authentication
- **CORS Support**: Configurable cross-origin resource sharing
- **Input Validation**: Pydantic model validation
- **SQL Injection Protection**: SQLAlchemy ORM protection

## 💳 Payment Integration

The platform integrates with Stripe for payment processing:

- Secure checkout sessions
- Webhook handling for payment events
- Support for multiple currencies
- Course pricing in cents for precision

## 🏢 Multi-Tenancy

The platform supports multiple organizations:

- Isolated data per organization
- Tenant-specific middleware
- Organization-based user management
- Scalable architecture for multiple clients

## 🧪 Testing

```bash
# Run tests (if test suite is available)
pytest

# Run with coverage
pytest --cov=app
```

## 📝 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Application environment | `development` |
| `DEBUG` | Debug mode | `true` |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://postgres:user@localhost:5432/coursehub` |
| `SECRET_KEY` | JWT secret key | `dev-secret-key-change` |
| `STRIPE_SECRET_KEY` | Stripe secret key | - |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook secret | - |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [API documentation](http://localhost:8000/docs) when running locally
2. Review the logs for error messages
3. Ensure all environment variables are properly set
4. Verify database connectivity

## 🔄 Roadmap

- [ ] Frontend dashboard
- [ ] Course video streaming
- [ ] Advanced analytics
- [ ] Mobile app API
- [ ] Email notifications
- [ ] Course certificates
- [ ] Discussion forums
- [ ] Assignment submissions

---

Built with ❤️ using FastAPI and modern Python practices.
