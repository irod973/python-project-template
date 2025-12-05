from loguru import logger
from metaflow import FlowSpec, IncludeFile, step


def script_path(filename):
    """
    A convenience function to get the absolute path to a file in this
    tutorial's directory. This allows the tutorial to be launched from any
    directory.

    """
    from pathlib import Path

    filepath = Path(__file__).parent / filename
    return str(filepath)

class SpinPrototypeFlow(FlowSpec):
    """Testing out the Spin feature"""

    movie_data = IncludeFile(
        "movie_data",
        default=script_path("movies.csv")
    )

    @step
    def start(self):
        import csv
        from io import StringIO

        self.rows = []
        for row in csv.reader(StringIO(self.movie_data), delimiter=","):
            logger.info(f"{row=}")
            self.rows.append(row)

        self.next(self.log_category)

    @staticmethod
    def is_category(row: list, category: str) -> bool:
        return category in row[2].split("|")

    @step
    def log_category(self):
        category = "Drama"
        logger.info(f"Logging {category=}")
        for row in self.rows:
            if self.is_category(row=row, category=category):
                logger.info(f"{row=}")
        self.next(self.end)

    @step
    def end(self):
        pass

if __name__ == "__main__":
    SpinPrototypeFlow()
