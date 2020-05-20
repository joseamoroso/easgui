from os.path import dirname, join
from textx import language, metamodel_from_file
@language("Easgui", "*.eui")
def easgui():
    "A language for generating simple interfaces with TkInter."
    return metamodel_from_file(join(dirname(__file__), "easgui.tx"))
