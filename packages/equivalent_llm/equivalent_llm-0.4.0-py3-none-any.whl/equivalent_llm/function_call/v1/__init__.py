#
# Function definition
#

EXTRACT_DATE_TIME = {
    'required': ['query'],
    'parameters': {
        'query': {
            'name': 'query',
            'equivalence': {
                'tester': 'get_equivalence_tester',
                'category': 'date, time, time range, date range',
            },
            'consistency': {
                'tester': 'get_category_consistency_tester',
                'instruction': 'latest',
                'category': 'date, time, time range, date range',
            },
            'grammar': {
                'tester': 'get_grammar_tester',
            },
        }
    }
}

EXTRACT_COORDINATES = {
    'required': [],
    'parameters': {
        'query': {
            'name': 'query',
            'equivalence': {
                'tester': 'get_equivalence_tester',
                'category': 'date, time, time range, date range',
            },
            'consistency': {
                'tester': 'get_category_consistency_tester',
                'instruction': 'latest',
                'category': 'place, land mark, district, building',
            },
            'grammar': {
                'tester': 'get_grammar_tester',
            },
        }
    }
}

GET_MOVIE_THEATERS = {
    'required': [],
    'parameters': {
        'movie_title': {
            'name': 'movie_title',
            'equivalence': {
                'tester': 'get_equivalence_tester',
                'category': 'movie title',
            },
            'consistency': {
                'tester': 'get_category_consistency_tester',
                'instruction': 'all',
                'category': 'movie title',
            },
        },
        'latitude': {
            'name': 'latitude',
            'equivalence': {
                'tester': 'get_equivalence_tester',
                'category': 'coordinate',
            },
            'consistency': {
                'tester': 'get_number_consistency_tester',
                'instruction': 'latest',
                'range': [-90, 90],
            },
        },
        'longitude': {
            'name': 'longitude',
            'equivalence': {
                'tester': 'get_equivalence_tester',
                'category': 'coordinate',
            },
            'consistency': {
                'tester': 'get_number_consistency_tester',
                'instruction': 'latest',
                'range': [-180, 180],
            },
        },
        'start_time': {
            'name': 'start_time',
            'equivalence': {
                'tester': 'get_equivalence_tester',
                'category': 'datetime, YYYY-mm-dd HH:MM:SS',
            },
            'consistency': {
                'tester': 'get_category_consistency_tester',
                'category': 'datetime, YYYY-mm-dd HH:MM:SS',
                'comment': 'Start point of time range. If the start time is not provided explicitly, it should be inferred from the compound of the current time and user request. Also, if there is not stated time, base time is kept as 00:00:00.',
                'instruction': 'all',
            },
        },
        'end_time': {
            'name': 'end_time',
            'equivalence': {
                'tester': 'get_equivalence_tester',
                'category': 'datetime, YYYY-mm-dd HH:MM:SS',
            },
            'consistency': {
                'tester': 'get_category_consistency_tester',
                'category': 'datetime, YYYY-mm-dd HH:MM:SS',
                'comment': 'End point of time range. If the end time is not provided explicitly, it should be inferred from the compound of the current time and user request. Also, if there is not stated time, base time is kept as 23:59:59.',
                'instruction': 'all',
            },
        },
        'selected_benefit': {
            'name': 'selected_benefit',
            'equivalence': {
                'tester': 'get_equivalence_tester',
                'category': 'benefit',
            },
            'consistency': {
                'tester': 'get_enum_consistency_tester',
                'items': ["무료 예매", "1+1 예매", "특별관 할인","4,000원 할인","50% 할인", ""],
                'instruction': 'all',
            }
        }
    },
}

GET_MOVIE_TITLES = {
    'required' : [],
    'parameters': {
        'start_time': {
            'name': 'start_time',
            'equivalence': {
                'tester': 'get_equivalence_tester',
                'category': 'datetime, YYYY-mm-dd HH:MM:SS',
            },
            'consistency': {
                'tester': 'get_category_consistency_tester',
                'category': 'datetime, YYYY-mm-dd HH:MM:SS',
                'comment': 'Start point of time range. If the start time is not provided explicitly, it should be inferred from the compound of the current time and user request. Also, if there is not stated time, base time is kept as 00:00:00.',
                'instruction': 'all',
            },
        },
        'end_time': {
            'name': 'end_time',
            'equivalence': {
                'tester': 'get_equivalence_tester',
                'category': 'datetime, YYYY-mm-dd HH:MM:SS',
            },
            'consistency': {
                'tester': 'get_category_consistency_tester',
                'category': 'datetime, YYYY-mm-dd HH:MM:SS',
                'comment': 'End point of time range. If the end time is not provided explicitly, it should be inferred from the compound of the current time and user request. Also, if there is not stated time, base time is kept as 23:59:59.',
                'instruction': 'all',
            },
        },
        'movie_theater': {
            'name': 'movie_theater',
            'equivalence': {
                'tester': 'get_equivalence_tester',
                'category': 'theater name',
            },
            'consistency': {
                'tester': 'get_category_consistency_tester',
                'category': 'theater name',
                'comment': 'Ignore words like "극장", "상영관", "영화관", and "theater"',
                'instruction': 'all',
            },
        },
        'query': {
            'name': 'query',
            'equivalence': {
                'tester': 'get_equivalence_tester',
                'category': 'actor, movie title, movie series, movie genre, country',
            },
            'consistency': {
                'tester': 'get_category_consistency_tester',
                'category': 'actor, movie title, movie series, movie genre, country',
                'comment': 'Ignore words like "영화", and "movie"',
                'instruction': 'latest',
            },
            'grammar': {
                'tester': 'get_grammar_tester',
            },
        },
    },
}

