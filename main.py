import re
import sys
import json

import requests
import jsonschema
import yaml

JSONSCHEMA_URL = "https://raw.githubusercontent.com/AntoineAugusti/udata-recommendations/add-source-score/udata_recommendations/schema.json"


def extract_slug(url):
    error_message = f"{url} is malformed. Expected a data.gouv.fr URL like https://www.data.gouv.fr/fr/datasets/jours-feries-en-france/"

    pattern = re.compile(r"^https://www\.data\.gouv\.fr/fr/datasets/(\S+)/$")

    try:
        match = pattern.match(url)
    except TypeError:
        raise ValueError(error_message)

    if not match:
        raise ValueError(error_message)

    return match.group(1)


def validate_recommendations(recommendations):
    """" Validate recommendations according to the JSON schema"""
    r = requests.get(JSONSCHEMA_URL, timeout=10)
    r.raise_for_status()
    schema = r.json()

    jsonschema.validate(recommendations, schema=schema)


def build_recommendation(item):
    return {
        "id": extract_slug(item["source"]),
        "recommendations": [
            {"id": extract_slug(r["id"]), "score": int(r["score"])}
            for r in item["recommendations"]
        ],
    }


def main():
    with open("recommendations.yml") as f:
        src = yaml.safe_load(f) or []

    recommendations = [build_recommendation(item) for item in src]

    validate_recommendations(recommendations)

    json.dump(recommendations, sys.stdout, indent=2)


if __name__ == "__main__":
    main()
