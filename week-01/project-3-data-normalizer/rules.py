# Normalization rules for Project 3 — Data Normalizer

COLUMN_ALIASES = {
    "First Name": "first_name",
    "Last Name": "last_name",
    "Ph Number": "phone",
    "Phone Number": "phone",
    "DOB": "date_of_birth",
    "Date Of Birth": "date_of_birth",
    "Country": "country",
    "Email Address": "email",
    "Gender": "gender",
    "Status": "status",
}

VALUE_MAPPINGS = {
    "gender": {
        "m": "male",
        "male": "male",
        "f": "female",
        "female": "female",
        "M": "male",
        "F": "female",
        "M/Male": "male",
        "female ": "female",
    },
    "country": {
        "usa": "US",
        "u.s.a": "US",
        "united states": "US",
        "us": "US",
        "uk": "UK",
        "united kingdom": "UK",
        "spain": "ES",
    },
    "status": {
        "active": "active",
        "inactive": "inactive",
        "pending": "pending",
        "n/a": None,
        "none": None,
        "not available": None,
    },
}

FORMAT_RULES = {
    "date_columns": ["date_of_birth", "dob"],
    "phone_columns": ["phone"],
    "text_columns": [
        "first_name",
        "last_name",
        "city",
        "state",
        "country",
        "status",
        "gender",
    ],
}

NULL_INDICATORS = [
    "N/A",
    "n/a",
    "none",
    "None",
    "not available",
    "?",
    "",
    "missing",
    "null",
    "NA",
]

DUPLICATE_KEYS = ["email"]
