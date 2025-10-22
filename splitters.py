import pandas as pd


def split_to_xy():
    df = pd.read_csv("dataset.csv")
    df[["Date"]].to_csv("X.csv", index=False)
    df[["INR_Rate"]].to_csv("Y.csv", index=False)
    print("✓ Созданы X.csv и Y.csv")


def split_by_years():
    df = pd.read_csv("dataset.csv")
    df["Date"] = pd.to_datetime(df["Date"])

    for year, group in df.groupby(df["Date"].dt.year):
        start_date = group["Date"].min().strftime("%Y%m%d")
        end_date = group["Date"].max().strftime("%Y%m%d")
        filename = f"{start_date}_{end_date}.csv"
        group.to_csv(filename, index=False)
        print(f"✓ {filename} ({len(group)} строк)")


def split_by_weeks():
    df = pd.read_csv("dataset.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df["YearWeek"] = (
        df["Date"].dt.isocalendar().year.astype(str)
        + "-"
        + df["Date"].dt.isocalendar().week.astype(str).str.zfill(2)
    )

    for week, group in df.groupby("YearWeek"):
        start_date = group["Date"].min().strftime("%Y%m%d")
        end_date = group["Date"].max().strftime("%Y%m%d")
        filename = f"{start_date}_{end_date}.csv"
        group[["Date", "INR_Rate"]].to_csv(filename, index=False)
        print(f"✓ {filename} ({len(group)} строк)")
