from user_account_system import UserAccountSystem

# Create an instance of the UserAccountSystem class and connect to the database
uas = UserAccountSystem('user_database.db')

# Register a new user
uas.register_user('john_doe', 'password123')

# Authenticate a user
if uas.authenticate_user('john_doe', 'password123'):
    print('Authentication successful')
else:
    print('Authentication failed')

# Change a user's password
uas.change_password('john_doe', 'new_password')

# List all users in the system
users = uas.list_users()
print('List of users:')
for user in users:
    print(user[0])
    
# Delete a user from the system
uas.delete_user('john_doe')

# Register a new user with an existing username (should return False)
if uas.register_user('john_doe', 'password123'):
    print('Registration successful')
else:
    print('Registration failed')
