import local_logger as ll

log = ll.LocalLogger()
f = ((123,432),(123,412),(111,213),(2132,444),(231,213))
rfid_id = (("fxas"),("sadasd"),("sadio309"),("dasdkasda"),("asdksamdas"))
log.write_file('arrival',rfid_id,f)

print(log.get_content('arrival')[-1]["rfid_tag"])
log.write_file('depature',f,rfid_id)
print(log.get_content('depature')[-1]["rfid_tag"])

log.delete_file()