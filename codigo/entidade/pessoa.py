from datetime import date as Date
from abc import ABC, abstractmethod


class AbstractPessoa(ABC):

	@abstractmethod
	def __init__(self, nome_completo: str, cpf: str, telefone: str, data_nascimento: Date):
		if isinstance(nome_completo, str):
			self.__nome = nome_completo
		if isinstance(cpf, str):
			self.__cpf = cpf
		if isinstance(telefone, str):
			self.__telefone = telefone
		if isinstance(data_nascimento, Date):
			self.__data_nascimento = data_nascimento

	@property
	def nome_completo(self) -> str:
		return self.__nome_completo

	@nome_completo.setter
	def nome_completo(self, nome_completo):
		if isinstance(nome_completo, str):
			self.__nome_completo = nome_completo

	@property
	def cpf(self) -> str:
		return self.__cpf

	@cpf.setter
	def cpf(self, cpf):
		if isinstance(cpf, str):
			self.__cpf = cpf
	
	@property
	def telefone(self) -> str:
		return self.__telefone

	@telefone.setter
	def telefone(self, telefone):
		if isinstance(telefone, str):
			self.__telefone = telefone

	@property
	def data_nascimento(self) -> Date:
		return self.__data_nascimento

	@data_nascimento.setter
	def data_nascimento(self, data_nascimento):
		if isinstance(data_nascimento, Date):
			self.__data_nascimento = data_nascimento