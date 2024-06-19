import re
from typing import Any, Optional

from equivalent_llm.parse import json_loads

def __get_entity(pattern: str, string: str) -> Optional[str]:
    r = re.search(pattern, string)
    return r.group() if r is not None else None

def extract_date_time(content: str, instructions: list, prompt_engine: Any) -> dict:
    """Extract time information from return value of function call extract_date_time

    Args:
        content (str): return value from extract_date_time fucntion call

    Returns:
        dict: start time, end time, and current time
    """
    start_time = r"(?<=start time:\s)\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}.*"
    end_time = r"(?<=end time:\s)\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}.*"
    current_time = r"(?<=Current time:\s)\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}.*"

    return {
        'name': 'extract_date_time',
        'parameters': {
            'start_time': __get_entity(start_time, content),
            'end_time': __get_entity(end_time, content),
            'current_time': __get_entity(current_time, content),
        },
        'role': 'function',
    }

def extract_coordinates(content: str, instructions: list, prompt_engine: Any) -> dict:
    """
    Extract latitude and longitude information from return value of function call extract_coordinatess

    Args:
        content (str): return value from extract_coordinates fucntion call

    Returns:
        dict: latitude and longitude
    """

    latitude = r"(?<=latitude:\s)-?\d{1,3}\.\d{1,6}"
    longitude = r"(?<=longitude:\s)-?\d{1,3}\.\d{1,6}"

    return {
        'name': 'extract_coordinates',
        'parameters': {
            'latitude': __get_entity(latitude, content),
            'longitude': __get_entity(longitude, content),
        },
        'role': 'function',
    }

def get_movie_theaters(content: str, instructions: list, prompt_engine: Any) -> dict:
    """
    Get list of movie theaters given coordinates

    Args:
        content (str): return value from get_movie_theaters fucntion call

    Returns:
        dict:
            reference_number,
            popular_theaters,
            recent_visited_theaters,
            user_preferred_theaters,
            requested_location_based_theaters
    """

    contents = content.split('\n')
    theaters = []
    information = []
    for c in contents[1:]:
        if c.startswith('- '):
            theaters.append(dict([c[2:].split(': ')]))
        elif c.startswith("Information:"):
            information.append(c[13:])

    theater_number = r"(?<=reference number:\s)theater_\d+"

    return {
        'name': 'get_movie_theaters',
        'parameters': {
            'theater_number': __get_entity(theater_number, contents[0]),
            'theaters': theaters,
            'information': information,
        },
        'role': 'function',
    }

def get_movie_titles(content: str, instructions: list, prompt_engine: Any) -> dict:
    """
    Get list of movie titles given coordinates

    Args:
        content (str): return value from get_movie_titles fucntion call

    Returns:
        dict:
            reference_number,
            movie_titles,
    """

    reference_number_pattern = r"(?<=reference number:\s)title_\d+"
    reference_number = ''
    titles = []
    information = []
    for c in content.split('\n'):
        if c.startswith('#'):
            reference_number = __get_entity(reference_number_pattern, c)
        elif c.startswith('- '):
            s = c[2:].split(': ')
            if len(s) > 2:
                s1 = ': '.join(s[1:])
            else:
                s1 = s[1]
            movie_type = s[0]
            title = [ t.strip()[1:-1] for t in s1.split(',') ]
            titles.append(dict(map(lambda i : (movie_type, title), [0])))
        elif c.startswith('Information'):
            information.append(c[13:])

    return {
        'name': 'get_movie_titles',
        'parameters': {
            'reference_number': reference_number if reference_number is not None else '',
            'titles': titles,
            'information': information,
        },
        'role': 'function',
    }

def get_movie_schedules(content: str, instructions: list, prompt_engine: Any) -> dict:
    """
    Get list of movie schedules given coordinates

    Args:
        content (str): return value from get_movie_schedules fucntion call

    Returns:
        dict:
            reference_number,
            movie_schedules,
    """

    reference_number_pattern = r"(?<=reference number:\s)schedule_\d+"

    reference_number = ''
    schedules = []
    notices = []
    for c in content.split('\n'):
        if c.startswith('#'):
            reference_number = __get_entity(reference_number_pattern, c)
        elif c.startswith('- '):
            s = c[2:].split(': ')
            theater = s[0]
            schedule = [ t.strip()[1:-1] for t in s[1].split(',') ]
            schedules.append(dict(map(lambda i : (theater, schedule), [0])))
        elif c.startswith('Notice'):
            notices.append(c[8:])

    return {
        'name': 'get_movie_schedules',
        'parameters': {
            'reference_number': reference_number if reference_number is not None else '',
            'schedules': schedules,
            'notices': notices,
        },
        'role': 'function',
    }

def book_movie_tickets(content: str, instructions: list, prompt_engine: Any) -> dict:
    url = r"(?<=URL:\s).*"
    return {
        'name': 'book_movie_tickets',
        'parameters': {
            'url': __get_entity(url, content),
        },
        'role': 'function',
    }

def search_movie_information(content: str, instructions: list, prompt_engine: Any) -> dict:
    movie_title = r"(?<='title':\s).*(?=\s)"
    movie_snippet = r"(?<=snippet:\s).*"

    content_list = content.split('\n')
    movies = []
    for i in range(1, len(content_list), 2):
        title = __get_entity(movie_title, content_list[i])
        snippet = __get_entity(movie_snippet, content_list[i + 1])
        movies.append({'title': title, 'snippet': snippet})

    return {
        'name': 'search_movie_information',
        'parameters': movies,
        'role': 'function',
    }

def search_benefit_for_booking_movie(content: str, instructions: list, prompt_engine: Any) -> dict:
    return {
        'name': 'search_benefit_for_booking_movie',
        'parameters': {
            'benefit': content,
        },
        'role': 'function',
    }

def search_benefit(content: str, instructions: list, prompt_engine: Any) -> dict:
    benefit_number = r"(?<=reference number:\s)benefit_\d+"
    membership = r"(?<=User membership:\s).+"
    included = r"(?<=Membership benefits included:\s).+"
    not_included = r"(?<=Membership benefits not included:\s).+"
    available_benefits = r"(?<=Benefits currently available:\s).+"
    benefit_details = r"(?<=-\s).+ benefit: .+"
    found_benefits = re.findall(benefit_details, content)
    benefits = []
    if found_benefits is not None and len(found_benefits) > 0:
        for benefit in found_benefits:
            b = benefit.split(' benefit: ')
            benefits.append({'benefit': b[0], 'available': b[1]})

    return {
        'name': 'search_benefit',
        'parameters': {
            'benefit_number': __get_entity(benefit_number, content),
            'membership': __get_entity(membership, content),
            'benefit_included': __get_entity(included, content),
            'benefit_not_included': __get_entity(not_included, content),
            'available_benefits': __get_entity(available_benefits, content),
            'benefits': benefits,
        },
        'role': 'function',
    }

def search_movie_reservation(content: str, instructions: list, prompt_engine: Any) -> dict:
    contents = json_loads(content)
    return {
        'name': 'search_movie_information',
        'parameters': contents,
        'role': 'function',
    }
