# Summary

A treebank of Scottish Gaelic based on the
[Annotated Reference Corpus Of Scottish Gaelic (ARCOSG)](https://github.com/Gaelic-Algorithmic-Research-Group/ARCOSG).

# Introduction

The Scottish Gaelic treebank takes data from ARCOSG, the Annotated Reference Corpus of Scottish Gaelic (Lamb _et al._ 2016) with the annotation scheme based on that in the Irish UD treebank. Full bibliographic details are to be had there.

It contains eight subcorpora of a varying number of original files, each of approximately 1000 tokens.
Not all of them have made it into release 2.6. The test and dev files are complete and the training set will be filled out, hopefully before 2.7.
All files listed below are in the training set unless they are explicitly marked as being in test or dev.
In the ARCOSG documentation the names of contributors are given in Gaelic, which I have kept and glossed with their names in English where they will be familiar to non-Gaelic speakers.

- Conversation. c01 is in test, c03 in dev and the rest in train. These are transcripts of interviews in the Western Isles from 1998 to 2000. In c03 and c04 speakers 2, 4 and 5 are children.
- Public interview. p04 is in test, p05 in dev and the rest in train.
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
    - fp04: from _Bith-eòlas_ ('Biology') by Ruairidh MacThòmais (Derick Thomson)
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

See https://universaldependencies.org/gd/index.html for detailed documentation.

# Acknowledgments

We wish to thank all of the contributors to ARCOSG and fellow Celtic language UD developers Teresa Lynn, Johannes Heinecke and Fran Tyers.

## References

* Colin Batchelor, 2019. Universal dependencies for Scottish Gaelic: syntax, in Proceedings of CLTW2019 at Machine Translation Summit XVII, Dublin, August
* Lamb, William, Sharon Arbuthnot, Susanna Naismith, and Samuel Danso. 2016. Annotated Reference Corpus of Scottish Gaelic (ARCOSG), 1997–2016 [dataset]. Technical report, University of Edinburgh; School of Literatures, Languages and Cultures; Celtic and Scottish Studies. https://doi.org/10.7488/ds/1411.
* Lynn, Teresa and Jennifer Foster, [Universal Dependencies for Irish] (http://www.nclt.dcu.ie/~tlynn/Lynn_CLTW2016.pdf), CLTW 2016, Paris, France, July 2016


# Changelog

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
