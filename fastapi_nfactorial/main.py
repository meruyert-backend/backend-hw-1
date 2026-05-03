from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/{num}")
def nfactorial(num: int):
    if num < 0:
        raise HTTPException(status_code=400, detail="Number must be non-negative")

    result = 1
    for i in range(1, num + 1):
        result *= i

    return {"nfactorial": result}
