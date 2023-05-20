# lecturers-pokedex-backend

URL: https://pokedex-uijzr7bcfa-ew.a.run.app

## `GET /users`

```JSON
[
    {
        "_id": "QjY9ErN5q0IOf720bel6",
        "name": "Doktor A",
    },
    {
        "_id": "mSt40X3ZPuEe5yCq2s2f",
        "name": "Doktor B"
    }
]
```

## `GET /users/{id}`

```JSON
{
    "_id": "QjY9ErN5q0IOf720bel6",
    "name": "Doktor A",
    "photo": "https://storage.googleapis.com/pokedex_photos/30f8f894-ed8f-11ed-8473-2cf05de1978c.jpeg",
    "dominantColor": "#bdd1db",
}
```

## `POST /users/`

Content-type: multipart/form-data
- photo: photo in JPEG format
- data: other fields as JSON
```JSON
{
    "name": "Doktor A"
}
```

## `PUT /users/{id}`
same as POST /users/:id

## `DELETE /users/{id}`