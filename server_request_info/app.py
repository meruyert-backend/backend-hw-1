def application(environ, start_response):
    method = environ.get("REQUEST_METHOD")
    path = environ.get("PATH_INFO")
    protocol = environ.get("SERVER_PROTOCOL")

    if path == "/info":
        if method == "GET":
            status = "200 OK"

            response_text = (
                f"Method: {method}\n"
                f"URL: {path}\n"
                f"Protocol: {protocol}"
            )

            response_body = response_text.encode("utf-8")
        else:
            status = "405 Method Not Allowed"
            response_body = b"Method Not Allowed"
    else:
        status = "404 Not Found"
        response_body = b"Not Found"

    headers = [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(response_body)))
    ]

    start_response(status, headers)
    return [response_body]