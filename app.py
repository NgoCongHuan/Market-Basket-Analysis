from faker import Faker

fake = Faker('vi_VN')

print("Name: ", fake.name())
print("Address:", fake.address())
print("Phone number:", fake.phone_number())
print("Email:", fake.email())
print("Company:", fake.company())
print("Job:", fake.job())
print("Date of Birth:", fake.date_of_birth())
print("Text:", fake.text())
print("City:", fake.city())
print("Country:", fake.country())