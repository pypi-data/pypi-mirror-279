import os,sys
import json
from multillm.BaseLLM import BaseLLM
from multillm.Prompt import Prompt
import requests
from anthropic import Anthropic



# Google ANTHROPIC interface
"""
The CLAUDE class extends the BaseModel class and overrides the get_response() method, providing an implementation.
The get_response() method takes a response parameter and returns the content of the first response in the given response object.
"""
class CLAUDE(BaseLLM):
    

    #implement here
    def __init__ (self, **kwargs):

       
        # add values here directly or if kwargs are specified they are taken from the config file
        defaults  = {
            "class_name" : "CLAUDE",
            "model" : "chat-bison@001",
            "credentials" : "key.json",
           
        }
        #if kwargs:
        # super().__init__(kwargs)
        #else:
        #    super().__init__(defaults)

        
   
    # Get Text
    def get_content(self, response):
        resp = response
        #sys.stdout = sys.__stdout__
    
        """ Get the text from the response of an LLM """
        try:
            if self.is_code(str(resp)):
                print("{0} response: {1}" .format(self.__class__.__name__,str(resp)))
                return str(resp), True
            else:
                #print('CLAUDE is not code')
                print("{0} response: {1}" .format(self.__class__.__name__,str(resp)))
                return str(resp), False
        except Exception as e:
            #print("error is_code() {0}" .format(str(e)))
            return('CLAUDE response failed {}'.format(e))


    def get_response(self, prompt: Prompt, taskid=None, convid = None):
        
        """Predict using a Large Language Model."""
        project_id = "verifai-ml-training"
        location = "us-central1"

        """ Get credentials file set in the config, and set appropriate variables for your model """
        if not os.path.exists(self.credentials):
            try:
                api_key = os.environ["ANTHROPIC_API_KEY"]
            except Exception as e:
                print('the env variable ANTHROPIC_API_KEY is not set')

        else:
            f = open(self.credentials, "r")
            api_key = str(f.readline()).strip()

        """
         curl -X POST https://api.anthropic.com/v1/messages \
         --header "x-api-key: $ANTHROPIC_API_KEY" \
         --header "anthropic-version: 2023-06-01" \
         --header "content-type: application/json" \
       """
        if self.url is not None:
            url = self.url
        else:
            url = "https://api.anthropic.com/v1/messages"
            
        payload = { "model": self.model,
            "max_tokens": 4096,
            "messages": [
                {"role": "user", "content": prompt.get_string()}
            ]
        }
        
        try:
            """ Call API """
            headers = {
                        "x-api-key" : api_key,
                        "anthropic-version" :  "2023-06-01",
                        "content-type" : "application/json"}
                        
            
            #print('calling {0} with Headers {1} , payload {2}' .format(url, headers, payload))
            response = requests.post(url, 
                                     data=json.dumps(payload),headers=headers)
            #print("Claude Response: {0}" .format(response.text))
            data = response.json()
            
        except Exception as e:
            print('error calling claude: {0}' .format(str(e)))
        
        
    
        #print('claude reponse: {0}' .format(data))
        resp = data["content"]
        r = resp[0]
        resp = r["text"]

        response, is_code = self.get_content(resp)


        if not response:
            return None, None
        #else: 
        #    content, is_code = self.get_content(response)
        if response and taskid:
            self.publish_to_redis(response, taskid)
        
        return(response), is_code


    def get_response2(self, prompt: Prompt, taskid=None, convid = None):
        
        """Predict using a Large Language Model."""
        project_id = "verifai-ml-training"
        location = "us-central1"

        """ Get credentials file set in the config, and set appropriate variables for your model """
        if not os.path.exists(self.credentials):
            try:
                api_key = os.environ["ANTHROPIC_API_KEY"]
            except Exception as e:
                print('the env variable ANTHROPIC_API_KEY is not set')

        else:
            f = open(self.credentials, "r")
            api_key = f.readline()

        
        client = Anthropic(
        # This is the default and can be omitted
        #api_key=os.environ.get("ANTHROPIC_API_KEY"),
        api_key=api_key
        )

        response = client.messages.create(
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": prompt.get_string(),
                }
                ],
                model="claude-2.1",
        )



        resp = response.model_dump_json()
        #  {"id": "msg_01WT3NWeLfgrAY7XQTVPHLPp", "content": [{"text":
        res = json.loads(resp)
        #print('claude reponse: {0}' .format(resp))
        resp = res["content"]
        r = resp[0]
        response = r["text"]
        


        if not response:
            return None, None
        else: 
            content, is_code = self.get_content(response)
        if content and taskid:
            self.publish_to_redis(content, taskid)
        
        return(content), is_code

