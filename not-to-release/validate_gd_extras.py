"""
Checks for things that aren't covered by the standard UD validation tools.

Some of these are specific to Scottish Gaelic and others are generic.
"""
from collections import Counter
import pyconll
import sys

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

def check_fixed(sentence):
    """
    Checks words linked by `fixed` against the list read in in read_fixed().

    Prints errors and returns the error count.
    """
    errors = 0
    allowed = read_fixed()
    for word, prev_word in ud_words(sentence, lambda t: t.deprel == "fixed"):
        norm_word_form = word.form.lower().replace("‘", "'").replace("’", "'")
        norm_prev_word_form = prev_word.form.lower().replace("‘", "'").replace("’", "'")
        if norm_word_form not in allowed:
            errors +=1
            print(f"E {sentence.id} {word.id} '{word.form}' not in fixed list")
        elif norm_prev_word_form not in allowed[norm_word_form]:
            errors +=1
            print(f"E {sentence.id} {word.id} '{prev_word.form} {word.form}' not in fixed list")
    return errors

def check_feats(sentence) -> int:
    """
    Checks the FEATS column for
    1. ExtPos if the node is head of the fixed relation
    2. Scottish Gaelic-specific features (currently AdvType).

    Returns an integer with the number of errors found.
    """
    errors = 0
    allowed_advtypes = ["Conj", "Man", "Loc", "Tim"]
    for word, prev_word in ud_words(sentence, lambda t: t.deprel == "fixed"):
        if prev_word.deprel != "fixed":
            if "ExtPos" not in prev_word.feats:
                errors += 1
                print(f"E {sentence.id} {prev_word.id} head of fixed should have ExtPos feature")
    for word in sentence:
        if "AdvType" in word.feats:
            for advtype in word.feats["AdvType"]:
                if advtype not in allowed_advtypes:
                    errors += 1
                    print(f"E {sentence.id} {word.id} Unrecognised AdvType {advtype}")
    return errors

def check_misc(sentence) -> int:
    """
    Checks the MISC column for ARCOSG-specific features and Scottish Gaelic-specific features.

    Returns an integer with the number of errors found.
    """
    errors = 0
    allowed_flattypes = ["Borrow", "Date", "Top", "Num", "Redup", "Name", "Foreign", "Time"]
    for word, _ in ud_words(sentence, lambda t: t.lemma in ["[Name]", "[Placename]"]):
        if "Anonymised" not in word.misc:
            errors += 1
            print(f"E {sentence.id} {word.id} Anonymised=Yes missing from MISC column")
    for word in sentence:
        if "FlatType" in word.misc:
            for flattype in word.misc["FlatType"]:
                if flattype not in allowed_flattypes:
                    errors += 1
                    print(f"E {sentence.id} {word.id} Unrecognised FlatType {flattype}")
    return errors

def check_others(sentence) -> int:
    """
    Checks for things that don't fit in anywhere else.

    Specifically:
    * that _ais_ is tagged as a NOUN
    * that reflexives are tagged as nmod, fixed or obl
    * that patronymics are tagged as part of a longer name
    * that the mark deprel is only used for PART and SCONJ
    * that the flat deprel is typed in the MISC column
    """
    errors = 0
    for word, prev_word in ud_words(sentence, lambda t: t.form in ["ais"] and t.upos != "NOUN"):
        errors +=1
        print(f"E {sentence.id} {word.id} UPOS for 'ais' should be NOUN")

    for word, prev_word in ud_words(sentence, lambda t: t.xpos == t.upos and t.feats == {}):
        errors +=1
        print(f"E {sentence.id} {word.id} XPOS {word.xpos} should not match UPOS if feats is empty")

    for word, prev_word in ud_words(sentence):
        if word.xpos == "Px" and word.deprel not in ["nmod", "fixed", "obl"]:
            errors += 1
            print(f"E {sentence.id} {word.id} {word.form} should be nmod or obl (or fixed)")
        if word.xpos == "Up" and word.deprel != "flat:name" and prev_word is not None and prev_word.xpos == "Nn":
            errors += 1
            print(f"E {sentence.id} {word.id} Patronymic should be flat:name")
        if word.deprel.startswith("mark") and word.upos not in ["PART", "SCONJ"]:
            errors += 1
            print(f"E {sentence.id} {word.id} mark should only be for PART or SCONJ")
        if word.deprel == "flat" and "FlatType" not in word.misc:
            errors += 1
            print(f"?E {sentence.id} {word.id} should be flat:name or flat:foreign, or FlatType should be specified")
    return errors

