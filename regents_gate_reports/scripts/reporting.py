from jinja2 import Environment, FileSystemLoader
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import io
import base64

def generate_chart(df, company, year):
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(df["date"], df["rebased"])
    ax.set_title(f"{company} Stock Price - {year}")
    ax.set_ylabel("Rebased Index (Start = 100)")
    ax.set_xlabel("Date")
    ax.grid(True)
    fig.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"

def generate_report(company: str, year: int):

    #base_path = Path(f"C:/Users/felix.mcdonald/Projects/regent/regents_gate_reports/data/processed/{company}") # path for testing locally

    this_dir = Path(__file__).resolve().parent # absolute path
    project_root = this_dir.parent
    base_path = project_root / "data" / "processed" / company

    template_dir = this_dir.parent / "templates"

    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("report.html")

    # Read csvs
    profile = pd.read_csv(base_path / "profile.csv").iloc[0]
    people = pd.read_csv(base_path / "people.csv")
    financials = pd.read_csv(base_path / "financials.csv")

    financials = financials[financials["quarter"].str.contains(str(year))]
    market = pd.read_csv(base_path / "market_data.csv", parse_dates=["date"])
    market = market[market["date"].dt.year == year].sort_values("date")

    chart_data = None
    
    # Rebase to 100 as outlined in task.md for reasonable comparison, my method was to divide all prices by the first price and multiply by 100. this set the first price
    # to 100 and all other prices relative to that.
    if not market.empty:
        market["rebased"] = 100 * market["last_price"] / market["last_price"].iloc[0]
        chart_data = generate_chart(market, company, year)

    html = template.render(
        company=company,
        year=year,
        profile=profile,
        people=people.to_dict(orient="records"),
        financials=financials.to_dict(orient="records"),
        chart_data=chart_data
    )

    with open(base_path / f"report_{year}.html", "w") as f:
        f.write(html)
