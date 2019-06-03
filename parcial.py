from direct.showbase.ShowBase import ShowBase   # Para usar panda
from direct.actor.Actor import Actor
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText, Point3, Vec3
from direct.interval.MetaInterval import Parallel, Sequence
import sys

class Parcial(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()

        # Camera
        self.camera.setPos(5, -60, 8)       # ( x , y , z )

        # Carga de un escenario
        self.Escenario = loader.loadModel("models/world")
        self.Escenario.reparentTo(self.render)
        #self.Escenario.setScale(.5, .5, .5)
        self.Escenario.setPos(30, 22, -8)


        # Carga de un Actor
        self.Ralph = Actor("models/ralph",
                                {"run": "models/ralph-run",
                                 "walk": "models/ralph-walk"})

        self.Ralph.setScale(.5, .5, .5)
        self.Ralph.setPos(0, 10, -1)        #(x   -IZQ  +DER   ,y   PROFUNDIDAD  ,z   +ARRIBA -ABAJO   )
        self.Ralph.reparentTo(self.render)

        # Animaciones parciales
        #self.Ralph.makeSubpart("corre", ["RightShoulder","LeftShoulder"])
        #self.Ralph.loop("walk", "corre")

        # Pos Interval
        #self.Ralph.setHpr(90, 0, 0)
        self.Ralph.loop("run")
        self.IzqDer = self.Ralph.posInterval(3, Point3(15, 10, -1), startPos = Point3(0, 10, -1))
        self.GI = self.Ralph.hprInterval(1, Point3(90, 0, 0))
        self.DerIzq = self.Ralph.posInterval(3, Point3(0, 10, -1), startPos = Point3(15, 10, -1))
        self.GD = self.Ralph.hprInterval(1, Point3(270, 0, 0))

        self.sec = Sequence(self.GI, self.IzqDer, self.GD, self.DerIzq)
        self.sec.loop()

        """
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
        self.MoverTronco = Sequence( self.TroncoDerecha, self.TroncoNormal, self.TroncoIzquierda)
        #self.MoverTronco.loop()

        # Secuencias de movimientos
        self.MoverCabeza = Sequence(self.CabezaArriba, self.CabezaAbajo)
        self.MoverBrazoDerecho = Sequence(self.BrazoDerechoAbajo, self.BrazoDerechoArriba)
        self.MoverBrazoIzquierdo = Sequence(self.BrazoIzquierdoAbajo, self.BrazoIzquierdoArriba)
        self.MoverCaderaDerechaIzquierda = Sequence(self.CaderaDerechaDerecha, self.CaderaDerechaNormal,
                                                    self.CaderaIzquierdaIzquierda, self.CaderaIzquierdaNormal)
        self.Giro = Sequence(self.GiroTotal)
        #self.MoverCabeza.loop()

        #self.Paralelo = Parallel(self.MoverBrazoDerecho, self.MoverBrazoIzquierdo, self.MoverCaderaDerechaIzquierda)
        #self.Paralelo.loop()
        """
        self.accept("escape", sys.exit)
        self.accept("q", self.camLeft)
        self.accept("e", self.camRight)
        self.accept("a", self.camIn)
        self.accept("d", self.camOut)
        self.accept("w", self.camUp)
        self.accept("s", self.camDown)

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

app = Parcial()
app.run()