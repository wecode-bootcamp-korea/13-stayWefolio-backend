def message(domain, uidb64, token):
    return f"Please confirm email from this address. \n\n URL: http://{domain}/user/{uidb64}/{token}"