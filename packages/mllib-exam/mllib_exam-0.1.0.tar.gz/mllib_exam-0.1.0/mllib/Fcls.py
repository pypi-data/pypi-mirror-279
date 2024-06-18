import yaml
from pathlib import Path
from pyperclip import copy
from loguru import logger

logger.disable(__name__)


class F:
    def __init__(self):
        path = Path(__file__).parent / "src"
        logger.info(path)
        self.data: dict = self.__parse_files(path)

    def __parse_files(self, path):
        all_data = []
        for file in path.iterdir():
            if file.suffix == ".yaml":
                with open(file, encoding="utf-8") as f:
                    all_data.extend(yaml.full_load(f))
        return all_data

    @staticmethod
    def __top_index(keys):
        keys = [str(key).lower() for key in keys]

        def wrap(data):
            text = data.get("text", "") + " ".join(
                map(str, data.get("keywords", None) or [])
            )
            text = text.lower()
            ind = sum(key in text for key in keys)
            return ind

        return wrap

    def find(self, key: str, ind=0):
        if isinstance(key, int):
            return self.data[key]["text"]
        keys = set(key.split())
        logger.info(keys)
        values = sorted(self.data, key=self.__top_index(keys), reverse=True)
        logger.info(values[0])
        return values[ind]["text"]

    def __call__(self, key, ind=0):
        copy(self.find(key, ind))


if __name__ == "__main__":
    f = F()
    print(f.find("признак выбор задача признак признак", 1))
