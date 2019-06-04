from direct.showbase.ShowBase import ShowBase   # Para usar panda
from direct.actor.Actor import Actor
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText, Point3, Vec3
from direct.interval.MetaInterval import Parallel, Sequence
from panda3d.core import PandaNode, NodePath, Camera, TextNode
import sys

# Función para añadir Instrucciones a la pantala
def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1, 1, 1, 1), scale=.05,
                        shadow=(0, 0, 0, 1), parent=base.a2dTopLeft,
                        pos=(0.08, -pos - 0.04), align=TextNode.ALeft)

class Parcial(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()

        # Instrucciones en pantalla
        self.Salir = addInstructions(.06, "[ESC]: Para Salir")
        self.Camara = addInstructions(.12, "[A]: Para Mover Cabeza")
        self.CabezaL = addInstructions(.18, "[S]: Para Mover Brazo Derecho")
        self.CabezaL = addInstructions(.24, "[D]: Para Mover Brazo Izquierdo")
        self.CaderaL = addInstructions(.30, "[F]: Para Mover Cadera")
        self.CaderaL = addInstructions(.36, "[G]: Para Mover Tronco")
        self.CaderaL = addInstructions(.42, "[H]: Para Girar")
        self.CaderaL = addInstructions(.48, "[Z]: Cabeza Cadera")
        self.CaderaL = addInstructions(.54, "[X]: Brazos")
        self.CaderaL = addInstructions(.60, "[C]: Giro Tronco")
        self.CaderaL = addInstructions(.66, "[V]: Todos a la vez")

        # Carga de un Actor
        self.Ralph = Actor("models/ralph",
                                {"run": "models/ralph-run",
                                 "walk": "models/ralph-walk"})

        self.Ralph.setScale(.5, .5, .5)
        self.Ralph.setPos(0, 10, -1)        #(x   -IZQ  +DER   ,y   PROFUNDIDAD  ,z   +ARRIBA -ABAJO   )
        self.Ralph.reparentTo(self.render)

                
        # Giro de ralph
        self.GiroTotal = self.Ralph.hprInterval(1.5, Point3(0,359,0))

        # Declaración de partes del cuerpo
        self.Cabeza = self.Ralph.controlJoint(None, 'modelRoot', 'Neck')
        self.BrazoDerecho = self.Ralph.controlJoint(None, 'modelRoot', 'RightShoulder')
        self.BrazoIzquierdo = self.Ralph.controlJoint(None, 'modelRoot', 'LeftShoulder')
        self.CaderaDerecha = self.Ralph.controlJoint(None, 'modelRoot', 'RightHip')
        self.CaderaIzquierda = self.Ralph.controlJoint(None, 'modelRoot', 'LeftHip')
        self.Tronco = self.Ralph.controlJoint(None, 'modelRoot', 'Chest')

        # Movimiento de Cabeza
        self.CabezaAbajo = self.Cabeza.hprInterval(0.5, Point3(0, 0, 0))
        self.CabezaArriba = self.Cabeza.hprInterval(0.5, Point3(20, 0, 0))

        # Movimientos de brazo derecho
        self.BrazoDerechoAbajo = self.BrazoDerecho.hprInterval(1.0, Point3(72.2059, 106.186, -45))
        self.BrazoDerechoArriba = self.BrazoDerecho.hprInterval(1.0, Point3(72.2059, 76.186, 6.02231))

        # Movimientos de brazo izquierdo
        self.BrazoIzquierdoAbajo = self.BrazoIzquierdo.hprInterval(1.0, Point3(160.1401, -22.1706, 6.55722))
        self.BrazoIzquierdoArriba = self.BrazoIzquierdo.hprInterval(1.0, Point3(80.1401, -52.1706, 6.55722))

        # Movimientos de cadera derecha
        self.CaderaDerechaDerecha = self.CaderaDerecha.hprInterval(0.5, Point3(4.9762, 0, 120))
        self.CaderaDerechaNormal = self.CaderaDerecha.hprInterval(0.5, Point3(4.9762, 0, 90))

        # Movimientos de cadera derecha
        self.CaderaIzquierdaIzquierda = self.CaderaIzquierda.hprInterval(0.5, Point3(5.02118, -0.862563, 62.9857))
        self.CaderaIzquierdaNormal = self.CaderaIzquierda.hprInterval(0.5, Point3(5.02118, -0.862563, 92.9857))

        # Movimientos del tronco
        #self.Tronco.setHpr(0, 50, 0)
        self.TroncoIzquierda = self.Tronco.hprInterval(0.5, Point3(0, 50, 0))
        self.TroncoDerecha = self.Tronco.hprInterval(0.5, Point3(0, -50, 0))
        self.TroncoNormal = self.Tronco.hprInterval(0.5, Point3(0, 0, 0))
        

        # Secuencias de movimientos
        self.MoverCabeza = Sequence(self.CabezaArriba, self.CabezaAbajo)
        self.MoverBrazoDerecho = Sequence(self.BrazoDerechoAbajo, self.BrazoDerechoArriba)
        self.MoverBrazoIzquierdo = Sequence(self.BrazoIzquierdoAbajo, self.BrazoIzquierdoArriba)
        self.MoverCaderaDerechaIzquierda = Sequence(self.CaderaDerechaDerecha, self.CaderaDerechaNormal,
                                                    self.CaderaIzquierdaIzquierda, self.CaderaIzquierdaNormal)
        self.MoverTronco = Sequence( self.TroncoDerecha, self.TroncoNormal, self.TroncoIzquierda)
        self.Giro = Sequence(self.GiroTotal)

        # Paralelos
        self.CaderaCabeza = Parallel(self.MoverCabeza, self.MoverCaderaDerechaIzquierda)
        self.Brazos = Parallel(self.MoverBrazoDerecho, self.MoverBrazoIzquierdo)
        self.GiroTronco = Parallel(self.Giro, self.MoverTronco)
        self.Todos = Parallel(self.MoverCabeza, self.MoverCaderaDerechaIzquierda, self.MoverBrazoDerecho, self.MoverBrazoIzquierdo, self.Giro, self.MoverTronco)

        self.accept("escape", sys.exit)
        self.accept("a", self.eCabeza)
        self.accept("s", self.eBrazoDerecho)
        self.accept("d", self.eBrazoIzquierdo)
        self.accept("f", self.eCadera)
        self.accept("g", self.eTronco)
        self.accept("h", self.eGiro)
        self.accept("z", self.eCadCab)
        self.accept("x", self.eBrazos)
        self.accept("c", self.eGiroT)
        self.accept("v", self.eTodos)


    def eCabeza(self):
        self.MoverCabeza.start()

    def eBrazoDerecho(self):
        self.MoverBrazoDerecho.start()

    def eBrazoIzquierdo(self):
        self.MoverBrazoIzquierdo.start()

    def eCadera(self):
        self.MoverCaderaDerechaIzquierda.start()

    def eTronco(self):
        self.MoverTronco.start()

    def eGiro(self):
        self.Giro.start()

    def eCadCab(self):
        self.CaderaCabeza.start()

    def eBrazos(self):
        self.Brazos.start()

    def eGiroT(self):
        self.GiroTronco.start()

    def eTodos(self):
        self.Todos.loop()

app = Parcial()
app.run()