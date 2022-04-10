from website import create_app
from logger import Logger

logger = Logger()

app = create_app()


if __name__ == "__main__":
    app.run()
