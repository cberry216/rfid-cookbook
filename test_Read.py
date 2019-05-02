from interface import Interface

interface = Interface()

print("Welcome to the RFID Cookbook - Test Edition")
print("Start scanning your recipe cards to get started")
print("or enter the card UID because you burnt the RFID scanner.")

uid = input("Enter UID values: ")

while True:
    if len(uid) != 5:
        uid = input("Invalid UID length (4 Numbers): ")
        continue

    interface.process_rfid(uid)
    uid = input("Enter UID values: ")
