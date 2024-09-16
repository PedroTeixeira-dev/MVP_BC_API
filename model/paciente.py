from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base

# colunas = Pregnancies,Glucose,BloodPressure,SkinThickness,test,BMI,DiabetesPedigreeFunction,Age,Outcome

class Paciente(Base):
    __tablename__ = 'pacientes'
    
    id = Column(Integer, primary_key=True)
    name = Column("Name", String(50))
    radius_mean = Column("RadiusMean", Float)
    texture_mean = Column("TextureMean", Float)
    perimeter_mean = Column("PerimeterMean", Float)
    area_mean = Column("AreaMean", Float)
    outcome = Column("Diagnostic", Integer, nullable=True)  # 0 para Benigno, 1 para Maligno
    data_insercao = Column(DateTime, default=datetime.now())
    
    def __init__(self, name: str, radius_mean: float, texture_mean: float, 
                 perimeter_mean: float, area_mean: float, outcome: int, 
                 data_insercao: Union[DateTime, None] = None):
        """
        Cria um Paciente com informações para previsão de câncer de mama.

        Arguments:
            name: nome do paciente
            radius_mean: média do raio
            texture_mean: média da textura
            perimeter_mean: média do perímetro
            area_mean: média da área
            outcome: diagnóstico (0 para benigno, 1 para maligno)
            data_insercao: data de quando o paciente foi inserido à base
        """
        self.name = name
        self.radius_mean = radius_mean
        self.texture_mean = texture_mean
        self.perimeter_mean = perimeter_mean
        self.area_mean = area_mean
        self.outcome = outcome

        # Se não for informada, será a data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao
