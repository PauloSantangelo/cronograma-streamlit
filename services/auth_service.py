def authenticate(username, password):
    valid_users = {"vibeadmin": "batman123"}
    return valid_users.get(username) == password
