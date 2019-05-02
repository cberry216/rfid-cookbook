from interface import Interface

interface = Interface()

print("Welcome to the RFID Cookbook - Test Edition")
print("Start scanning your recipe cards to get started")
print("or enter the card UID because you burnt the RFID scanner.")

uid = input("Enter UID values: ")

while True:
    uid_vals = list(map(lambda x: int(x), uid.split(',')))
    if len(uid) != 5:
        uid = input("Invalid UID length (5 Numbers): ")
        continue

    interface.process_rfid(uid_vals)
    uid = input("Enter UID values: ")
    uid_vals = list(map(lambda x: int(x), uid.split(',')))
