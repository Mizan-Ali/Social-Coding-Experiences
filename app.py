from logger import Logger
from website import create_app

logger = Logger()

app = create_app()


if __name__ == "__main__":
    app.run()
