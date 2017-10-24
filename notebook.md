###cerchio
```python
def circle ( p ) :
alpha = p [ 0 ]
return [ COS ( alpha ) , SIN ( alpha ) ]
obj = MAP ( circle ) ( INTERVALS ( 2 * PI ) ( 32 ) )
VIEW ( obj )
```

###spirale
```python
def circle ( p ) :
    alpha = p [ 0 ]
    return [ COS ( alpha ) , SIN ( alpha ) , alpha]
obj = MAP ( circle ) ( INTERVALS ( 2 * PI ) ( 32 ) )
VIEW ( obj )

def spiral(h):
	def spiral0(p):
		alpha=p[0]
		return [COS(alpha),SIN(alpha),alpha/(2*PI)]
	return spiral0

obj=MAP(spiral(0.2))(dom)

dom2D=PROD([INTERVALS(2*PI)(24),INTERVALS(1)(1)])

def ball(p):
	a,r=p
	return [r*COS(a),r*SIN(a)]

o=MAP(ball)(dom2D)


def spiral(p):
	a,r=p
	return[r*COS(a),r*SIN(a),a*0.2/(2*PI)]
```

###tempio
```python
def Column(r,h):
	basis = CUBOID([2*r*1.2, 2*r*1.2, h/12.0])
	trunk = CYLINDER([r, (10./12)*h])(12)
	capital = basis
	beam = S(1)(3)(capital)
	return INSR(TOP)([basis,trunk, capital, beam])
col = Column(1,12)

def ColRow(n):
	return COMP([INSR(RIGHT),N(n)])(col)
ColRow(4)

VIEW(INSR(RIGHT)(N(4)(col)))



def gable(radius,h,n):
	w=1.2*radius
	l = 3*n*(2*w)
	basis=COMP([EMBED(1),CUBOID])([l,w])
	apex=MKPOL([[[l/2,0,h/2],[l/2,w,h/2]],[[1,2]],None])
	return JOIN([basis,apex])

rawgable = TOP([ColRow(4),gable(1,12,4)])

Temple1=COMP([STRUCT,CAT]) ([ 
[rawgable,T(2)(6)],
NN(4)([ColRaw(4),T(2)(6)]),
[rawgable] ])

Temple1=STRUCT(NN(40)(ColRow(4)))

 verts = [[0,0],[0,4],[4,0],[4,4],[2,6]]

 cells = [[1,2,3,4,5]]

 casa = MKPOL([verts,cells,None])
type(casa)
 VIEW(casa)

porta = CUBOID([1,3])

finestra = CUBOID([1,1.5])

VIEW(STRUCT(AA(SKELETON(1))([casa,porta,finestra])))

Tp = T(1)(1.5)
Tf=T([1,2])([2.75,1.5])

figura = STRUCT([casa,Tp(porta),Tf(finestra)])

VIEW(SKELETON(1)(figura))
figura = DIFFERENCE([casa,Tp(porta),Tf(finestra)])

modello = PROD([figura,Q(4)])

 Tc = T(1)(4)

VIEW(STRUCT([Tc,modello]))

VIEW(STRUCT(NN(10)([Tc,modello]))))

Ty = T(2)(10)

VIEW(STRUCT(NN(20)([Tz,STRUCT(NN(10)([Tc,modello]))])))

VIEW(STRUCT([SPHERE(1)([8,8]),STRUCT([T(3)(2),CONE([1.0,3.0])(16)]),CYLINDER([1.0,2.0])(20),TORUS([3,4])([50,50]),STRUCT([T(2)(-1),T(1)(-1),T(3)(-1),CUBOID([2,2,-5])])]))
```


###traslazione
```python
T([1,2,3])([0.5,1.5,1])(CUBOID([3,4,5]))
```

###scalamento
```python
S([1,2,3])([0.5,1.5,1])(CUBOID([3,4,5]))
```

###rotazioni
```python
###
R([1,2])(PI/3)(CUBOID([3,4,5]))

###
def element():
return COMP([ T([1,2]),([-5,-5]))(CUBOID([10,10,2]))]);

element = COMP([T([1,2]),([-5,-5]))(CUBOID([10,10,2]));
column=STRUCT(NN(10)([element,T(3)(2),R([1,2])(PI/8)]));

###
R(m,a)=Rx(-b)Ry(-g)Rz(a)Ry(g)Rx(b)

R(m,a)=Qm^-1 Rz(a) Qm
Qm
```
