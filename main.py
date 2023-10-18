import requests
import json
import secrets
import string
import os


url_token = f"https://nebula.starbreeze.com/iam/v3/oauth/token"
string_length = 32
random_bytes = secrets.token_bytes(16)

random_string = ''.join(secrets.choice(string.hexdigits) for i in range(string_length))

token_header = {
        "Host": "nebula.starbreeze.com",
    "Content-Type": "application/x-www-form-urlencoded",
    "Authorization": "Basic MGIzYmZkZjVhMjVmNDUyZmJkMzNhMzYxMzNhMmRlYWI6",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.289 Electron/25.8.3 Safari/537.36",
    "Accept": "*/*",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US",
}
data_token = {
    "username": None,
    "password": None,
    "grant_type": "password",
    "client_id": random_string,
    "extend_exp": "true"
}

print("Login to Nebula Account")

username_request = input("Enter your EmailID: ")
password_request = input("Enter the Password: ")
data_token["username"] = username_request
data_token["password"] = password_request
response_token_value = requests.post(url_token, headers=token_header, data=data_token)
while True:
    try:
        if response_token_value.status_code == 200:
            response_data = {
                "user_id": response_token_value.json().get("user_id", ""),
                "token": response_token_value.json().get("access_token", "")
            }
            break
        else:
            print("Invalid Login. Please enter a again.")
            exit(0)
    except ValueError:
        print("Invalid input.")

with open("response.json", "w") as json_file:
    json.dump(response_data, json_file, indent=4)
print("Option - 1 : Buy C-Stacks")
print("Option - 2 : Custom Buy")
print("Option - 3 : Heist Favors")
print("Option - 4 : Import Customized Save Game")

options = {
    1: "Option - 1 : Buy C-Stacks",
    2: "Option - 2 : Custom Buy",
    3: "Option - 3 : Heist Favors",
    4: "Option - 4 : Modded Save"
}
with open("response.json", "r") as config_file:
   config_data = json.load(config_file)
account_id = config_data.get("user_id", "")
authorization_token = config_data.get("token", "")

url = f"https://nebula.starbreeze.com/platform/public/namespaces/pd3/users/{account_id}/orders"
url_save_data = f"https://nebula.starbreeze.com/cloudsave/v1/namespaces/pd3/users/{account_id}/records/progressionsavegame"

headers = {
    "Accept-Encoding": "deflate, gzip",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {authorization_token}",
    "Namespace": "pd3",
    "Game-Client-Version": "1.0.0.0",
    "AccelByte-SDK-Version": "21.0.3",
    "AccelByte-OSS-Version": "0.8.11",
    "User-Agent": "PAYDAY3/++UE4+Release-4.27-CL-0 Windows/10.0.19045.1.256.64bit",
}
data = {
    "itemId": None,  
    "quantity": 1,
    "price": None,
    "discountedPrice": None,
    "currencyCode": None,
    "region": "SE",
    "language": "en-US",
    "returnUrl": "http://127.0.0.1"
}

with open('modded_save_data.json', 'r') as json_file:
    request_headers_data = json.load(json_file)
sava_data_profile = request_headers_data

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print(f"The file '{file_path}' does not exist.")

def get_valid_currencycode():

    while True:
        currency_custom = input("Enter currency: ").strip()
        if currency_custom.isalpha():
            return currency_custom.upper()
        else:
            print("Invalid input.")            
while True:
    try:
        choice = int(input("Enter the option: "))
        if choice in options:
            break
        else:
            print("Invalid choice. Please enter a valid option.")
    except ValueError:
        print("Invalid input. Please enter a valid option.")

repeat_request = int(input("Enter the total number of times you want the request to send: "))  

if choice == 1:
    for _ in range(repeat_request):
        data["itemId"] = "dd693796e4fb4e438971b65eecf6b4b7"
        data["price"] = 90000
        data["discountedPrice"] = 90000
        data["currencyCode"] = "CASH"
        response = requests.post(url, json=data, headers=headers)
        print(f"C-Stacks Bought successfully - {_ + 1}")
        delete_file("response.json")  

elif choice == 2:
        item_id_custom = input("Enter itemID: ")
        price_custom = int(input("Enter price: "))
        discounted_custom = int(input("Enter discountedprice: "))
        currency_custom = get_valid_currencycode()
        data["itemId"] = item_id_custom
        data["price"] = price_custom
        data["discountedPrice"] = discounted_custom
        data["currencyCode"] = currency_custom
        for _ in range(repeat_request):
            response = requests.post(url, json=data, headers=headers)
            print(f"Custom Item Purchased - {_ + 1}")
        delete_file("response.json") 

elif choice == 3: 
    with open('Payday3_offsets.json', 'r') as json_file:
        item_id_json = json.load(json_file)
    for _ in range(repeat_request):
        print(f"Heist Item Purchased - {_ + 1}")
        for item_id in item_id_json["itemId"]:
            if item_id == "65a355215bb8473bbf9d3f2661211899":
                data["itemId"] = item_id
                data["price"] = 1999
                data["discountedPrice"] = 1999
                data["currencyCode"] = "CASH"
                print(f"Item Purchased = {item_id}")
            else:
                data["itemId"] = item_id
                data["price"] = 1000
                data["discountedPrice"] = 1000
                data["currencyCode"] = "CASH"
                print(f"Item Purchased = {item_id}")
            response = requests.post(url, json=data, headers=headers)
    delete_file("response.json") 

elif choice == 4:
    response = requests.post(url_save_data, json=sava_data_profile, headers=headers)
    #with open('response_save_data.txt', 'w') as text_file:
        #text_file.write(response.text)
    print("Modded Save loaded!")
    delete_file("response.json") 
