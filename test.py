import models

dependent = models.Dependent("3347")

# body = {
#     "name": "Jane Doe",
#     "relationship": "Wife",
#     "gender": "2",
#     "date_of_birth": "1945-08-17"
# }

# print(dependent.post(body))

# print (dependent.get_all())

# body = {
#     "dependent_id": "7",
#     "name": "Jane Doeeee",
#     "relationship": "Wife",
#     "gender": "2",
#     "date_of_birth": "1945-08-17"
# }
# print (dependent.put(body))

print (dependent.delete("6"))