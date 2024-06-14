import json
import concurrent.futures
from langchain_community.llms import Ollama
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.socket_mode.response import SocketModeResponse


class Publication:
    def __init__(self,publication_filled, llm_use:bool=True) -> None:
        self.publication_filled = publication_filled
        
        self.title = self.get_publication_title()
        self.abstract = self.get_publication_abstract().lower()
        self.author = self.get_author_name()
        self.year = self.get_year()
        self.url = self.get_publication_url()
        self.citation = self.get_citation()
        self.topic = self.get_topic() if not llm_use else self.get_topic_LLM()
        
    def get_topic(self,output_file="json/ouput.json", # à voir cette histoire avec get_topic et __get_topic
                  input_file="json/response.json") -> list[str]:
        try:
            with open(output_file,'r') as file:
                data = json.load(file)
            return data[self.author]['topic']
        except Exception as e:
            return self.__get_topic(input_file)
        
    def get_publication_url(self) -> str:
        return self.publication_filled['pub_url']
    
    def get_publication_title(self) -> str:
        return self.publication_filled['bib']['title'] 

    def get_publication_abstract(self) -> str:
        return self.publication_filled['bib']['abstract']

    def get_author_name(self) -> str:
        return self.publication_filled['bib']['author']

    def get_year(self) -> str:
        return self.publication_filled['bib']['pub_year']
    
    def get_citation(self) -> str:
        return self.publication_filled['bib']['citation']
    
    def get_topic_LLM(self,input_file="json/response.json") -> dict:
        with open(input_file, 'r') as file:
            data = json.load(file)
                    
        llm = Ollama(
        model="llama3")  # assuming you have Ollama installed and have llama3 model pulled with `ollama pull llama3 `
        parser = JsonOutputParser()
        
        new_text = """The output should be formatted as a JSON instance that conforms to the JSON schema below.

        As an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}
        the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.

        Here is the output schema:
        ```
        {"topic": {'Machine Learning: [Keyword1, keyword2, keyword3], 'Batteries: [keyword1, keyword2, keyword3]}
        ```
        """


        prompt = PromptTemplate(
            template="Here is a text: {abstract} Please identify the topics from the following list: {liste}. Note: A single text can belong to multiple topics, so please list all relevant topics.  \n{format_instructions}"
        ,
            input_variables=["abstract","liste","topics"],
            partial_variables={"format_instructions": new_text}
        )


        chain = prompt | llm | parser
        topics = chain.invoke({"abstract": self.abstract, "liste": data.keys()})
        return topics['topic']
        
        
    def __get_topic(self
            , file) -> list[str]:
        
        topics = []
        with open(file, 'r') as file:
            data = json.load(file)
        
        for category, item in data.items():
            for keyword in item['keywords']:
                if keyword in self.abstract:
                    topics.append(category)
                if keyword in self.title:
                    topics.append(category)
    
                    
        return list(set(topics))
                
        
    
def setup_json(author):
    try:
        author = author[:-1]
        author_filled = Author(author)
        author_filled.setup_author('json/ouput.json')
        print(f"Topics for {author} have been updated")
    except Exception as e:
        print(f"Couldn't find the google scholar profile for {author}: {e}")

def setup() -> None:
    with open("authors.txt","r") as file:
        authors = file.readlines()
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:  # Adjust max_workers as needed
        executor.map(setup_json, authors)


def process_scholar(scholar,Bot: Bot):
    key = scholar[0]
    value = scholar[1]
    try:

        author = Author(key)
        #print(f'value title= {value["title"]} \n author title = {author.get_last_publication()["bib"]["title"]}')
        if value['title'] != author.get_last_publication()['bib']['title']:
            
            print(f"Updating topics for {author}")
            
            try:
                last_publication = Publication(author.get_last_publication())
            except Exception as e:
                print(f"Couldn't fetch the last publication for {author}: {e}")
                
            
            text_message = f":rolled_up_newspaper::test_tube: {author.author_name} has an update on Google Scholar!\n\
                    ```Title: {last_publication.title}\nCitation: {last_publication.citation}\nYear: {last_publication.year}```"
            try:
                response = Bot.client.chat_postMessage(
                channel=Bot.channel_id, 
                text=text_message)
            except Exception as e:
                print(f"Couldn't send the message to slack: {e}")
            
            # Updating the Json file
            try:
                author.setup_author('json/ouput.json')
            except Exception as e:
                print(f"Couldn't Overwrite the old data for: {author}: {e}")

        
        print(f"Topics for {author} have been updated")
    except Exception as e:
        print(f"Couldn't find the google scholar profile for {author}: {e}")

class Bot:
    def __init__(self, slack_bot_token:str, slack_app_token:str, channel_id:str):
        self.slack_bot_token = slack_bot_token
        self.client = WebClient(token=self.slack_bot_token)
        self.channel_id = channel_id
        self.slack_app_token = slack_app_token
        self.socket_mode_client = SocketModeClient(app_token=self.slack_app_token)
        self.register_handler_to_client()
        
    def process_slash_command(self,payload):
        command = payload['command']
        user_id = payload['user_id']
        text = payload['text']
        channel_id = payload['channel_id']

        if command == '/hello':
            response_message = f"Hello <@{user_id}>!"

            try:
                # Post the message
                self.client.chat_postMessage(
                    channel=channel_id,
                    text=response_message
                )
                print("/hello was successfully posted")
            except SlackApiError as e:
                print(f"Error posting message: {e.response['error']}")
                
        elif command == '/setup':
            response_message = f"Hello <@{user_id}>! It's loading Data, it might take some time"
            try:
                # Post the message
                self.client.chat_postMessage(
                    channel=channel_id,
                    text=response_message
                )
                print("/setup was successfully posted")
                setup() # This function is not defined yet
                self.client.chat_postMessage(
                    channel=channel_id,
                    text="Set up is complete"
                )

            except SlackApiError as e:
                print(f"Error posting message: {e.response['error']}")

    def handle_socket_mode_request(self, req: SocketModeRequest):
        if req.type == "slash_commands":
            self.process_slash_command(req.payload)
            self.socket_mode_client.send_socket_mode_response(SocketModeResponse(envelope_id=req.envelope_id))
        
    def register_handler_to_client(self):
        self.socket_mode_client.socket_mode_request_listeners.append(self.handle_socket_mode_request)    

                

class Author:
    def __init__(self,author) -> None:
        self.author_name = author
        
    def __repr__(self) -> str:
        return self.author_name



    def get_last_publication(self):
        search_query = scholarly.search_author(self.author_name)
        first_author_result = next(search_query)
        author = scholarly.fill(first_author_result )
        first_publication = sorted(author['publications'], 
                                   key= lambda x: int(x['bib']['pub_year']) if 'pub_year' in x['bib'] else 0, 
                                   reverse=True)[0]
        first_publication_filled = scholarly.fill(first_publication)
        return first_publication_filled


    def setup_author(self,output_file):
        with open(output_file,'r') as file:
            data = json.load(file)
        author_last_publication = Publication(self.get_last_publication())
        
        data[self.author_name] = {"title": author_last_publication.title,
                                    "abstract": author_last_publication.abstract,
                                    "topic": author_last_publication.topic, 
                                    "author": author_last_publication.author, 
                                    "year": author_last_publication.year,
                                    "url": author_last_publication.url,}
        
        with open(output_file,'w') as file:
            json.dump(data, file)

if __name__ == "__main__":
    print("Author module is working!")
    author = Author('Mehrad Ansari')
    print(author.get_last_publication())
    pub = Publication(author.get_last_publication())
    pub.get_author_name()