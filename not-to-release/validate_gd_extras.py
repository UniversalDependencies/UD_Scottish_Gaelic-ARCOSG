"""
Checks for things that aren't covered by the standard UD validation tools.

Some of these are specific to Scottish Gaelic and others are generic.
"""
import sys
from collections import Counter
from udapi.core.document import Document

def check_bi(node) -> int:
    """
    Checks that the verb _bi_ does not have a node linked to it that should be linked by xcomp:pred.
    Candidate relations are obl, xcomp, obl:smod and advmod.
    Note that in the last case there are adverbs that won't be suitable if they are adverbs of time.
    We also use OblType in the MISC column for phrases like "mar eisimpleir" = 'for example'.

    Returns an integer with the count of errors.
    """
    errors = 0
    deprels = [c.deprel for c in node.children]
    if "xcomp:pred" not in deprels and deprels != []:
        possible_predicates = [n for n in node.children if possible_predicate(n)]
        if possible_predicates != []:
            print(f"E {node.address()} should have an xcomp:pred among {possible_predicates}")
        objs = [p for p in possible_predicates if p.deprel == "obj" and p.upos != "PART"]
        for obj in objs:
            # check what Irish does about obj of bi.
            errors += 1
            print(f"E {obj.address()} bi should not have obj")
    return errors

def check_clause_types(node, speech_lemmata) -> (int, int):
    """
    Checks that mark and mark:prt and ccomp, advcl and acl:relcl work together properly.
    For example, if the head of a clause or complement is marked with both mark and mark:prt,
    mark takes precedence.

    Returns an (int, int) tuple of the number of errors and number of warnings found.
    """
    errors = 0
    warnings = 0

    ids = {}
    deprels = {}
    forms = {}
    feats = {}

    child_deprels = [c.deprel for c in node.children if c.udeprel == "mark"]
    if "mark" in child_deprels:
        if node.udeprel != "advcl" and node.parent.lemma not in speech_lemmata:
            warnings += 1
            print(f"W {node.address()} deprel should be advcl:* not {node.deprel}")                
    elif "mark:prt" in child_deprels:
        particle_children = [c for c in node.children if c.upos == "PART"]
        for particle in particle_children:
            if particle.feats["PartType"] == "Cmpl" and node.deprel != "ccomp":
                warnings += 1
                print(f"W {node.address()} deprel should be ccomp not {node.deprel}")
            if particle.feats["PronType"] == "Rel" and node.deprel != "acl:relcl":
                warnings += 1
                print(f"W {node.address()} deprel should be acl:relcl not {node.deprel}")
    return errors, warnings

def check_cleft(node) -> int:
    """
    Checks that CleftType has been correctly assigned to the head of a cleft.
    Returns an integer with the count of errors.
    """
    errors = 0
    child_deprels = [c.deprel for c in node.children]
    if "csubj:cleft" in child_deprels or "csubj:outer" in child_deprels:
        if "CleftType" not in node.feats:
            errors += 1
            print(f"E {node.address()} is a cleft and should have CleftType")
    if "csubj:cleft" not in child_deprels and "csubj:outer" not in child_deprels and "CleftType" in node.feats:
        cleft_phrase = " ".join([d.form for d in node.descendants(add_self = True)])
        errors += 1
        print(f"E {node.address()} '{cleft_phrase}' is not a cleft and '{node.form}' should not have CleftType")
    return errors