def check_ranges(sentence) -> (int, int):
    """
    Checks that deprels that can only go in one direction go in that direction and
    does some sense checks on the length.

    Numbers are difficult so there are special cases built in for _ceud_ 'hundred',
    _fichead_ 'twenty' and symbols.

    Returns a tuple of the errors found and warnings found.
    """
    leftward_only = ["acl:relcl", "flat", "fixed"]
    rightward_only = ["case", "cc", "cop", "mark", "nummod"]
    short_range = {"compound": 2 ,"det": 3, "fixed": 2, "flat": 4}
    errors = 0
    warnings = 0
    head_upos = {}
    for word in sentence:
        head_upos[word.id] = word.upos
    for word, prev_word in ud_words(sentence):
        deprel_range = abs(int(word.id) - int(word.head))
        if word.deprel in leftward_only and int(word.head) > int(word.id):
            warnings += 1
            print(f"W {sentence.id} {word.id} {word.deprel} goes wrong way (usually) for gd")
        if word.deprel in rightward_only and\
           int(word.head) < int(word.id) and\
           prev_word.xpos != "Uo" and\
               word.form not in ["ceud", "fichead"] and\
               head_upos[word.head] != "SYM":
            errors += 1
            print(f"E {sentence.id} {word.id} {word.deprel} goes wrong way for gd")

        if word.deprel in short_range and\
           deprel_range > short_range[word.deprel] and\
           (prev_word is not None and word.deprel != prev_word.deprel):
            if deprel_range < short_range[word.deprel] + 3:
                warnings += 1
                code = "W"
            else:
                errors += 1
                code = "E"
            print(f"{code} {sentence.id} {word.id} Too long a range ({deprel_range}) for {word.deprel}")
        if word.deprel in ["nsubj", "obj"] and\
           word.upos not in ["NOUN", "PART", "PRON", "PROPN", "NUM", "SYM", "X"] and\
           int(word.head) < int(word.id):
            if "ExtPos" in word.feats:
                pass
            else:
                errors +=1
                print(f"E {sentence.id} {word.id} nsubj and (rightward) obj should only be for NOUN, PART, PRON, PROPN, NUM, SYM or X")
    return errors, warnings

def check_heads_for_upos(sentence) -> int:
    """
    Checks that for example obl is headed by something verbal and nmod something nominal.

    Returns an integer number of errors found in the sentence
    """
    errors = 0
    head_ids = {}
    heads = {
        "acl": ["NOUN"],
        "acl:relcl": ["NOUN", "NUM", "PART", "PRON", "PROPN"],
        "advcl:relcl": ["ADJ", "ADV", "VERB"],
        "obl": ["VERB", "ADJ", "ADV"],
        "obl:smod": ["VERB", "ADJ", "ADV"],
        "obl:tmod": ["VERB", "ADJ", "ADV"],
        "nmod": ["NOUN", "NUM", "PRON", "PROPN", "SYM", "X"],
        "appos": ["NOUN", "NUM", "PRON", "PROPN", "SYM", "X"]
    }
    for word, _ in ud_words(sentence, lambda t: t.deprel in heads):
        head_ids[int(word.head)] = (word.deprel, word.id)

    for word, _ in ud_words(sentence, lambda t: int(t.id) in head_ids and "VerbForm" not in t.feats):
        actual = word.upos
        correct = heads[head_ids[int(word.id)][0]]
        if actual not in correct:
            errors +=1
            print(f"E {sentence.id} {word.id} {head_ids[int(word.id)][1]} head of {head_ids[int(word.id)]} must be one of ({', '.join(correct)}) not {actual}")
        if word.form == "ais":
            errors +=1
            print(f"E {sentence.id} {word.id} 'ais' should not be a head")
    return errors

