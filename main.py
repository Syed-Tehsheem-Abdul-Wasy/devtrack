def main():
    print("Hello from dev-track!")


if __name__ == "__main__":
    main()



#register router in main.py
from app.routers import auth

app.include_router(auth.router)