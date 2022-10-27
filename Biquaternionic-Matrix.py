from sympy import *
import sympy.algebras.quaternion as qt

"""
To begin any biquaternion q can created using q = qt.Quaternion(w1 + I*w2, x1 + I*x2, y1 + I*y2, z1 + I*z2), where w1,..z2 are either numbers or sympy Symbols.
The problem though is that when showing these numbers sympy will show complex i and quaternionic i as the same symbol. To fix this I defined the method {disp}
"""


def disp(q):
  """
      The sympy.algebra.quaternion method {Quaternion} can incode this number system, but it does not distinguish between complex i and quaternionic I, 
      which are technically different. 
      
      Given a biquaternion q = w + x I + y J + z K created through the quaternion method of sympy, the methods q.a = w, q.b = x etc... 
      To distinguish in the display of these quaternions, the {disp} method takes this biquaternion and converts the quaternionic units i,j,k
      into \hat{I} \hat{J} \hat{K}, to better distinguish them from complex i
      
      This has no effect on the variable q, and all operations done on q work the same as they would for the Quaternion class.
      This is just for display purposes.
  """
        ihat, jhat, khat = symbols('\hat{I} \hat{J} \hat{K}')
        return q.a + ihat*q.b + jhat*q.c + khat*q.d
        
def quaternize(a,b):
"""
At present the only way to define a biquaternion is by specifying the 8 numbers w1,...z2. In order to make this quicker, the method {quaternize}
takes as input two strings a and b and makes a biquaternion in which the 4 complex real components are w1, x1, y1, z1 = a_0, a_1, a_2, a_3 and 
the 4 complex imaginary components are w2, x2, y2, z2 = b_0, b_1, b_2, b_3. 
"""
  stringvec = ''
  for i in range(4):
    stringvec = stringvec + (a + "_{" + str(i) + "} " + b + "_{" + str(i) + "} ")
  q0, p0, q1, p1, q2, p2, q3, p3 = symbols(stringvec)
  return qt.Quaternion(q0 + p0*I,q1 + p1*I,q2 + p2*I,q3 + p3*I)


class bq:
    def __init__(self, q00, q01, q10, q11):
        self.q00, self.q01, self.q10, self.q11 = q00, q01, q10, q11



        
    def comp(self, n, m):
        if n == 0:
            if m == 0:
                return self.q00
            elif m == 1:
                return self.q01
            else: pass
        elif n == 1:
            if m == 0:
                return self.q10
            elif m == 1:
                return self.q11
            else:pass
        else: pass
        
    def show(self):
        # Shows the Qmatrix in simplified form
        
        return Matrix([[Q.disp(self.q00), Q.disp(self.q01)],
                       [Q.disp(self.q10), Q.disp(self.q11)]])
    
    def scale(self, a):
        return Q(a*self.q00, a*self.q01, a*self.q10, a*self.q11)
    
    def add(self, P):
        return Q(self.q00 + P.q00, self.q01 + P.q01, self.q10 + P.q10, self.q11 + P.q11)
    
    def dot(self, P):
        qp00, qp10 = self.q00*P.q00 + self.q01*P.q10, self.q00*P.q01 + self.q01*P.q11
        qp01, qp11 = self.q10*P.q00 + self.q11*P.q10, self.q10*P.q01 + self.q11*P.q11
        return Q(simplify(qp00), simplify(qp10),simplify(qp01), simplify(qp11))
    
    def commutator(self, P):
        return self.dot(P).add((P.dot(self)).scale(-1))
    
    def anticommutator(self, P):
        return self.dot(P).add(P.dot(self))
    
   # These are some important quaternions that come up alot, accessed via Qmatrix.V for all V in the list bellow.
    
    O = qt.Quaternion(0,0,0,0)
    U = qt.Quaternion(1,0,0,0)
    Ihat = qt.Quaternion(0,1,0,0)
    Jhat =qt.Quaternion(0,0,1,0)
    Khat = qt.Quaternion(0,0,0,1)
    V = qt.Quaternion(0, 0, I/sqrt(2), I/sqrt(2))
    


    def Basis(a,b,c,d,w,x,y,z):
        Z0 = Q.σ0.scale(a).add(Q.s.scale(b).add(Q.t.scale(c).add(Q.r.scale(d))))

        Z1 = Q.σ0.scale(w).add(Q.u1.scale(x).add(Q.u2.scale(y).add(Q.u3.scale(z))))
        return [Z0, Z1]
        
    def ize(w,x,y,z):
        return Qmatrix(quaternize(w), quaternize(x),quaternize(y),quaternize(z))
  
