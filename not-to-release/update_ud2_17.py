"""
Applies updates for Scottish Gaelic CONLL files for Universal Dependencies release 2.17.
"""

import sys
from udapi.core.document import Document

document = Document(filename = sys.argv[1])

genders = { "m": "Masc", "f": "Fem" }
numbers = { "s": "Sing", "p": "Plur" }
cases = { "d": "Dat", "g": "Gen"}

for b in document.bundles:
    root = b.get_tree()
    nodes = root.descendants
    for node in nodes:
        if node.upos == "DET" and node.xpos.startswith("Td"):
            """
            https://github.com/UniversalDependencies/UD_Scottish_Gaelic-ARCOSG/issues/60
            """
            if len(node.xpos) > 3:
                node.feats["Definite"] = "Def"
                node.feats["PronType"] = "Art"
                node.feats["Number"] = numbers[node.xpos[2]]
                if node.xpos[3] in ["m", "f"]:
                    node.feats["Gender"] = genders[node.xpos[3]]
                if len(node.xpos) > 4 and node.xpos[4] in ["d", "g"]:
                    node.feats["Case"] = cases[node.xpos[4]]
        if node.upos == "AUX":
            """
            https://github.com/UniversalDependencies/UD_Scottish_Gaelic-ARCOSG/issues/61
            """
            if node.xpos.startswith("W"):
                node.feats["VerbForm"] = "Fin"
                if "q" in node.xpos:
                    node.feats["Mood"] = "Int"
                else:
                    node.feats["Mood"] = "Ind"

document.store_conllu(sys.argv[2])
