import re
import sys
import json

import requests
import jsonschema
import yaml

JSONSCHEMA_URL = "https://raw.githubusercontent.com/opendatateam/udata-recommendations/master/udata_recommendations/schema.json"


def extract_slug(url):
    error_message = f"{url} is malformed. Expected a data.gouv.fr URL like https://www.data.gouv.fr/fr/datasets/jours-feries-en-france/"

    pattern = re.compile(r"^https://www\.data\.gouv\.fr/fr/(dataset|reuse)s/(\S+)/$")

    try:
        match = pattern.match(url)
    except TypeError:
        raise ValueError(error_message)

    if not match:
        raise ValueError(error_message)

    return match.group(1), match.group(2)


def get_type(recommendation):
    return recommendation['type'] if 'type' in recommendation else "dataset"


def is_external(type: str) -> bool:
    return type == "external"


def validate_recommendations(recommendations):
    """" Validate recommendations according to the JSON schema"""
    r = requests.get(JSONSCHEMA_URL, timeout=10)
    r.raise_for_status()
    schema = r.json()

    jsonschema.validate(recommendations, schema=schema)


def build_recommendations(item):
    return {
        "id": extract_slug(item["source"])[1],
        "recommendations": [
            format_recommendation(r)
            for r in item["recommendations"]
        ],
    }


def format_recommendation(recommendation):
    type = get_type(recommendation)
    return {
        "id": recommendation["id"] if is_external(type) else extract_slug(recommendation["id"])[1],
        "score": int(recommendation["score"]),
        "type": type,
        "messages": recommendation["messages"] if "messages" in recommendation else {}
    }

def main():
    with open("recommendations.yml") as f:
        src = yaml.safe_load(f) or []

    recommendations = [build_recommendations(item) for item in src]

    validate_recommendations(recommendations)

    json.dump(recommendations, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
