from dataclasses import dataclass

@dataclass
class ResultModel:
    tipo_cruzamento: str
    chave1: str
    chave2: str
    total_anos: int