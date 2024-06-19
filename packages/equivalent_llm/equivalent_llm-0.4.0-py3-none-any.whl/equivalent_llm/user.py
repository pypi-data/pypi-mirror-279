from logging import Logger

from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.output_parsers import PydanticOutputParser

from pydantic.v1 import BaseModel, Field

from equivalent_llm.engine import PromptEngine

__system_template = '''
- Format instructions: {format_instructions}
- When you reserve a movie at movie theater, check following entities.
- Entities: DATETIME, LOCATION, THEATER, COORDINATES, ACTOR, NOWSHOWING, CREATING_COUNTRY, SHOWING_COUNTRY, MOVIE_GENRE, MOVIE_SERIES, MOVIE_TITLE, DECISION, RESERVATION
- DATETIME: time, data, and datetime
- THEATER: theater name. Specially it includes LOCATION + '극장', LOCATION + '상영관', or LOCATION + 'THEATER'.
- LOCATION: city, district, place name, landmark, company name near a theater, or so on. MUST NOT include theater name.
- COORDINATES: coordinates by longitude and latitude
- ACTOR: well-known actor or actress names
- NOWSHOWING: now showing in theaters
- CREATING_COUNTRY: creating country of movie
- SHOWING_COUNTRY: showing country
- MOVIE_GENRE: movie genre, which also includes special circumstance like "mood", "dating", and "relaxation".
- MOVIE_SERIES: movie series name, which is not specific movie title but is a group of movies.
- MOVIE_TITLE: specific movie title.
- DECISION: acception or rejection in English or Korean
- RESERVATION: reservation, booking, or cancelation

=== Popular MOVIE TITELS ===
* 공포의 외인구단

=== Popular ACTOR & ACTRESS NAMES ===
'''

temp ='''
- LOCATION: city, district, place name, landmark, company name near a theater, or so on. MUST NOT include theater name.

'''

__human_template = '''
What kinds of entities are contained below message?
- Choose the entity type at first and describe the evidence of decision.
- MUST exclude entities out of instructions
- If THEATER and LOCATION are confused, TREAT both entities are found.
- MUST include DATETIME, LOCATION, THEATER entities. Fill '' when there is not any the evidence.
-----
MESSAGE: {message}
'''
temp ='''
'''

class UserEntity(BaseModel):
    entity: str = Field(desription="Entity type in user input message")
    keyword: str = Field(description="Core keyword of entity")
    evidence: str = Field(description="Evidence of decision")

class ListOfUserEntity(BaseModel):
    entities: list[UserEntity] = Field(description="List of entities")

def get_entities(message: str, instructions: list, prompt_engine: PromptEngine, logger: Logger) -> dict:
    system_template = SystemMessagePromptTemplate.from_template(__system_template)
    human_template = HumanMessagePromptTemplate.from_template(__human_template)
    chat_prompt_template = ChatPromptTemplate.from_messages(
        [system_template, human_template]
    )

    parser = PydanticOutputParser(pydantic_object=ListOfUserEntity)
    final_prompt = chat_prompt_template.format_prompt(
        message=message,
        format_instructions=parser.get_format_instructions()
    ).to_messages()
    logger.debug(f"Prompt for user input message: {final_prompt}")

    parsed = prompt_engine.invoke(final_prompt)
    parsed['role'] = 'user'
    parsed['name'] = 'user'
    parsed['request'] = message
    return parsed
