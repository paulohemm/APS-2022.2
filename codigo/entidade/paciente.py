from datetime import date as Date
from entidade.pessoa import AbstractPessoa


class Paciente(AbstractPessoa):
	def __init__(self, nome_completo: str, cpf: str, telefone: str, data_nascimento: Date):
		super().__init__(nome_completo, cpf, telefone, data_nascimento)
		self.__dose_vacina = 0

	@property
	def dose_vacina(self) -> int:
		return self.__dose_vacina

	@dose_vacina.setter
	def dose_vacina(self, dose_vacina):
		if isinstance(dose_vacina, int):
			self.__dose_vacina = dose_vacina