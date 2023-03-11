#CRIANDO SISTEMA DETECTOR DE FRAUDES EM INSTALAÇÕES DE ENERGIA ELÉTRICA
#USANDO LÓGICA FUZZY

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt 
get_ipython().run_line_magic('matplotlib', 'inline')

# Variáves de Entrada

consumo = ctrl.Antecedent(np.arange(0, 21, 1), 'Consumo')
tarifa = ctrl.Antecedent(np.arange(0, 200, 1), 'Tarifa')
gasto = ctrl.Antecedent(np.arange(0, 60, 1), 'Gasto de Energia')
resultado = ctrl.Consequent(np.arange(0, 39, 1), 'Resultado Final')

# Criação automática das variáveis fuzzy de Entrada
consumo.automf(3)
tarifa.automf(3)
gasto.automf(3)

#CRIANDO AS VIEW DAS VARIÁVEIS DE ENTRADA
consumo.view()
tarifa.view()
gasto.view()

# Criação da variável Fuzzy de Saida,
# 
resultado['gato'] = fuzz.trimf(resultado.universe, [0, 0, 12])
resultado['normal'] = fuzz.trimf(resultado.universe, [10, 15, 25])
resultado['suspeito'] = fuzz.trimf(resultado.universe, [22, 29, 35])

#Criando as regras
regra1 = ctrl.Rule(consumo['poor'] | tarifa['poor']|gasto['average'], resultado['normal'])
regra2 = ctrl.Rule(consumo['average'] | tarifa['average']|gasto['good'], resultado['suspeito'])
regra3 = ctrl.Rule(consumo['poor'] | tarifa['average']|gasto['good'], resultado['gato'])

"""
regra1.view()

regra2.view()

regra3.view()

"""
#VERIFICANDO AS REGRAS
resultado_ctrl = ctrl.ControlSystem([regra1, regra2, regra3])
valorresultado = ctrl.ControlSystemSimulation(resultado_ctrl)

# Dados de entrada
input_consumo = float(input("Digite o valor de consumo: ")) #Ex.: 5.258
input_tarifa = int(input("Digite o valor da tarifa de consumo: ")) #Ex.: 150
input_gasto = float(input("Digite o valor unitário no período: ")) #Ex.: 0.256

# Dados de entrada
valorresultado.input['Consumo'] = input_consumo 
valorresultado.input['Tarifa'] = input_tarifa
valorresultado.input['Gasto de Energia'] = input_gasto


#Calculando o valor da conta de energia para o mês
valor_conta = (input_tarifa*input_gasto)
print("\n")
print("O valor total da sua fatura é R$ "+ str(round(valor_conta,2)))

# Calculando o resultado
valorresultado.compute()
print("\n")
print ("Nível de medição: " + str(round(valorresultado.output['Resultado Final'],2)))

#VERIFICANDO O RESULTADO, COM BASE NOS VALORES DE ENTRADA
if valorresultado.output['Resultado Final'] <=13:
    print("\n")
    print("É gato!")
elif valorresultado.output['Resultado Final'] <=19:
    print("\n")
    print("Ligação normal")
else:
    print("\n")
    print("Ligação suspeita")

#EXIBINDO O GRÁFICO DO RESULTADO
resultado.view(sim = valorresultado)

