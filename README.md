# Flood Mapping Project

Container-ready Sentinel-1 flood mapping application using Google Earth Engine.

## Run locally

```bash
cd Flood_Mapping_Project
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export EE_PROJECT_ID=your-google-cloud-project-id
earthengine authenticate
PYTHONPATH=src python -m api
```

Open http://localhost:8086. The API exposes `GET /health` and `POST /api/run`.

## Run with Docker

```bash
docker build -t flood-mapping .
docker run --rm -p 8086:8086 \
  -e EE_PROJECT_ID=your-project-id \
  -v "$HOME/.config/earthengine:/root/.config/earthengine:ro" \
  flood-mapping
```

For hosted deployment, use Application Default Credentials or a service account
through the platform secret manager; never commit credential files.

## Deploy to Vercel

Use `Flood_Mapping_Project` as the Vercel project root. The included
`pyproject.toml` explicitly points Vercel to `src.api:app`.

Add these Vercel environment variables:

- `EE_PROJECT_ID`: a Google Cloud project with Earth Engine enabled
- `EE_SERVICE_ACCOUNT_JSON`: the complete service-account JSON key

The local `earthengine authenticate` flow is not available inside Vercel.
