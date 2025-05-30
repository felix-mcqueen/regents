from load import run_loader
from reporting import generate_report
from pathlib import Path

def main():
    report_year = 2020

    # STAGE 1: Process raw data
    print("🔄 Running data loader...")
    run_loader()
    print("✅ All company data exported to /data/processed/\n")

    # STAGE 2: Generate reports for all companies
    this_dir = Path(__file__).resolve().parent
    project_root = this_dir.parent
    processed_dir = project_root / "data" / "processed"

    companies = [folder.name for folder in processed_dir.iterdir() if folder.is_dir()]

    print(f"📝 Generating annual reports for all companies ({report_year})...")
    for company in companies:
        try:
            generate_report(company, report_year)
            print(f"{company} - report saved.")
        except Exception as e:
            print(f"{company} - failed to generate report: {e}")

if __name__ == "__main__":
    main()
