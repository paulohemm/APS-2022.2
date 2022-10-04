from datetime import date as Date
from entidade.pessoa import AbstractPessoa


class Paciente(AbstractPessoa):
	def __init__(self, nome: str, cpf: str, data_nascimento: Date):
		super().__init__(nome, cpf)
		self.__data_nascimento = data_nascimento

	@property
	def data_nascimento(self) -> Date:
		return self.__data_nascimento

	@data_nascimento.setter
	def data_nascimento(self, data_nascimento):
		if isinstance(data_nascimento, Date):
			self.__data_nascimento = data_nascimento
