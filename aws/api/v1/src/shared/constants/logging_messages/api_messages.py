class ApiMessages:
    class Error:
        pass

    class Info:
        RESPONSE_CREATED = "Response created with status: {status}, message: {message}"
        REDIRECT_CREATED = "Redirect created with status: {status}, location: {location}"
