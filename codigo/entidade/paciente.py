from datetime import date as Date
from entidade.pessoa import AbstractPessoa


class Paciente(AbstractPessoa):
	def __init__(self, nome: str, cpf: str, telefone: str, data_nascimento: Date):
		super().__init__(nome, cpf, telefone, data_nascimento)
		self.__dose_vacina = 0

	@property
	def dose_vacina(self) -> int:
		return self.__dose_vacina

	@dose_vacina.setter
	def dose_vacina(self, dose_vacina):
		if isinstance(dose_vacina, int):
			self.__dose_vacina = dose_vacina

	@property
	def fabricante_vacina(self) -> int:
		return self.__fabricante_vacina

	@fabricante_vacina.setter
	def fabricante_vacina(self, fabricante_vacina):
		if isinstance(fabricante_vacina, str):
			self.__fabricante_vacina = fabricante_vacina

	@property
	def lote_vacina(self) -> str:
		return self.__lote_vacina

	@lote_vacina.setter
	def lote_vacina(self, lote_vacina):
		if isinstance(lote_vacina, str):
			self.__lote_vacina = lote_vacina
