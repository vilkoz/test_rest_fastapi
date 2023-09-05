# Notes about task

The package `encode/databases` was chosen as db engine only to quickly demonstrate async db interaction (as async endpoints were required by test project description), I would not go without ORM (with sqlalchemy core) on the real project.

On my opinion, migrations, code documentation and in-depth covered swagger documentation are way out of the scope of this "3 hour" task.

# Run project with docker and docker compose

Requirements: `docker (23.0.1)`

Create db tables:
```
docker compose run -it backend python3 main.py
```

Run the service:
```
docker compose up --build -d
```

Open in browser `http://localhost:8080/docs`

