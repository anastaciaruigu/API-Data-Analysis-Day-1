# API-Data-Analysis-Day-1
My data analysis project 1
# Pesa Pulse: Customer Directory Analysis

A Python analysis of the customer directory shared by Pesa Pulse's new API partner. It answers the marketing team's first questions before they plan regional campaigns: **how many customers are there, where are they, and what does the data look like?**

Built as Day 1 of the Squad Python Specialization (Data Science, AI & Analytics).

## Background

Pesa Pulse is a Nairobi fintech start-up. Its new partner exposes a customer directory through a REST API. As the junior analyst, I pull the data, explore its nested structure, extract the attributes that matter, and answer "where are our customers?" first with plain Python structures and then with pandas, ending with a chart ready for a slide.

Data source: [JSONPlaceholder Users API](https://jsonplaceholder.typicode.com/users), a free mock endpoint returning 10 customers with nested address, geo and company objects.

## Project structure

```
.
├── analysis.py                          # Full analysis, all tasks
├── README.md
└── output/
    ├── customers.csv                    # Flat customer table
    ├── city_counts.csv                  # Customers per city
    ├── customer_distribution.png        # Customers by city
    └── email_tld_distribution.png       # Customers by email TLD
```

## How to run

1. Clone the repository and move into it.
2. Install the dependencies:
   ```bash
   pip install requests pandas matplotlib
   ```
3. Run the script:
   ```bash
   python analysis.py
   ```

The script prints its findings to the console and writes the CSVs and charts to `output/` (the folder is created if missing). Matplotlib uses the non-interactive `Agg` backend, so charts are saved to files rather than opened in a window.

## Approach

| Task | Function | What it does |
|------|----------|--------------|
| 1 | `get_customers(url)` | Fetches the API with a 10 second timeout, checks the status code with `raise_for_status()`, and returns the parsed list. On a network or HTTP error it prints a clear message and returns an empty list instead of crashing. |
| 2 | `explore(record, indent)` | Recursively walks one customer record and prints every key with its Python type, indented by depth. |
| 3 | `extract_attributes(customers)` | Returns one flat dict per customer with id, name, username, email, email domain, phone, city, zipcode, latitude, longitude, company and website. Latitude and longitude are converted to floats. |
| 4 | `unique_cities(customers)` | Uses a set comprehension to find distinct cities. |
| 5 | `city_counts(customers)`, `email_domain_counts(customers)` | City counts use a loop with `dict.get`; email domain counts use a dict comprehension. No `Counter`, no pandas. Both are printed from most to least common, with ties listed alphabetically. |
| 6 | `to_dataframe(rows)` | Builds a DataFrame, prints its shape and `dtypes`, and cross-checks the hand-written counts with `value_counts()`. |
| 7 | CSV export | Writes `output/customers.csv` and `output/city_counts.csv` without the pandas index. |
| 8 | `plot_distribution(counts, path)` | Saves a horizontal bar chart, most common category at the top. |

## Data structure

Each customer record has these top-level fields: `id`, `name`, `username`, `email`, `phone`, `website`, `address` and `company`.

**Nested attributes**

- `address` is a dictionary containing `street`, `suite`, `city`, `zipcode` and `geo`.
- `address["geo"]` is a dictionary one level deeper, containing `lat` and `lng` (stored as strings in the API, so they are converted to floats).
- `company` is a dictionary containing `name`, `catchPhrase` and `bs`.

**Reaching the deepest value**

The deepest attributes sit three levels down, at `customer["address"]["geo"]["lat"]` and `customer["address"]["geo"]["lng"]`.

## Findings

- **10 customers** in the directory.
- **10 unique cities**, so the number of unique cities equals the number of customers. Every customer lives in a different city, which tells marketing that city-level campaigns would each reach a single customer. Regional campaigns will need a coarser grouping (such as country, region or coordinate clusters) to reach meaningful numbers.
- **Email domains are also all unique** (10 domains for 10 customers), so a domain chart is just as flat as the city chart.
- **Email TLDs show real variation.** `.biz` is the most common with 3 customers, and `.tv`, `.net`, `.org`, `.ca`, `.info`, `.me` and `.io` each appear once.
- pandas agrees with the hand-written counts: `value_counts()` on `city` and on `email_domain` matches the dictionary results.

### Which chart is more useful?

`customer_distribution.png` (customers by city) is accurate but not informative: with one customer per city, every bar has the same length and there is nothing to compare. `email_tld_distribution.png` (customers by email TLD) is the more useful chart because the bars differ in height and it shows a concentration (`.biz`) that marketing can actually look at. It is the one to put on a slide, with the caveat that TLD is only a rough proxy for customer type or origin.

## Assumptions and limitations

- The API is a **mock dataset**. The names, cities and coordinates are fictional and do not reflect Pesa Pulse's real Nairobi customer base, so the findings demonstrate the method rather than real marketing insight.
- Email domains are lowercased before counting so that capitalization differences do not create duplicate domains.
- Email TLD is taken as the text after the last dot in the domain.
- `customers.csv` contains a subset of columns: `id`, `name`, `username`, `email`, `email_domain` and `city`.
- If the API request fails, the script reports the error and continues with an empty customer list, so downstream outputs will be empty.

## Skills demonstrated

Requests and APIs, JSON, nested dictionaries and lists, sets, dict comprehensions, pandas, CSV export and matplotlib visualization.
