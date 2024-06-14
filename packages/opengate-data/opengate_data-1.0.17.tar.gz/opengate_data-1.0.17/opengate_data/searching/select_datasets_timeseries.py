from opengate_data.utils.utils import validate_type


class SelectDatasetTimeseriesBuilder:
    def __init__(self):
        self._select_template = {"select": []}

    def add(self, fields: list[str]) -> 'SelectDatasetTimeseriesBuilder':
        """
        Adds fields to the select clause.

        Args:
            fields (list[str]): A list of fields to retrieve.

        Returns:
            SelectDatasetTimeseriesBuilder: Returns itself to allow for method chaining.

        Example:
            builder.add(["ID", "msRaw"]).add(["At"]).add(["SpecificType", "Modelo"])
        """
        validate_type(fields, list, "fields")

        for field in fields:
            validate_type(field, str, "field")
            if field not in self._select_template["select"]:
                self._select_template["select"].append(field)

        return self

    def build(self) -> list[str]:
        """
        Builds the final select clause.

        Returns:
            list[str]: The final select clause.

        Raises:
            ValueError: If no select criteria have been added.
        """
        if not self._select_template["select"]:
            raise ValueError("No select criteria have been added")
        return self._select_template["select"]
