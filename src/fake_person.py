from faker import Faker

def create_person():
    myfactory = Faker('en_GB')
    firstName = myfactory.first_name()
    lastName = myfactory.last_name()
    fullName = firstName + " " + lastName
    address = myfactory.address()
    phoneNumber = myfactory.phone_number()
    email = myfactory.email()
    job = myfactory.job()
    company = myfactory.company() + " " + myfactory.company_suffix()
    geo = myfactory.local_latlng(country_code="US", coords_only=False)
    return {
        'FirstName': firstName,
        'LastName':  lastName,
        'FullName': fullName,
        'Address': address,
        'PhoneNumber': phoneNumber,
        "EmailAddress" : email,
        "Profession" : job,
        "Company" : company,
        "CompanyAddress" : myfactory.address(),
        "HQLocation" : geo

    }

if __name__ == "__main__":
    print(create_person() )