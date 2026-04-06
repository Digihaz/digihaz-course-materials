"""DIGIHAZ shared Python utilities."""


def load_dataset(path):
    """Load a dataset from the digihaz-datasets repo."""
    import pandas as pd
    return pd.read_csv(path)
