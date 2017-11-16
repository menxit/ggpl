from pyplasm import *

def ring(r, R):
	y = lambda (u, v) : v * math.sin(u)
	x = lambda (u, v) : v * math.cos(u)
	dom = T(2)(r)(PROD([INTERVALS(2*PI)(32),INTERVALS(R-r)(32)]))
	return MAP([x,y])(dom)

def bezier():
    b = BEZIER(S1)([[0,0], [1,0], [0,1], [0,0]])
    g = MAP(b)(INTERVALS(1)(32))
    return g

def spiral(r, h):
    x = lambda u : r * math.cos(u[0])
    y = lambda u : r * math.sin(u[0])
    z = lambda u : h*u[0]/(2*PI)
    return CONS([x,y,z])

dom = INTERVALS(2*PI)(18)

VIEW(MAP(spiral(2, 20))(dom))

#VIEW(bezier())
#VIEW(ring(.5, 1))


def Arch(length, w, depth):
    def Arch1(angle):
        radius = (length/2)/(cos(angle/ 2))
        print (radius)
        ArchSurf2D = ArchSurface(1, .5)
        #domain2D = COMP([T(1)(angle / 2), PROD([INTERVALS(PI - angle)(16), Q(1)])])
        #ceiling = MAP(ArchSurf2D)(domain2D)

        #domain3D = PROD([domain2D, Q(1)])
        #Surf3D_0 = AfaL([K(9), ArchSurf2D])
        #Surf3D_1 = AL([K(depth), ArchSurf2D])
        #SolidMap = BEZIER(S3)([Surf3D_0, Surf3D_1])
        return CUBOID([1,1,1])
        #return T(3)(COMP([DIFFERENCE(ceiling), MAP(SolidMap)])(domain3D))

    return Arch1
