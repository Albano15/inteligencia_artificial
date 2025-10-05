#Sistemas Especialista

import experta

base_conhecimento = {
    "sol": {
        "quente": "Ir à Praia",
        "ameno": "Fazer uma caminhada no parque"
    },
    "nublado": {
        "quente": "Visitar um parente com ar condicionado",
        "ameno": "Ficar em casa e tomar café"
    },
    "chuva": {
        "quente": "Ficar na chuva",
        "ameno": "Ficar em casa comendo pipoca"
    }
}

# Motor de inferência (SIMPLES)

def motor_inferencia_clima(fatos):
    clima = fatos.get('clima')
    temperatura = fatos.get('temperatura')

    if clima in base_conhecimento and temperatura in base_conhecimento[clima]:
        return base_conhecimento[clima][temperatura]
    else:
        return "Não tenho recomendação para esta combinação de clima e temperatura."
    
# Simulação

fatos = {
    "clima": "chuva",
    "temperatura": "ameno"
}

conclusao = motor_inferencia_clima(fatos)
print(f"Fatos: {fatos}")
print(f"Recomendação do sistema: {conclusao}")

# Forward e Backward

fatos = ["tem_pelos", "voa", "produz_leite"]
regras = [
    {
        "se": ["tem_penas", "voa"],
        "entao": "e_pessaro"
    },
    {
        "se": ["tem_penas", "pode_cantar"],
        "entao": "e_canario"
    },
    {
        "se": ["tem_pelos", "produz_leite"],
        "entao": "e_mamifero"
    },
    {
        "se": ["tem_pelos", "voa"],
        "entao": "e_morcego"
    },
    {
        "se": ["tem_pelos", "pode_cantar"],
        "entao": "e_pirata"
    },
    {
        "se": ["tem_pelos", "late"],
        "entao": "e_cachorro"
    }
]

# Motor de Inferência (Forward)

def motor_inferencia_forward(fatos_init, regras):
    fatos_derivados = list(fatos_init)
    novo_fato = True

    while novo_fato:
        novo_fato = False
        for regra in regras:
            condicao_satisfeita = all(condicao in fatos_derivados for condicao in regra["se"])

            if condicao_satisfeita and regra["entao"] not in fatos_derivados:
                fatos_derivados.append(regra["entao"])
                print(f"Regra disparada: SE {regra['se']} ENTAO {regra['entao']}")
                print(f"Fatos adicionado: {regra['entao']}")
                novo_fato = True

    return fatos_derivados

# Simulação

print(f"Fatos iniciais: {fatos}")
fatos_finais = motor_inferencia_forward(fatos, regras)
print(f"Fatos finais: {fatos_finais}")

# Biblioteca Experta
from experta import *

class Caracteristica(Fact):
    "Representa uma característica observada"
    pass

class Animal(KnowledgeEngine):
    @DefFacts()
    def fatos_iniciais(self):
        yield Caracteristica("tem_penas")
        yield Caracteristica("voa")
        yield Caracteristica("pode_cantar")
        print("Fatos iniciais carregados.")

    @Rule(Caracteristica("tem_penas"), Caracteristica("voa"))
    def regra_e_passaro(self):
        print("Regra disparada: SE tem_penas e voa ENTAO e_passaro")
        self.declare(Fact(animal="e_passaro"))

    @Rule(Fact(animal="e_passaro"), Caracteristica("pode_cantar"))
    def regra_e_canario(self):
        print("Regra disparada: SE e_passaro e pode_cantar ENTAO e_canario")
        self.declare(Fact(animal="canário"))

    @Rule(Fact(animal=MATCH.tipo))
    def print_resultado(self, tipo):
        if tipo == "canário":
            print(f"Conclusão final do sistema, o tipo de anial é: {tipo}")


animal = Animal()
animal.reset()
animal.run()