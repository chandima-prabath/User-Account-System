# User Account System Module

The User Account System module is a Python class that provides methods to manage user accounts for a server. The module uses SQLite as the database backend to store user account information.

## Installation

The User Account System module requires the sqlite3 module and the bcrypt module. You can install these modules by running the following command:

```
pip install -r requirements.txt
```

## Usage

To use the User Account System module, import it into your Python code and create an instance of the UserAccountSystem class. You need to provide the filename of the SQLite database to use for storing user accounts. If the database file does not exist, it will be created automatically.

```python
from user_account_system import UserAccountSystem

db_file = 'users.db'
uas = UserAccountSystem(db_file)
```

### Registering a new user

To register a new user, call the register_user method with the username and password as arguments. The password will be hashed using bcrypt before being stored in the database.

```python
username = 'johndoe'
password = 'secret123'
if uas.register_user(username, password):
    print('User {} registered successfully.'.format(username))
else:
    print('User {} already exists.'.format(username))
```

### Authenticating a user

To authenticate a user, call the authenticate_user method with the username and password as arguments. The password will be hashed using bcrypt and compared to the stored hash in the database.

```python
username = 'johndoe'
password = 'secret123'
if uas.authenticate_user(username, password):
    print('User {} authenticated successfully.'.format(username))
else:
    print('Authentication failed for user {}.'.format(username))
```

### Deleting a user

To delete a user, call the delete_user method with the username as argument.

```python
username = 'johndoe'
uas.delete_user(username)
print('User {} deleted successfully.'.format(username))
```

### Changing a user's password

To change a user's password, call the change_password method with the username and new password as arguments. The new password will be hashed using bcrypt before being stored in the database.

```python
username = 'janedoe'
new_password = 'newsecret456'
uas.change_password(username, new_password)
print('Password for user {} changed successfully.'.format(username))
```

### Listing all users

To list all registered users, call the list_users method. The method returns a list of tuples containing the usernames.

```python
users = uas.list_users()
for user in users:
    print(user[0])
```

## New Changes

### Password Hashing Algorithm

The User Account System module now uses bcrypt for secure password hashing instead of SHA-256. Bcrypt is a widely-used password hashing algorithm that is designed to be slow and computationally expensive, making it more difficult for attackers to crack passwords.

### Password Complexity Validation

The module now enforces a minimum password complexity policy. Passwords must be at least 8 characters long and must contain at least one uppercase letter, one lowercase letter, and one digit.

### Password Reset Functionality
A new method, reset_password, has been added to the UserAccountSystem class. This method allows users to reset their passwords if they have forgotten them. When called, the method generates a new random password for the user, which is then emailed to the user's registered email address.

## Security Considerations

When using the User Account System module, it is important to properly secure your database and implement appropriate password policies to prevent attacks such as SQL injection and password cracking. Here are some best practices to follow:

* Use a strong and unique passphrase to encrypt your database file.
* Use prepared statements when executing SQL queries to prevent SQL injection attacks.
* Enforce strong password policies, such as minimum length and complexity requirements, and encourage users to choose strong and unique passwords.
* Use rate limiting or account lockout mechanisms to prevent brute-force attacks against user accounts.
* Regularly backup your database file and monitor for any suspicious activity.

## Conclusion

The User Account System module provides a simple and easy-to-use interface for managing user accounts in your server applications. It uses SQLite as the database backend and bcrypt for secure password hashing. The module provides methods for registering new users, authenticating existing users, deleting user accounts, changing user passwords, and listing all registered users. By following best practices for database security and password policies, you can ensure the security and integrity of your user account system.