def check_closed_classes(sentence) -> int:
    """
    Some parts of speech do not readily take new members - prepositions, conjunctions and
    determiners for example. This means we can write a list of allowed lemmata and check
    against them as unlisted ones are likely to be tagging errors.
    """
    errors = 0
    """
    Notes:
    ADP: 'ar' is a variant of 'thar' here, 'ma' is a variant of 'mu'.
    DET: 'sa' is a variant of 'seo'
    """

    allowed = {
        "ADP": [
            "a", "à", "ach", "ag", "an", "aig", "air", "ar", "as", "ás", "bho", "cum", "de", "do", "eadar", "fa",
            "far", "fo", "gun", "gu", "gus", "le", "ma", "mar", "mu", "mun", "na", "o", "os", "rè",
            "ri", "ro", "roimh", "seach", "thar", "tre", "treimh", "tro", "troimh", "tarsaing", "tarsainn",
            "tarsuinn",
            "aindeoin", "ainneoin", "airson", "a-measg", "am-measg", "aonais", "a-rèir", "a-réir",
            "a-thaobh", "beul",
            "broinn", "cionn", "cùl", "deidh",
            "dèidh", "déidh", "deidhinn", "feadh", "lùib", "measg", "rèir", "ruige", "réir", "sgath", "son",
            "taca", "timcheall", "timchioll"
        ],
        "DET": [
            "a", "an", "ar", "do", "gach", "mo", "sa", "san", "seo", "sin", "sineach", "siud", "ud",
            "uile", "ur"
        ],
        "CCONJ": [
            "a", "ach", "agus", "air", "is", "na", "neo", "no", "so", "oir", "sgàth", "thoireadh",
            "thoradh"
        ],
        "PRON": [
            "na",
            "mo", "do", "a", "ar", "ur", "an",
            "mi", "thu", "e", "i", "sinn", "sibh", "iad",
            "seo", "so", "sin", "sean", "siud", "siod",
            "a-seo", "a-sin", "a-siud",
            "seothach", "sineach", "siudach", "siodach",
            "fèin", "féin", "cèile", "céile", "a-chèile",
            "bè", "cà", "cà'", "c'à", "càil", "càit", "càite", "carson", "cia", "ciamar", "cò", "có", "cuine",
            "dè", "dé", "diamar", "ge", "b'e", "gu", "mar", "mheud", "car", "son",
            "gar", "bith", "brith"
        ],
        "SCONJ": [
            "a", "'air", "air", "airson", "'ar", "agus", "am", "an", "aon", "as",
            "bho", "bhon", "bho'n", "bith", "brì", "brith",
            "chionn", "co-dhiù",
            "fad", "far", "feadh", "fhad", "fiù",
            "gair", "ge", "ged", "gu", "gus", "is", "leis", "linn",
            "ma", "man", "mar", "mara", "mas", "mu", "mun", "mur", "mura", "mus",
            "nuair", "'nuair", "ò", "o", "o'n", "on", "ri", "sailleadh", "seach", "sgàth",
            "theagamh", "uair"
        ]
    }
    
    if node.misc["ModernLemma"] != "":
        lemma = node.misc["ModernLemma"]
    elif node.misc["CorrectLemma"] != "":
        lemma = node.misc["CorrectLemma"]
    else:
        lemma = node.lemma
    if "Foreign" not in node.feats and node.xpos != "Xsi" and lemma not in allowed[node.upos]:
        errors += 1
        print(f"E {node.address()} '{lemma}' not allowed for {node.upos} ({node.xpos})")
    return errors

def check_csubj(node) -> int:
    """
    Checks that the heads of the cop relation do not have nodes linked to them that should be linked
    by csubj:cleft or csubj:cop.
    Candidate relations are acl, acl:relcl, ccomp and xcomp.

    Returns an integer with the count of errors.
    """
    errors = 0
    csubj_candidates = ["xcomp", "acl", "ccomp", "acl:relcl"]
    allowed_deprels = ["csubj:cleft", "csubj:cop", "nsubj"]
    child_deprels = [c.deprel for c in node.children]
    if "cop" in child_deprels:
        print("{node.address() check this {child_deprels}")
    return errors

