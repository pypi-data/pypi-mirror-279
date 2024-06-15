#Safety of file protection systems

def is_safe(file_permissions, user_requests):
    for request in user_requests:
        user = request['user']
        file = request['file']
        operation = request['operation']

        # Check if the user has the required permissions for the requested operation on the file
        if file not in file_permissions or operation not in file_permissions[file] or user not in file_permissions[file][operation]:
            return False

    return True

# Example usage
file_permissions = {
    'file1': {
        'read': ['user1', 'user2'],
        'write': ['user2']
    },
    'file2': {
        'read': ['user1'],
        'write': ['user1']
    }
}

user_requests = [
    {'user': 'user1', 'file': 'file1', 'operation': 'read'},
    {'user': 'user2', 'file': 'file1', 'operation': 'write'},
    {'user': 'user3', 'file': 'file2', 'operation': 'read'}
]

result = is_safe(file_permissions, user_requests)
print(result)
