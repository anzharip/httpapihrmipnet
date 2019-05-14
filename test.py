import models

emergency_contact = models.EmergencyContact("3347")

# print (emergency_contact.get_all())

# print (emergency_contact.get('4'))

# print (emergency_contact.get_last_eec_seqno_value())

# body = {
#     "emergency_contactid": "5",
#     "name": "Jane Doeee",
#     "relationship": "Wife",
#     "mobile": "080989999",
#     "home_telephone": "080989999",
#     "work_telephone": "080989999",
#     "address": "Jl. Majapahit 26R"
# }

# print (emergency_contact.put(body))

print (emergency_contact.delete("6"))