def check_feats_column(node) -> int:
    """
    Checks the FEATS column for
    1. ExtPos if the node is head of the fixed relation
    2. AdvType for ADV.
    3. NounType for PROPN.

    Returns an integer with the number of errors found.
    """
    errors = 0
    allowed_advtypes = ["Conj", "Man", "Loc", "Tim"]
    allowed_nountypes = ["Chr", "Cmn", "Eth", "Glt", "Nau", "Nos", "Org", "Prs", "Top"]
    if node.deprel == "fixed" and node.prev_node.deprel != "fixed":
        if "ExtPos" not in node.prev_node.feats:
            errors += 1
            print(f"E {node.prev_node.address()} head of fixed should have ExtPos feature")
    if "AdvType" in node.feats:
        if node.feats["AdvType"] not in allowed_advtypes:
            errors += 1
            print(f"E {node.address()} Unrecognised AdvType {node.feats['AdvType']}")
    if node.upos == "PROPN" and "NounType" not in node.feats:
            errors += 1
            print(f"E {node.address()} NounType must be in FEATS for PROPN '{node.form}'")
    if "NounType" in node.feats:
        if node.feats["NounType"] not in allowed_nountypes:
            errors += 1
            print(f"E {node.address()} Unrecognised NounType {node.feats['NounType']}")
    return errors

def read_fixed():
    """
    Returns a dictionary of lemmata keyed by surface.
    The lemmata are n - 1 and the surface is n.
    """

    allowed = {}
    with open("fixed.gd") as fixed:
        for phrase in fixed:
            words = phrase.split()
            if len(words) > 3:
                if words[3] in allowed:
                    allowed[words[3]].append(words[2])
                else:
                    allowed[words[3]] = [words[2]]
            if len(words) > 2:
                if words[2] in allowed:
                    allowed[words[2]].append(words[1])
                else:
                    allowed[words[2]] = [words[1]]
            if words[1] in allowed:
                allowed[words[1]].append(words[0])
            else:
                allowed[words[1]] = [words[0]]
    return allowed

def check_fixed_expressions(node, allowed_fixed) -> int:
    """
    Checks words linked by `fixed` against the list read in in read_fixed().

    Prints errors and returns the error count.
    """
    errors = 0
    norm_node_form = node.form.lower().replace("‘", "'").replace("’", "'")
    if node.misc["CorrectForm"] != "":
        norm_node_form = node.misc["CorrectForm"]
    elif node.misc["ModernForm"] != "":
        norm_node_form = node.misc["ModernForm"]
    norm_prev_node_form = node.prev_node.form.lower().replace("‘", "'").replace("’", "'")
    if node.prev_node.misc["CorrectForm"] != "":
        norm_prev_node_form = node.prev_node.misc["CorrectForm"]
    elif node.prev_node.misc["ModernForm"] != "":
        norm_prev_node_form = node.prev_node.misc["ModernForm"]
    if norm_node_form not in allowed_fixed:
        errors +=1
        print(f"E {node.address()} '{node.form}' not in fixed list")
    elif norm_prev_node_form not in allowed_fixed[norm_node_form]:
        errors +=1
        print(f"E {node.address()} '{norm_prev_node_form} {norm_node_form}' not in fixed list")
    return errors

def check_misc_column(node) -> int:
    """
    Checks the MISC column for ARCOSG-specific features and Scottish Gaelic-specific features.

    Returns an integer with the number of errors found.
    """
    errors = 0
    allowed_flattypes = ["Borrow", "Date", "Top", "Num", "Redup", "Name", "Foreign", "Time"]
    if node.lemma in ["[Name]", "[Placename]"] and "Anonymised" not in node.misc:
        errors += 1
        print(f"E {node.address()} Anonymised=Yes missing from MISC column")
    if node.udeprel == "flat" and "FlatType" not in node.misc:
        errors += 1
        print(f"E {node.address()} FlatType required for flat:* deprel")
    if "FlatType" in node.misc:
        if node.udeprel != "flat":
            errors += 1
            print(f"E {node.address()} FlatType not allowed for non-flat deprel")
        if node.misc["FlatType"] not in allowed_flattypes:
            errors += 1
            print(f"E {node.address()} Unrecognised FlatType {node.misc['FlatType']}")
    return errors

