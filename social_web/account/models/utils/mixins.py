class QueryTemplate:
    CREATE_USER_TEMPLATE = f"""
            INSERT INTO {{table}}
            (email, first_name, last_name, password_hash, date_of_birth, 
            date_joined, date_edited, blocked, is_staff, is_superuser) 
            VALUES ({{email}}, {{first_name}}, {{last_name}}, {{password_hash}}, {{date_of_birth}}, 
            NOW(), NOW(), FALSE, FALSE, FALSE)
            RETURNING id;
        """