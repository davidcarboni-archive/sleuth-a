import logging
import sleuth

from flask import Flask
import requests
import os

import b3


app = Flask("Service-a")

port = int(os.getenv("PORT", "8001"))
service_b = os.getenv("SERVICE_B", "http://localhost:8002/")


@app.route('/')
def service():
    log = logging.getLogger(app.name)
    log.setLevel(logging.INFO)
    log.info(app.name + " has been called.")
    log.info("B3 span values: " + str(b3.values()))

    with b3.SubSpan() as headers:
        log.info("B3 subspan values: " + str(b3.values()))
        log.debug("Making a request to service B")
        r = requests.get(service_b, headers=headers)
        log.debug("Service B said: " + str(r.text))

    return "Service call succeeded (" + app.name + ")"


if __name__ == "__main__":

    app.before_request(b3.start_span)
    app.after_request(b3.end_span)
    app.run(
        host="0.0.0.0",
        port=int(port),
        debug=True,
        threaded=True
    )
