from pathlib import Path

import pandas as pd

PROJECT_DIR = Path(__file__).parent
DATA_DIR = PROJECT_DIR / "data"
CLEAN_DIR = PROJECT_DIR / "output" / "clean" / "tfl_line_status"


def load_statuses() -> pd.DataFrame:
    """Load every clean CSV into one DataFrame."""
    files = sorted(CLEAN_DIR.glob("date=*/*.csv"))
    df = pd.concat((pd.read_csv(f) for f in files), ignore_index=True)
    df["fetched_at"] = pd.to_datetime(df["fetched_at"])
    return df


def main() -> None:
    df = load_statuses()
    print("Rows and columns:", df.shape)
    print(df.head())
    print(df.dtypes)

    problems = df[df["status"] != "Good Service"]
    print(f"\n{len(problems)} snapshots with problems:")
    print(problems[["fetched_at", "line_name", "status"]].head(10))

    tube = df[df["mode"] == "tube"].rename(columns={"line_name": "tube_line"})
    print("\nTube lines:", sorted(tube["tube_line"].unique()))

    print("\nStatus counts:")
    print(df["status"].value_counts())

    summary = (
        df.assign(has_problem=df["status"] != "Good Service")
        .groupby(["mode", "line_id", "line_name"], as_index=False)
        .agg(snapshots=("status", "size"), problems=("has_problem", "sum"))
    )
    summary["problem_rate"] = (summary["problems"] / summary["snapshots"] * 100).round(1)
    summary = summary.sort_values(["problem_rate", "line_name"], ascending=[False, True])
    print("\nProblem rate by line:")
    print(summary.to_string(index=False))


    lines = pd.read_csv(DATA_DIR / "lines.csv")
    left = summary.merge(lines, on="line_id", how="left")
    inner = summary.merge(lines, on="line_id", how="inner")
    print(f"\nLeft join: {len(left)} rows. Inner join: {len(inner)} rows.")
    print("Lines with no colour:", list(left.loc[left["colour"].isna(), "line_name"]))

    out_path = PROJECT_DIR / "output" / "line_problem_rate.csv"
    left.to_csv(out_path, index=False)
    print(f"\nSaved {len(left)} rows to {out_path.relative_to(PROJECT_DIR)}")

if __name__ == "__main__":
    main()
    