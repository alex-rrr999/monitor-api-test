import json
import requests

def main():
    options = [
        'guid', 
        'brand', 
        'name', 
        'resolution', 
        'dimensions', 
        'rate' 
    ]

    user = input(f'\n\nguid, brand, name, resolution, dimensions, rate\n> ')

    if user in options:
        user1 = input(f'\nSearching {user} == ')
    else:
        print('\n\ninvalid option')
        main()

    try:
        response = requests.get(f'http://127.0.0.1:5000/monitors?{user}={user1}')
    except Exception as e:
        print(e)
        main()
    
    #final request
    if response.status_code == 200:
        data = response.json()

        parse = json.dumps(data)

        data_dict = json.loads(parse)
        for guid, brand, name, resolution, dimensions, rate in zip(data_dict["data"]["guid"].values(), data_dict["data"]["brand"].values(), data_dict["data"]["name"].values(), data_dict["data"]["resolution"].values(), data_dict["data"]["dimensions"].values(), data_dict["data"]["rate"].values()):
            print(f"GUID: {guid}\nBrand: {brand}\nName: {name}\nResolution: {resolution}\nDimensions: {dimensions}\nRate: {rate}\n\n")


    else:
        print(f'Error {response.status_code}: {response.reason}')

    main()


main()