def check_others(sentence) -> int:
    """
    Checks for things that don't fit in anywhere else.

    Specifically:
    * that _ais_ is tagged as a NOUN
    * that patronymics are tagged as part of a longer name
    * that the mark deprel is only used for PART and SCONJ
    """
    errors = 0
    if node.form == "ais" and node.upos != "NOUN":
        errors +=1
        print(f"E {node.address()} UPOS for 'ais' should be NOUN")    
    if node.xpos == node.upos and node.feats == {}:
        errors +=1
        print(f"E {node.address()} XPOS {node.xpos} should not match UPOS if feats is empty")
    if node.xpos == "Up" and node.deprel != "flat:name" and node.prev_node.xpos == "Nn":
        errors += 1
        print(f"E {node.address()} Patronymic should be flat:name")
    if node.deprel is None:
        errors += 1
        print(f"E {node.address()} deprel must not be None")
    elif node.udeprel == "mark" and node.upos not in ["PART", "SCONJ"]:
        errors += 1
        print(f"E {node.address()} mark should only be for PART or SCONJ")
    return errors

def check_proper_names(sentence) -> (int, int):
    """
    https://github.com/UniversalDependencies/UD_Scottish_Gaelic-ARCOSG/issues/52

    Checks that surfaces indicating determiners or adjectives are tagged grammatically
    rather than with flat:name.

    Returns an integer number of errors.
    """
    errors = 0
    warnings = 0
    topo_surfaces = ["am", "an", "a'", "na" ,"nan", "nam", "ear", "tuath", "deas", "iar",
                     "meadhonach"]
    patro_surfaces = ["mac", "nic", "'ic"]
    if node.deprel == "flat:name":
        if node.form.lower() in surfaces or node.lemma.lower() in topo_surfaces:
            errors += 1
            print(f"E {node.address()} deprel should reflect the grammar")
    if node.upos == "PROPN" and word.form.lower() in patro_surfaces:
        errors += 1
        print(f"E {node.address()} UPOS should be PART")
    if node.upos == "PROPN" and node.prev_node.upos == "DET" and node.deprel == "flat:name":
        warnings +=1
        print(f"W {node.address()} consider nmod")
    if node.upos == "PROPN" and node.feats["Case"] == "Gen" and node.deprel == "flat:name":
        warnings +=1
        print(f"W {node.address()} consider nmod")
    return errors, warnings

def check_oblique_marking(node) -> int:
    """
    https://github.com/UniversalDependencies/UD_Scottish_Gaelic-ARCOSG/issues/45

    Words linked to their heads by nmod or obl should be marked with a case deprel
    or have Case=Dat or Case=Gen.

    https://github.com/UniversalDependencies/UD_Scottish_Gaelic-ARCOSG/issues/51
    Added check for Promoted in the MISC column to waive the error when a sentence is incomplete.
    """
    errors = 0
    if node.deprel in ["obl:smod", "obl:tmod"]:
        errors += 1
        print(f"E {node.address()} {node.deprel}: this deprel is obsolete")
    if node.deprel in ["nmod", "obl"] and "Promoted" not in node.misc:
        child_deprels = [c.deprel for c in node.children]
        if "case" not in child_deprels and node.feats["Case"] not in ["Dat", "Gen"]:
            errors += 1
            print(f"E {node.address()} UNMARKED '{node.form}' should be {node.udeprel}:unmarked")
    if node.deprel in ["nmod:unmarked", "obl:unmarked"]:
        child_deprels = [c.deprel for c in node.children]
        if "case" in child_deprels and node.feats["Case"] in ["Dat", "Gen"]:
            errors += 1
            print(f"E {node.address()} MARKED {node.udeprel} should not be tagged unmarked")
    return errors


