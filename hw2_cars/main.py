from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello"}


# cars
cars = []

for i in range(1, 21):
    cars.append({
        "id": i,
        "name": f"Car {i}",
        "year": "2020"
    })

@app.get("/cars")
def get_cars(page: int = 1, limit: int = 10):
    start = (page - 1) * limit
    end = start + limit
    return cars[start:end]


@app.get("/cars/{id}")
def get_cars_by_id(id: int):
    for car in cars:
        if car["id"] == id:
            return car
    raise HTTPException(status_code=404, detail="Not found")



# users
users = []

for i in range(1, 21):
    users.append({
        "id": i,
        "email": f"user{i}@test.com",
        "first_name": f"Name{i}",
        "last_name": f"Surname{i}",
        "username": f"user_{i}"
    })



@app.get("/users/{id}", response_class=HTMLResponse)
def get_users_by_id(id: int):
    for user in users:
        if user["id"] == id:
            return f"""
            <h1>{user['first_name']} {user['last_name']}</h1>
            <p>Email: {user['email']}</p>
            <p>Username: {user['username']}</p>
            """
    raise HTTPException(status_code=404, detail="Not found")


@app.get("/users", response_class=HTMLResponse)
def get_users(page: int = 1, limit: int = 10):
    start = (page - 1) * limit
    end = start + limit
    paginated_users = users[start:end]

    html = "<h1>Users</h1>"
    html += "<table border='1'>"

    for user in paginated_users:
        html += f"""
        <tr>
            <td>{user['username']}</td>
            <td>
                <a href="/users/{user['id']}">
                    {user['first_name']} {user['last_name']}
                </a>
            </td>
        </tr>
        """

    html += "</table><br>"

    # Previous button
    if page > 1:
        html += f'<a href="/users?page={page-1}&limit={limit}">Previous</a> '

    # Next button
    if end < len(users):
        html += f'<a href="/users?page={page+1}&limit={limit}">Next</a>'

    return html
