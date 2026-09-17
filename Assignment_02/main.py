from rental import Vehicle, Renter, ElectricCar, Motorbike


# Create vehicles and a renter
car = Vehicle("Toyota", "Yaris", "1AB234")
electric_car = ElectricCar("Tesla", "Model 3", "2EV567", 75)
motorbike = Motorbike("Honda", "CBR500R", "3MB890", 500)

renter = Renter("Alice", 12345)

# Rent and return a vehicle
print(car)

car.rent()
renter.rented.append(car)
print(car)

car.return_vehicle()
renter.rented.remove(car)
print(car)

# Test invalid renter name
try:
    Renter("", 12345)
except ValueError as e:
    print("Caught ValueError:", e)

# Test invalid license number
try:
    Renter("Bob", 0)
except ValueError as e:
    print("Caught ValueError:", e)

# Test polymorphism
vehicles = [car, electric_car, motorbike]

print("\nAll vehicles:")
for vehicle in vehicles:
    print(vehicle)
