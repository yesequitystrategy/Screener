def get_sectors(df):

    return sorted(
        df["Sector"].dropna().unique()
    )


def get_stocks(df, sector):

    return sorted(
        df[df["Sector"] == sector]["Name"].dropna().unique()
    )