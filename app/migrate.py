import subprocess
import sys


def run_command(command):
    """Run a system command."""
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Error running command: {command}")
        print(result.stderr)
        sys.exit(result.returncode)
    print(result.stdout)


def create_migration(message):
    """Create a new migration with the specified message."""
    print("Creating a new migration...")
    run_command(f"alembic revision --autogenerate -m \"{message}\"")


def apply_migration():
    """Apply the latest migration to the database."""
    print("Applying migration...")
    run_command("alembic upgrade head")


# def main():
#     if len(sys.argv) < 2:
#         print("Usage: python migrate.py <migration_message>")
#         sys.exit(1)

#     migration_message = sys.argv[1]
#     create_migration(migration_message)
#     apply_migration()
#     print("Migration complete!")


# if __name__ == "__main__":
#     main()
