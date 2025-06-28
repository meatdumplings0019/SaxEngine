from src.Vebp.builder import Builder

Builder.from_package().add_assets(["README.md", "vebp-package.json"], "lib").build()