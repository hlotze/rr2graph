"""provides io related functions"""

from datetime import datetime

import numpy as np
import pandas as pd

# ---------------------------------------------------------
# EXCEL-DATUM PARSER
# ---------------------------------------------------------


def parse_excel_date(val):
    """Parst dd.mm.YY, dd.mm.YYYY, ISO-Datum und Excel-Seriendatum."""
    try:
        excel_origin = pd.Timestamp("1899-12-30")

        # Fall 1: Excel-Seriendatum als int oder float
        if isinstance(val, (int, float)) and not pd.isna(val):
            return excel_origin + pd.to_timedelta(int(val), unit="D")

        # Fall 2: Excel-Seriendatum als String (z. B. "45231")
        if isinstance(val, str):
            s = val.strip()
            if s.isdigit():
                return excel_origin + pd.to_timedelta(int(s), unit="D")

        # Fall 3: Pandas hat es bereits als Timestamp eingelesen
        if isinstance(val, pd.Timestamp):
            delta = (val - excel_origin).days
            if 1 < delta < 60000:
                return excel_origin + pd.to_timedelta(delta, unit="D")
            return val

        # Fall 4: Normales Datum
        return pd.to_datetime(
            val,
            dayfirst=True,
            errors="coerce",
        )

    except Exception:
        return pd.NaT


# ---------------------------------------------------------
# HEART DATA
# ---------------------------------------------------------


def _to_pydate(val):
    """Konvertiert Timestamp / numpy.datetime64 /
    datetime → echtes Python date."""
    if isinstance(val, pd.Timestamp):
        return val.to_pydatetime().date()
    if isinstance(val, datetime):
        return val.date()
    if isinstance(val, np.datetime64):
        return pd.to_datetime(val).to_pydatetime().date()
    return val  # sollte nie passieren


def read_heart_data(fn: str) -> pd.DataFrame:
    df = pd.read_excel(
        fn,
        sheet_name="data",
        header=0,
        dtype=str,
        engine="openpyxl",
        keep_default_na=False,
    )

    # Leere Strings in echte NaT umwandeln
    df.loc[df["time"].str.strip() == "", "time"] = pd.NaT

    # 2. Datum robust parsen
    df["date"] = df["date"].apply(parse_excel_date)

    # 3. Zeit robust parsen
    df["time"] = pd.to_datetime(df["time"], format="%H:%M:%S", errors="coerce").dt.time

    # 4. Zeilen ohne Zeit entfernen
    df = df.dropna(subset=["time"])

    # WICHTIG: Wenn alles weg ist → sofort zurück
    if df.empty:
        return df

    # 5. date_time erzeugen
    df["date_time"] = df.apply(
        lambda r: (
            datetime.combine(_to_pydate(r["date"]), r["time"])
            if pd.notna(r["date"]) and pd.notna(r["time"])
            else pd.NaT
        ),
        axis=1,
    )

    # 6. Woche einfügen
    df.insert(0, "week", df["date_time"].dt.isocalendar().week)

    # 7. Typen korrigieren
    df["rr_syst"] = df["rr_syst"].astype("int64")
    df["rr_diast"] = df["rr_diast"].astype("int64")
    df["heart_rate"] = df["heart_rate"].astype("int64")

    # 8. Aufräumen
    df.drop(columns=["date", "time", "weight"], inplace=True)

    # 9. Nur gültige Zeilen behalten
    return df.dropna(subset=["date_time"])



# ---------------------------------------------------------
# WEIGHT DATA
# ---------------------------------------------------------


def read_weight_data(fn: str) -> pd.DataFrame:
    """Read the excel file into pd.DataFrame df_weight"""
    df = pd.read_excel(
        fn,
        sheet_name="data",
        header=0,
        keep_default_na=False,
        converters={"date": lambda x: x},
    )

    df.drop(columns=["time", "rr_syst", "rr_diast", "heart_rate"], inplace=True)

    # Datum robust parsen
    df["date"] = df["date"].apply(parse_excel_date)
    # Gewicht wird nur einmal pro Tag gemessen und
    # in den Graphiken angezeigt, auf 10:00:00
    df["date"] = df["date"].dt.normalize() + pd.Timedelta(hours=10)

    # Nur echte Datumswerte behalten
    df = df[df["date"].apply(lambda x: isinstance(x, pd.Timestamp))]

    # Gewicht robust in float konvertieren
    df["weight"] = pd.to_numeric(df["weight"], errors="coerce")

    # Nur Zeilen mit gültigem Gewicht behalten
    df = df.dropna(subset=["weight"])

    # Woche einfügen
    df.insert(0, "week", df["date"].dt.isocalendar().week)

    return df


# ---------------------------------------------------------
# TESTDATEN-GENERATOR
# ---------------------------------------------------------


def generate_test_data_xlsx() -> None:  # pragma: no cover
    """generate an Excel file with test data for 6 months"""
    days = pd.date_range(
        start=pd.Timestamp.now() - pd.DateOffset(months=6),
        end=pd.Timestamp.now(),
        freq="D",
    )

    weights = 60 + np.random.normal(loc=0, scale=1.5, size=len(days))
    df_weight = pd.DataFrame({"date": days, "weight": weights.round(1)})

    def random_time_cluster():
        cluster = np.random.choice(["morning", "noon", "evening"], p=[0.45, 0.25, 0.30])
        if cluster == "morning":
            hour = np.random.randint(6, 10)
        elif cluster == "noon":
            hour = np.random.randint(12, 15)
        else:
            hour = np.random.randint(18, 22)
        minute = np.random.choice(range(0, 60, 10))
        return pd.to_datetime(f"{hour:02d}:{minute:02d}:00").time()

    def rr_with_outliers():
        syst = np.random.randint(110, 135)
        diast = np.random.randint(65, 85)
        hr = np.random.randint(60, 95)
        if np.random.rand() < 0.05:
            syst += np.random.randint(15, 30)
            diast += np.random.randint(10, 20)
            hr += np.random.randint(15, 30)
        if np.random.rand() < 0.03:
            syst += np.random.randint(5, 15)
            diast += np.random.randint(0, 10)
            hr += np.random.randint(20, 40)
        if np.random.rand() < 0.02:
            syst += np.random.randint(20, 40)
            diast += np.random.randint(10, 25)
            hr += np.random.randint(10, 25)
        return syst, diast, hr

    records = []
    for d in days:
        n = np.random.randint(2, 5)
        for _ in range(n):
            t = random_time_cluster()
            syst, diast, hr = rr_with_outliers()
            records.append(
                {
                    "date": d,
                    "time": t,
                    "rr_syst": syst,
                    "rr_diast": diast,
                    "heart_rate": hr,
                }
            )

    df_rr = pd.DataFrame(records)
    df = df_rr.merge(df_weight, on="date", how="left")
    df["weight"] = df.groupby("date")["weight"].transform(
        lambda x: [x.iloc[0]] + [np.nan] * (len(x) - 1)
    )
    df["date"] = df["date"].dt.strftime("%d.%m.%Y")
    df["time"] = df["time"].astype(str)
    df = df[["date", "weight", "time", "rr_syst", "rr_diast", "heart_rate"]]
    df.to_excel("test_rr_data.xlsx", sheet_name="data", index=False)
    print("Fertig! Datei: test_rr_data.xlsx")
    print(df.head())
