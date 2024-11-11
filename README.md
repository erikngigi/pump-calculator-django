# Django Crypto Calculator

A simple Django-based cryptocurrency calculator that allows users to perform basic calculations on cryptocurrency values. This calculator is self-contained, relying on custom inbuilt calculations rather than external APIs.

## Features

- **Custom Calculation**: Performs real-time calculations using custom conversion rates.
- **User-friendly Interface**: Easy-to-use, minimalistic interface with form-based inputs.

## Requirements

- Python 3.8+
- Django 3.2+
- Optional: `virtualenv` for creating an isolated Python environment

## Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/django-crypto-calculator.git
    cd django-crypto-calculator
    ```

2. **Set Up Virtual Environment**

    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run Migrations**

    ```bash
    python manage.py migrate
    ```

5. **Create Superuser (optional for admin access)**

    ```bash
    python manage.py createsuperuser
    ```

6. **Run the Server**

    ```bash
    python manage.py runserver
    ```

    Access the application at `http://127.0.0.1:8000`.

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.
