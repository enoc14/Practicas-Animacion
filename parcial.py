from direct.showbase.ShowBase import ShowBase   # Para usar panda
from direct.actor.Actor import Actor
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText, Point3
from direct.interval.MetaInterval import Parallel, Sequence
import sys

class Parcial(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()

        self.Ralph = Actor("models/ralph.egg.pz",
                                {"run": "models/ralph-run",
                                 "walk": "models/ralph-walk"})
        self.Ralph.setScale(.5, .5, .5)
        self.Ralph.setPos(0, 7, -1)
        self.Ralph.reparentTo(self.render)

        # Animaciones parciales
        self.Ralph.makeSubpart("corre", ["RightShoulder","LeftShoulder"])
        self.Ralph.loop("walk", "corre")

        # Giro de ralph
        self.GiroTotal = self.Ralph.hprInterval(1.5, Point3(0,359,0))
        self.Giro = Sequence(self.GiroTotal)

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
        self.MoverTronco = Sequence( self.TroncoDerecha, self.TroncoNormal, self.TroncoIzquierda)
        #self.MoverTronco.loop()

        # Secuencias de movimientos
        self.MoverCabeza = Sequence(self.CabezaArriba, self.CabezaAbajo)
        self.MoverBrazoDerecho = Sequence(self.BrazoDerechoAbajo, self.BrazoDerechoArriba)
        self.MoverBrazoIzquierdo = Sequence(self.BrazoIzquierdoAbajo, self.BrazoIzquierdoArriba)
        self.MoverCaderaDerechaIzquierda = Sequence(self.CaderaDerechaDerecha, self.CaderaDerechaNormal,
                                                    self.CaderaIzquierdaIzquierda, self.CaderaIzquierdaNormal)
        #self.MoverCaderaDerechaIzquierda.loop()

        #self.Paralelo = Parallel(self.MoverBrazoDerecho, self.MoverBrazoIzquierdo, self.MoverCaderaDerechaIzquierda)
        #self.Paralelo.loop()

        self.accept("escape", sys.exit)


app = Parcial()
app.run()