import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

SERVICE_URL = os.getenv("SERVICE_URL")


class EchoClient:
  """
  A client class for interacting with the Echo server.
  """
  def __init__(self, 
               echo_ai_key, 
               org_id, 
               server_url = "https://echov1.onrender.com",
               canary_prob = 0.1):
    self.server_url = server_url
    self.echo_ai_key = echo_ai_key
    self.org_id = org_id
    self.canary_prob = canary_prob

  def chat(self, text_prompt, **kwargs):
    data = {
       "message": text_prompt, 
       'echo_ai_key':self.echo_ai_key,
       'org_id':self.org_id,
       'canary_prob':self.canary_prob,
       'kwargs':kwargs
       }

    response = requests.post(self.server_url, json=data)

    # Check response status code
    if response.status_code == 200:
    # Successful response
        response_data = response.json()
        echoed_message = response_data.get("message")
        # print(f"ECHO.AI: {echoed_message}")
    else:
        # Error response
        echoed_message = f"Error: {response.status_code} - {response.text}"
        # print(echoed_message)
        

    return echoed_message
  

  def close(self):
    """
    Closes the socket connection.
    """
    self.sock.close()

# Export the EchoClient class
__all__ = ['EchoClient']
