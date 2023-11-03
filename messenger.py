from dotenv import load_dotenv
import os
import requests
import sqlite3


#function to get phone number from db
def get_phone_from_db(recipient_email):
    connection = sqlite3.connect('email_mapping.db')
    cursor = connection.cursor()
    cursor.execute("SELECT phone_number FROM email_mapping WHERE email=?", (recipient_email,)) 
    result = cursor.fetchone()
    connection.close()
    return result[0] if result else None


def post_whatsapp_message(endpoint, ACCESS_TOKEN, MESSAGE_CONTENT, phone):
  #define the API endpoint URL
  url = endpoint

  #define headers
  headers = {
      "Authorization": ACCESS_TOKEN,
      "Content-Type": "application/json",
  }



# #define the request data in JSON format
#   data = {
#       "messaging_product": "whatsapp",
#       "to": phone,
#       "type": "text",
#       "text": {
#          #"header": "You Have New Mail",
#          "body": MESSAGE_CONTENT
#       } 
#   }

  #print(MESSAGE_CONTENT)

  #define the request data in JSON format
  data = {
      "messaging_product": "whatsapp",
      "to": phone,
      "type": "template",
      "template": {
         "name": "email_notification",
         "language": {"code": "en"}
      } 
  }
   
  #print(data)

  #SEND POST
  response = requests.post(url, json = data, headers=headers)

  #check response
  if response.status_code == 200:
      #successful
      print("Request was successful")
      print("Response content:", response.text)
  else:
      print("Request failed with status code:", response.status_code)
      #print("Response content:", response.text)



if __name__ == '__main__':
  #grabbing the api key from the .env file
  load_dotenv()
  api_token = os.getenv('whatsapp_auth_token')
  endpoint = os.getenv('endpoint_path')
  content = os.getenv('message_content')

  #print("Access token:", whatsapp_token)

  email = input("Enter the recipient's e-mail: ")
  user_phone = get_phone_from_db(email)
  post_whatsapp_message(endpoint, api_token, content, user_phone)
