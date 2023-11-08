from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import database, Revista
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]  

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class RevistaCreate(BaseModel):
    link: str
    image: str
    titulo: str

@app.post("/upload/")
async def upload_revista(revista: RevistaCreate):
    query = Revista.insert().values(
        link=revista.link,
        image=revista.image,
        titulo=revista.titulo
    )
    revista_id = await database.execute(query)
    return {"message": "Revista guardada exitosamente", "revista_id": revista_id}

@app.get("/revistas/")
async def get_revistas():
    query = Revista.select()
    revistas = await database.fetch_all(query)
    revistas_list = [dict(rv) for rv in revistas]
    return revistas_list

@app.delete("/revistas/{revista_id}")
async def delete_revista(revista_id: int):
    query = Revista.delete().where(Revista.c.id == revista_id)
    result = await database.execute(query)

    if result == 0:
        raise HTTPException(status_code=404, detail="Revista no encontrada")

    return {"message": f"Revista con ID {revista_id} eliminada"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