def check_reported_speech(sentence) -> int:
    """
    See https://universaldependencies.org/u/dep/ccomp.html

    Reported speech is ccomp of the verb of saying except where that interrupts speech, in which
    case parataxis is used.
    In that case the speech verb attaches to the root of the reported speech.
    """
    speech_lemmata = ["abair", "aidich", "bruidhinn", "cabadaich", "can", "èigh", "faighnich",
                      "foighneach", "freagair", "inns"]
    errors = 0
    q = -1
    z = -1
    n_open_quotes = 0
    n_close_quotes = 0
    speech_blocks = []
    parataxes = []
    root_id = 0
    lemmata = { t.id: t.lemma for t, _ in ud_words(sentence)}
    for i, word in enumerate(sentence):
        if word.deprel == "parataxis":
            parataxes.append((word.id, word.lemma, word.head))
        if word.deprel == "root":
            root_id = int(word.id)
        if word.xpos == "Fq":
            n_open_quotes = n_open_quotes + 1
            q = word.id
        if word.xpos == "Fz" or i == len(sentence) - 1 and q != -1:
            n_close_quotes = n_close_quotes + 1
            z = word.id
            speech_blocks.append((q, z))
            q = z = -1
    if (n_open_quotes > 1 or n_close_quotes > 1) and len(parataxes) > 0:
        root_in_quote = False
        for speech_block in speech_blocks:
            if int(speech_block[0]) < root_id < int(speech_block[1]):
                root_in_quote = True
        if int(speech_blocks[0][0]) < 2 and not root_in_quote:
            errors += 1
            print(f"{sentence.id} ERROR root should be inside quote")
    if len(speech_blocks) == 0 or int(speech_blocks[0][0]) > 2:
        for parataxis in parataxes:
            if lemmata[parataxis[2]] in speech_lemmata and parataxis[1] != "arsa":
                errors += 1
                print(f"E {sentence.id} {parataxis[0]} deprel should be ccomp")
    return errors

def check_target_deprels(sentence) -> int:
    """
    Currently checks two deprels:
    that cc connects a conjunction to a node that is linked to its parent by conj.
    that case has a target that has an allowed deprel to its parent.
    There is an additional check for 'case' that the target of case is not a clefted expression.

    Returns an integer number of errors
    """
    errors = 0
    target_ids = {}
    targets = {
        "cc": ["conj"],
        "case": ["dep", "obl", "advmod", "nmod", "nummod", "xcomp", "xcomp:pred", "ccomp",\
                 "acl", "acl:relcl", "conj", "csubj:cop"]
    }
    for word, _ in ud_words(sentence, lambda t: t.deprel in targets):
        if word.feats.get("CleftType") is not None:
            target_ids[int(word.head)] = word.deprel

    for word, _ in ud_words(sentence, lambda t: int(t.id) in target_ids):
        actual = word.deprel
        correct = [*targets[target_ids[int(word.id)]], "root", "parataxis", "reparandum",\
                   "appos", "orphan"]
        if actual not in correct:
            errors +=1
            print(f"E {sentence.id} {word.id} target of {target_ids[int(word.id)]} must be one of ({', '.join(correct)}) not {actual}")
    return errors

