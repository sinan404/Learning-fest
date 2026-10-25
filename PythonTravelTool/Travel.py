
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("COUNTRY_API_KEY")
API_URL = os.getenv("COUNTRY_API_URL")

country_name = input("Enter a country name: ").strip()

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

try:
    url = f"{API_URL}/{country_name}"
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    data = response.json()
    country = data["data"]["objects"][0]

    name = country["names"]["common"]
    capitals = country.get("capitals", [])
    capital = capitals[0]["name"] if capitals else "Not available"

    currencies = country.get("currencies", [])
    currency = currencies[0]["name"] if currencies else "Not available"

    population = country.get("population", "Not available")
    region = country.get("region", "Not available")

    languages = country.get("languages", [])
    language_names = [
        language["name"] for language in languages
    ]

    neighbours = country.get("borders", [])


    snapshot = {
        "Country": name,
        "Capital": capital,
        "Currency": currency,
        "Population": population,
        "Languages": ", ".join(language_names) if language_names else "Not available",
        "Region": region,
        "Neighbour country codes": ", ".join(neighbours) if neighbours else "None"
    }

    for key, value in snapshot.items():
        if key == "Population" and isinstance(value, int):
            value = f"{value:,}"
        print(f"{key}: {value}")

except requests.Timeout:
    print("Error: The request timed out. Please try again.")

except requests.ConnectionError:
    print("Error: Could not connect. Check your internet connection.")

except requests.HTTPError as error:
    print(f"Error: The API returned an HTTP error: {error}")

except (ValueError, KeyError, IndexError, TypeError) as error:
    print(f"Error: The API returned unexpected data: {error}")

except requests.RequestException as error:
    print(f"Error: Request failed: {error}")
