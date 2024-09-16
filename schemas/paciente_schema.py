from pydantic import BaseModel
from typing import Optional, List
from model.paciente import Paciente
import json
import numpy as np

class PacienteSchema(BaseModel):
    """Define como um novo paciente a ser inserido deve ser representado
    """
    name: str = "Maria"
    radius_mean: float = 12.34
    texture_mean: float = 18.56
    perimeter_mean: float = 78.90
    area_mean: float = 450.0

class PacienteViewSchema(BaseModel):
    """Define como um paciente será retornado
    """
    id: int = 1
    name: str = "Maria"
    radius_mean: float = 12.34
    texture_mean: float = 18.56
    perimeter_mean: float = 78.90
    area_mean: float = 450.0
    outcome: str = "Benigno"  # Resultado da previsão
    
class PacienteBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.
    Ela será feita com base no nome do paciente.
    """
    name: str = "Maria"

class ListaPacientesSchema(BaseModel):
    """Define como uma lista de pacientes será representada
    """
    pacientes: List[PacienteSchema]

    
class PacienteDelSchema(BaseModel):
    """Define como um paciente para deleção será representado
    """
    name: str = "Maria"
    
# Apresenta apenas os dados de um paciente    
def apresenta_paciente(paciente):
    """Retorna uma representação do paciente seguindo o esquema para previsão de câncer de mama."""
    return {
        "id": paciente.id,
        "name": paciente.name,
        "radius_mean": paciente.radius_mean,
        "texture_mean": paciente.texture_mean,
        "perimeter_mean": paciente.perimeter_mean,
        "area_mean": paciente.area_mean,
        "outcome": paciente.outcome  # Pode ser Positivo ou Negativo
    }
    
# Apresenta uma lista de pacientes
def apresenta_pacientes(pacientes: List[Paciente]):
    """ Retorna uma representação do paciente seguindo o schema definido em
        PacienteViewSchema, adaptado para os atributos de previsão de câncer de mama.
    """
    result = []
    for paciente in pacientes:
        result.append({
            "id": paciente.id,
            "name": paciente.name,
            "radius_mean": paciente.radius_mean,
            "texture_mean": paciente.texture_mean,
            "perimeter_mean": paciente.perimeter_mean,
            "area_mean": paciente.area_mean,
            "outcome": paciente.outcome  # Pode ser "Benigno" ou "Maligno"
        })

    return {"pacientes": result}
