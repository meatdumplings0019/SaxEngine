from src.Vebp.builder import Builder

b = (Builder("Test")
     .set_console(True)
     .set_script("run.py").add_assets(["README.md"], "./Sax")
     .build())
