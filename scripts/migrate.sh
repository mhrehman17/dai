#!/bin/bash

# This script automates the database migration for the decentralized AI system.
# It utilizes Alembic to manage migrations, ensuring the database is up-to-date with the latest schema changes.

# Define environment variables for database URL
DB_URL=${DB_URL:-"sqlite:///./dai_project.db"}
MIGRATIONS_DIR="migrations"

# Check if Alembic is installed
if ! command -v alembic &> /dev/null
then
    echo "Alembic could not be found. Please make sure all dependencies are installed by running:"
    echo "pip install -r requirements.txt"
    exit 1
fi

# Initialize Alembic migration folder if it does not exist
if [ ! -d "$MIGRATIONS_DIR" ]; then
    alembic init "$MIGRATIONS_DIR"
    echo "Alembic migration directory initialized: $MIGRATIONS_DIR"
fi

# Update Alembic configuration to include the database URL
sed -i "s|# sqlalchemy.url = driver://user:pass@localhost/dbname|sqlalchemy.url = $DB_URL|" "$MIGRATIONS_DIR/alembic.ini"

# Generate a new migration script
alembic revision --autogenerate -m "Auto migration"
if [ $? -eq 0 ]; then
    echo "Migration script generated successfully."
else
    echo "Error: Failed to generate migration script."
    exit 1
fi

# Apply the migration to the database
alembic upgrade head
if [ $? -eq 0 ]; then
    echo "Database migrated successfully."
else
    echo "Error: Failed to apply migration."
    exit 1
fi

# Completion message
echo "Migration completed successfully. Database is up-to-date."
