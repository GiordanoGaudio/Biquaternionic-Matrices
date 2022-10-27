from sympy import *
import sympy.algebras.quaternion as qt

"""

----------------------------------------------------------------------------------------------
BIQUATERNIONS
----------------------------------------------------------------------------------------------

      What are biquaternions in python?
      
      ---------------------------------
      
      The sympy.algebra.quaternion method {Quaternion} can incode this biquaternionic number system. 
      Any biquaternion q can created using q = qt.Quaternion(w1 + I*w2, x1 + I*x2, y1 + I*y2, z1 + I*z2),
      where w1,..z2 are either real numbers or sympy Symbols representing real numbers.
      I will define some important biquaternions to demonstrate how the package works  
      
"""

Z     = qt.Quaternion(0,0,0,0)                                                           # 0
U     = qt.Quaternion(1,0,0,0)                                                           # 1
i     = qt.Quaternion(I,0,0,0)                                                           # complex i
Ihat  = qt.Quaternion(0,1,0,0)                                                           # quaternionic i
Jhat  = qt.Quaternion(0,0,1,0)                                                           # quaternionic j
Khat  = qt.Quaternion(0,0,0,1)                                                           # quaternionic k


"""
    As it turns out, it will be important to quickly reference our basis vectors through an index
"""

def V(n):
  if n == 0: return U
  elif n == 1: return Ihat
  elif n == 2: return Jhat
  elif n == 3: return Khat
  else: pass

"""
  
    Algebra?
    ----------------------
    

    In the class Quaternion, algebra is defined as expected so +, -, * are all defined.
    The class also has methods like .exp() and .norm() etc.
    
    


    Conjugations?
    -------------

    There are 7 different types of ways to conjugate a biquaternion
    
    star is the complex conjugate
    tilde is the quaternionic conjugate
    bar is both at once
    
   hat1, 2, 3 conjugates everything but Ihat, Jhat, or Khat.
   Its easy to show that hat(q,n) = -V(n)*q*V(n) where V is the function defined above
   
   asterix1, 2, 3 conjugates only Ihat, Jhat, or Khat
   Its easy to show that asterix(q,n) = tilde(hat(q,n))
   
   and sthat, stasterix are star and hat or asterix respectively
   
   CAUTION: If using symbols, then you need to declare that the symbols are real! 
   
"""

def star(q):        return qt.Quaternion(conjugate(q.a), conjugate(q.b), conjugate(q.c), conjugate(q.d))

def tilde(q):       return qt.Quaternion(q.a,-q.b, -q.c, -q.d)

def bar(q):         return star(tilde(q))

def hat(q, n):      return -V(n)*q*V(n)

def asterix(q, n):  return tilde(hat(q,n)) 

def stasterix(q,n): return star(asterix(q,n))

def sthat(q,n):     return star(hat(q,n))

"""

Include all conjugations into a single function

"""


def conj(q, k = 0, n = 1, m = 0):
    if k == 0: return star(q)
    elif k == 1: return tilde(q)
    elif k == 2: return bar(q)
    elif k == 3:
        if m == 0: return hat(q,n)
        elif m == 1: return sthat(q,n)
        else: pass
    elif k == 4:
        if m == 0: return asterix(q,n)
        elif m == 1: return stasterix(q,n)
        else: pass
    else: pass
    
    

"""

    CAUTION
    --------
    
    You should be carefull when using these methods (https://docs.sympy.org/latest/modules/algebras.html) as they were 
    defined to work for quaternions and not biquaternions.
    As an example if you use the method .inverse() you could get into trouble
    as the inverse formula in the quaternions can divide by 0 in the biquaternions so...
    
    SOME BIQUATERNIONS DO NOT HAVE INVERSES
    
    The rule is, an inverse exists if q.norm() = q*tilde(q) != 0.
    
    This happens iff
    
        w1^2 + x1^2 + y1^2 + z1^2 = w2^2 + x2^2 + y2^2 + z2^2
    
                and
                
        w1w2 + x1x2 + y1y2 + z1z2 = 0

"""



"""
 
      Displaying them
      ---------------
 
       Given a biquaternion q = w + x I + y J + z K created through the quaternion method of sympy, the methods q._ return a component of the biquaternion
      (q.a = w, q.b = x, q.c = y, q.d = z, all of which are complex numbers)
      
      To better distinguish in the display of these biquaternions, the {disp} method takes this biquaternion and shows the quaternionic units i,j,k
      into \hat{I} \hat{J} \hat{K}, and shows complex i as i.
      This has no effect on the variable q, and all operations done on q work the same as they would for the Quaternion class.
      This is just for display purposes.
  
"""

def disp(q):
  ihat, jhat, khat = symbols('\hat{I} \hat{J} \hat{K}')                           # New quaternionic units
  return q.a + ihat*q.b + jhat*q.c + khat*q.d                                    # Change in display
        
"""

    Defining them symbolically
    --------------------------

    At present the only way to define a biquaternion is by specifying the 8 numbers w1,...z2. In order to make this quicker, the method {quaternize}
    takes as input two strings a and b and makes sympy Symbols a_0, ... b_3. Then it defines a biquaternion q = w + x I + y J + z K
    in which the 4 complex real components are w1, x1, y1, z1 = a_0, a_1, a_2, a_3 and 
    the 4 complex imaginary components are w2, x2, y2, z2 = b_0, b_1, b_2, b_3. 
    
"""
    
    
def quaternize(a,b):
  stringvec = ''
  for i in range(4):
    stringvec = stringvec + (a + "_{" + str(i) + "} " + b + "_{" + str(i) + "} ")        # Creates a string of "a_0 b_0 ... a_3 b_3"
  q0, p0, q1, p1, q2, p2, q3, p3 = symbols(stringvec, real = True)                                    # Converts these into sympy Symbols
  return qt.Quaternion(q0 + p0*I,q1 + p1*I,q2 + p2*I,q3 + p3*I)                          # makes of them a biquaternion