def check_ranges(node) -> (int, int):
    """
    Checks that deprels that can only go in one direction go in that direction and
    does some sense checks on the length.

    Numbers are difficult so there are special cases built in for _ceud_ 'hundred',
    _fichead_ 'twenty' and symbols.

    Returns a tuple of the errors found and warnings found.
    """
    leftward_only = ["acl:relcl", "flat", "fixed"]
    rightward_only = ["case", "cc", "cop", "mark"]
    short_range = {"compound": 3, "det": 3, "fixed": 3, "flat": 4}
    errors = 0
    warnings = 0
    if node.deprel in leftward_only and node.parent > node:
        warnings += 1
        print(f"W {node.address()} {node.deprel} goes wrong way (usually) for gd")
    elif node.deprel in rightward_only and node.parent < node:
        errors += 1
        print(f"E {node.address()} {node.deprel} goes wrong way for gd")
    elif node.deprel == "nummod" and node.parent < node:
        if node.parent.upos != "SYM" and node.prev_node.xpos != "Uo":
            errors += 1
            print(f"E {node.address()} nummod goes wrong way for gd")
    if node.deprel in short_range:
        range = abs(node.ord - node.parent.ord)
        if range > short_range[node.deprel]:
            if range < short_range[node.deprel] + 3:
                warnings += 1
                code = "W"
            else:
                errors += 1
                code = "E"
            print(f"{code} {node.address()} Too long a range ({range}) for {node.deprel}")
    if node.deprel in ["nsubj", "obj"] and\
           node.upos not in ["NOUN", "PART", "PRON", "PROPN", "NUM", "SYM", "X"] and\
           node.parent < node:
            if "ExtPos" in node.feats:
                pass
            else:
                errors +=1
                print(f"E {node.address()} nsubj and (rightward) obj should only be for NOUN, PART, PRON, PROPN, NUM, SYM or X")
    return errors, warnings

def check_parent_upos(node) -> int:
    """
    Checks that for example obl is headed by something verbal and nmod something nominal.
    See https://github.com/UniversalDependencies/UD_Scottish_Gaelic-ARCOSG/issues/46 for more details.

    Returns an integer number of errors found in the sentence
    """
    errors = 0
    allowed_parent_upos = {
        "acl": ["NOUN"],
        "acl:relcl": ["NOUN", "NUM", "PART", "PRON", "PROPN"],
        "advcl:relcl": ["ADJ", "ADV", "VERB"],
        "obl": ["VERB", "ADJ", "ADV"],
        "nmod": ["NOUN", "NUM", "PART", "PRON", "PROPN", "SYM", "X"],
        "appos": ["NOUN", "NUM", "PART", "PRON", "PROPN", "SYM", "X"]
    }
    if node.deprel in allowed_parent_upos and "VerbForm" not in node.parent.feats:
        if node.parent.upos not in allowed_parent_upos[node.deprel]:
            errors += 1
            print(f"E {node.parent.address()} parent of '{node.form}' ({node.address()}/{node.deprel}) must be one of ({', '.join(allowed_parent_upos[node.deprel])}) not {node.parent.upos}")
    return errors


def check_reported_speech(root, speech_lemmata) -> int:
    """
    See https://universaldependencies.org/u/dep/ccomp.html

    Reported speech is ccomp of the verb of saying except where that interrupts speech, in which
    case parataxis is used.
    In that case the speech verb attaches to the root of the reported speech.
    """
    errors = 0
    nodes = root.descendants()
    root_id = [o.ord for o in root.children][0]
    quotes = [n for n in nodes if n.xpos in ["Fq", "Fz"]]
    speech_blocks = []
    open_quote = None
    root_in_quote = False
    for quote in quotes:
        if quote.xpos == "Fq":
            open_quote = quote.ord
        if quote.xpos == "Fz":
            if open_quote is not None:
                speech_blocks.append((open_quote, quote.ord))
                if open_quote < root_id < quote.ord:
                    root_in_quote = True
                open_quote = None
            else:
                speech_blocks.append((1, quote.ord))
                if root_id < quote.ord:
                    root_in_quote = True
    if open_quote is not None:
        speech_blocks.append((open_quote, len(nodes) - 1))
        root_in_quote = True
    parataxes = [n for n in nodes if n.deprel == "parataxis"]
    if speech_blocks != [] and parataxes != []:
        if speech_blocks[0][0] < 2 and not root_in_quote:
            errors += 1
            print(f"E {root.address()} root should be inside quote")
    if speech_blocks == [] or speech_blocks[0][0] > 2:
        for parataxis in parataxes:
            if parataxis.parent.lemma in speech_lemmata and parataxis.lemma != "arsa":
                errors += 1
                print(f"E {parataxis.address()} deprel should be ccomp")
    return errors

