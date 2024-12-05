import os
import json
import datetime
import uvicorn


from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, field_validator, model_validator, Field, EmailStr
from schwifty import IBAN
from sepaxml import SepaDD
from typing_extensions import Self

app = FastAPI()


class Donee(BaseModel):
    name: str
    keyword: str


class Account(BaseModel):
    name: str
    iban: str
    agreement: bool

    @field_validator("iban")
    @classmethod
    def valide_iban(cls, v: str) -> str:
        if not IBAN(v, allow_invalid=True).is_valid:
            raise ValueError("Das ist keine gültige IBAN")
        return IBAN(v).formatted


class Info(BaseModel):
    name: str
    email: EmailStr

    amount: int = Field(gt=0)
    account: Account
    timestamp: str = str(datetime.datetime.now())
    donee: Donee

    def create_filename(self):
        return f"{self.name}_{self.account.iban}_{self.donee.name}.json"

    @model_validator(mode="after")
    def check_unique(self) -> Self:
        a = f"{self.name}_{self.account.iban}.json"
        if f"{a}" in os.listdir("./uploads"):
            raise ValueError(
                "Diese Spende scheint genau so schon zu existieren. Bei Fragen wende dich an: vorstand@queer-lexikon.net"
            )
        return self


@app.get("/")
async def root():
    return RedirectResponse("static/index.html")


@app.post("/generate")
async def generate(info: Info):
    possible_filename = info.create_filename()
    if possible_filename not in os.listdir("./uploads"):
        print(possible_filename)
        print(os.listdir("./uploads"))
        serializable_info = jsonable_encoder(info)
        with open(f"./uploads/{possible_filename}", "x") as fp:
            json.dump(serializable_info, fp, indent=4)
        return {"success": True}

    return {"success": False, "already_exists": True}


app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
