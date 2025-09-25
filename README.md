# AutoChord API 🎶

A FastAPI service that performs chord recognition on audio files using 
the [AutoChord](https://pypi.org/project/autochord/) model.  
Designed for accessibility, automation, and integration with no‑code 
platforms like Base44.

---

## 🚀 Features
- Upload a `.wav` file and get back chord predictions in JSON.
- Runs in **model‑only mode** (no Vamp plugin required).
- Containerized with Docker for easy deployment on Railway or Render.
- Swagger UI available at `/docs`.

---

## 🛠️ Local Development

Clone the repo and install dependencies:

```bash
git clone https://github.com/Shaigabe/autochord-api.git
cd autochord-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

