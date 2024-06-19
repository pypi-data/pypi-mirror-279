import time
from typing import Mapping, Optional, Sequence

PORT = 8909
HOST = "127.0.0.1"

if __name__ == "__main__":
    from flask import Flask, jsonify

    app = Flask(__name__)

    @app.route("/")
    def home():
        return jsonify({"library": "flask"})

    app.run(port=PORT, host=HOST)


# We have the option to not inherit from the OtelTest base class, in which case we name our class so it contains
# "OtelTest". This has the benefit of not requiring a dependency on oteltest in the script's environment.
class FlaskOtelTest:
    def environment_variables(self) -> Mapping[str, str]:
        return {}

    def requirements(self) -> Sequence[str]:
        return (
            "opentelemetry-distro",
            "opentelemetry-exporter-otlp-proto-grpc",
            "opentelemetry-instrumentation-flask",
            "flask==2.3.3",
            "jsonify",
        )

    def wrapper_command(self) -> str:
        return "opentelemetry-instrument"

    def on_start(self) -> Optional[float]:
        import http.client

        # Todo: replace this sleep with a liveness check!
        time.sleep(10)

        conn = http.client.HTTPConnection(HOST, PORT)
        conn.request("GET", "/")
        print("response:", conn.getresponse().read().decode())
        conn.close()

        # The return value of on_script_start() tells oteltest the number of seconds to wait for the script to
        # finish. In this case, we indicate 30 (seconds), which, once elapsed, will cause the script to be terminated,
        # if it's still running. If we return `None` then the script will run indefinitely.
        return 30

    def on_stop(self, tel, stdout: str, stderr: str, returncode: int) -> None:
        # local import so oteltest is not needed for parsing this script
        from oteltest import telemetry

        span = telemetry.first_span(tel)
        assert telemetry.span_attribute_by_name(span, "http.method") == "GET"
