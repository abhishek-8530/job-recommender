import os
import pandas as pd

# =========================
# GET PROJECT ROOT
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# =========================
# BUILD CSV PATH
# =========================
csv_path = os.path.join(BASE_DIR, "data", "roles.csv")

# =========================
# LOAD DATA SAFELY
# =========================
def load_roles():
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"❌ roles.csv not found at: {csv_path}")

    if os.path.getsize(csv_path) == 0:
        raise ValueError("❌ roles.csv is empty!")

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        raise ValueError(f"❌ Error reading CSV: {e}")

    # Validate columns
    if "role" not in df.columns or "skills" not in df.columns:
        raise ValueError("❌ CSV must contain 'role' and 'skills' columns!")

    return df


# =========================
# TEST RUN
# =========================
if __name__ == "__main__":
    roles_df = load_roles()

    print("✅ Available Job Roles:\n")
    print(roles_df["role"].to_string(index=False))