def check_multiples(sentence) -> int:
    """
    Checks for multiple nsubjs or objs
    Returns an integer number of errors.
    """
    errors = 0
    counts = Counter()
    for word, _ in ud_words(sentence, lambda t: t.deprel in ["nsubj", "obj"]):
        key = (word.head, word.deprel)
        counts[key] += 1
    for key in counts:
        if counts[key] > 1:
            errors += 1
            print(f"E {sentence.id} Count for {key[1]} on node {key[0]} is {counts[key]} not 0 or 1")
    return errors
        
def check_target_upos(sentence) -> int:
    """
    Checks that, for example, the part of speech of a node linked by amod is ADJ
    Returns an integer number of errors.
    """
    errors = 0
    targets = {
        "amod": ["ADJ"],
        "flat:name": ["ADJ", "DET", "NUM", "PART", "PROPN"],
        "nmod": ["NOUN", "NUM", "PART", "PRON", "PROPN", "X"]
    }
    for word, _ in ud_words(sentence,\
                             lambda t: t.deprel in targets and t.upos not in targets[t.deprel]):
        errors += 1
        print(f"E {sentence.id} {word.id} UPOS for {word.deprel} must be one of ({', '.join(targets[word.deprel])}) not {word.upos}")
    return errors

def ud_words(ud_sentence, condition = lambda x: True):
    """
    Returns the 'words' and their predecessors in the UD sense by rejecting multiword tokens.
    """
    prev_word = None
    for word in [s for s in ud_sentence if not s.is_multiword()]:
        # the condition may only apply to UD words
        if condition(word):
            yield word, prev_word
        prev_word = word

def check_relatives(sentence) -> int:
    """Checks the possibilities for relative particles"""
    errors = 0
    heads = {}
    for word, prev_word in ud_words(sentence,\
                                      lambda t: t.xpos in ["Q-r", "Qnr"] and\
                                      t.deprel == "mark:prt"):
        message_stub = f"E {sentence.id} {word.id} deprel for '{word.form}'"
        if prev_word is not None:
            if prev_word.upos == "ADP":
                errors += 1
                print(f"E {message_stub} should be obl, nmod or xcomp:pred")
            elif prev_word.lemma in ["carson", "ciamar", "cuin'"]:
                errors += 1
                print(f"E {message_stub} should be advmod or xcomp:pred")
            elif prev_word.upos not in ["CCONJ", "SCONJ"]:
                heads[word.head] = []
                errors += 1
                print(f"E {message_stub} should usually be nsubj or obj")
    for word,_ in ud_words(sentence, lambda t: t.head in heads):
        heads[word.head].append(word.deprel)
    if heads:
        for head in heads:
            print(f"{sentence.id} {head} {heads[head]} suggestion: {suggest_relative_deprel(heads[head])}")
    return errors

def suggest_relative_deprel(deprels) -> str:
    """
    Suggests a deprel for the relative particle 'a'.

    Returns a string containing either "nsubj" or "obj".
    """
    if "nsubj" not in deprels:
        return "nsubj"
    return "obj"

def check_cleft(sentence) -> int:
    """
    Checks that CleftType has been correctly assigned to the head of a cleft.
    Returns an integer with the count of errors.
    """
    errors = 0
    cop_heads = [t.head for t, _ in ud_words(sentence, lambda t: t.deprel == "cop")]
    cleft_heads = [t.head for t, _ in ud_words(sentence, lambda t: t.deprel in ["csubj:cleft", "csubj:outer"])]
    for word, _ in ud_words(sentence, lambda t: t.id in cop_heads and t.feats.get("CleftType") is not None):
        if word.id not in cleft_heads:
            errors += 1
            print(f"{sentence.id} {word.id} is not a cleft and should not have CleftType")
    return errors