def check_parent_deprel(node) -> int:
    """
    Currently checks two deprels:
    that cc connects a conjunction to a node that is linked to its parent by conj.
    that case has a target that has an allowed deprel to its parent.
    There is an additional check for 'case' that the target of case is not a clefted expression.

    Returns an integer number of errors.
    """
    errors = 0
    generic_deprels = ["parataxis", "reparandum", "root"]
    allowed_parent_deprels = {
        "cc": ["conj"],
        "case": ["dep", "obl", "advmod", "nmod", "nummod", "xcomp", "xcomp:pred", "ccomp",\
                 "acl", "acl:relcl", "conj", "csubj:cop"]
    }
    if node.deprel in allowed_parent_deprels and node.feats.get("CleftType") is None:
        correct = [*allowed_parent_deprels[node.deprel], *generic_deprels]
        if node.parent.deprel not in correct:
            errors +=1
            print(f"E {node.address()}-{node.parent.address()} deprel must be one of {correct} not {node.parent.deprel}")
    return errors

def check_multiples(node) -> int:
    """
    Checks for multiple nsubjs, objs or xcomp:preds.
    Returns an integer number of errors.
    """
    errors = 0
    singleton_deprels = ["nsubj", "obj", "xcomp:pred"]
    for singleton_deprel in singleton_deprels:
        children = [c for c in node.children if c.deprel == singleton_deprel]
        if len(children) > 1:
            errors += 1
            print(f"E {node.address()} too many {singleton_deprel} ({[c.ord for c in children]}) for '{node.form}'")
    return errors

def check_mwes(node) -> int:
    """
    Checks for multiword tokens in the UD sense like leam and rium that should be broken up.
    """
    errors = 0
    mwes = ["agam", "agat", "aige", "aice", "againn", "agaibh", "aca",
            "dhomh", "dhut", "dhi", "dhuinn", "dhaibh", "dhiubh",
            "leam", "leat", "leatha", "leotha", "rium", "riut", "rithe", "f'a", "fodha", "uam"]
    dubia = ["ann", "leis", "ris"]
    dubia_exceptions = ["am", "an", "a", "gach", "a-seo", "a-seothach", "a-sin", "a-sineach", "a-siud", "na", "gu", "nach"]
    if node.misc["CorrectForm"] != "":
        norm_node_form = node.misc["CorrectForm"]
    elif node.misc["ModernForm"] != "":
        norm_node_form = node.misc["ModernForm"]
    else:
        norm_node_form = node.form
    if norm_node_form.lower() in mwes and node.upos == "ADP":
        errors += 1
        print(f"E {node.address()} '{node.form}' is a MWE and should be split up")
    if node.next_node is not None:
        if node.next_node.misc["CorrectLemma"] != "":
            norm_next_node_lemma = node.next_node.misc["CorrectLemma"]
        elif node.next_node.misc["ModernLemma"] != "":
            norm_next_node_lemma = node.next_node.misc["ModernLemma"]
        else:
            norm_next_node_lemma = node.next_node.lemma
        if norm_node_form in dubia and norm_next_node_lemma not in dubia_exceptions:
            print(f"? {node.address()} '{node.form}' is probably a MWE as the next token is '{node.next_node.form}' (lemma '{node.next_node.lemma}')")
    return errors

