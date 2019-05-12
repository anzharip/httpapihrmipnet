# import models
# import bcrypt

# user = models.User("anzhari", "123123")

# password = b"123123"
# hashed = bytes(user.login()[2], "utf-8")

# print (password, hashed)

# print (type(password), type(hashed))

# if bcrypt.checkpw(password, hashed):
#     print("It Matches!")
# else:
#     print("It Does not Match :(")

##
import models
user = models.User("brian", "password")
print (user.login())