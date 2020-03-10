import math
import pandas as pd

from typing import Any, List

class Item:
    def __init__(self, data: pd.Series, headers: List[str], sensitive_attr: str):
        """Initialises an Item object

        Args:
            data: The data that the item contains
            headers: The columns/headers that we care about anonymising

        """
        self.data: pd.Series = data
        self.headers: List[str] = headers
        self.sensitive_attr: str = data[sensitive_attr] if sensitive_attr else None
        self.parent = None

    def tuple_distance(self, t) -> float:
        """Calculates the distance between the two tuples

        Args:
            t: The tuple to calculate the distance to

        Returns: The distance to the tuple

        """
        s = self.data[self.headers]
        t = t.data[self.headers]
        error = s.sub(t).abs()
        mean_squared_error = error.pow(2).mean(axis=0)
        return math.sqrt(mean_squared_error)

    def update_attribute(self, header: str, value: float):
        """Updates a value in the tuple's data

        Args:
            header: The header to change
            value: The value to change to

        """
        self.data[header] = value

    def __getitem__(self, key: str) -> Any:
        """Gets the attribute-value for a given key

        Args:
            key: The key to get the data for

        Returns: The value for the given key

        """
        return self.data[key]

    def __str__(self) -> str:
        """Creates a string representation of the tuple
        Returns: A string representation of the tuple

        """
        return self.data.to_string()

    def __eq__(self, i):
        return self.headers == i.headers and self.data.equals(i.data)