def check_relatives(node) -> int:
    """
    Checks the deprel for relative particles.

    Where they are acting pronominally they should have the deprel that reflects its use
    in the sentence, say `nsubj` when it is acting as a subject.
    """
    errors = 0
    message_stub = f"{node.address()} deprel for '{node.form}'"
    if node.prev_node.upos == "ADP":
        errors += 1
        print(f"E {message_stub} should be obl:unmarked, nmod:unmarked or xcomp:pred")
    elif node.prev_node.lemma in ["carson", "ciamar", "cuine", "cuin'"]:
        errors += 1
        print(f"E {message_stub} should be advmod or xcomp:pred")
    elif node.prev_node.upos not in ["CCONJ", "SCONJ"] and not node.prev_node.is_root():
        errors += 1
        print(f"E {message_stub} should usually be nsubj or obj")
    return errors

def check_child_upos(node) -> int:
    """
    Checks that, for example, the part of speech of a node linked by amod is ADJ
    Returns an integer number of errors.

    https://github.com/UniversalDependencies/UD_Scottish_Gaelic-ARCOSG/issues/45
    Added more checks for nmod:unmarked, obl:unmarked and removed ADJ and DET from most lists.

    https://github.com/UniversalDependencies/UD_Scottish_Gaelic-ARCOSG/issues/51
    Added check for Promoted in the MISC column to waive the error when a sentence is incomplete.
    """
    errors = 0
    allowed_upos = {
        "amod": ["ADJ"],
        "flat:name": ["NUM", "PART", "PROPN"],
        "nmod": ["NOUN", "NUM", "PART", "PRON", "PROPN", "X"],
        "nmod:poss": ["DET", "PRON"],
        "nmod:unmarked": ["NOUN", "NUM", "PART", "PRON", "PROPN", "X"],
        "obl": ["NOUN", "NUM", "PART", "PRON", "PROPN", "X"],
        "obl:unmarked": ["NOUN", "NUM", "PART", "PRON", "PROPN", "X"]
    }
    children = [c for c in node.children if c.deprel in allowed_upos and "Promoted" not in c.misc]
    for child in children:
        extpos = child.feats.get("ExtPos")
        if child.upos not in allowed_upos[child.deprel]:
            if extpos is None or extpos not in allowed_upos[child.deprel]:
                errors += 1
                print(f"E {child.address()} '{child.lemma}': {child.upos} should be one of {allowed_upos[child.deprel]}")
    return errors

def possible_predicate(node) -> bool:
    """
    Given a node, check whether it could be a predicate of the verb _bi_.
    There are special rules for advmod and obl.
    If the advmod or obl indicates time or manner then it is not a predicate.

    Returns a boolean.
    """
    if node.deprel in ["xcomp", "xcomp:pred"]:
        return True
    if node.deprel == "advmod":
        if node.feats["AdvType"] is not None:
            return "Loc" in node.feats["AdvType"]
        return False
    if node.deprel in ["obl", "obl:unmarked"]:
        if node.misc["OblType"] is not None:
            return "Loc" in node.misc["OblType"]
        return True
    return False

