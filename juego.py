from direct.showbase.ShowBase import ShowBase   # Para usar panda
from panda3d.core import PandaNode, NodePath, Camera, TextNode
from direct.gui.OnscreenText import OnscreenText, Point3
from direct.gui.OnscreenImage import OnscreenImage
from direct.actor.Actor import Actor
from direct.gui.DirectGui import *
import sys
import random
import threading

def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1), scale=.05,
                        shadow=(0, 0, 0, 1), parent=base.a2dTopLeft,
                        pos=(0.08, -pos - 0.04), align=TextNode.ALeft)

class Juego(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()

        # Instrucciones en pantalla
        self.ralph_escape = addInstructions(.06, "[ESC]: Para Salir")
        self.ralph_run = addInstructions(.12, "[A]: Para Empezar Juego")

        """self.Ralph = Actor("models/lomito") 
        self.Ralph.setScale(.5, .5, .5)
        self.Ralph.reparentTo(self.render)
        self.Ralph.setPos(0, 10, -1)
        self.Ralph.setHpr(-90,5,15)"""
        #self.Ralph.listJoints()

        # Variables globales para el control
        self.arrayGlobal = []
        self.sonidoGlobal = -1

        # Carga de imágenes
        self.Perro = OnscreenImage(image='src/images/Dog.png')
        self.Caballo = OnscreenImage(image='src/images/Horse.png')
        self.Leon = OnscreenImage(image='src/images/Lion.png')
        self.Gato = OnscreenImage(image='src/images/Cat.png')
        self.Elefante = OnscreenImage(image='src/images/Elephant.png')
        self.Oveja = OnscreenImage(image='src/images/Sheep.png')
        self.Correcto = OnscreenImage(image='src/images/correcto.png', pos=(100, 100, 100))
        self.Incorrecto = OnscreenImage(image='src/images/incorrecto.png', pos=(100, 100, 100))
        self.arrayRespuestas = [self.Correcto, self.Incorrecto]
        self.arrayImages = [self.Perro, self.Caballo, self.Leon, self.Gato, self.Elefante, self.Oveja]

        # Carga de audio
        self.audioPerro = loader.loadSfx("src/sounds/Dog.mp3")
        self.audioCaballo = loader.loadSfx("src/sounds/Dog.mp3")
        self.audioLeon = loader.loadSfx("src/sounds/Lion.mp3")
        self.audioGato = loader.loadSfx("src/sounds/Dog.mp3")
        self.audioElefante = loader.loadSfx("src/sounds/Elephant.wav")
        self.audioOveja = loader.loadSfx("src/sounds/Sheep.mp3")
        self.arrayAudios = [self.audioPerro, self.audioCaballo, self.audioLeon, self.audioGato, self.audioElefante, self.audioOveja]

        # Aprende a usar botones prro
        self.btn1 = DirectButton(text = "1", scale=.1, command=self.verificaRespuesta, extraArgs=[0])
        self.btn2 = DirectButton(text="2", scale=.1, command=self.verificaRespuesta, extraArgs=[1])
        self.btn3 = DirectButton(text="3", scale=.1, command=self.verificaRespuesta, extraArgs=[2])
        self.btn4 = DirectButton(text="4", scale=.1, command=self.verificaRespuesta, extraArgs=[3])
        self.btn5 = DirectButton(text="5", scale=.1, command=self.verificaRespuesta, extraArgs=[4])
        self.btn6 = DirectButton(text="6", scale=.1, command=self.verificaRespuesta, extraArgs=[5])
        self.arrayBotones = [self.btn1, self.btn2, self.btn3, self.btn4, self.btn5, self.btn6]

        # Primer evento para desaparecer all de pantalla
        self.limpiarPantalla(False)

        # Eventos con teclas
        self.accept("escape", sys.exit)
        self.accept("a", self.iniciaJuego)

    def verificaRespuesta(self, num):
        if len(self.arrayGlobal) == 6:
            self.arrayAudios[num].stop()
            self.limpiarPantalla(True)
            print("El juego ha terminado")
        else:
            if self.sonidoGlobal == num:
                print("Animal correcto")
                self.arrayAudios[num].stop()
                self.mostrarResultado(0)
                self.generarSonido()
            else:
                print("Te equivocaste")
                self.mostrarResultado(1)

    def iniciaJuego(self):
        self.insertarImagenes()
        self.generarSonido()

    def insertarImagenes(self):
        cont = -1
        for x in range(6):
            if cont <= 1:
                self.arrayImages[x].setPos(cont,0,.5)
                self.arrayBotones[x].setPos(cont,0,.19)
            else:
                self.arrayImages[x].setPos(cont-3,0,-.3)
                self.arrayBotones[x].setPos(cont-3, 0, -.60)
            cont += 1

    def generarSonido(self):
        rand = self.sonidoGlobal
        if len(self.arrayGlobal) != 0:
            while rand in self.arrayGlobal:
                rand = random.randint(0, 5)
        else:
            rand = random.randint(0, 5)

        self.arrayAudios[rand].play()
        self.arrayGlobal.append(rand)
        self.sonidoGlobal = rand
        print("elemento: ", rand)

    def limpiarPantalla(self, c):
        for x in range(len(self.arrayBotones)):
            self.arrayImages[x].setScale(.2, .2, .2)
            self.arrayImages[x].setPos(100, 100, 100)
            self.arrayBotones[x].setPos(100, 100, 100)
            if c:
                self.arrayGlobal.pop()

    def mostrarResultado(self,op):
        self.arrayRespuestas[op].setScale(.4, .4, .4)
        self.arrayRespuestas[op].setPos(0, 0, 0)
        timer = threading.Timer(interval = 2.0, function = self.quitaImagen, args = [op])
        timer.start()

    def quitaImagen(self, pos):
        self.arrayRespuestas[pos].setPos(100, 100, 100)

app = Juego()
app.run()