GET_MOVIE_SCHEDULES = {
    'required' : ['movie_title', 'movie_theater', 'start_time'],
    'parameters': {
        'movie_title': {
            'name': 'movie_title',
            'equivalence': {
                'tester': 'get_equivalence_tester',
                'category': 'movie title',
            },
            'consistency': {
                'tester': 'get_category_consistency_tester',
                'category': 'movie title',
                'instruction': 'all',
            },
        },
        'movie_theater': {
            'name': 'movie_title',
            'equivalence': {
                'tester': 'get_equivalence_tester',
                'category': 'movie theater',
            },
            'consistency': {
                'tester': 'get_category_consistency_tester',
                'category': 'movie theater',
                'instruction': 'all',
            },
        },
        'start_time': {
            'name': 'start_time',
            'equivalence': {
                'tester': 'get_equivalence_tester',
                'category': 'datetime, YYYY-mm-dd HH:MM:SS',
            },
            'consistency': {
                'tester': 'get_category_consistency_tester',
                'category': 'datetime, YYYY-mm-dd HH:MM:SS',
                'comment': 'Start point of time range. If the start time is not provided explicitly, it should be inferred from the compound of the current time and user request. Also, if there is not stated time, base time is kept as 00:00:00.',
                'instruction': 'all',
            },
        },
        'end_time': {
            'name': 'end_time',
            'equivalence': {
                'tester': 'get_equivalence_tester',
                'category': 'datetime, YYYY-mm-dd HH:MM:SS',
            },
            'consistency': {
                'tester': 'get_category_consistency_tester',
                'category': 'datetime, YYYY-mm-dd HH:MM:SS',
                'comment': 'End point of time range. If the end time is not provided explicitly, it should be inferred from the compound of the current time and user request. Also, if there is not stated time, base time is kept as 23:59:59.',
                'instruction': 'all',
            },
        },
        'selected_benefit': {
            'name': 'selected_benefit',
            'equivalence': {
                'tester': 'get_equivalence_tester',
                'category': 'benefit',
            },
            'consistency': {
                'tester': 'get_enum_consistency_tester',
                'items': ["무료 예매", "1+1 예매", "특별관 할인","4,000원 할인","50% 할인", ""],
                'instruction': 'all',
            }
        }
    }
}

BOOK_MOVIE_TICKETS = {
    'required' : ['movie_title', 'movie_theater', 'movie_schedule', 'user_consent'],
    'parameters': {
        'movie_title': {
            'name': 'movie_title',
            'equivalence': {
                'tester': 'get_equivalence_tester',
                'category': 'movie title',
            },
            'consistency': {
                'tester': 'get_category_consistency_tester',
                'category': 'movie title',
                'instruction': 'all',
            },
        },
        'movie_theater': {
            'name': 'movie_title',
            'equivalence': {
                'tester': 'get_equivalence_tester',
                'category': 'movie theater',
            },
            'consistency': {
                'tester': 'get_category_consistency_tester',
                'category': 'movie theater',
                'instruction': 'all',
            },
        },
        'movie_schedule': {
            'name': 'movie_schedule',
            'equivalence': {
                'tester': 'get_equivalence_tester',
                'category': 'datetime, YYYY-mm-dd HH:MM:SS, movie schedule',
            },
            'consistency': {
                'tester': 'get_category_consistency_tester',
                'category': 'datetime, YYYY-mm-dd HH:MM:SS, movie schedule',
                'instruction': 'all',
            },
        },
        'user_consent': {
            'name': 'user_consent',
            'equivalence': {
                'tester': 'get_equivalence_tester',
                'category': 'consent',
            },
            'consistency': {
                'tester': 'get_enum_consistency_tester',
                'items': [True, False],
                'instruction': 'all',
            },
        },
    }
}

SEARCH_MOVIE_INFORMATION = {
    'required': ['query'],
    'parameters': {
        'query': {
            'name': 'query',
            'equivalence': {
                'tester': 'get_equivalence_tester',
                'category': 'movie title',
            },
            'consistency': {
                'tester': 'get_category_consistency_tester',
                'category': 'movie title',
                'instruction': 'all',
            },
            'grammar': {
                'tester': 'get_grammar_tester',
            },
        },
    }
}

SEARCH_BENEFIT_FOR_BOOKING_MOVIE = {
    'required': [],
    'parameters': {
        'grade': {
            'name': 'grade',
            'equivalence': {
                'tester': 'get_equivalence_tester',
                'category': 'grade',
            },
            'consistency': {
                'tester': 'get_category_consistency_tester',
                'category': 'grade',
                'instruction': 'all',
            },
        },
    }
}

SEARCH_MOVIE_RESERVATION = {
    'required': [],
    'parameters': {
        'intent': {
            'name': 'intent',
            'equivalence': {
                'tester': 'get_equivalence_tester',
                'category': 'enum',
            },
            'consistency': {
                'tester': 'get_enum_consistency_tester',
                'items': ["search_movie_reservation", "cancel_movie_reservation"],
                'instruction': 'all',
            },
        },
        'query': {
            'name': 'query',
            'equivalence': {
                'tester': 'get_equivalence_tester',
                'category': 'reservation',
            },
            'consistency': {
                'tester': 'get_category_consistency_tester',
                'category': 'reservation',
            },
            'grammar': {
                'tester': 'get_grammar_tester',
            },
        },
    }
}

CANCEL_MOVIE_RESERVATION = {
    'required': [],
    'parameters': {
        'query': {
            'name': 'query',
            'equivalence': {
                'tester': 'get_equivalence_tester',
                'category': 'reservation',
            },
            'consistency': {
                'tester': 'get_category_consistency_tester',
                'category': 'reservation',
                'instruction': 'all',
            },
            'grammar': {
                'tester': 'get_grammar_tester',
            },
        },
    }
}
