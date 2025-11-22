# Tourist Destinations CRUD Web Application

A Django-based web application for managing tourist destinations. This application allows administrators to perform CRUD operations on tourist destination information.

## Features

- Create, Read, Update, and Delete tourist destinations
- Manage destination details including:
  - Place Name
  - Weather information
  - Location (State, District)
  - Google Map Link
  - Description
  - Multiple images per destination
- Admin dashboard for easy management
- Responsive design for all devices

## Prerequisites

- Python 3.8+
- PostgreSQL
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd tourist-destinations
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Update the database credentials and other settings in `.env`

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

8. Access the admin panel at `http://127.0.0.1:8000/admin/`

## Project Structure

```
tourist_destinations/
├── destinations/          # Main app for tourist destinations
│   ├── migrations/       # Database migrations
│   ├── static/           # Static files (CSS, JS, images)
│   ├── templates/        # HTML templates
│   ├── admin.py         # Admin configuration
│   ├── apps.py          # App config
│   ├── forms.py         # Forms for the app
│   ├── models.py        # Database models
│   ├── urls.py          # App URLs
│   └── views.py         # View functions
├── tourist_destinations/  # Project settings
│   ├── settings.py      # Main settings file
│   ├── urls.py          # Main URL configuration
│   └── wsgi.py          # WSGI configuration
├── .env                 # Environment variables
├── manage.py            # Django management script
└── requirements.txt     # Python dependencies
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
