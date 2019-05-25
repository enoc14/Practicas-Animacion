from direct.showbase.ShowBase import ShowBase   # Para usar panda
from direct.actor.Actor import Actor
from panda3d.core import PandaNode, NodePath, Camera, TextNode
from direct.gui.OnscreenText import OnscreenText, Point3
from direct.interval.MetaInterval import Parallel, Sequence
from direct.gui.OnscreenImage import OnscreenImage
import sys

# Function to put instructions on the screen.
def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1), scale=.05,
                        shadow=(0, 0, 0, 1), parent=base.a2dTopLeft,
                        pos=(0.08, -pos - 0.04), align=TextNode.ALeft)

class Proyecto(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.disableMouse()

        #Instrucciones
        self.ralph_escape = addInstructions(.06, "[ESC]: Para Salir")
        self.ralph_run = addInstructions(.12,"[A]: Para Correr")
        self.ralph_saluda = addInstructions(.18, "[S]: Para Saludar")
        self.ralph_giraD = addInstructions(.24, "[E]: Girar a la derecha")
        self.ralph_giraI = addInstructions(.30, "[Q]: Girar a la izquierda")

        # Carga de Actor
        """self.Ralph = Actor("models/ralph",
                           {"run": "models/ralph-run",
                            "walk": "models/ralph-walk"})
        self.Ralph.setScale(.5,.5,.5)
        self.Ralph.reparentTo(self.render)
        self.Ralph.setPos(0,10,-1)   # X,Y,Z"""

        # Carga de imágenes
        self.Perro = OnscreenImage(image = 'src/images/Dog.png')
        self.Vaca = OnscreenImage(image='src/images/Cow.png')
        self.Leon = OnscreenImage(image='src/images/Lion.png')
        self.Perro.setScale(.2,.2,.2)
        self.Vaca.setScale(.2, .2, .2)
        self.Leon.setScale(.2, .2, .2)
        self.Perro.setPos(-1, 0, 0)
        self.Vaca.setPos(0, 0, 0)
        self.Leon.setPos(1, 0, 0)

        # Carga de audio
        self.audioPerro = loader.loadSfx("src/sounds/Dog.mp3")
        self.audioPerro.play()

        #self.audioPerro.play()

        # Definir articulaciones con Joint
        """self.BrazoDerecho = self.Ralph.controlJoint(None, 'modelRoot', 'RightShoulder')
        self.BrazoIzquierdo = self.Ralph.controlJoint(None, 'modelRoot', 'LeftShoulder')

        # Movimientos con el brazo derecho
        self.moverBrazoDerechoAbajo = self.BrazoDerecho.hprInterval(1.0, Point3(72.2059, 106.186,-45))
        self.moverBrazoDerechoArriba = self.BrazoDerecho.hprInterval(1.0, Point3(72.2059, 76.186, 6.02231))
        self.Secuencia1 = Sequence(self.moverBrazoDerechoAbajo, self.moverBrazoDerechoArriba)

        # Movimientos con el brazo izquierdo
        self.moverBrazoIzquierdoAbajo = self.BrazoIzquierdo.hprInterval(1.0, Point3(160.1401, -22.1706, 6.55722))
        self.moverBrazoIzquierdoArriba = self.BrazoIzquierdo.hprInterval(1.0, Point3(80.1401, -52.1706, 6.55722))
        self.Secuencia2 = Sequence(self.moverBrazoIzquierdoAbajo, self.moverBrazoIzquierdoArriba)

        # Movimientos paralelos
        self.Paralelo = Parallel(self.Secuencia1, self.Secuencia2)"""

        # Add Eventos
        self.accept("escape", sys.exit)
        self.accept("a", self.ralphRun)
        self.accept("s", self.ralphSaluda)
        self.accept("q", self.ralphGiraI)
        self.accept("e", self.ralphGiraD)

    def ralphRun(self):
        self.Ralph.loop("run")

    def ralphSaluda(self):
        if self.Paralelo.isPlaying():
            self.Paralelo.finish()
        else:
            self.Paralelo.loop()

    def ralphGiraI(self):
        i = self.Ralph.getH()
        self.Ralph.setHpr(i-10,0,0)

    def ralphGiraD(self):
        i = self.Ralph.getH()
        self.Ralph.setHpr(i+10,0,0)

app = Proyecto()
app.run()