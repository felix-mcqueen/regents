from load import run_loader
from reporting import generate_report

def main():
    company_name = "Allen-Mcguire"  # Example company name for report generation
    year = 2020  # Example year for report generation

    # STAGE 1: Run the data processor
    print("Running data loader...")
    run_loader()
    print("All company data exported to /data/processed/\n")

    # STAGE 2: Generate report for a single company
    print("Generating annual report...")
    generate_report(company_name, year)
    print(f"Report saved to /data/processed/{company_name}/report_{year}.html")

if __name__ == "__main__":
    main()
