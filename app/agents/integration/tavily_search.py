from tavily import TavilyClient
from langsmith import traceable
from dotenv import load_dotenv

# .env ファイルをロード
load_dotenv()

client = TavilyClient()

from agents.integration.integration import Integration

class TavilyLLM(Integration):

    def execute(self, system_prompts: list[str], user_prompts: list[str]):
        response = self.__execute(system_prompts=system_prompts, user_prompts=user_prompts)
        return response['answer']
    
    @traceable(name="Tavily")
    def __execute(self, system_prompts: list[str], user_prompts: list[str]):
        return client.search(
            query='\n'.join(system_prompts + user_prompts),
            search_depth='basic',
            include_answer=True,
            include_raw_content=False,
        )
