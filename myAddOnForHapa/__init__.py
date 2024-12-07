from . import fetchPhrases
from aqt import mw
from aqt.utils import showInfo, qconnect
from aqt.qt import *

def AddTodaysPhrases() -> None:
    deck_id = mw.col.decks.id("Hapa")
    mw.col.decks.select(deck_id)
    noteType = mw.col.models.by_name("基本")

    rootUrl = 'https://hapaeikaiwa.com/blog/category/podcast-column'
    [url_list, title_list] = fetchPhrases.fetch_podcast_url_list(rootUrl)
    length = 10#len(url_list)
    result = ""
    for i in range(0, length):
        url = url_list[i]
        title = title_list[i]
        if not fetchPhrases.isNormalTitle(title):
            result += title + "(skipped)\n"
            continue
        phrase_list = fetchPhrases.fetch_phrases_of_the_day(url)
        titleNum = fetchPhrases.getTitleNum(title)
        ids = mw.col.find_cards("tag:%s" % titleNum)
        if (len(ids) == 0 and phrase_list != None):
            result += title + ","
            for phrase in phrase_list:
                new_note = mw.col.new_note(noteType)
                new_note["表面"] = phrase.jp + "<br>" + phrase.example_jp
                new_note["裏面"] = phrase.en + "<br>" + phrase.example_eng
                new_note.addTag(titleNum)
                mw.col.add_note(new_note, deck_id)
    showInfo(result)


#     phrase_list = fetchPhrases.fetch_phrases_of_the_day(url)
#     phrase.example_eng = example_element.ul.li.b.text
# AttributeError: 'NoneType' object has no attribute 'li'



action = QAction("AddTodaysPhrases", mw)
qconnect(action.triggered, AddTodaysPhrases)
mw.form.menuTools.addAction(action)

