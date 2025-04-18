<<<<<<< HEAD
# Perficient Chatbot
=======
CHARM Assistant
====

### Getting started
1. Copy repo and navigate to `ai_module` dir
2. Install dependencies by running the following command:
```bash
pip install -r requirements.txt
```
3. Set up environment variables:
   - Copy `.env.example` to `.env` and fill in your credentials
   - Required variables include:
     - `AZURE_DEVOPS_TOKEN`: Your Azure DevOps personal access token
     - `AZURE_DEVOPS_ORG`: Your organization ID
     - `OPENAI_API_KEY`: Your OpenAI API key
4. Run test mode to try it out:
```bash
streamlit run src/demo.py
```
5. If running backend, go to parent folder and run:
```bash
uvicorn backend.api.main:app
```
>>>>>>> faecc72 (migrate from school repo)
