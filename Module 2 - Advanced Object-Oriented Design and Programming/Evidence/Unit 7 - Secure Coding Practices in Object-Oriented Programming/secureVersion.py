# Unit 7 - Secure Coding Practices in Object-Oriented Programming
# This code demonstrates secure coding practices by implementing password hashing and salting using bcrypt.
# It also includes a simple rate-limiting mechanism to prevent brute-force attacks.

# Importing necessary libraries for password hashing and rate limiting
import bcrypt
import time
from collections import defaultdict

# Class to represent a user with a hashed password
class User:
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

# Class to handle authentication and user management
class AuthenticationSystem:
    def __init__(self, max_attempts=5, lockout_time=60):
        self.users = {}
        self.failed_attempts = defaultdict(list)
        self.max_attempts = max_attempts
        self.lockout_time = lockout_time
        
    def _is_rate_limited(self, username):
        now = time.time()
        self.failed_attempts[username] = [t for t in self.failed_attempts[username] if now - t < self.lockout_time]
        return len(self.failed_attempts[username]) >= self.max_attempts 
    
    # Method to add a new user with password hashing and validation
    def _validate_password_policy(self, password):
       if len(password) < 8:
           return False, "Password must be at least 8 characters long."
       if not any(char.isupper() for char in password):
           return False, "Password must contain at least one uppercase letter."
       if not any(char.islower() for char in password):
           return False, "Password must contain at least one lowercase letter."
       if not any(char.isdigit() for char in password):
           return False, "Password must contain at least one digit."
       return True, "Password is valid."
    
    # Method to add a new user with password hashing and validation 
    def add_user(self, username, password):
        if not username or not isinstance(username, str):
            raise ValueError("Invalid username")
        valid, message = self._validate_password_policy(password)
        if not valid:
            raise ValueError(message)
        if username in self.users:
            raise ValueError("Username already exists")
        # Hash the password with a unique salt using bcrypt
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) 
        self.users[username] = User(username, password_hash)  

    # Method to authenticate a user with rate limiting
    def authenticate(self, username, password):
        if self._is_rate_limited(username):
            print("Too many failed attempts. Please try again later.")
            return False
        user = self.users.get(username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash):
            return True
        self.failed_attempts[username].append(time.time())
        return False    

# Example usage
if __name__ == "__main__":
    auth_system = AuthenticationSystem()
    try:
        auth_system.add_user("admin", "Admin123")  # Strong password
        auth_system.add_user("user1", "User1234")  # Strong password
    except ValueError as e:
        print(e)

    # Simulate authentication attempts
    print(auth_system.authenticate("admin", "Admin123"))  # True
    print(auth_system.authenticate("admin", "WrongPassword"))  # False
    print(auth_system.authenticate("admin", "WrongPassword"))  # False
    print(auth_system.authenticate("admin", "WrongPassword"))  # False
    print(auth_system.authenticate("admin", "WrongPassword"))  # False
    print(auth_system.authenticate("admin", "WrongPassword"))  # Too many attempts, should


                 
        
        
    
    