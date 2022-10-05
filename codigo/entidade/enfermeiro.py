from datetime import date
from entidade import AbstractPessoa


class Enfermeiro(AbstractPessoa):
	def __init__(self, nome: str, cpf: str, telefone: str, data_nascimento: date, matricula_coren: str):
		super().__init__(nome, cpf, telefone, data_nascimento)
		self.__matricula_coren = matricula_coren

	@property
	def matricula_coren(self) -> str:
		return self.__matricula_coren

	@matricula_coren.setter
	def matricula_coren(self, matricula_coren):
		if isinstance(matricula_coren, str):
			self.__matricula_coren = matricula_coren
