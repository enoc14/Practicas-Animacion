from direct.showbase.ShowBase import ShowBase   # Para usar panda
from direct.actor.Actor import Actor
from direct.gui.OnscreenText import OnscreenText, Point3, Vec3
from direct.interval.MetaInterval import Parallel, Sequence
from panda3d.core import PandaNode, NodePath, Camera, TextNode
import sys

# Función para añadir Instrucciones a la pantala
def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1), scale=.05,
                        shadow=(0, 0, 0, 1), parent=base.a2dTopLeft,
                        pos=(0.08, -pos - 0.04), align=TextNode.ALeft)

class ActorParcial(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()

        # Instrucciones en pantalla
        self.Salir = addInstructions(.06, "[ESC]: Para Salir")
        self.Camara = addInstructions(.12, "[Q,E,A,D,W,S]: Para Controlar Camara")
        self.CabezaL = addInstructions(.18, "[G]: Para Mover Cabeza")
        self.CaderaL = addInstructions(.18, "[G]: Para Mover Cadera")

        # Cargar el Actor con sus animaciones
        self.Ralph = Actor("models/ralph")
        self.Ralph.setScale(.5, .5, .5)
        self.Ralph.setPos(0, 10, -1)        #(x   -IZQ  +DER   ,y   PROFUNDIDAD  ,z   +ARRIBA -ABAJO   )
        self.Ralph.reparentTo(self.render)

        # Declaración de partes del cuerpo
        self.Cabeza = self.Ralph.controlJoint(None, 'modelRoot', 'Neck')
        self.CaderaDerecha = self.Ralph.controlJoint(None, 'modelRoot', 'RightHip')
        self.CaderaIzquierda = self.Ralph.controlJoint(None, 'modelRoot', 'LeftHip')

        # Movimiento de Cabeza
        self.CabezaAbajo = self.Cabeza.hprInterval(0.5, Point3(0, 0, 0))
        self.CabezaArriba = self.Cabeza.hprInterval(0.5, Point3(20, 0, 0))

        # Movimientos de cadera derecha
        self.CaderaDerechaDerecha = self.CaderaDerecha.hprInterval(0.5, Point3(4.9762, 0, 120))
        self.CaderaDerechaNormal = self.CaderaDerecha.hprInterval(0.5, Point3(4.9762, 0, 90))

        # Movimientos de cadera izquierda
        self.CaderaIzquierdaIzquierda = self.CaderaIzquierda.hprInterval(0.5, Point3(5.02118, -0.862563, 62.9857))
        self.CaderaIzquierdaNormal = self.CaderaIzquierda.hprInterval(0.5, Point3(5.02118, -0.862563, 92.9857))

        # Secuencias de movimientos
        self.MoverCabeza = Sequence(self.CabezaArriba, self.CabezaAbajo)
        self.MoverCaderaDerechaIzquierda = Sequence(self.CaderaDerechaDerecha, self.CaderaDerechaNormal,
                                                    self.CaderaIzquierdaIzquierda, self.CaderaIzquierdaNormal)

         # Eventos de los botones
        self.accept("escape", sys.exit)
        self.accept("q", self.camLeft)
        self.accept("e", self.camRight)
        self.accept("a", self.camIn)
        self.accept("d", self.camOut)
        self.accept("w", self.camUp)
        self.accept("s", self.camDown)
        self.accept("g", self.eventCabeza)
        self.accept("h", self.eventCadera)

    def eventCabeza(self):
    	self.MoverCabeza.loop()

    def eventCadera(self):
    	self.MoverCaderaDerechaIzquierda.loop()

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

app = ActorParcial()
app.run()