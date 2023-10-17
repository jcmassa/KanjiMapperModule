#import japanize_matplotlib
import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
import os
import codecs


#Bajar tff con caracteres japoneses
#Pegar en carpeta tff en (Instalación de python)\Lib\site-packages\matplotlib\mpl-data\fonts\ttf
#Borrar cache en la siguiente ruta
#print(matplotlib.get_cachedir()) 


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
path = os.path.join(__location__, "lastexport.txt")

def comparten(kanji1, kanji2):
    return kanji1[0] == kanji2[0] or kanji1[1] == kanji2[0] or kanji1[0] == kanji2[1] or kanji1[1] == kanji2[1]
    
    #,u"", u"",u"",u"",u""
def poseeHiragana(kanji):
    hiraganas = [u"あ", u"い",u"う",u"え",u"お",u"か", u"き",u"く",u"け",u"こ",u"ま", u"み",u"む",u"め",u"も",u"な", u"に",u"ぬ",u"の",u"ね",u"ら", u"り",u"る",u"れ",u"ろ",u"ざ", u"じ",u"ず",u"ぜ",u"ぞ",u"が", u"ぎ",u"ぐ",u"げ",u"ご",u"さ", u"し",u"す",u"せ",u"そ",u"た", u"ち",u"つ",u"て",u"と",u"は", u"ひ",u"ふ",u"へ",u"ほ",u"ば", u"び",u"ぶ",u"べ",u"ぼ",u"ぱ", u"ぴ",u"ぷ",u"ぺ",u"ぽ", u"や", u"よ", u"わ",u"を"]
    return any(h in kanji for h in hiraganas)
    
testsite_array = []    
with codecs.open('lastexport.txt', encoding='utf-8') as f:
    for line in f:
        if (not(poseeHiragana(line))):
            testsite_array.append(line.strip())



#u convierte a unicode
#kanjiArrayRaw = [u"敗北", u"提灯", u"提示", u"指示", u"展示", u"精密", u"精悍", u"密着", u"着想", u"密着"]
kanjiArrayRaw = testsite_array[:1000]
kanjiArray = list(dict.fromkeys(kanjiArrayRaw))



G=nx.Graph()
for kanji in kanjiArray:
    G.add_node(kanji)
    
for i in range(len(kanjiArray)):
    for j in range(i + 1, len(kanjiArray)):
        if(comparten(kanjiArray[i], kanjiArray[j])):
            G.add_edge(kanjiArray[i], kanjiArray[j])
        

    
    
G.remove_nodes_from(list(nx.isolates(G)))

   
pos = nx.spring_layout(G, k=0.50, iterations=500) #funciona pero es ilegible、agregar iteraciones lo hace mas legible

nx.draw(G, pos= pos, with_labels=True,node_color="red",node_size=1000,font_color="black",font_family='Aozora Mincho', font_size=10, font_weight="bold",edge_color="black")


# k controls the distance between the nodes and varies between 0 and 1
# iterations is the number of times simulated annealing is run
# default k=0.1 and iterations=50

figure = plt.gcf()  # get current figure
figure.set_size_inches(64, 36) #x 100 pixeles

plt.savefig('saveaspng.png')



