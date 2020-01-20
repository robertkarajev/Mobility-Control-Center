# import local_file as ll
import json


path = ["34L","45L","22R","5R","5V"]
direction = ['V','R', 'B', 'L']
pathing = []
direct = []
x = path[-1]

for i in path:
    for j in direction:
        if j in i:
            
            length = i.split(j)

            pathing.append(length[0])
            direct.append(j)

print(pathing)
print(direct)




# log = ll.LocalFile()

# example_cards = ["5c6e522e","5c79af3e","5c75a37e","5c716c9e","5c7313de"]
# curent_card = '5c75a37e'
# local = []
# log.write_file("arrival", example_cards)
# log.write_file("depature", example_cards)

# if log.get_content('depature'):
#     for i in (log.get_content('depature')[1:]):
#         local.append(i['rfid_tag'])
        
#     print(local)
    
#     if curent_card in local:
#         index = local.index(curent_card)
#         local = local[index:]
#         print(local)


# elif log.get_content('arrival'):
#     print("hio")

        # print(log.get_content('depature')[i]["rfid_tag"])
# print(log.get_content('arrival'))
# log = ll.LocalLogger()
# f = ((123,432),(123,412),(111,213),(2132,444),(231,213))
# rfid_id = (("fxas"),("sadasd"),("sadio309"),("dasdkasda"),("asdksamdas"))
# log.write_file('arrival',rfid_id,f)

# print(log.get_content('arrival')[-1]["rfid_tag"])
# log.write_file('depature',f,rfid_id)
# print(log.get_content('depature')[-1]["rfid_tag"])

# log.delete_file()