def check_csubj(sentence) -> int:
    """
    Checks that the heads of the cop relation do not have nodes linked to them that should be linked
    by csubj:cleft or csubj:cop.
    Candidate relations are acl, acl:relcl, ccomp and xcomp.

    Returns an integer with the count of errors.
    """
    errors = 0
    ids = {}
    deprels = {}
    csubj_candidates = ["xcomp", "acl", "ccomp", "acl:relcl"]
    cop_heads = [t.head for t, _ in ud_words(sentence, lambda t: t.deprel == "cop")]
    allowed_deprels = ["csubj:cleft", "csubj:cop", "nsubj"]
    for word, _ in ud_words(sentence, lambda t: t.head in cop_heads and t.deprel in csubj_candidates or t.deprel in allowed_deprels):
        if word.head in ids:
            ids[word.head].append(word.id)
            deprels[word.head].append(word.deprel)
        else:
            ids[word.head] = [word.id]
            deprels[word.head] = [word.deprel]
    for key in deprels:
        stub = f"E {sentence.id} {key}"
        if "csubj:cop" not in deprels[key] and "csubj:cleft" not in deprels[key] and "nsubj" not in deprels[key]:
            print(f"{stub} head of cop should have a csubj:* among {list(zip(ids[key], deprels[key]))}")
            errors +=1
    return errors

def check_bi(sentence) -> int:
    """
    Checks that the verb _bi_ does not have a node linked to it that should be linked by xcomp:pred.
    Candidate relations are obl, xcomp, obl:smod and advmod.
    Note that in the last case there are adverbs that won't be suitable if they are adverbs of time.
    We also use OblType in the MISC column for phrases like "mar eisimpleir" = 'for example'.

    Returns an integer with the count of errors.
    """
    errors = 0
    candidate_ids = {}
    candidate_deprels = {}
    candidate_upos = {}
    bi_ids = [t.id for t,_ in ud_words(sentence, lambda t: t.lemma == "bi")]

    for word, _ in ud_words(sentence, lambda t: t.head in bi_ids and possible_predicate(t)):
        if word.head in candidate_ids:
            candidate_ids[word.head].append(word.id)
            candidate_deprels[word.head].append(word.deprel)
            candidate_upos[word.head].append(word.upos)
        else:
            candidate_ids[word.head] = [word.id]
            candidate_deprels[word.head] = [word.deprel]
            candidate_upos[word.head] = [word.upos]

    for key in candidate_deprels:
        stub = f"E {sentence.id} {key}"
        if "xcomp:pred" not in candidate_deprels[key]:
            id_deprel_pairs = list(zip(candidate_ids[key], candidate_deprels[key]))
            print(f"{stub} bi should have an xcomp:pred among {id_deprel_pairs}")
            errors += 1
        if "obj" in candidate_deprels[key] and "PART" not in candidate_upos[key]:
            # check what Irish does about obj of bi.
            errors += 1
            print(f"E {stub} bi should not have obj")
    return errors

def possible_predicate(word) -> bool:
    """
    Given a word, check whether it could be a predicate of the verb _bi_.
    There are special rules for advmod and obl.
    If the advmod or obl indicates time or manner then it is not a predicate.
    Returns a boolean.
    """
    possible_deprels = ["xcomp", "obl:smod", "xcomp:pred"]
    if word.deprel in possible_deprels:
        return True
    if word.deprel == "advmod":
        if word.feats.get("AdvType") is not None:
            return "Loc" in word.feats["AdvType"]
        return False
    if word.deprel == "obl":
        if word.misc.get("OblType") is not None:
            return "Loc" in word.misc["OblType"]
        return True
    return False