"""

----------------------------------------------------------------------------------------------
2 by 2 MATRICES OF BIQUATERNIONS
----------------------------------------------------------------------------------------------

      Now that we have the ability to define, manipulate, and show biquaternions, 
      we are ready to define matrices of them. I will do this in a class
      and define many important methods with them.
      
      Firstly, a biquaternionic matrix has 4 components and should represent
      the matrix:
      
      q00 q01
      q10 q11
      
      Where qij is a biquaternion so defined with the qt.Quaternion method.
      
"""


class BQ_Matrix:
    def __init__(self, q00, q01, q10, q11):
        self.q00, self.q01, self.q10, self.q11 = q00, q01, q10, q11

    """

        The following method simply extracts the component. So if Q is a BQ_Matrix
        then Q.comp(0,0) = q00

    """

        
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
    
    """
    
        Showing the Matrix
        ------------------

        To display a biquaternionic matrix, we make use of the Matrix method from
        sympy along with the display function defined for biquaternions. 
            
        To show the matrix use Q.show()

    """    
        
    def show(self):
        return Matrix([[disp(self.q00), disp(self.q01)],
                      [disp(self.q10), disp(self.q11)]])
                      
    """
    
        Scaling
        ---------

        To multiply a matrix by a scalar do it component wise keeping in mind
        that the biquaternions are noncommutative so we need to specify 
        the side (right or left)


    """    
                      
    
    def scale(self, a, side = 0):
        if side == 0: # Right multiplication (by default)
            return BQ_Matrix(a*self.q00, a*self.q01, a*self.q10, a*self.q11)
        
        elif side == 1: # Left multiplication
            return BQ_Matrix(self.q00*a, self.q01*a, self.q10*a, self.q11*a)
        
    """
    
        Addition of Matrices
        -------------------

        Add to matrices component wise


    """            
    
    def add(self, P): 
        return BQ_Matrix(self.q00 + P.q00, self.q01 + P.q01, 
                         self.q10 + P.q10, self.q11 + P.q11)
    
    """

        Multiplication of Matrices
        -----------------------------
        
        Using the normal rules of matrix multiplication (keeping order in mind)


    """    
    
    def dot(self, P):
        qp00, qp10 = self.q00*P.q00 + self.q01*P.q10, self.q00*P.q01 + self.q01*P.q11
        qp01, qp11 = self.q10*P.q00 + self.q11*P.q10, self.q10*P.q01 + self.q11*P.q11
        return Q(simplify(qp00), simplify(qp10),simplify(qp01), simplify(qp11))
    
    """

       (Anti)Commutator
       -------------------
       
       The commutator and anticommutator is very important in physics. They are
       defined by AB - BA or AB + BA respectively, and tell us if AB = BA or -BA
       
       In this class that would be A.dot(B).add((B.dot(A)).scale(+1 or -1))


    """    
    
    def commutator(self, P):
        return self.dot(P).add((P.dot(self)).scale(-1))
    
    def anticommutator(self, P):
        return self.dot(P).add(P.dot(self))
    


    """
        Trace
        -----
        
        The trace of a matrix is the sum of its diagonal components
    
    """
    
    def tr(self):
        return self.q00 + self.q11

    """
        Determinant
        ------------
        
        CAUTION: The determinant of a biquaternionic matrix does not always exist!
        
        We'll say that the matrix is determinable iff q00 = 0, or is invertable
        
       If the matrix is determinable then the determinant is given by
       
       -q10*q01 iff q00 == 0
       
       q00*q11 - q00*q10*q00.inverse()*q01 else
       
       This is called the Dieudonne determinant for noncommutative algebras
    
    """
    
    def det(self):
        if self.q00 == Z:
            return - self.q10*self.q01
        elif simplify(self.q00.norm()) == 0: 
            print ("The matrix is indeterminable")
            return
        else:
            return  self.q00*self.q11 - self.q00*self.q10*self.q00.inverse()*self.q01
            
    """
        Transpose
        ---------
        
        As usually defined
    
    """       
    
    def T(self):
        return BQ_Matrix(self.q00, self.q10, self.q01, self.q11)
    
    """
    
        Conjugates and Daggers
        ----------------------
        
        For each of the conjugations defined, there is a kind of hermitian conjugation of the matrix
        
        Look to the conjugate function for a legend on which inputs do what
    
    """
    
    def Conj(self, k = 0, n = 1, m = 0):
        return BQ_Matrix(conj(self.q00, k,n,m), conj(self.q01, k,n,m), conj(self.q10, k,n,m), conj(self.q11, k,n,m))
    
    def dag(self, k = 0, n = 1, m = 0):
        return self.Conj(k,m,n).T()
    
    """
    
        Lastly, a way to quickly make biquaternionic matrix would be nice in the same way we have quaternize
        
        Well seperate our 4 types of variables into their real and imaginary components 
        and let quaternize make a subscript for every quaternionic component

    
    """   
        
    def ize(w,x,y,z):
        stringvec = ''
        for A in ['a', 'b', 'c', 'd']:
            stringvec = stringvec + (A + "^{re} ")
        for A in ['a', 'b', 'c', 'd']:
            stringvec = stringvec + (A + "^{im} ")
        w0,x0,y0,z0,w1,x1,y1,z1, dump = stringvec.split(' ')
        
        W = quaternize(w0,w1)
        X = quaternize(x0,x1)
        Y = quaternize(y0,y1)
        Z = quaternize(z0,z1)
        
        
        return BQ_Matrix(W,X,Y,Z)
  
