FROM python:3.12-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    nginx \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy aplikasi
COPY . .

# Setup Nginx
RUN rm -f /etc/nginx/sites-enabled/default
COPY nginx.conf /etc/nginx/sites-available/mtk
RUN ln -s /etc/nginx/sites-available/mtk /etc/nginx/sites-enabled/

# Port
EXPOSE 80 8867

# Start script
CMD ["./deploy.sh"]