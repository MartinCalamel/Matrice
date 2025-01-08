"""
Author: Martin Calamel
Created: 2024-12-16
Description: classe matrice pour la gestion de matrice et le calcule matriciel
TODO: - [ OK ] definition Matrice
      - [ OK ] Transposée
      - [ OK ] calcule matriciel
      - [ NO ] inverse
      - [ NO ] factorisation
      - [ NO ] identité (changer la definition pour ne pas avoir a définir une matrice pour l'utiliser)
      - [ OK ] determinant
"""
import sys

class Matrice:
    def __init__(self, matrice : list):
        self.matrice : list = self.init_matrice(matrice)
        self.dim : tuple = (len(self.matrice[0]), len(matrice))
        self.T : list = self.transpose()
    
    def __str__(self):
        """
        Méthode pour le print

        #output : str texte à afficher avec print
        """
        res = ""
        for i in self.matrice:
            res += str(i) + "\n"
        return res

    def check_construction(self, matrice : list) -> bool:
        """
        # Fonction pour verifier la juste construction d'une matrice

        #input : matrice a verifier
        #output : juste construction bool
        """
        if type(matrice) == list:
            if type(matrice[0]) == list:
                x_size = len(matrice[0])
                return all([type(i) == list and len(i) == x_size for i in matrice])
        return False
    
    def init_matrice(self, matrice : list) -> list:
        """
        fonction pour initialiser la matrice si celle-ci est bien définie

        #output : list matrice
        """
        if self.check_construction(matrice):
            return matrice
        else:
            print("Erreur Matrice(): Bad definition... ")
            print(f"please check : \n{matrice}")
            sys.exit()
    
    def transpose(self):
        """
        # Calcule d'une transposée : 
        ``` 
        [[11,12,13],     [[11,21,31],
         [21,22,23],  =>  [12,22,32],
         [31,32,33]]      [13,23,33]]
        ```
        #output : list matrice transposée
        """

        matrice = self.matrice
        transpose_mat = self.create_zero(self.dim[1],self.dim[0])
        for i in range(len(matrice)):
            for j in range(len(matrice[i])):
                transpose_mat[j][i] = matrice[i][j]
        return transpose_mat
    
    def check_mul(self, matrice_B : 'Matrice') -> bool:
        """
        Fonction pour verifier que deux matrice peuvent se multiplier

        #input : sois même et l'autre matrice
        output : peuvent se multiplier bool
        """
        return self.dim[1] == matrice_B.dim[0]
    
    def create_zero(self, m : int, n : int) -> 'Matrice':
        """
        fonction pour crée une matrice de zero avec la dimension (m,n)

        #input : - m dimension n°1
                 - n dimension n°2
        #output : mat_zero Matrice()
        """
        mat_zero = [[0 for __ in range(m)] for _ in range(n)]
        return mat_zero
    
    def identity(self,dim: int):
        """
        créer la matrice identité de dimension dim x dim
        """
        mat = self.create_zero(dim,dim)
        for i in range(dim):
            mat[i][i] = 1
        return Matrice(mat)
    
    def __matmul__(self, matrice_B : 'Matrice') -> 'Matrice':
        """
        Méthode de multiplication de matrice

        #input : matrice de taille compatible
        #output : Matrice resultant de la multiplication
        """
        if self.check_mul(matrice_B):
            result_mat = self.create_zero(self.dim[0],matrice_B.dim[1])

            for i in range(self.dim[0]):
                for j in range(matrice_B.dim[1]):
                    result_mat[i][j] = sum([self.matrice[i][k]*matrice_B.matrice[k][j] for k in range(self.dim[1])])
            return Matrice(result_mat)
        
        print("Erreur Matrice() : matrice can't multiplie...")
        print("Please check dimension")
        sys.exit()
    
    def __rmatmul__(self, matrice_B : 'Matrice') -> 'Matrice':
        """
        Méthode de multiplication de matrice

        #input : matrice de taille compatible
        #output : Matrice resultant de la multiplication
        """
        return self.__matmul__(matrice_B)
    
    def __mul__(self, scalaire : float) -> 'Matrice':
        """
        Méthode de multiplication par un scalaire

        #input : un scalaire
        #output : matrice resultant de la multiplication
        """
        result_mat = self.create_zero(self.dim[0],self.dim[1])
        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                result_mat[i][j] = self.matrice[i][j] * scalaire
        return Matrice(result_mat)
    
    def __rmul__(self, scalaire : float) -> 'Matrice':
        """
        Méthode de multiplication par un scalaire

        #input : un scalaire
        #output : matrice resultant de la multiplication
        """
        return self.__mul__(scalaire)
    
    def __getitem__(self,index):
        """
        slicing personnalisé pour les matrices

        usage : [ln_start:ln_stop:ln_step,col_start:col_stop,col_step]
        """
        indice_slice = [None, None]
        for i, item in enumerate(index):
            if isinstance(item, slice):
                indice_slice[i] = item
            else:
                indice_slice[i] = slice(item, item+1, 1)
        M = self.matrice
        n = self.dim[0]
        p = self.dim[1]
        ind_lines = range(n)[indice_slice[0]]
        ind_cols = range(p)[indice_slice[1]]
        sub_array =[[M[i][j] for j in ind_cols] for i in ind_lines]
        return Matrice(sub_array)

    def select(self, indice: int, mat: 'Matrice'):
        """
        Retourne la matrice sauf la ligne de l'indice et la première colone

        Permet de calculer le determinant de façon recursive (development en ligne) 

        #input : indice de la ligne a enlever, matrice de depart
        #output : matrice recalculer.
        """
        mat_res = []
        for i in range(mat.dim[0]):
            if i != indice:
                ligne = [mat.matrice[i][j] for j in range(1, mat.dim[1])]
                mat_res.append(ligne)
        return Matrice(mat_res)

    def det(self):
        """
        fonction pour calculer le determinant de la matrice self

        #output : float
        """
        if self.is_carre():
            det = self._det(self)
            return det
        print("erreur Matrice dim")

    def _det(self, matrice):
        """
        fonction recursive pour le calcule du determinant
        
        #input : Matrice
        #output : float
        """
        # condition de sortie
        if matrice.dim == (2,2):
            return matrice.matrice[0][0]*matrice.matrice[1][1] - matrice.matrice[0][1]*matrice.matrice[1][0]
        else :
            det = 0
            for i in range(matrice.dim[0]):
                det += matrice.matrice[i][0]*self._det(self.select(i,matrice))
            return det

    def is_carre(self) -> bool:
        """
        fonction qui renvoie si une matrice est carré
        """
        return self.dim[0] == self.dim[1]
    
    





    
    
    
if __name__ == "__main__":
    A = Matrice([[11,12,13],[21,22,23],[31,32,33]])
    print(A)
    print(A.dim)
    print(A.T)

    I = Matrice([[]]).identity(3)
    print(I)

    A1 = Matrice([[1,2],[2,1]])
    B2 = Matrice([[0,1],[1,0]])

    print(A.select(2,A))

    print(A1@B2)

    D1 = Matrice([[1, -1], [3, 4]])
    print(D1.det(), "doit retourner 7")
    D2 = Matrice([[1,2,3],[0,4,5],[0,0,6]])
    print(D2.det(), "doit retourner 24")

