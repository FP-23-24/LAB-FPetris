import unittest
from utiles import inicializa_tablero, coloca_pieza, busca_filas_completas, posicion_valida, rota_pieza

class TestUtiles(unittest.TestCase):

    def test_inicializa_tablero(self):
        # Tamaños estándar
        self.assertEqual(inicializa_tablero(3, 2), [[None, None, None], [None, None, None]])
        # Tablero de una sola fila y columna
        self.assertEqual(inicializa_tablero(1, 1), [[None]])
        # Tablero no cuadrado
        self.assertEqual(inicializa_tablero(2, 3), [[None, None], [None, None], [None, None]])

    def test_coloca_pieza(self):
        # Colocar una pieza simple en un tablero vacío
        tablero = [[None, None, None], [None, None, None], [None, None, None]]
        pieza = [[True]]
        coloca_pieza(tablero, pieza, 1, 1, 'red')
        self.assertEqual(tablero, [[None, None, None], [None, 'red', None], [None, None, None]])

        # Colocar una pieza más compleja en un tablero vacío
        tablero = [[None, None, None], [None, None, None], [None, None, None]]
        pieza = [[True, True], [False, True]]
        coloca_pieza(tablero, pieza, 0, 0, 'blue')
        self.assertEqual(tablero, [['blue', 'blue', None], [None, 'blue', None], [None, None, None]])


    def test_busca_filas_completas(self):
        # Sin filas completas
        tablero = [['red', None, 'red'], [None, 'red', None], ['blue', None, 'blue']]
        self.assertEqual(busca_filas_completas(tablero), [])

        # Varias filas completas
        tablero = [['red', 'red', 'red'], [None, 'red', None], ['blue', 'blue', 'blue']]
        self.assertEqual(busca_filas_completas(tablero), [0, 2])

        # Tablero vacío
        self.assertEqual(busca_filas_completas(inicializa_tablero(3, 2)), [])

    def test_posicion_valida(self):
        tablero = inicializa_tablero(4, 4)
        pieza = [[True, True], [True, False]]

        # Posición válida
        self.assertTrue(posicion_valida(tablero, pieza, 1, 1))

        # Colisión con pieza existente
        coloca_pieza(tablero, pieza, 2, 2, 'red')
        self.assertFalse(posicion_valida(tablero, pieza, 2, 2))

        # Fuera del tablero a la izquierda
        self.assertFalse(posicion_valida(tablero, pieza, -1, 1))

        # Fuera del tablero por la parte superior
        self.assertFalse(posicion_valida(tablero, pieza, 1, -1))

        # Fuera del tablero por la parte inferior
        self.assertFalse(posicion_valida(tablero, pieza, 1, 3))

    def test_rota_pieza(self):
        # Pieza de 3x2
        pieza = [[True, False, True], [False, True, False]]
        self.assertEqual(rota_pieza(pieza), [[False, True], [True, False], [False, True]])

        # Pieza de 1x1 (no debería cambiar)
        pieza_unica = [[True]]
        self.assertEqual(rota_pieza(pieza_unica), [[True]])

        # Pieza de 2x3
        pieza = [[True, False], [True, True], [False, True]]
        self.assertEqual(rota_pieza(pieza), [[False, True, True], [True, True, False]])

        # Pieza de 2x2 (forma de L)
        pieza_L = [[True, False], [True, True]]
        self.assertEqual(rota_pieza(pieza_L), [[True, True], [True, False]])

if __name__ == '__main__':
    unittest.main()
