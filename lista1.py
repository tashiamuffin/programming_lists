###Stwórz klasę Vector przechowującą kolekcję liczb. Zaimplementuj
#• konstruktor przyjmujący rozmiar wektora jako argument (domyślnie 3),
#• metodę do losowej generacji elementów wektora,
#• metodę do wczytywania elementów wektora z listy podanej jako argument,
#• operator dodawania i odejmowania dwóch wektorów (powinien rzucać wyjątek ValueError w sytuacji, kiedy wektory mają różne rozmiary),
#• mnożenie wektora przez skalar,
#• metodę wyliczającą długość wektora,
#• metodę wyliczającą sumę elementów wektora,
#• metodę wyliczającą iloczyn skalarny dwóch wektorów,
#• reprezentację tekstową wektora,
#• operator [] pozwalający na dostęp do konkretnych elementów wektora,
#• operator in sprawdzający przynależność elementu do wektora.
#Kod powinien być napisany w formie modułu, z częścią wykonywalną testującą klasę. Proszę zwrócić szczególną uwagę na udokumentowanie modułu i metod


class Vector:
    """The class Vector can be used for analizing vectors in different dimensions, it can help with adding them, making scalar products or calculating their length. It contains methods such as initializing one, method generate, method load, operators such as add, sub and mul, method length, sum, multiply, operator str, getitem and contains. initializing operator that takes a positive argument and saves it as a size of a vector. The size is by default equal 3. Vector's coordinates are being presented as a list containg its elements, the size is a number of elements in that list. It generates the list of initial coordinates = 0 """

    def __init__(self, n=3):       
        if n <= 0:
            raise ValueError('dimension cannot be a negative number')
        else:
            self.n = n
            self.vector = []
            for i in range(0, self.n):
                self.vector.append(0)

    def random_values(self):
        """ a method that generates random integer coordinates for a vector, taking no argument. It clears the previous coordinates and returns new ones."""
        import random
        self.vector.clear()
        for n in range(0, self.n):
            self.vector.append(random.randint(-100, 100))
        return self.vector

    def from_list(self, lista):
        """ a method that loads coordinates from the list taken as a argument, unless the size of the list is different than the size of a vector (then ValueError is raised). It clears the previous coordinates and returns new ones."""
        if len(lista) != self.n:
            raise ValueError('different sizes, cannot load')
        else:
            for i in lista:
                if type(i) != int and type(i) != float:
                    raise ValueError('elements cannot be strings')
            self.vector.clear()
            for n in range(0, len(lista)):
                 self.vector.append(lista[n])
            return self.vector

    def __add__(self, wektor):
        """ an operator that takes a vector as an argument and adds it to the other one, which is changed and the method returns the new coordinates. If vectors are different sizes ValueError is raised"""
        if self.n == wektor.n:
            add = []
            for n in range(0, self.n):
                add.append(self.vector[n] + wektor.vector[n])
            return add
        else:
            raise ValueError('different sizes')

    def __sub__(self, wektor):
        """ an operator that takes a vector as an argument and substract it from the other one, which is changed and the method returns the new coordinates. If vectors are different sizes ValueError is raised"""
        if self.n == wektor.n:
            diff =[]
            for n in range(0, self.n):
                diff.append(self.vector[n] - wektor.vector[n])
            return diff
        else:
            raise ValueError('different sizes')
    
    def __mul__(self,skalar):
        """ an operator that takes a number (a scalar) and a vector and returns a new vector's coordinates which are the old ones multiplied by the scalar. """
        prod = Vector(self.n)
        for n in range(0, self.n):
            prod.vector[n] = (self.vector[n] * skalar)
        return prod.vector

    def __rmul__(self, skalar):
        """ an operator that takes a number (a scalar) and a vector and returns a new vector's coordinates which are the old ones multiplied by the scalar. """
        prod = Vector(self.n)
        for n in range(0, self.n):
            prod.vector[n] = (self.vector[n] * skalar)
        return prod.vector

    def vec_len(self):
        import math
        """ a method that calculates and returns a vector's length by adding its squared elements and then square rooting their sum. """
        sum = 0
        for n in range(0, self.n):
            sum = sum + self.vector[n] ** 2
        d = math.sqrt(sum)
        return d

    def elem_sum(self):
        """ a method that calculates and returns a vector coordinates' sum. """
        sum = 0
        for i in range(0, self.n):
            sum = sum + self.vector[i]
        return sum

    def scalar_prod(self, wektor):
        """ a method that takes two vectors and calculates and returns their scalar product. If vectors are different sizes ValueError is raised"""
        if self.n == wektor.n:
            sum = 0
            for n in range(0, self.n):
                sum = sum + self.vector[n] * wektor.vector[n]
            return sum
        else:
            raise ValueError('different sizes')

    def __str__(self):
        """ an operator that returns a text representation of a vector"""
        return "{}".format(self.vector)

    def __getitem__(self, index):
        """ an operator that takes a number as an argument and returns an element on its equivalent position in vector's coordinates """
        if type(index) != int :
            raise ValueError('wrong type of a number')
        elif index > self.n:
            raise ValueError("number out of list's range")        
        else:
            a = self.vector[index]
            return a

    def __contains__(self, element):
        """ an operator that takes an element as an argument and returns True or False that depends on whether vector's coordinates contains it or not. If the argument is not a number ValueError is raised"""
        if type(element) != int and type(element) != float:
            raise ValueError('element must be numbers')
        if element in self.vector:
            return True
        else:
            return False

