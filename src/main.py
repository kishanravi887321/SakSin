# # import redis
# # import os

# # # Use your Upstash Redis URL
# # redis_url = "rediss://default:AZoYAAIjcDFjZDY3ZDU3MzVlOGMNDVlOTgyYTBhMTAwMDIxZTgwYXAxMA@internal-raptor-39448.upstash.io:6379"

# # # Connect to Upstash Redis
# # r = redis.from_url(redis_url, decode_responses=True)

# # # Find all conversation keys or all keys
# # keys = r.keys("*")  # You can also use "*" to clear everything

# # # Delete each key
# # for key in keys:
# #     print(f"Deleting: {key}")
# #     r.delete(key)

# # print("✅ All conversation data deleted.")
# import requests

# url = "https://bf979707349e.ngrok-free.app/api/generate"
# headers = {"Content-Type": "application/json"}
# data = {
#     "model": "qwen2.5:1.5b",
#     "prompt": "write a code for make a string palindrome",
#     "stream": False
# }

# response = requests.post(url, json=data, headers=headers)
# print(response.json()["response"])
