"""
Applies updates for Scottish Gaelic CONLL files for Universal Dependencies release 2.16.
"""
import sys
from udapi.core.document import Document

document = Document(filename = sys.argv[1])

advtype_mapping = { "Rs": "Loc", "Rt": "Tim", "Rg": "Man", "Uf": "Man", "Uq": "Man", "Xsi": "Loc" }
for b in document.bundles:
    root = b.get_tree()
    nodes = root.descendants
    for node in nodes:
        if node.xpos == "Q-s":
            """
            https://github.com/UniversalDependencies/UD_Scottish_Gaelic-ARCOSG/issues/34
            """
            node.deprel = "mark"
        if node.deprel == "fixed" and node.prev_node.deprel != "fixed":
            """
            https://github.com/UniversalDependencies/UD_Scottish_Gaelic-ARCOSG/issues/36
            """
            if "ExtPos" not in node.prev_node.feats:
                node.prev_node.feats["ExtPos"] = node.prev_node.upos
        if node.upos == "ADV":
            """
            https://github.com/UniversalDependencies/UD_Scottish_Gaelic-ARCOSG/issues/38
            """
            if node.xpos not in advtype_mapping:
                print(node.address(), node.form, node.upos, node.xpos)
            else:
                node.feats["AdvType"] = advtype_mapping[node.xpos]
        if "csubj:cleft" in [c.deprel for c in node.children]:
            """
            https://github.com/UniversalDependencies/UD_Scottish_Gaelic-ARCOSG/issues/39
            """
            if node.upos == "ADJ":
                node.feats["CleftType"] = "Adj"
            elif node.upos == "ADV":
                node.feats["CleftType"] = "Adv"
            elif node.upos == "VERB" or node.upos == "NOUN" and node.feats["VerbForm"] == "Vnoun":
                node.feats["CleftType"] = "Verb"
            elif node.upos in ["NOUN", "NUM", "PART", "PRON", "PROPN"]:
                if node.upos == "PART" and "Pat" not in node.feats["PartType"]:
                    print(f"{node.address()} {node.form} {node.upos} {node.feats}")
                elif "case" in [c.deprel for c in node.children]:
                    node.feats["CleftType"] = "Obl"
                else:
                    node.feats["CleftType"] = "Nom"
            else:
                print(f"{node.address()} {node.form} {node.upos}")
        if "csubj:cop" in [c.deprel for c in node.children]:
            """
            https://github.com/UniversalDependencies/UD_Scottish_Gaelic-ARCOSG/issues/39
            """
            node.feats.pop("CleftType", None)
        if (node.xpos.startswith("Nn") or node.xpos in ["Mr", "Up", "Xfe", "Y"]) and node.deprel == "flat:name":
            node.misc["FlatType"] = "Name"
        if node.upos == "PROPN" and "Glt" in node.feats["NounType"]:
            node.feats.pop("Number", None)
        if node.upos == "NOUN" and node.lemma == "gaidheil":
            node.feats["NounType"] = "Eth"
            node.upos = "PROPN"
        if node.upos == "NOUN" and node.lemma == "gàidhlig":
            node.feats.pop("Number", None)
            node.feats["NounType"] = "Glt"
            node.upos = "PROPN"
        if node.upos == "NOUN" and node.lemma == "gaidhealtachd":
            node.feats.pop("Number", None)
            node.feats["NounType"] = "Top"                
            node.upos = "PROPN"
        if node.upos == "PROPN" and node.xpos.startswith("Nn") and "NounType" not in node.feats:
            node.feats["NounType"] = "Prs"
        if node.deprel == "flat:foreign":
            node.misc["FlatType"] = "Foreign"
        if node.xpos == "Nt" and node.feats["NounType"] is None:
            """
            https://github.com/UniversalDependencies/UD_Scottish_Gaelic-ARCOSG/issues/40
            """
            node.upos = "PROPN"
            node.feats["NounType"] = "Top"
            if node.deprel == "flat":
                node.deprel = "flat:name"
                node.misc["FlatType"] = "Top"
        if node.xpos in ["Pd", "Px", "Uq"] and "case" not in [c.deprel for c in node.children]:
            """
            https://github.com/UniversalDependencies/UD_Scottish_Gaelic-ARCOSG/issues/45
            
            Mark:
            * demonstratives, usually "seo" or "sin",
            * interrogatives, usually "dè" or "cò", and
            * reflexives, usually "fhèin" or "fhìn" as :unmarked.
            """
            if node.deprel == "nmod":
                node.deprel = "nmod:unmarked"
            if node.deprel == "obl":
                node.deprel = "obl:unmarked"
        if node.xpos == "Q-r":
            """
            https://github.com/UniversalDependencies/UD_Scottish_Gaelic-ARCOSG/issues/45
            
            Mark relative particles as :unmarked
            """
            if node.deprel == "obl":
                node.deprel = "obl:unmarked"
        if node.xpos in ["Xa", "Y"] and node.upos != "NUM":
            """
            https://github.com/UniversalDependencies/UD_Scottish_Gaelic-ARCOSG/issues/47
            
            Mark abbreviations with `Abbr=Yes`
            """
            node.feats["Abbr"] = "Yes"

document.store_conllu(sys.argv[2])
