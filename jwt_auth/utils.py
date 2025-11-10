def get_access_token_from_request(request) -> str | None:
    auth_header = request.headers.get('Authorization', '')
    access_token = None
        
    token_parts = auth_header.split(' ')
    if len(token_parts) != 2 or token_parts[0].lower() != 'bearer':
        return
    
    access_token = auth_header.split(' ')[1]
    return access_token