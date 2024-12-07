import os
import sys
import pathlib
import importlib.util
import pprint
import tempfile

if __name__ != "__main__":
	from aqt import mw
	from aqt.qt import *
	from aqt.utils import showInfo, qconnect
	from anki import sound, cards, media

def import_from_path(module_name):
	addon_root = pathlib.Path(__file__).resolve().parent
	source_path = addon_root / 'libs' / module_name /'__init__.py'
	spec = importlib.util.spec_from_file_location(module_name, source_path)
	module = importlib.util.module_from_spec(spec)
	sys.modules[module_name] = module
	spec.loader.exec_module(module)
	return module

# working dir: C:\Users\guita\AppData\Roaming\Anki2\addons21\playEnglishSounds\
# media dir: C:\Users\guita\AppData\Roaming\Anki2\ユーザー 1\collection.media
# make .mp3 file in media dir via media.add_file()
def genAudioFile(text, filename):
	tts=gTTS(text=text, lang='en')
	with tempfile.TemporaryDirectory() as tempDir:
		filepath = os.path.join(tempDir, filename)
		tts.save(filepath)
		mw.col.media.add_file(filepath)
	

# add sound on card. depend on myAddOnForHapa module
def addSoundOnCard(card, filename, result) -> str:
	text = card.note()["裏面"].split("<br>")[1]
	genAudioFile(text, filename)
	card.note()["裏面"] += f"<br>[sound:{filename}]"
	card.answer_av_tags().append(sound.SoundOrVideoTag(filename))
	return (
		f"text: {text}\n" 
		f"audio file: {os.path.join(os.getcwd(),filename)}\n\n"
	)

# for test
def showSoundInfo(card):
	result = ""
	for string in card.note()["裏面"].split("<br>"):
		result += f"{string}\n"
	result += "avtag:"
	for av_tag in card.answer_av_tags():
		result += f"{av_tag.filename},"
	showInfo(result)

# check the card has sound tag
def hasSound(card) -> bool:
	for string in card.note()["裏面"].split("<br>"):
		if (string.startswith("[sound:")):
			return True
	return False

def addSoundEntireCards():
	mw.col.decks.select(mw.col.decks.id("Hapa"))
	result = ""
	for tag in range(300, 508):
		ids = mw.col.find_cards("tag:%s" % tag)
		for idx in range(0, len(ids)):
			card = mw.col.get_card(ids[idx])
			if not hasSound(card):
				result += addSoundOnCard(card, f"audio_{tag}_{str(idx)}.mp3", result)
				mw.col.update_note(card.note())
	showInfo(result)




gtts = import_from_path("gtts")
pygame = import_from_path("pygame")
from gtts import gTTS


if __name__ != "__main__":
	action = QAction("TestForSound", mw)
	qconnect(action.triggered, addSoundEntireCards)
	mw.form.menuTools.addAction(action)
