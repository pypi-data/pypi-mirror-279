import yaml
from pathlib import Path
from pyperclip import copy
from loguru import logger

logger.disable(__name__)


class E:
    def __init__(self):
        path = Path(__file__).parent / "src"
        logger.info(path)
        self.data: dict = self.__parse_files(path)

    def __parse_files(self, path):
        all_data = {}
        for file in path.iterdir():
            if file.suffix == ".yaml":
                with open(file, encoding="utf-8") as f:
                    all_data.update(yaml.full_load(f))
        return all_data

    @staticmethod
    def __top_index(keys):
        keys = [str(key).lower() for key in keys]
        all_keys = {}
        for key in keys:
            for le in range(len(key), 2, -1):
                for start in range(len(key) - le):
                    all_keys[key[start : start + le]] = le / len(key)

        def wrap(data):
            text = data.get("text", "") + " ".join(
                map(str, data.get("keywords", None) or [])
            )
            text = text.lower()
            ind = sum(value for key, value in all_keys.items() if key in text)

            return ind

        return wrap

    def find(self, key: str, ind=0):
        keys = set(key.split())
        logger.info(keys)
        values = sorted(self.data.values(), key=self.__top_index(keys), reverse=True)
        logger.info(values[0])
        copy(values[ind]["text"])

    def __call__(self, key, ind=0):
        self.find(key, ind)
