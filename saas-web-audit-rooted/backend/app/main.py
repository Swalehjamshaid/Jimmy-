from fastapi import FastAPI
app=FastAPI()
@app.get("/api/v1/healthz")
def h():return{"status":"ok"}