def check_passive(sentence) -> int:
    """
    Checks for the deprecated pattern where rach is the head and the infinitive is the dependent.

    The correct pattern is for the infinitive to be the head and rach to be connected with aux:pass.
    Exceptions are made for where somebody goes to do something, which is similar to the deprecated
    pattern but not, of course, a passive.

    There is a further pattern rach + aig... + infinitive which is not deprecated but I haven't
    coded in.
    Example n02_026 in test.

    Returns an integer errors
    """
    errors = 0
    ids = {}
    rach_ids = [t.id for t, _ in ud_words(sentence,\
                                         lambda t: t.lemma == "rach" and t.upos != "NOUN")]
    adps = {}
    for t, _ in ud_words(sentence, lambda t: t.deprel == "case"):
        adps[t.head] = t.lemma
    for word, _ in ud_words(sentence, lambda t: t.head in rach_ids):
        if word.head in ids:
            ids[word.head].append(word.id)
        else:
            ids[word.head] = [word.id]
    for key in ids:
        indexed_deprels = [(i, sentence[i].deprel) for i in ids[key]]
        deprels = [d[1] for d in indexed_deprels]
        if "xcomp" in deprels and "nsubj" not in deprels:
            rach_aig = False
            if "obl" in deprels:
                for deprel in indexed_deprels:
                    if deprel[1] == "obl" and adps[deprel[0]] == "aig":
                        rach_aig = True
            if not rach_aig:
                for word_id in ids[key]:
                    word = sentence[word_id]
                    if word.deprel == "xcomp":
                        message_stub = f"E {sentence.id} {word.id} '{word.form}'"
                        print(f"{message_stub} should be the head")
                        errors +=1
    return errors

def check_clauses(sentence) -> (int, int):
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
    deprels_to_check = ["ccomp", "advcl", "acl:relcl"]

    clause_ids = [t.id for t in sentence if t.deprel in deprels_to_check]
    for word, _ in ud_words(sentence, lambda t: t.head in clause_ids):
        if word.head in ids:
            ids[word.head].append(word.id)
            deprels[word.head].append(word.deprel)
            forms[word.head].append(word.form)
            feats[word.head].append(word.feats)
        else:
            ids[word.head] = [word.id]
            forms[word.head] = [word.form]
            deprels[word.head] = [word.deprel]
            feats[word.head] = [word.feats]
    for key in deprels:
        if 'mark' in deprels[key]:
            if sentence[key].deprel != "advcl":
                warnings += 1
                print(f"W {sentence.id} {key} deprel should be advcl")
        elif 'mark:prt' in deprels[key]:
            for feat in feats[key]:
                if "PartType" in feat and "Cmpl" in feat["PartType"]\
                   and sentence[key].deprel != "ccomp":
                    warnings += 1
                    print(f"W {sentence.id} {key} deprel should be ccomp")
                if "PronType" in feat and "Rel" in feat["PronType"]\
                   and sentence[key].deprel != "acl:relcl":
                    warnings += 1
                    print(f"W {sentence.id} {key} deprel should be acl:relcl")

    return errors, warnings

def validate_corpus(corpus):
    """Prints a number of errors and a number of warnings."""
    total_errors = 0
    total_warnings = 0

    old_id = ""
    for tree in corpus:
        doc_id = tree.id.split("_")[0]
        if doc_id != old_id and not tree.meta_present("newdoc id"):
            print(f"E newdoc id declaration missing for {tree.id}")
            total_errors += 1
        old_id = doc_id
        total_errors += check_others(tree)
        total_errors += check_feats(tree)
        total_errors += check_misc(tree)
        total_errors += check_fixed(tree)
        errors, warnings = check_ranges(tree)
        total_errors += errors
        total_warnings += warnings
        total_errors += check_heads_for_upos(tree)
        total_errors += check_target_deprels(tree)
        total_errors += check_target_upos(tree)
        total_errors += check_bi(tree)
        total_errors += check_cleft(tree)
        total_errors += check_csubj(tree)
        total_errors += check_reported_speech(tree)
        total_errors += check_multiples(tree)
        total_errors += check_passive(tree)
        total_errors += check_relatives(tree)
        errors, warnings = check_clauses(tree)
        total_errors += errors
        total_warnings += warnings

    if total_errors == 0:
        print("*** PASSED ***")
    else:
        print(f"*** FAILED *** with {total_errors} error{'s' if total_errors != 1 else ''} and {total_warnings} warning{'s' if total_warnings != 1 else ''}")

validate_corpus(pyconll.load_from_file(sys.argv[1]))
