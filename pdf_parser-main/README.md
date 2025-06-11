# Service Bulletin Parser API

This repository hosts a FastAPI service that parses uploaded engine service bulletin PDFs.

## Files

- **app.py**: FastAPI application  
- **requirements.txt**: Python dependencies  
- **.gitignore**: ignores caches/logs  

## Usage

1. **Deploy** on Railway (or any host):  
   - Set start command to  
     ```
     uvicorn app:app --host 0.0.0.0 --port $PORT
     ```  
   - Add `OPENAI_API_KEY` in environment variables if you extend with LLM calls.

2. **Local run** (for testing):  
   ```bash
   pip install -r requirements.txt
   uvicorn app:app --reload
   ```

3. **API endpoint**  
   ```
   POST /parse
   Form field: file (PDF)
   Response JSON: { filename, engine, text_preview }
   ```

## Next Steps

- Integrate OpenAI extraction in place of `text_preview`  
- Lock down CORS origins  
- Add tests & CI (GitHub Actions)
