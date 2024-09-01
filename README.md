## Deployment

Current deployed at `http://url-shortener-weld-seven.vercel.app/docs`
So do check it out

# URL Shortener API

This is a simple URL shortener API built with FastAPI and PostgreSQL. It allows users to shorten long URLs and redirect to the original URLs using the shortened versions.

## Features

- Shorten long URLs
- Redirect to original URLs using short codes
- PostgreSQL database for persistent storage
- Efficient handling of duplicate URLs
- Error handling for invalid requests

## Requirements

- Python 3.7+
- PostgreSQL
- pip

## Quick Start

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your PostgreSQL database and create a `.env` file with your database URL:
   ```
   DATABASE_URL=postgresql://user:password@localhost/dbname
   ```
5. Run these script in your posgresql cli/local editor 

   ```
   CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    original_url TEXT NOT NULL,
    short_code VARCHAR(6) UNIQUE NOT NULL
   );

   CREATE INDEX idx_original_url ON urls(original_url);
   CREATE INDEX idx_short_code ON urls(short_code);
   ``` 

6. Run the application:
   ```
   python main.py
   ```

The API will be available at `http://localhost:8000`.

## API Usage

### Shorten a URL

```
POST /shorten
Content-Type: application/json

{
    "url": "https://www.example.com/very/long/url/that/needs/shortening"
}
```

### Redirect to Original URL

Simply visit the shortened URL:

```
GET /{short_code}
```

## Project Structure

- `main.py`: Contains the FastAPI application, database models, and API endpoints
- `requirements.txt`: List of Python dependencies
- `README.md`: This file
- `.env`: (Create this file) Contains environment variables like DATABASE_URL

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
