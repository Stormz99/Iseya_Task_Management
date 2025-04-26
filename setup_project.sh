#!/bin/bash

#  Project Name
PROJECT_NAME="Iseya"

# Check if Python3 is Installed
check_python () {
    if ! command -v python3 &>/dev/null; then
        echo "⚠️ Python 3 is not installed. Installing..."
        brew install python3
    else
        echo "✅ Python 3 is installed"
    fi
}

# 🛠️ Setup Virtual Environment
setup_virtualenv () {
    if [ ! -d "venv" ]; then
        echo "🔧 Creating virtual environment..."
        python3 -m venv venv
    fi

    # Activate virtual environment
    source venv/bin/activate
    echo " Virtual environment activated"
}

# 🛠️ Create Project Directory Structure
create_project_structure () {
    echo "📂 Creating project structure..."
    mkdir -p $PROJECT_NAME/{app/{models,routes,schemas,services,utils,auth,docs,core},alembic/versions}
    cd $PROJECT_NAME
}

# 🛠️ Create Core Files
create_core_files () {
    touch app/__init__.py \
          app/main.py \
          app/config.py \
          app/models/task.py \
          app/routes/task_routes.py \
          app/schemas/task_schemas.py \
          app/services/task_service.py \
          app/utils/error_handling.py \
          app/auth/auth_handler.py \
          app/auth/auth_bearer.py \
          app/core/security.py \
          .env .gitignore requirements.txt README.md alembic.ini
}

# 🛠️ Generate .env with PostgreSQL Connection String
generate_env_file () {
SECRET_KEY=$(openssl rand -hex 32)
cat <<EOL > .env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=iseyadb
DB_USER=abiodun
DB_PASSWORD=12345

DATABASE_URL=postgresql+asyncpg://abiodun:12345@localhost:5432/iseyadb

# JWT Configuration
SECRET_KEY=$SECRET_KEY
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
EOL
}

# ✅ Install FastAPI, Alembic, Asyncpg and Dependencies
install_dependencies () {
cat <<EOL > requirements.txt
fastapi[all]
uvicorn
pydantic
sqlalchemy
asyncpg
alembic
bcrypt
python-dotenv
python-jose[cryptography]
passlib[bcrypt]
EOL

    echo " Installing dependencies..."
    pip install -r requirements.txt
}

# Initialize Alembic
initialize_alembic () {
    echo "⚡ Initializing Alembic..."
    alembic init alembic
}

# 🛠️ Replace alembic.ini with correct database URL
update_alembic_ini () {
    sed -i '' "s|# sqlalchemy.url = driver://user:pass@localhost/dbname|sqlalchemy.url = postgresql+asyncpg://abiodun:12345@localhost:5432/iseyadb|" alembic.ini
}

# Run All Functions in Order
check_python
setup_virtualenv
create_project_structure
create_core_files
generate_env_file
install_dependencies
initialize_alembic
update_alembic_ini

echo " Project Setup Complete! Ready to Build FastAPI Task Manager Iseya 🔥"
