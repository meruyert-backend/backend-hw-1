def application(environ, start_response):
    method = environ.get("REQUEST_METHOD")
    path = environ.get("PATH_INFO")

    if method == "GET" and path == "/ping":
        status = "200 OK"
        response_body = b"pong"
    else:
        status = "404 Not Found"
        response_body = b"Not Found"

    headers = [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(response_body)))
    ]

    start_response(status, headers)
    return [response_body]
