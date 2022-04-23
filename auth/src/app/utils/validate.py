def validate(data, regex):
    """Custom Validator"""
    return True if re.match(regex, data) else False


def validate_password(password: str):
    """Password Validator"""
    reg = r"\b^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$\b"
    return validate(password, reg)


def validate_email(email: str):
    """Email Validator"""
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return validate(email, regex)


def validate_login(login: str):
    """Login Validator"""
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return validate(login, regex)


def validate_login_and_password(login, password):
    """login and Password Validator"""
    if not (login and password):
        return {
            'login': 'login is required',
            'password': 'Password is required'
        }
    if not validate_login(login):
        return {
            'login': 'login is invalid'
        }
    if not validate_password(password):
        return {
            'password': 'Password is invalid, Should be atleast 8 characters with \
                upper and lower case letters, numbers and special characters'
        }
    return True


def validate_login_and_password_email(login, password):
    """login and Password Validator"""
    if not (login and password):
        return {
            'login': 'login is required',
            'password': 'Password is required'
        }
    if not validate_login(login):
        return {
            'login': 'login is invalid'
        }
    if not validate_password(password):
        return {
            'password': 'Password is invalid, Should be atleast 8 characters with \
                upper and lower case letters, numbers and special characters'
        }
    return True