def check_passive(node) -> int:
    """
    Checks for the deprecated pattern where rach is the head and the infinitive is the dependent.

    The correct pattern is for the infinitive to be the head and rach to be connected with aux:pass.

    The exceptions are where rach indicates motion, and the heuristics are:
    * if the verbal noun has an object
    * if the verbal noun is in an expression like "air chall" or "air dhith"
    * if a spatial adverb qualifies rach
    * rach + aig... + infinitive which is not deprecated. (example n02_026 in test)

    Returns an integer of the number of errors.
    """
    errors = 0
    intransitives = ["coisich", "fuirich", "ruith"]
    xcomps = [c for c in node.children if c.deprel == "xcomp" and c.lemma not in intransitives]
    for xcomp in xcomps:
        objs = [c for c in xcomp.children if c.deprel == "obj"]
        airs = [c for c in xcomp.children if c.deprel == "case" and c.lemma == "air"]
        spatial_advs = [c for c in node.children if c.deprel == "advmod" and c.feats["AdvType"] == "Loc"]
        spatial = len(spatial_advs) + len(airs) + len(objs) > 0
        rach_aig = False
        for oblique in [c for c in node.children if c.deprel == "obl"]:
            if len([c for c in oblique.children if c.deprel == "case" and c.lemma == "aig"]) > 0:
                rach_aig = True
        if not rach_aig and not spatial:
            errors += 1
            print(f"E {node.address()} should not be the head in this passive construction. Suggest {xcomp.address()}")
    return errors

def check_passive_agent(node) -> int:
    """
    Checks infinitives for (a) being passive and (b) having candidates for obl:agent.

    Returns an integer of the number of errors.
    """
    if "aux:pass" in [c.deprel for c in node.children]:
        for oblique in [c for c in node.children if c.deprel == "obl"]:
            adps = [a for a in oblique.children if a.deprel == "case"]
            for adp in [l for l in adps if l.lemma == "le"]:
                print(f"? {adp.parent.address()} consider obl:agent")
    return 0

allowed_fixed = read_fixed()
speech_lemmata = ["abair", "aidich", "bruidhinn", "cabadaich", "can", "èigh", "faighnich",
                      "foighneach", "freagair", "inns"]
total_errors = 0
total_warnings = 0
document = Document(filename = sys.argv[1])
for b in document.bundles:
    root = b.get_tree()
    nodes = root.descendants
    total_errors = total_errors + check_reported_speech(root, speech_lemmata)
    for node in nodes:
        errors, warnings = check_ranges(node)
        total_errors = total_errors + errors
        total_warnings = total_warnings + warnings
        total_errors = total_errors + check_feats_column(node)
        total_errors = total_errors + check_misc_column(node)
        total_errors = total_errors + check_mwes(node)
        total_errors = total_errors + check_others(node)
        if not node.is_root():
            total_errors = total_errors + check_parent_deprel(node)
            total_errors = total_errors + check_parent_upos(node)
        if node.lemma == "bi":
            total_errors = total_errors + check_bi(node)
        if node.children != []:
            total_errors = total_errors + check_child_upos(node)
            total_errors = total_errors + check_cleft(node)
            total_errors = total_errors + check_multiples(node)
        if node.upos in ["ADP", "CCONJ", "DET", "PRON", "SCONJ"]:
            total_errors = total_errors + check_closed_classes(node)
        if node.deprel in ["acl:relcl", "advcl", "advcl:relcl", "ccomp"]:
            errors, warnings = check_clause_types(node, speech_lemmata)
            total_errors = total_errors + errors
            total_warnings = total_warnings + warnings
        if node.deprel == "fixed":
            total_errors = total_errors + check_fixed_expressions(node, allowed_fixed)
        if node.udeprel in ["nmod", "obl"]:
            total_errors = total_errors + check_oblique_marking(node)
        if node.lemma == "rach" and node.upos == "VERB":
            total_errors = total_errors + check_passive(node)
        if node.feats["VerbForm"] == "Inf":
            total_errors = total_errors + check_passive_agent(node)
        if node.xpos in ["Q-r", "Qnr"] and node.deprel == "mark:prt":
            total_errors = total_errors + check_relatives(node)

if total_errors == 0:
    if total_warnings == 0:
        print("*** PASSED ***")
    else:
        print(f"*** PASSED *** with {total_warnings} warnings")
else:
    print(f"*** FAILED *** with {total_errors} error{'s' if total_errors != 1 else ''} and {total_warnings} warning{'s' if total_warnings != 1 else ''}")

