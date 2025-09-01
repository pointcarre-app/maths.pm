# FastAPI app with uvicorn
web: PYTHONPATH=/app uvicorn src.app:app --workers 2 --timeout-keep-alive 60 --host 0.0.0.0 --port $PORT --proxy-headers

# Health check endpoint
# healthcheck: curl -f http://localhost:$PORT/api/health || exit 1
