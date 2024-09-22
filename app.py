from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import *
from logger import logger
from schemas import *
from flask_cors import CORS

# Instanciando o objeto OpenAPI
info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo tags para agrupamento das rotas
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
paciente_tag = Tag(name="Paciente", description="Adição, visualização, remoção e predição de pacientes com câncer")

# Rota home
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect('/openapi')

# Rota de listagem de pacientes
@app.get('/pacientes', tags=[paciente_tag],
         responses={"200": PacienteViewSchema, "404": ErrorSchema})
def get_pacientes():
    """Lista todos os pacientes cadastrados na base."""
    session = Session()
    pacientes = session.query(Paciente).all()
    
    if not pacientes:
        logger.warning("Não há pacientes cadastrados na base :/")
        return {"message": "Não há pacientes cadastrados na base :/"}, 404
    else:
        logger.debug(f"{len(pacientes)} pacientes encontrados")
        return {"pacientes": apresenta_pacientes(pacientes)}, 200

# Rota de adição de paciente
@app.post('/paciente', tags=[paciente_tag],
          responses={"200": PacienteViewSchema, "400": ErrorSchema, "409": ErrorSchema})
def add_paciente(form: PacienteSchema):
    """Adiciona um novo paciente à base de dados."""
    try:
        # Preparando os dados para o modelo
        X_input = PreProcessador.preparar_form(form)
        # Carregando o modelo
        model_path = './MachineLearning/pipelines/rf_cancers_pipeline.pkl'
        modelo = Pipeline.carrega_pipeline(model_path)
        # Realizando a predição
        outcome = int(Model.preditor(modelo, X_input)[0])

        paciente = Paciente(
            name=form.name,
            radius_mean=form.radius_mean,
            texture_mean=form.texture_mean,
            perimeter_mean=form.perimeter_mean,
            area_mean=form.area_mean,
            outcome=outcome
        )

        logger.debug(f"Dados recebidos do formulário: {form}")
        logger.debug(f"Checando se paciente já existe com nome: '{form.name}'")

        session = Session()

        # Checando se paciente já existe na base
        if session.query(Paciente).filter(Paciente.name == form.name).first():
            error_msg = "Paciente já existente na base :/"
            logger.warning(f"Erro ao adicionar paciente '{paciente.name}': {error_msg}")
            return {"message": error_msg}, 409

        # Adicionando paciente
        session.add(paciente)
        session.commit()
        logger.debug(f"Adicionado paciente de nome: '{paciente.name}'")
        return apresenta_paciente(paciente), 200

    except Exception as e:
        error_msg = "Não foi possível salvar novo usuário :/"
        logger.warning(f"Erro ao adicionar paciente '{form.name}': {error_msg} - Detalhes: {str(e)}")
        return {"message": error_msg}, 400


# Rota de busca de paciente por nome
@app.get('/paciente', tags=[paciente_tag],
         responses={"200": PacienteViewSchema, "404": ErrorSchema})
def get_paciente(query: PacienteBuscaSchema):
    """Busca um paciente cadastrado na base a partir do nome."""
    paciente_nome = query.name
    logger.debug(f"Coletando dados sobre paciente '{paciente_nome}'")
    session = Session()
    paciente = session.query(Paciente).filter(Paciente.name == paciente_nome).first()

    if not paciente:
        error_msg = f"Paciente {paciente_nome} não encontrado na base :/"
        logger.warning(f"Erro ao buscar paciente '{paciente_nome}': {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Paciente encontrado: '{paciente.name}'")
        return apresenta_paciente(paciente), 200

# Rota de remoção de paciente por nome
@app.delete('/paciente', tags=[paciente_tag],
            responses={"200": PacienteViewSchema, "404": ErrorSchema})
def delete_paciente(query: PacienteBuscaSchema):
    """Remove um paciente cadastrado na base a partir do nome."""
    paciente_nome = unquote(query.name)
    logger.debug(f"Deletando paciente '{paciente_nome}'")

    session = Session()
    paciente = session.query(Paciente).filter(Paciente.name == paciente_nome).first()

    if not paciente:
        error_msg = "Paciente não encontrado na base :/"
        logger.warning(f"Erro ao deletar paciente '{paciente_nome}': {error_msg}")
        return {"message": error_msg}, 404
    else:
        session.delete(paciente)
        session.commit()
        logger.debug(f"Paciente '{paciente_nome}' deletado com sucesso")
        return {"message": f"Paciente {paciente_nome} removido com sucesso!"}, 200

if __name__ == '__main__':
    app.run(debug=True)