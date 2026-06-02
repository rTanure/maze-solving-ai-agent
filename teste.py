from src.utils.resultados.resultado_a_star import ResultadoAStar
import time

resultado = ResultadoAStar()

resultado.start()

resultado.addCusto()
resultado.addCusto()
resultado.addCusto()
resultado.addCusto()
resultado.addCusto()

resultado.addExpandidos()
resultado.addExpandidos()
resultado.addExpandidos()

resultado.addPassos()
resultado.addPassos()

resultado.addfronteira()

time.sleep(0.2)

resultado.finish()

resultado.salvarResultado()