from pathlib import Path
import pandas as pd
import json
import re

# Load company data from raw csv
def load_companies(raw_dir):   
    # Find the single CSV file in companies/
    csv_file = next((raw_dir / "companies").glob("*.csv"))
    companies_df = pd.read_csv(csv_file)
    return companies_df

# Load people data from raw json files
def load_people(raw_dir, companies):
    records = []

    for file in ((raw_dir / "people").glob("*.json")):
        with open(file) as f:
            data = json.load(f)
            company_lei = data.get("lei")
            company_name = data.get("company_name")
            for person in data.get("people", []):
                records.append({
                    "lei": company_lei,
                    "company_name": company_name,
                    "person_name": person.get("name"),
                    "email": person.get("email"),
                    "title": person.get("title"),
                    "appointed": person.get("appointed")
                })
    people = pd.DataFrame(records)
    # print(f"peopledf: {people.head(10)}")
    # print(f"companiesdf: {companies.head(10)}")

    people_df = pd.merge(people, companies, on="lei", how="left")

    return people_df

# Load market data from raw parquet files

def load_market_data(raw_dir):
    # Pick a file to inspect
    file_path = next((raw_dir / "market_data").glob("*.parquet"))
    df = pd.read_parquet(file_path)
    # Check whether first row contains "last"
    if df.iloc[0].eq("last").any():
        df = df.drop(index=0).reset_index(drop=True)

    # Convert all columns to numeric (in case they're still strings)
    df = df.apply(pd.to_numeric, errors='coerce')

    # Create a placeholder date index (e.g., business days)
    df["date"] = pd.date_range(start="2020-01-01", periods=len(df), freq="B")

    # Convert from wide to tidy format
    tidy = df.set_index("date").stack().reset_index()
    # Drop the 'metric' column
    df = tidy.drop(columns=["metric"])

    # Set 'date' as index and stack
    df = df.set_index("date")
    market_df = df.stack().reset_index()

    # Rename columns
    market_df.columns = ["date", "figi", "last_price"]

    return market_df

# Extract quarter and year from sheet names using regex
def extract_quarter_key(sheet_name):
    """
    Converts sheet names like 'Q2 2021' into a (year, quarter) tuple for sorting.
    """
    match = re.match(r"Q(\d)\s+(\d{4})", sheet_name)
    if match:
        q, y = match.groups()
        return int(y), int(q)
    return (0, 0)

# Process file for a given company and saves quarterly financial data to a CSV file.
def process_financials(company_name, 
                       raw_dir
                       ):
    # print(f"company_name: {company_name}")
    file_path = raw_dir / "financial_statements" / f"{company_name}.xlsx"
    if not file_path.exists(): # In case the file does not exist
        return None
    try:
        sheet_dict = pd.read_excel(file_path, sheet_name=None, engine='openpyxl')

    except Exception as e:
        print(f"Failed to read {file_path.name}: {e}")
        return None

    sorted_sheets = sorted(sheet_dict.items(), key=lambda x: extract_quarter_key(x[0])) # Sorts shees by quarter and year using above regex function
    
    # print(f"Found sheets for {company_name}: {list(sheet_dict.keys())}")
    records = []
    for sheet_name, df in sorted_sheets:
        try:
            temp = df.set_index(df.columns[0]).T
            temp["quarter"] = sheet_name
            temp["company"] = company_name
            records.append(temp)
        except Exception:
            continue

    if not records:
        return None

    financials_df = pd.concat(records, ignore_index=True)
    # print(f"financials_df: {financials_df.head(10)}")
    return financials_df

def export_data(company_row, people_df, financials_df, market_df):
    lei = company_row["lei"]
    figi = company_row["figi"]
    name = company_row["name"]
    
    out_dir = Path("regents_gate_reports/data/processed") / name
    out_dir.mkdir(parents=True, exist_ok=True)

    # Filter components
    profile = company_row.to_frame().T
    people = people_df[people_df["lei"] == lei]
    
    financials = financials_df[financials_df["company"] == name] 
    market = market_df[market_df["figi"] == figi]

    # Write each to its own file
    profile.to_csv(out_dir / "profile.csv", index=False)
    if not people.empty:
        people.to_csv(out_dir / "people.csv", index=False)
    if not financials.empty:
        financials.to_csv(out_dir / "financials.csv", index=False)
    if not market.empty:
        market.to_csv(out_dir / "market_data.csv", index=False)

def run_loader():
   # raw_dir = Path("C:/Users/felix.mcdonald/Projects/regent/regents_gate_reports/data/raw") # path for testing locally

    this_dir = Path(__file__).resolve().parent # absolute path
    project_root = this_dir.parent

    # Reference the raw data directory
    raw_dir = project_root / "data" / "raw" 
    print("📥 Loading companies...")
    companies_df = load_companies(raw_dir)

    print("👥 Loading people...")
    people_df = load_people(raw_dir, companies_df)

    print("📊 Loading market data...")
    market_df = load_market_data(raw_dir)

    print("📈 Processing financials and exporting...")
    financials_records = []
    for company_name in companies_df["name"]:
        f_df = process_financials(company_name, raw_dir)
        if f_df is not None:
            financials_records.append(f_df)

    financials_df = pd.concat(financials_records, ignore_index=True) if financials_records else pd.DataFrame()

    for _, row in companies_df.iterrows():
        export_data(row, people_df, financials_df, market_df)

    print("✅ All company data exported to /data/processed/")
