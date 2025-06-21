# Gunakan image Python resmi
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Salin semua file ke dalam image
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set Streamlit port
ENV PORT 8080

# Jalankan Streamlit
CMD streamlit run app.py --server.port=$PORT --server.enableCORS=false
