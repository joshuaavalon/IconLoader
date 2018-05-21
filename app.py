from logging import getLogger
from pathlib import Path

from flask import Flask, send_from_directory
from requests.exceptions import SSLError

from icon_loader import utils

app = Flask(__name__)

logger = getLogger(__name__)


@app.route("/<domain>/icon.png")
def get_icon(domain):
    # noinspection PyBroadException
    try:
        cache_dir = Path(app.config["CACHE_FOLDER"])
        icon = cache_dir.joinpath(f"{domain}.png")
        if icon.exists():
            return send_from_directory(cache_dir, f"{domain}.png")
        try:
            utils.download_favicon(f"https://{domain}", icon)
        except SSLError:
            utils.download_favicon(f"http://{domain}", icon)
        if icon.exists():
            return send_from_directory(cache_dir, f"{domain}.png")
    except Exception:
        logger.exception("Get icon fail", exc_info=1)
    return send_from_directory(".", filename="icon.png")


def main():
    app.config.from_object("icon_loader.config")
    app.config.from_envvar("OVERRIDE_CONFIG", silent=True)
    app.run()


if __name__ == "__main__":
    main()
