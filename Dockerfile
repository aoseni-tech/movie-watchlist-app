# Use official Python image
FROM python:3-slim

# Set working directory
WORKDIR /app

# Copy app files
COPY dist/movie_watchlist-1.0.0-py2.py3-none-any.whl .

COPY wsgi.py .

RUN pip install movie_watchlist-1.0.0-py2.py3-none-any.whl

RUN pip install gunicorn

# Run the app using Gunicorn
CMD ["gunicorn", "-b", ":8080", "wsgi:application"]
