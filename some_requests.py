import requests

# POST
# response = requests.post(
#     "http://localhost:8000/cameras",
#     json={
#         "cross_street_1": "7th Ave",
#         "cross_street_2": "W 50th St",
#         "zipcode": "10019",
#         "speed_limit": 25,
#         "direction": "N"
#     }
# )
# print(response.json())

# PUT
# response = requests.put(
#     "http://localhost:8000/cameras/11",
#     json={"speed_limit": 30}
# )
# print(response.json())
#
# DELETE
# response = requests.delete("http://localhost:8000/cameras/11")
# print(response.json())