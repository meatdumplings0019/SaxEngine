from src.Vebp.Data import VebpData


class Pack(VebpData):
    FILENAME = "vebp-pack.json"

    @staticmethod
    def generate_default() -> dict:
        return {}