Jika Jalankan Tanpa Docker (Development Lokal)
1. Install Redis di lokal
# Ubuntu/Debian
sudo apt install redis-server

2. Jalankan Redis
redis-server

3. Set REDIS_URL di .env atau environment
REDIS_URL=redis://localhost:6379/0

# macOS
brew install redis

# 1. Setup
git clone your-repo
cd mtk-app

# 2. Edit secret key
echo "SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')" >> .env

# 3. Jalankan
docker-compose up -d

# 4. Akses
http://localhost