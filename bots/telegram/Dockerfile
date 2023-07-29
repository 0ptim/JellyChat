# Python Version
FROM python:3.10.12

# Create Docker User
RUN useradd --create-home appuser
WORKDIR /home/appuser

# Copy Files
COPY jellychatapi.py .
COPY logger.py .
COPY telegram/ .

# Install Dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && chown -R appuser:appuser .

# Change User
USER appuser

# Start Script
CMD ["python", "telegram_bot.py"]
