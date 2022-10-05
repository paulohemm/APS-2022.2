from datetime import date as Date
from abc import ABC, abstractmethod


class AbstractPessoa(ABC):

	@abstractmethod
	def __init__(self, nome: str, cpf: str, telefone: str, data_nascimento: Date):
		if isinstance(nome, str):
			self.__nome = nome
		if isinstance(cpf, str):
			self.__cpf = cpf
		if isinstance(telefone, str):
			self.__telefone = telefone
		if isinstance(data_nascimento, Date):
			self.__data_nascimento = data_nascimento

	@property
	def nome(self) -> str:
		return self.__nome

	@nome.setter
	def nome(self, nome):
		if isinstance(nome, str):
			self.__nome = nome

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