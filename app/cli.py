import typer
from app.database import create_db_and_tables, get_session, drop_all
from app.models import User
from fastapi import Depends
from sqlmodel import select
from sqlalchemy.exc import IntegrityError

cli = typer.Typer()

@cli.command()
def initialize():
    with get_session() as db: # Get a connection to the database
        drop_all() # delete all tables
        create_db_and_tables() #recreate all tables
        bob = User('bob', 'bob@mail.com', 'bobpass') # Create a new user (in memory)
        db.add(bob) # Tell the database about this new data
        db.commit() # Tell the database persist the data
        db.refresh(bob) # Update the user (we use this to get the ID from the db)
        print("Database Initialized")

@cli.command()
def get_user(username:str):
    # The code for task 5.1 goes here. Once implemented, remove the line below that says "pass"
    pass

@cli.command()
def get_all_users():
    # The code for task 5.2 goes here. Once implemented, remove the line below that says "pass"
    pass


@cli.command()
def change_email(username: str, new_email:str):
    # The code for task 6 goes here. Once implemented, remove the line below that says "pass"
    pass

@cli.command()
def create_user(username: str, email:str, password: str):
    # The code for task 7 goes here. Once implemented, remove the line below that says "pass"
    pass

@cli.command()
def delete_user(username: str):
    # The code for task 8 goes here. Once implemented, remove the line below that says "pass"
    pass


if __name__ == "__main__":
    cli()
import typer
from app.database import create_db_and_tables, get_session, drop_all
from app.models import User
from fastapi import Depends
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_

cli = typer.Typer()

@cli.command()
def initialize():
    with get_session() as db: # Get a connection to the database
        drop_all() # delete all tables
        create_db_and_tables() #recreate all tables
        bob = User('bob', 'bob@mail.com', 'bobpass') # Create a new user (in memory)
        db.add(bob) # Tell the database about this new data
        db.commit() # Tell the database persist the data
        db.refresh(bob) # Update the user (we use this to get the ID from the db)
        print("Database Initialized")

@cli.command()
def get_user(username:str = typer.Argument(..., help="Exact username of the user to retrieve.")):
    # The code for task 5.1 goes here. Once implemented, remove the line below that says "pass"
    with get_session() as db:
        user = db.exec(select(User).where(User.username == username)).first()
        if not user:
            print(f"{username} not found!")
            return
        print(user)

@cli.command()
def get_all_users():
    # The code for task 5.2 goes here. Once implemented, remove the line below that says "pass"
    with get_session() as db:
        users = db.exec(select(User)).all()
        if not users:
            print("No users found")
            return
        for user in users:
            print(user)


@cli.command()
def change_email(
    username: str = typer.Argument(..., help="Username of the user to update."),
    new_email:str = typer.Argument(..., help="New email address to set.")
):
    # The code for task 6 goes here. Once implemented, remove the line below that says "pass"
    with get_session() as db:
        user = db.exec(select(User).where(User.username == username)).first()
        if not user:
            print(f"{username} not found! Unable to update email.")
            return

        user.email = new_email
        db.add(user)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            print("Email already taken!")
            return

        print(f"Updated {user.username}'s email to {user.email}")

@cli.command()
def create_user(
    username: str = typer.Argument(..., help="Unique username for the new user."),
    email:str = typer.Argument(..., help="Unique email for the new user."),
    password: str = typer.Argument(..., help="Password for the new user (will be hashed).")
):
    # The code for task 7 goes here. Once implemented, remove the line below that says "pass"
    with get_session() as db:
        newuser = User(username, email, password)
        try:
            db.add(newuser)
            db.commit()
            db.refresh(newuser)
        except IntegrityError:
            db.rollback()
            print("Username or email already taken!")
            return

        print(newuser)

@cli.command()
def delete_user(username: str = typer.Argument(..., help="Username of the user to delete.")):
    # The code for task 8 goes here. Once implemented, remove the line below that says "pass"
    with get_session() as db:
        user = db.exec(select(User).where(User.username == username)).first()
        if not user:
            print(f"{username} not found! Unable to delete user.")
            return
        db.delete(user)
        db.commit()
        print(f"{username} deleted")


@cli.command()
def search_users(query: str = typer.Argument(..., help="Partial text to match in username OR email.")):
    with get_session() as db:
        q = f"%{query}%"
        users = db.exec(
            select(User).where(or_(User.username.like(q), User.email.like(q)))
        ).all()

        if not users:
            print("No users found")
            return

        for user in users:
            print(user)


@cli.command()
def list_users(
    limit: int = typer.Argument(10, help="How many users to return (default: 10)."),
    offset: int = typer.Argument(0, help="How many users to skip first (default: 0).")
):
    if limit < 1:
        print("limit must be at least 1")
        return
    if offset < 0:
        print("offset must be 0 or greater")
        return

    with get_session() as db:
        users = db.exec(select(User).offset(offset).limit(limit)).all()

        if not users:
            print("No users found")
            return

        for user in users:
            print(user)


if __name__ == "__main__":
    cli()