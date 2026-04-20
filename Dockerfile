FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy everything
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports
EXPOSE 8000
EXPOSE 8501

# Run API + Streamlit properly
CMD ["sh", "-c", "uvicorn src.api.app:app --host 0.0.0.0 --port 8000 & exec streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0"]

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
CMD curl -f http://localhost:8000/ || exit 1