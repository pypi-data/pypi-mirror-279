import requests

from langchain_community.llms import Ollama

from threading import Thread

configuration = {
    "llm": "llama3",
    "delay_response": False
}


class Conversation:
    external_id = 0
    additional_prompts = []
    chat_history = False
    conditions = []

class Conditions:
    def check(self, message, conversation_history):
        try:
            condition_response = requests.get("http://web:8000/api/v1/knowledgebase/conditions").json()
            
            if len(Conditions) == 0:
                return print("The condition list is empty")

            prompt = f"""
                Given a list of instructions:: {condition_response}.
                determine if any item exactly matches the provided user question.
                Return a JSON object containing the 'id' of the item that matches.
                If no match is found, return a JSON object with the 'id' set to 0.
                Example of the JSON response:
                {{"id": 1}}
                Note: Ensure that the JSON response strictly follows JSON format rules,
                with property names enclosed in double quotes. 
                Provide only the JSON as the response.
            """
            
            messages = [
                { "role": "system", "content": prompt },
            ]
            
            if conversation_history:
                messages.extend([
                    {
                        "role": "human" if message['user_generated']
                        else "assistant", "content": message['message']
                    } for message in conversation_history
                ])

            messages.append(
                { "role": "user", "content": f"{message}" }
            )

            llm = configuration.get("llm")
            llm = Ollama(llm(llm))
            response = llm.invoke(messages).content

            response = int(response)
            self.response_check_async(response)
            print("not available yet")
        except Exception as exc:
            print(exc)
            return None

    def check_async(self, message, messages):
        Thread(target=self.check, args=(message, messages)).start()
    
    def response_check_async(self, index):
        try:
            function = requests.get(f"http://web:8000/api/v1/knowledgease/functions/{index}").json()

            local_scope = {}
            exec(function.function.function, {}, local_scope)

            function = local_scope.get("function")
            function()
        except Exception as exc:
            print(f"error happened when running condition - function, Err: {exc}")
            return None


class RagEndpoint:
    labels = []
    message = {
        "id": 0,
        "message": "",
        "timestamp": "date",
        "conversation_id": 0
    }
    condition = {
        "id": 0,
        "condition": ""
    }

    def similarity_search(self, message, size):
        print("send the mesage and size for sim search")