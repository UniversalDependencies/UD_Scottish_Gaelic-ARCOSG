# Summary

A treebank of Scottish Gaelic based on the
[Annotated Reference Corpus Of Scottish Gaelic (ARCOSG)](https://github.com/Gaelic-Algorithmic-Research-Group/ARCOSG).

# Introduction

The Scottish Gaelic treebank takes data from ARCOSG, the Annotated Reference Corpus of Scottish Gaelic (Lamb _et al._ 2016) with the annotation scheme based on that in the Irish UD treebank.
Full bibliographic details are to be had there.

It contains eight subcorpora of a varying number of original files, each of approximately 1000 tokens.
All files listed below are in the training set unless they are explicitly marked as being in test or dev.
In the ARCOSG documentation the names of contributors are largely given in Gaelic, which I have kept and glossed with their names in English where they will be familiar to non-Gaelic speakers.

- Conversation. c01 is in test, c03 in dev and the rest in train. These are transcripts of interviews in the Western Isles from 1998 to 2000. In c03 and c04 speakers 2, 4 and 5 are children.
- Sport. s06 is in test, s08 in dev and the rest in train. s01 to s05 are _Radio nan Gàidheal_ commentary on a match between Scotland and Australia; s06 to s10 on Scotland _vs._ Yugoslavia.
- Oral narrative.
    - n01: _Na Trì Leinntean Canaich_ (test)
    - n02: _Conall Gulban_ (dev)
    - n03: _Na Fiantaichean_
    - n04: _Gille an Fheadain Duibh_
    - n05: _Bodach Ròcabarraigh_
    - n06: _Iain Beag MacAnndra_
    - n07: _Fear a' Churracain Ghlais_
    - n08: _Boban Saor_
    - n09: _Bean 'ic Odrum_
    - n10: _Blàr Chàirinis_
- News scripts from _Radio nan Gàidheal_ in the early 1990s.
    - ns01: Màiri Anna NicUalraig (Mary Ann Kennedy)
    - ns02: Dòmhnall Moireasdan
    - ns03: Iseabail NicIllinnein
    - ns04: Innes Rothach
    - ns05: Innes Rothach (test)
    - ns06: Pàdraig MacAmhlaigh (dev)
    - ns07: Dòmhnall Moireasdan (test)
    - ns08: Màiri Anna NicUalraig (dev)
    - ns09: Seumas Domhnallach
    - ns10: Seumas Domhnallach
- Public interview
    - p01: _Peataichean_, conversation on Coinneach MacÌomhair's programme
    - p02: Fred MacAulay and Martin MacDonald
    - p03: John MacInnes and William Matheson
    - p04: Geamaichean Sholais 1, conversation on Coinneach MacÌomhair's programme (test)
    - p05: Geamaichean Sholais 2 (dev)
    - p06: Bonn Comhraidh, 1980s political discussion programme
    - p07: Conversation on Coinneach MacÌomhair's programme 2000-01-17 part 1
    - p08: Conversation on Coinneach MacÌomhair's programme 2000-01-17 part 2
- Fiction
    - f01: _Am Fainne_ by Eilidh Watt
    - f02: from _Cùmhnantan_ by Tormod MacGill-Eain
    - f03: _Droch Àm_ by Pòl MacAonghais (test)
    - f04: _Spàl Tìm_ by Cailean T. MacCoinneach
    - f05: _Teine a Loisgeas_ by Eilidh Watt
    - f06: _Beul na h-Oidhche_ by Somhairle MacGill-Eain (Sorley Maclean)
    - f07: from _An t-Aonaran_ by Iain Mac a' Ghobhainn (Iain Crichton Smith)
    - f08: _Briseadh na Cloiche_ by Iain Moireach (dev)
- Formal prose:
    - fp01: _Trì Ginealaichean_ by D. E. Dòmhnallach
    - fp02: _Nua-Bhàrdachd Ghàidhlig_ by Dòmhnall MacAmhlaigh (Donald MacAulay)
    - fp03: _Mairead N. Lachlainn_ by Somhairle MacGill-Eain (test)
    - fp04: from _Bith-eòlas_ ('Biology'), a translation by Ruairidh MacThòmais (Derick Thomson)
    - fp05: _Aramach am Bearnaraidh_
    - fp06: _Blàr a' Chumhaing_ by Iain A. MacDonald
    - fp07: _Na Marbhrannan_ by Coinneach D. MacDhòmhnaill
    - fp08: _Cainnt is Cànan_ by J. MacInnes
    - fp09: from Dòmhnall Uilleam Stiùbhart (Donald William Stewart)'s unpublished PhD thesis (dev)
- Popular writing: columns from _The Scotsman_:
    - pw01: _An Cuir am Papa..._ by Aileig O Hianlaidh (Alex O'Henley)
    - pw02: _A bith mar Chorra..._ by Joina NicDhomnaill (test)
    - pw03: _Pàdraig Sellar_ by Ùisdean MacIllinnein
    - pw04: _A' Cur Às Dhuinn Fhìn_ by Aonghas Mac-a-Phì
    - pw05: _Aon Dùthaich_ by Murchadh MacLeòid
    - pw06: _Blas a' Ghuga_ by Coinneach MacLeòid (dev)
    - pw07: _Luchd-ciùil_ by Criosaidh Dick
    - pw08: _Na Gàidheil Ùra_ by Criosaidh Dick
    - pw09: _A' Siubhail gu Rèidh_ by Tormod Domhnallach (dev)
    - pw10: _Poileaticeans_ by Niall M. Brownlie
    - pw11: _Oifigeir Gàidhlig_ by Aileig O Hianlaidh (test)

See https://universaldependencies.org/gd/index.html for detailed linguistic documentation.

# Acknowledgments

We wish to thank all of the contributors to ARCOSG and fellow Celtic language UD developers Teresa Lynn, Kevin Scannell, Johannes Heinecke and Fran Tyers.

## References

* Colin Batchelor, 2019. Universal dependencies for Scottish Gaelic: syntax, in Proceedings of CLTW2019 at Machine Translation Summit XVII, Dublin, August
* Lamb, William, Sharon Arbuthnot, Susanna Naismith, and Samuel Danso. 2016. Annotated Reference Corpus of Scottish Gaelic (ARCOSG), 1997–2016 [dataset]. Technical report, University of Edinburgh; School of Literatures, Languages and Cultures; Celtic and Scottish Studies. https://doi.org/10.7488/ds/1411.
* Lynn, Teresa and Jennifer Foster, [Universal Dependencies for Irish] (http://www.nclt.dcu.ie/~tlynn/Lynn_CLTW2016.pdf), CLTW 2016, Paris, France, July 2016


# Changelog

* 2025-05-15 v2.16
  * Speech reviewed in the light of the current ccomp/parataxis guidelines
  * AdvType and CleftType added to FEATS
  * nmod:unmarked and obl:unmarked now used and replacing other subtypes of obl
  * advcl:relcl added
  * Promoted=Yes added to MISC column to help the local validator
  * Names brought into line with UD specification
  * obl:agent added for passives
  * Extra NounTypes added for proper nouns
* 2024-11-15 v2.15
  * Added PronType, VerbForm and Mood features systematically.
* 2024-05-15 v2.14
  * Restricted the use of flat:foreign to where there are extended phrases rather than just two-word expressions.
  * Fixed some appositions.
* 2023-11-15 v2.13
  * Particles and numbers now lemmatised.
  * NumType and NumForm features added.
  * PartType on cha, chan and nach fixed.
  * _dè cho_ annotated consistently.
* 2023-05-15 v2.12
  * Content clauses should all be `acl` now.
  * Anonymised places and people have `Anonymised=Yes` in the MISC column.
* 2022-11-15 v2.11
  * Passives formed with _rach_ 'to go' now mirror those in English and other languages using the `aux:pass`, `nsubj:pass` and very occasionally the `nsubj:outer` deprels.
* 2022-05-15 v2.10
  * All of ARCOSG now in the treebank.
* 2021-11-15 v2.9
  * Small fixes to README.md
  * Some missing sentences added.
  * Added `PronType=Int` for interrogative pronouns and `PronType=Art` for articles.
  * Made sure interrogative pronouns were all pronouns and adjusted trees and documentation accordingly.
* 2021-05-15 v2.8
  * _ri linn 's_ is a fixed expression now.
  * the _'_ in, for example, _'dol_ is no longer a separate token.
  * `flat` has been replaced with `flat:name` in personal names and `flat:foreign` in foreign expressions. It remains for placenames, dates and telephone numbers.
  * `nmod` and `obl` have been reviewed and corrected throughout the corpus and now replace `compound` for _f(h)(è)in_ and _a/ri chèile_.
  * Documents identified with `newdoc`.
* 2020-11-15 v2.7
  * `Poss=Yes` added in line with Irish.
  * Tokens in the original with XPOS beginning `Sap` and `Spp` are divided into their component words.
  * Systematic tidying of `acl:relcl`, `advcl` and `ccomp`.
  * `PronType=Emp` replaced with `Form=Emp` in line with Irish and extended to other parts of speech.
  * `PART`s with XPOS `Qa` now tagged correctly `PartType=Cmpl`
  * Words with UPOS `AUX` now have full features.
  * The English borrowing _so_ is `CCONJ` not `SCONJ`.
  * _'s_ in _fad 's_ and the like is now related to _fad_ or _o chionn_ by `fixed`.
  * Cosubordinative _agus_ and _is_ are now `SCONJ` like in Irish.
  * _ach_ is `PART` where it is a focus particle rather than a preposition or a conjunction.
  * Use of `xcomp:pred` consistent in the sport subcorpora where the root is a footballer rather than _bi_.
* 2020-05-15 v2.6
  * Small fixes to README.md.
  * Some missing sentences added to dev and test, bringing them both over 10000 words.
* 2019-11-15 v2.5
  * Initial release in Universal Dependencies.


<pre>
=== Machine-readable metadata (DO NOT REMOVE!) ================================
Data available since: UD v2.5
License: CC BY-SA 4.0
Includes text: yes
Genre: nonfiction fiction news spoken 
Lemmas: converted from manual
UPOS: converted from manual
XPOS: manual native
Features: converted from manual
Relations: converted from manual
Contributors: Batchelor, Colin
Contributing: here
Contact: colin.r.batchelor@googlemail.com
===============================================================================
</pre>
