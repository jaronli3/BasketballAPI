import bcrypt

# just checks yes or no if the user-passed in password matches 
# (not true perfect authorization)



# create user password 
# hashes and salts the password and sends to db 
def hash_and_salt_password(password):
    # Generate a random salt
    salt = bcrypt.gensalt()

    # Hash the password using the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    # get the hashed and salted password
    hashed_password.decode('utf-8')

    

