#!/bin/bash

# This script resets the database for the decentralized AI system by dropping all tables and re-applying migrations.
# WARNING: This script will remove all data from the database. Use with caution!

# Define environment variables for the database URL
DB_URL=${DB_URL:-"sqlite:///./dai_project.db"}
MIGRATIONS_DIR="migrations"

# Function to confirm action
echo "WARNING: This action will delete all data in the database and reset its structure. Do you wish to continue? (yes/no)"
read confirmation
if [ "$confirmation" != "yes" ]; then
    echo "Database reset operation canceled."
    exit 0
fi

# Check if Alembic is installed
if ! command -v alembic &> /dev/null
then
    echo "Alembic could not be found. Please make sure all dependencies are installed by running:"
    echo "pip install -r requirements.txt"
    exit 1
fi

# Drop the existing database tables
python -c "from sqlalchemy import create_engine; engine = create_engine('$DB_URL'); engine.execute('DROP TABLE IF EXISTS alembic_version CASCADE'); engine.execute('DROP SCHEMA public CASCADE'); engine.execute('CREATE SCHEMA public'); print('Database reset successfully.')"
if [ $? -eq 0 ]; then
    echo "Database tables dropped successfully."
else
    echo "Error: Failed to drop database tables."
    exit 1
fi

# Re-apply migrations
if [ -d "$MIGRATIONS_DIR" ]; then
    alembic upgrade head
    if [ $? -eq 0 ]; then
        echo "Database migrations applied successfully."
    else
        echo "Error: Failed to apply database migrations."
        exit 1
    fi
else
    echo "Error: Migrations directory not found. Please initialize Alembic migrations first."
    exit 1
fi

# Completion message
echo "Database reset and migration completed successfully. The database is now up-to-date."
