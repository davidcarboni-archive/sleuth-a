import logging
import sleuth

from flask import Flask
import requests
import os

import b3


app = Flask("Service-a")
log = logging.getLogger(app.name)
log.setLevel(logging.INFO)

port = int(os.getenv("PORT", "8001"))
service_b = os.getenv("SERVICE_B", "http://localhost:8002/")


@app.route('/')
def service():
    log.info(app.name + " has been called.")

    with b3.SubSpan() as headers:
        log.debug("Making a request to service B")
        r = requests.get(service_b, headers=headers)
        log.debug("Service B said: " + str(r.text))

    return "Service call succeeded (" + app.name + ")"


if __name__ == "__main__":

    log.debug("Starting " + app.name)

    app.before_request(b3.start_span)
    app.after_request(b3.end_span)
    app.run(
        host="0.0.0.0",
        port=int(port),
        debug=True,
        threaded=True
    )
