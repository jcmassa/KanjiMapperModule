# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
# import all of the Qt GUI library
from aqt.qt import *
from aqt import gui_hooks
import win32ui


import os

from anki import decks



#from cssutils import parseStyle 

import requests
from bs4 import BeautifulSoup
import shutil
import re

addon_path = os.path.dirname(__file__)
addonfoldername = os.path.basename(addon_path)
CLEANR = re.compile('<.*?>') 


def comparten(kanji1, kanji2):
    return kanji1[0] == kanji2[0] or kanji1[1] == kanji2[0] or kanji1[0] == kanji2[1] or kanji1[1] == kanji2[1]



def purificarTexto(texto):
    #soup = BeautifulSoup(texto, 'html.parser')
    #return soup.get_text()
    cleantext = re.sub(CLEANR, '', texto)
    return cleantext

def mappearKanji(deckId):
    dlg = win32ui.CreateFileDialog(0, "txt")
    dlg.DoModal()
    parent_dir = dlg.GetPathName()
    cartas = mw.col.decks.cids(deckId).copy()
    extractedKanji = list[str]()
    for cId in cartas:
        note = mw.col.get_note(mw.col.get_card(cId).nid)
        try:
            currWord = purificarTexto(str(note.fields[0]))
        except RuntimeWarning:
            pass
        if (len(currWord) == 2):
            extractedKanji.append(currWord)
    for kanji in extractedKanji:
        logText(parent_dir, kanji)



def logText(parent_dir, texto): 
    f = open(parent_dir, "a")
    f.write(texto + "\n")
    f.close()

def addGear2(deck_browser, content):
    gear_abs = addon_path
    os.makedirs(gear_abs, exist_ok=True)
    if not os.listdir(gear_abs):
        shutil.copytree(src=addon_path, dst=gear_abs, dirs_exist_ok=True)

    soup = BeautifulSoup(content.tree, 'html.parser')
    #svgPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "btn.svg").replace('\\','/')
    svgPath = f"/_addons/{addonfoldername}/files/btn.png"
    decks = soup.find_all('tr', {'class': 'deck'})
    for deck in decks:
        currDeckId = deck["id"]        
        tdsFirst = deck.find('td', {'class': 'decktd'})
        if tdsFirst is not None:
            tdsFirst['colspan'] = 6
        newTd = soup.new_tag("td", id= str(currDeckId))
        newA = soup.new_tag("a", href = '')
        newBtn = soup.new_tag("img", src = svgPath)
        newBtn['class'] = "gears"
        newBtn['onClick'] = f"return pycmd('mapDeck:{currDeckId}')"
        newA.insert(1, newBtn) 
        newTd.insert(1, newA)
        deck.append(newTd)

    header = soup.find('th', {'align': 'start'}) 
    if header is not None:
        header['colspan'] = 6

    initialRow = soup.find('tr')
    if initialRow is not None:
        newTh = soup.new_tag("th")
        newTh['class'] = "optscol"
        initialRow.append(newTh)




    
    content.tree = str(soup)


#Verifica si el mensaje es el propio mapDeck, si no "pasa" el handled para que lo evalúe anki      
def mapDeck(handled, message, context):  # args=["handled: tuple[bool, Any]", "message: str", "context: Any"]
    if "mapDeck" in message:
        deckId = message[message.find(':') + 1:]
        if deckId is not None:
            mappearKanji(str(deckId))
        # our message, call onMark() on the reviewer instance
        # and don't pass message to other handlers
        return (True, None)
    else:
        # some other command, pass it on
        return handled


def initialize_addon():
    #Esto copia los archivos a la ruta relativa
    # give permission to access png files
    mw.addonManager.setWebExports(__name__, r'.+\.png')
    # get this add-on's root directory name
    addon_package = mw.addonManager.addonFromModule(__name__)
    # of course you can also use pathlib
    # addon_package = pathlib.Path(__file__).resolve().parent.name
    
    gui_hooks.deck_browser_will_render_content.append(addGear2)
    gui_hooks.webview_did_receive_js_message.append(mapDeck)


initialize_addon()