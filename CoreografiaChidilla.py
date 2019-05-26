from direct.showbase.ShowBase import ShowBase
from direct.actor.Actor import Actor
from direct.gui.OnscreenText import OnscreenText, Point3
from direct.interval.MetaInterval import Parallel, Sequence
import sys

class CoreografiaSS(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.disableMouse()
        self.Ralph = Actor("models/ralph")
        self.Ralph.setScale(.5, .5, .5)
        self.Ralph.reparentTo(self.render)
        self.Ralph.setPos(0, 10, -1)
        self.Ralph.listJoints()

        #Mover Piesecillo Ralph
        self.PieRalphIzq = self.Ralph.controlJoint(None, 'modelRoot', 'LeftBall')

        self.BrazoRalphDrc = self.Ralph.controlJoint(None, 'modelRoot', 'RightShoulder')
        self.CodoRalphDrc = self.Ralph.controlJoint(None, 'modelRoot', 'RightElbow')
        

        self.PieIzqAbajo = self.PieRalphIzq.hprInterval(0.3, Point3(0, 0, 0))
        self.PieIzqArriba = self.PieRalphIzq.hprInterval(0.3, Point3(0, -20, 0))
        self.MoverPieIzq = Sequence(self.PieIzqArriba, self.PieIzqAbajo)
        self.MoverPieIzq.loop()
                            #BajarBrazo RotarMano
        self.BrazoRalphDrc.setHpr(10, 0, 10)
        self.CodoRalphDrc.setHpr(60, 170, 0)

        self.accept("q", self.moverDerecha)
        self.accept("e", self.moverIzquierda)
        self.accept("escape", sys.exit)


    def moverDerecha(self):
        x = self.Ralph.getH()
        self.Ralph.setHpr(x+10, 0, 0)

    def moverIzquierda(self):
        x = self.Ralph.getH()
        self.Ralph.setHpr(x-10, 0, 0)


app = CoreografiaSS()
app.run()