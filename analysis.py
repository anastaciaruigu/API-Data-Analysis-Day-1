"""
Day 1 - API Data Analysis Using Python Structures
Squad Python Specialization - Data Science, AI & Analytics
"""
from dbm import error
import json
from os import path
import os
import os
from pathlib import Path
from unittest import result

import matplotlib.pyplot as plt
import pandas as pd
import requests
import matplotlib 
matplotlib.use("Agg")

API_URL = "https://jsonplaceholder.typicode.com/users"


def get_customers(url: str = API_URL) -> list[dict]:
    """Fetch the customer list. Report failures clearly instead of crashing."""
    try:
        response = requests.get(url,timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.request.exceptions.RequestException as error:
        print(f"Error fetching customers: {error}")
        return []

customers = get_customers()
print(customers)


def explore(record: dict, indent: int = 0) -> None:
    """Print every key in a (possibly nested) record with its type, indented by depth."""
    pad = " " * indent
    if isinstance(record, dict):
        for key, value in record.items():
            print(f"{pad}{key}:{type(value).__name__}") #class <str>
            explore(value, indent + 4)
    elif isinstance(record, list):
        for i, item in enumerate(record):
            if isinstance(item, (dict, list)):
                print(f"{pad}{i}:{type(item).__name__}")
                explore(item, indent + 4)

if customers:
    explore(customers[0])


def extract_attributes(customers: list[dict]) -> list[dict]:
    """Return one flat dict per customer with the attributes listed in the task."""
    rows = [
        # creating an empty list , inisde it will have many dictionaries, each dictinary has individual attributes from the jason file(a nested dictinary)
    ]
    # customers is the whole jason file with (eg 500 customers), c stands for one out of the 500 customers.
    for c in customers:
        rows.append({
            'id': c['id'],
            'name': c['name'],
            "username": c["username"],
            "email": c["email"],
            "email_domain": c["email"].split("@")[-1].lower(),
            "phone": c["phone"],
            "city": c["address"]["city"],
            "zipcode": c["address"]["zipcode"],
            "latitude": float(c["address"]["geo"]["lat"]),
            "longitude": float(c["address"]["geo"]["lng"]),
            "company": c["company"]["name"],
            "website": c["website"],
        })
    return rows

result_x = extract_attributes(customers)
print(result_x)


def unique_cities(customers: list[dict]) -> set[str]:
    """Return the set of distinct cities."""
    return {customer["address"]["city"] for customer in customers}
print(unique_cities(customers))



def city_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per city using a loop and/or a dict comprehension (no Counter, no pandas)."""
    counts = {}

    for c in customers:
        city = c["address"]["city"]
        counts[city] = counts.get(city, 0) + 1

    return counts

def email_domain_counts(customers: list[dict]) -> dict[str, int]:
    """Return {email domain: number of customers} using a dict comprehension."""
    domains = [c["email"].split("@")[-1].lower() for c in customers]
    return {d: domains.count(d) for d in set(domains)}


def print_sorted(counts: dict[str, int], title: str) -> None:
    """Print counts from most to least common, ties listed alphabetically."""
    print(title)
    for name, n in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        print(f"  {name}: {n}")


distinct_email = email_domain_counts(customers)
print(distinct_email)
      
distict_count = city_counts(customers)
print_sorted(city_counts(customers), "Customers by city")
print_sorted(email_domain_counts(customers), "Customers by email domain")
print(distict_count)

domain_result = email_domain_counts(customers)

sorted_domains = dict(
    sorted(
        domain_result.items(),
        key=lambda item: item[1],
        reverse=True
    )
)

print("Customers by email domain:")
print(sorted_domains)

def to_dataframe(rows: list[dict]) -> pd.DataFrame:
  df = pd.DataFrame(rows)
  return df
df = to_dataframe(result_x)
pd.set_option("display.max_columns", None)
print(df.shape)
print(df.dtypes)
print(df)

# If output folder exists
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# Export customers.cv
df.to_csv(OUTPUT_DIR / "customers.csv", index=False)

cols = ["id", "name", "username", "email", "email_domain", "city"]  # use the ones from the resource
df[cols].to_csv(OUTPUT_DIR / "customers.csv", index=False)

# Export city_counts.csv
counts = city_counts(customers)

city_df = pd.DataFrame(list(counts.items()), columns=["city", "count"])
city_df.to_csv(OUTPUT_DIR / "city_counts.csv", index=False)

if __name__ == "__main__":
    # ... earlier steps ...
    df = to_dataframe(customers)

    OUTPUT_DIR.mkdir(exist_ok=True)
    df.to_csv(OUTPUT_DIR / "customers.csv", index=False)

    counts = city_counts(customers)
    pd.DataFrame(list(counts.items()), columns=["city", "count"]).to_csv(
        OUTPUT_DIR / "city_counts.csv", index=False
    )
    print("Saved output/customers.csv and output/city_counts.csv")

print(pd.read_csv("output/customers.csv").head())
print(pd.read_csv("output/city_counts.csv").head())


import os
import matplotlib.pyplot as plt

def plot_distribution(counts: dict[str, int], path: str, title: str = "Customer distribution") -> None:
    """Save a horizontal bar chart of counts, most common at the top."""
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

    items = sorted(counts.items(), key=lambda item: (item[1], item[0]))  # smallest first, so largest ends up on top
    labels = [name for name, _ in items]
    values = [n for _, n in items]

    fig, ax = plt.subplots(figsize=(8, max(3, 0.4 * len(labels))))
    ax.barh(labels, values)
    ax.set_title(title)
    ax.set_xlabel("Number of customers")
    ax.set_xticks(range(0, max(values) + 1))   
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)            


plot_distribution(city_counts(customers), "output/customer_distribution.png", "Customers by city")

df["email_domain"] = df["email"].str.split("@").str[1]
df["tld"] = df["email_domain"].str.split(".").str[-1]
print(df["tld"].value_counts())

tld_counts = df["tld"].value_counts().to_dict()
plot_distribution(tld_counts, "output/email_tld_distribution.png", "Customers by email TLD")


import requests


def fetch_customers() -> list[dict]:
    response = requests.get("https://jsonplaceholder.typicode.com/users", timeout=10)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    # Steps 1-2: load the data
    customers = fetch_customers()
    print(customers[0])  # check the shape of one customer

    # Steps 3-5: counts
    cities = unique_cities(customers)
    print("Unique cities:", len(cities), "| Customers:", len(customers))

    by_city = city_counts(customers)
    by_domain = email_domain_counts(customers)
    print("City counts:", by_city)
    print("Email domain counts:", by_domain)

    # Step 6: DataFrame
    df = to_dataframe(customers)
    print("Shape:", df.shape)
    print(df.dtypes)
    print("City counts match pandas:", df["city"].value_counts().to_dict() == by_city)

    # Step 7: export
    print(pd.read_csv("output/customers.csv").head())
    print(pd.read_csv("output/city_counts.csv").head())

    # Step 8: charts
    plot_distribution(by_city, Path("output/customer_distribution.png"), title="Customers by city")
    plot_distribution(by_domain, Path("output/email_domain_distribution.png"), title="Customers by email domain")

    # Extra: TLD chart
    df["tld"] = df["email_domain"].str.split(".").str[-1]
    print(df["tld"].value_counts())
    plot_distribution(df["tld"].value_counts().to_dict(), Path("output/email_tld_distribution.png"), title="Customers by email TLD")

    print("Saved charts to output/")
