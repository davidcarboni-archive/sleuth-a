import logging
import sleuth

from flask import Flask
import requests

import b3


app = Flask("Service-a")


@app.route('/')
def service():
    logger.info(app.name + " has been called.")

    with b3.SubSpan() as headers:
        logger.debug("Making a request to service B")
        r = requests.get("http://localhost:8002/", headers=headers)
        logger.debug("Service B said: " + str(r.text))

    return "Service call succeeded (" + app.name + ")"


if __name__ == "__main__":

    logging.getLogger().setLevel(logging.INFO)
    logger = logging.getLogger(__name__)
    logger.debug("Starting " + app.name)

    app.before_request(b3.start_span)
    app.after_request(b3.end_span)
    app.run(
        host="0.0.0.0",
        port=int(8001),
        debug=True,
        threaded=True
    )
