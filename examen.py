from direct.showbase.ShowBase import ShowBase   # Para usar panda
from direct.actor.Actor import Actor
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText, Point3, Vec3
from direct.interval.MetaInterval import Parallel, Sequence
from panda3d.core import PandaNode, NodePath, Camera, TextNode
import sys
import threading

# Función para añadir Instrucciones a la pantala
def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1), scale=.05,
                        shadow=(0, 0, 0, 1), parent=base.a2dTopLeft,
                        pos=(0.08, -pos - 0.04), align=TextNode.ALeft)

class Examen(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()

        # Instrucciones en pantalla
        self.Salir = addInstructions(.06, "[ESC]: Para Salir")
        self.StartRutina = addInstructions(.12, "[G]: Para Empezar Rutina")
        self.StartRutina = addInstructions(.18, "[Q,E,A,D,W,S]: Para Controlar Camara")

        # Camera
        self.camera.setPos(10, -30, 3)       # ( x , y , z )

        # Cargar el audio
        self.Audio = loader.loadSfx("src/sounds/sia.mp3")

        # Cargar el escenario
        self.Escenario = loader.loadModel("models/world")
        self.Escenario.reparentTo(self.render)
        self.Escenario.setPos(30, 22, -8)

        # Cargar el Actor con sus animaciones
        self.Ralph = Actor("models/ralph",
                           {"run": "models/ralph-run",
                            "walk": "models/ralph-walk",
                            "jump": "models/ralph-jump"})
        self.Ralph.setScale(.5, .5, .5)
        self.Ralph.setPos(15, 10, -1)        #(x   -IZQ  +DER   ,y   PROFUNDIDAD  ,z   +ARRIBA -ABAJO   )
        self.Ralph.reparentTo(self.render)

        # Animaciones parciales
        self.Ralph.makeSubpart("corre", ["RightShoulder","LeftShoulder"])

        # Declaración de partes del cuerpo
        self.Cabeza = self.Ralph.controlJoint(None, 'modelRoot', 'Neck')

        # Movimiento de Cabeza
        self.CabezaAbajo = self.Cabeza.hprInterval(0.5, Point3(0, 0, 0))
        self.CabezaArriba = self.Cabeza.hprInterval(0.5, Point3(20, 0, 0))

        # Definición de Intervalos
        self.IzqDer = self.Ralph.posInterval(3, Point3(15, 10, -1), startPos = Point3(0, 10, -1))
        self.GI = self.Ralph.hprInterval(1, Point3(90, 0, 0))
        self.DerIzq = self.Ralph.posInterval(3, Point3(0, 10, -1), startPos = Point3(15, 10, -1))
        self.GD = self.Ralph.hprInterval(1, Point3(270, 0, 0))
        self.intervalo01 = self.Ralph.actorInterval("walk", loop=1, constrainedLoop=1, duration=2)
        self.intervalo02 = self.Ralph.actorInterval("jump", loop=1, constrainedLoop=1, duration=2)
        self.GN = self.Ralph.hprInterval(1, Point3(0, 0, 0))

        # Secuencias para el baile
        self.Caminar = Sequence(self.intervalo02, self.GD, self.DerIzq, self.GI, self.IzqDer, self.intervalo02, self.GN, self.CabezaArriba, self.CabezaAbajo, self.CabezaArriba, self.CabezaAbajo)
        self.CabezaMov = Sequence(self.CabezaArriba, self.CabezaAbajo, self.CabezaArriba, self.CabezaAbajo, self.CabezaArriba, self.CabezaAbajo, self.CabezaArriba, self.CabezaAbajo)

        # Usando el paralel
        self.Paralelo = Parallel(self.CabezaMov, self.Caminar)

        # Eventos de los botones
        self.accept("escape", sys.exit)
        self.accept("q", self.camLeft)
        self.accept("e", self.camRight)
        self.accept("a", self.camIn)
        self.accept("d", self.camOut)
        self.accept("w", self.camUp)
        self.accept("s", self.camDown)
        self.accept("g", self.Iniciar)

    def Iniciar(self):
        self.Audio.play()
        self.Paralelo.start()
        timer = threading.Timer(interval = 16.0, function = self.Subpart)
        timer.start()

    def Subpart(self):
        self.Ralph.loop("run", "corre")

    def camLeft(self):
        x = self.camera.getX()
        self.camera.setX(x - 2)

    def camRight(self):
        x = self.camera.getX()
        self.camera.setX(x + 2)

    def camUp(self):
        y = self.camera.getY()
        self.camera.setY(y + 2)

    def camDown(self):
        y = self.camera.getY()
        self.camera.setY(y - 2)

    def camIn(self):
        z = self.camera.getZ()
        self.camera.setZ(z + 2)

    def camOut(self):
        z = self.camera.getZ()
        self.camera.setZ(z - 2)

app = Examen()
app.run()