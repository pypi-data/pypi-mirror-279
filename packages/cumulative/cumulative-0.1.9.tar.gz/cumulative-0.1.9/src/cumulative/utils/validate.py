import numpy as np

from cumulative.utils.warnings import warn


class ValidationWarning(UserWarning):
    pass


class Validate:
    def __init__(self, c):
        self.c = c

    def check(self, prefix: str = None):
        """
        Verify that linked cumulative data frame doesn't countain nans or infs,
        that there are both rows and columns. If issues are detected,
        a warning is generated, with `prefix` string.
        """

        df = self.c.df

        if prefix:
            prefix = "[" + prefix + "] "
        else:
            prefix = ""

        # Check for invalid values (nans, infs)
        count_rows = len(df)
        count_invalid_rows = df.isin([np.inf, -np.inf, np.nan]).any(axis=1).sum()
        if count_invalid_rows > 0:
            warn(
                f"{prefix}Invalid rows (nans or infs): "
                f"{count_invalid_rows} ({count_invalid_rows / count_rows * 100:.0f}%)",
                category=ValidationWarning,
                stacklevel=1,
            )

        # TODO: check arrays in cell values

        # Check for duplicate column names
        if len(set(df.columns)) != len(df.columns):
            warn(f"{prefix}Duplicate column names", category=ValidationWarning, stacklevel=1)

        if len(df.columns) == 0:
            warn(f"{prefix}No columns", category=ValidationWarning, stacklevel=1)

        if len(df) == 0:
            warn(f"{prefix}No rows", category=ValidationWarning, stacklevel=1)
