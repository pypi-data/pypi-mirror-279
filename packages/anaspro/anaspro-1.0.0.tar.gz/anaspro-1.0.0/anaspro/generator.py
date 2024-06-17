from faker import Faker
import random
import os
import json

fake = Faker()

class RandomDataGenerator:
    def __init__(self):
        self.countries = self.load_countries()

    def load_countries(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        countries_file = os.path.join(current_dir, 'data', 'countries.json')
        with open(countries_file, 'r', encoding='utf-8') as f:
            countries = json.load(f)
        return countries

    def generate_username(self):
        return fake.user_name()

    def generate_password(self):
        return fake.password(length=random.randint(8, 16), special_chars=True, digits=True, upper_case=True, lower_case=True)

    def generate_email(self, username):
        return f"{username}@gmail.com"

    def generate_phone_number(self):
        country = random.choice(list(self.countries.keys()))
        country_code = self.countries[country]
        if country == "Egypt":
            prefix = random.choice(["10", "11", "12", "15"])
            phone_number = prefix + ''.join(random.choices('0123456789', k=8))
        else:
            phone_number = ''.join(random.choices('0123456789', k=10))
        return country, f"{country_code}{phone_number}"

    def generate_random_data(self):
        username = self.generate_username()
        password = self.generate_password()
        email = self.generate_email(username)
        country, phone_number = self.generate_phone_number()

        return {
            'username': username,
            'password': password,
            'email': email,
            'country': country,
            'phone_number': phone_number
        }

def main():
    generator = RandomDataGenerator()
    data = generator.generate_random_data()
    print(data)

if __name__ == "__main__":
    main()
