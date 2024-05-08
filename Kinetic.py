
def computeKenetic(velocity, mass):
    return round(0.5 * mass * (velocity ** 2), 2)

print("Lets Calculate the Object Kinetic energy.")
print("Please Fill up the following: \n")

mass = float(input("Enter mass in Kilograms: "))
velocity = float(input("Enter velocity in meters per second: "))
print("The object's kenetic energy is: " + str(computeKenetic(velocity, mass)) + "J.")


