fakestore/
│
├── app/                           # Core application logic
│   ├── crud/                      # Add/Update/Delete operations
│   │   ├── add.py
│   │   ├── update.py
│   │   └── delete.py
│   │
│   ├── extract/                   # API data extraction logic
│   │   ├── tables.py              # API endpoints for each table
│   │   └── fetchers/              # Separate fetchers for each resource
│   │       ├── products.py
│   │       ├── users.py
│   │       └── carts.py
│   │
│   └── sync/                      # Incremental load logic
│       └── sync_engine.py
│
├── config/                        # Configuration files
│   ├── config.py                  # Python config parser
│   ├── config.json                # Custom settings (like polling time, etc.)
│   └── .env                       # Environment variables (DB credentials)
│
├── dashboard/                     # Flask-based CRUD UI
│   ├── web.py                     # Dynamic CRUD API (products/users/carts)
│   └── model_mapper.py           # Table name -> SQLAlchemy model map
│
├── db/                            # Database handling
│   ├── models.py                  # SQLAlchemy ORM models
│   └── engine.py                  # SQL Server connection setup
│
├── logs/                          # Log files for sync, errors, etc.
│   └── sync.log
│
├── main.py                        # Main entrypoint: Infinite sync loop
├── requirements.txt               # Python dependencies
├── docker-compose.yml             # Docker setup for app + SQL Server
├── Dockerfile                     # Docker image for the Python app
└── setup.sh                       # Shell script to bootstrap everything

