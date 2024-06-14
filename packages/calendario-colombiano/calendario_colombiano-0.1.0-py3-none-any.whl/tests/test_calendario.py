import unittest
from datetime import date, timedelta
from calendario_colombiano.calendario import CalendarioColombiano

class TestCalendarioColombiano(unittest.TestCase):
    def setUp(self):
        self.calendario = CalendarioColombiano()

    def calcular_pascua(self, anio):
        # Algoritmo de Butcher para calcular la Pascua
        a = anio % 19
        b = anio // 100
        c = anio % 100
        d = b // 4
        e = b % 4
        f = (b + 8) // 25
        g = (b - f + 1) // 3
        h = (19 * a + b - d - g + 15) % 30
        i = c // 4
        k = c % 4
        l = (32 + 2 * e + 2 * i - h - k) % 7
        m = (a + 11 * h + 22 * l) // 451
        mes = (h + l - 7 * m + 114) // 31
        dia = ((h + l - 7 * m + 114) % 31) + 1
        return date(anio, mes, dia)

    def proximo_lunes(self, fecha):
        return fecha + timedelta(days=(7 - fecha.weekday()))

    def test_festivos_fijos(self):
        for anio in range(2020, 2031):  # Probar en un rango de años
            with self.subTest(anio=anio):
                festivos = self.calendario.obtener_festivos(anio)
                festivos_fijos = [
                    date(anio, 1, 1),  # Año Nuevo
                    date(anio, 5, 1),  # Día del Trabajo
                    date(anio, 7, 20),  # Grito de Independencia
                    date(anio, 8, 7),  # Batalla de Boyacá
                    date(anio, 12, 8),  # Inmaculada Concepción
                    date(anio, 12, 25),  # Navidad
                ]
                for festivo in festivos_fijos:
                    self.assertIn(festivo, festivos)

    def test_festivos_moviles(self):
        for anio in range(2020, 2031):  # Probar en un rango de años
            with self.subTest(anio=anio):
                festivos = self.calendario.obtener_festivos(anio)
                pascua = self.calcular_pascua(anio)
                festivos_moviles = [
                    pascua - timedelta(days=3),  # Jueves Santo
                    pascua - timedelta(days=2),  # Viernes Santo
                    self.proximo_lunes(pascua + timedelta(days=39)),  # Ascensión de Jesús
                    self.proximo_lunes(pascua + timedelta(days=60)),  # Corpus Christi
                    self.proximo_lunes(pascua + timedelta(days=67)),  # Sagrado Corazón
                ]
                for festivo in festivos_moviles:
                    self.assertIn(festivo, festivos)

    def test_es_festivo(self):
        for anio in range(2020, 2031):  # Probar en un rango de años
            with self.subTest(anio=anio):
                self.assertTrue(self.calendario.es_festivo(date(anio, 1, 1)))  # Año Nuevo
                self.assertFalse(self.calendario.es_festivo(date(anio, 1, 2)))  # No festivo

if __name__ == '__main__':
    unittest.main()
