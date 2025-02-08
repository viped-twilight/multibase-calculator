"""
Módulo para operações com números em diferentes bases.

Descrição
===========
Este módulo fornece a classe `NumericBase` para representar números em 
diferentes bases numéricas (base 2 a base 36). Permite realizar operações de 
soma e multiplicação entre números em diferentes bases, convertendo-os 
automaticamente para uma base comum antes da operação. A classe `NumericBase` 
inclui métodos para conversão entre bases, validação de caracteres e 
representação em string.

Estrutura
=========
O módulo define:
- `CONVENTIONS`: Uma lista de caracteres válidos para representar números em diferentes bases (0-9 e A-Z);
- `validate_char()`: Função para validar se um caractere é válido para a base numérica;
- `base`, `valueLabel`, `Base`, `ValueLabel`, `Char`: Tipos customizados para base e valor do número;
- `NumericBase`: Classe principal para representar um número em uma base específica.

Funcionalidades
===============
- Representação de números em diferentes bases.
- Conversão entre bases numéricas.
- Operações de adição e multiplicação entre números em bases diferentes.
- Validação de caracteres para garantir a integridade da base numérica.
- Formatação de saída em string para exibição.

Finalidade
==========
Este módulo foi criado para facilitar a manipulação de números em diferentes 
bases numéricas, fornecendo uma estrutura de dados e funções para realizar 
operações e conversões de forma eficiente e segura.


Sobre
=====
Versão: 1.0.0
Autor: Pedro Costa
Data: 28/11/2024
"""
from dataclasses import dataclass
from typing import NewType, Annotated, Literal, Callable, Any
import numpy as np

CONVENTIONS = np.array([*"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"], dtype=np.str_)

def validate_char(val:str) -> str | ValueError:
        """Valida se o caractere está na lista de caracteres válidos e se é um
        valor único

        Args:
            `val` (str): Caractere a ser validado

        Raises:
            `ValueError`: Se o caractere não estiver na lista de caracteres válidos

        Returns:
            str: Caractere validado
        """
        conventions = CONVENTIONS
        if isinstance(val, str) and len(val) == 1:
            val = val.upper()
            if val in conventions:
                return val
            else:
                raise ValueError(f'O valor "{val}" não é válido. Não está na lista de caracteres válidos: {conventions}.')
        else:
            raise ValueError(f'O valor "{val}" não é válido. Deve ser um único caractere.')

base = NewType('base', int)
valueLabel = NewType('valueLabel', str)
Base = Annotated[int, int]
ValueLabel = Annotated[str, str]
Char = Annotated[str, validate_char]


@dataclass
class NumericBase(object):
    '''
    Representa um número em uma base numérica específica.

    Attributes:
    -----------
        atual_base: int
            A base numérica atual do número.
        value: str
            O valor do número como uma string.
        CONVENTIONS: list[Char, Char, ...]
            Uma lista de caracteres válidos para representar números em diferentes bases.
        erros: Literal["coerce", "strict"] = "strict"
            A estratégia de tratamento de erros durante a conversão.
            
            "strict": realiza operações apenas quando os dois números fornecidos estão
                      na mesma base numérica.
            "coerce": realiza operações mesmo que os números estejam em bases diferentes.
                      Para isso, é realizado a conversão dos números para a mesma base.
                      Por padrão, a conversão é feita de modo que o número de maior base
                      seja a base alvo da conversão, ou seja, converte-se o número de 
                      menor base para a maior base da operação.
            
            | Por padrão, é "strict".

    Methods:
    --------
        type_of_value:
            Retorna o tipo do valor de entrada, verificando se é float ou int.
        convert_base:
            Converte o número para uma base numérica diferente.
        convert_to_digit:
            Converte um caractere em um dígito numérico.
        convert_to_char:
            Converte um dígito numérico em um caractere.
        __add__:
            Soma dois números (int | float) em uma base numérica específica, 
            utilizado a sobrecarga do operador `+`.
        __mul__:
            Multiplica dois números (int | float) em uma base numérica específica,
            utilizando a sobrecarga do operador `*`.
        __sub__:
            Subtração de dois números (int | float) em uma base numérica específica,
            utilizado a sobrecarga do operador `-`.
        __truediv__:
            Divisão de dois números (int | float) em uma base numérica específica, 
            utilizado a sobrecarga do operador `/`.

    Usage:
    ------
        >>> num = NumericBase(9, "12")
        >>> num.atual_base
        9
        >>> num.value
        '12'
        >>> num1, num2 = NumericBase(9, "12"), NumericBase(9, "5")
        >>> num1 - num2
        NumericBase(atual_base=9, value='6', erros='strict')
        
        >>> num1, num2 = NumericBase(9, "12"), NumericBase(9, "5", "coerce")
        >>> num1 - num2
        NumericBase(atual_base=9, value='6', erros='strict')

        >>> num1, num2 = NumericBase(10, "40.2", "coerce"), NumericBase(8, "0.2", "coerce")
        >>> num1 - num2
        NumericBase(atual_base=10, value='49.95', erros='coerce')

        >>> num1, num2 = NumericBase(9, "12"), NumericBase(9, "5")
        >>> num1 + num2
        NumericBase(atual_base=9, value='17', erros='strict')
    '''
    atual_base: int | base | Base
    value: str | valueLabel | ValueLabel
    CONVENTIONS = CONVENTIONS
    erros: Literal["coerce", "strict"] = "strict"
    
    class _Helper:
        """
        Submódulo interno contendo funções auxiliares utilizadas para operações
        com listas de dígitos representando números em bases arbitrárias.
        """
        @staticmethod
        def erros_tratament(func: Callable) -> Callable:
            def wrapper(self: "NumericBase", other: "NumericBase", *args, **kwargs) -> Any:
                if (self.erros == "strict" or other.erros == "strict") and self.atual_base != other.atual_base:
                    raise ValueError("As bases devem ser iguais para a operação.")
                elif self.erros == "coerce" and other.erros == "coerce" and self.atual_base != other.atual_base:
                    maior_base = max(self.atual_base, other.atual_base)
                    self = self.convert_base(final_base=maior_base)
                    other = other.convert_base(final_base=maior_base)
                    self.erros = "coerce"
                    other.erros = "coerce"
                return func(self, other, *args, **kwargs)
            return wrapper
        
        @staticmethod
        def get_erros(this: "NumericBase", other: "NumericBase") -> Literal["coerce", "strict"]:
            if this.erros == "strict" or other.erros == "strict":
                return "strict"
            elif this.erros == "coerce" and other.erros == "coerce":
                return "coerce"
            else:
                return "strict"
        
        @staticmethod
        def convert_integer(num_str: str, source: int, target: int) -> list:
            """Converte a parte inteira do número (string) da base 'source' para
            uma lista de dígitos na base 'target' utilizando o método de Horner.
            """
            digits = [int(CONVENTIONS.tolist().index(ch.upper())) for ch in num_str]
            result = [0]
            for d in digits:
                result = NumericBase._Helper.multiply_in_base(result, source, target)
                result = NumericBase._Helper.add_in_base(result, d, target)
            return result

        @staticmethod
        def convert_fraction(frac_str: str, source: int, target: int, precision: int = 10) -> list:
            """Converte a parte fracionária do número (string) da base 'source' para
            uma lista de dígitos na base 'target'. Utiliza divisão longa para obter
            uma expansão com a precisão desejada.
            """
            if frac_str == "":
                return []
            numer = NumericBase._Helper.convert_integer(frac_str, source, target)
            # Calcula o denominador: source^(número de dígitos da fração)
            denom = [1]
            for _ in range(len(frac_str)):
                denom = NumericBase._Helper.multiply_in_base(denom, source, target)
            quotient, _ = NumericBase._Helper.long_division(numer, denom, target, precision)
            while len(quotient) < precision:
                quotient.insert(0, 0)
            return quotient

        @staticmethod
        def convert_number(num_str: str, source: int, target: int, precision: int = 10) -> tuple:
            """Separa o número (string) em parte inteira e fracionária e as converte
            para listas de dígitos na base 'target'. Se a base de origem já for a mesma que
            a target, faz apenas a conversão dos caracteres.
            """
            if '.' in num_str:
                int_str, frac_str = num_str.split('.')
            else:
                int_str, frac_str = num_str, ""
            if source == target:
                int_part = [int(CONVENTIONS.tolist().index(ch.upper())) for ch in int_str] if int_str != "" else [0]
                frac_part = [int(CONVENTIONS.tolist().index(ch.upper())) for ch in frac_str] if frac_str != "" else []
            else:
                int_part = NumericBase._Helper.convert_integer(int_str, source, target)
                frac_part = NumericBase._Helper.convert_fraction(frac_str, source, target, precision)
            return int_part, frac_part

        @staticmethod
        def add_in_base(number: list, addend: int, base_val: int) -> list:
            """Soma um inteiro pequeno (addend) à lista de dígitos 'number' na base 'base_val'."""
            result = number[:]  # Cópia da lista
            i = len(result) - 1
            carry = addend
            while i >= 0 and carry:
                s = result[i] + carry
                result[i] = s % base_val
                carry = s // base_val
                i -= 1
            while carry:
                result.insert(0, carry % base_val)
                carry //= base_val
            return result

        @staticmethod
        def multiply_in_base(number: list, multiplier: int, base_val: int) -> list:
            """Multiplica a lista de dígitos 'number' por 'multiplier' na base 'base_val'."""
            result = [0] * len(number)
            carry = 0
            for i in range(len(number) - 1, -1, -1):
                prod = number[i] * multiplier + carry
                result[i] = prod % base_val
                carry = prod // base_val
            while carry:
                result.insert(0, carry % base_val)
                carry //= base_val
            return result

        @staticmethod
        def compare_lists(a: list, b: list) -> int:
            """Compara duas listas de dígitos (MSD primeiro).
            Retorna 1 se a > b, 0 se iguais e -1 se a < b.
            """
            if len(a) != len(b):
                return 1 if len(a) > len(b) else -1
            for x, y in zip(a, b):
                if x != y:
                    return 1 if x > y else -1
            return 0

        @staticmethod
        def subtract_lists(a: list, b: list, base_val: int) -> tuple[list, int]:
            """
            Subtrai duas listas de dígitos (a - b) na base 'base_val', assumindo que ambas
            tenham o mesmo tamanho (com zeros à esquerda se necessário). Retorna uma tupla (resultado, borrow_final).
            """
            result = [0] * len(a)
            borrow = 0
            for i in range(len(a) - 1, -1, -1):
                diff = a[i] - b[i] - borrow
                if diff < 0:
                    diff += base_val
                    borrow = 1
                else:
                    borrow = 0
                result[i] = diff
            return result, borrow

        @staticmethod
        def pad_lists(a: list, b: list, left: bool = False) -> tuple[list, list]:
            """Adiciona zeros à esquerda (ou à direita) para que as listas 'a' e 'b' tenham o mesmo tamanho."""
            if len(a) < len(b):
                pad = [0] * (len(b) - len(a))
                a = (pad + a) if left else (a + pad)
            elif len(b) < len(a):
                pad = [0] * (len(a) - len(b))
                b = (pad + b) if left else (b + pad)
            return a, b

        @staticmethod
        def long_division(dividend: list, divisor: list, base_val: int, precision: int) -> tuple[list, list]:
            """
            Realiza divisão longa entre 'dividend' e 'divisor' na base 'base_val'. Retorna uma tupla (quociente, resto)
            em que o quociente possui 'precision' dígitos adicionais para a parte fracionária.
            """
            quotient = []
            remainder = dividend[:]  # Cópia do dividendo

            # Cálculo da parte inteira (assume-se que dividend e divisor já estão "compactados")
            while NumericBase._Helper.compare_lists(remainder, divisor) >= 0:
                count = 0
                while NumericBase._Helper.compare_lists(remainder, divisor) >= 0:
                    r_padded, d_padded = NumericBase._Helper.pad_lists(remainder, divisor, left=True)
                    r_padded, d_padded = NumericBase._Helper.subtract_lists(r_padded, d_padded, base_val)
                    remainder = r_padded
                    count += 1
                quotient.append(count)
                # Para este exemplo, assume-se que a parte inteira é obtida em uma única iteração
                break
            if not quotient:
                quotient = [0]

            # Cálculo da parte fracionária: realiza 'precision' iterações
            for _ in range(precision):
                remainder = NumericBase._Helper.multiply_in_base(remainder, base_val, base_val)
                count = 0
                while NumericBase._Helper.compare_lists(remainder, divisor) >= 0:
                    r_padded, d_padded = NumericBase._Helper.pad_lists(remainder, divisor, left=True)
                    r_padded, d_padded = NumericBase._Helper.subtract_lists(r_padded, d_padded, base_val)
                    remainder = r_padded
                    count += 1
                quotient.append(count)
            return quotient, remainder

    def type_of_value(self:"NumericBase") -> type:
        '''
        About
        ======
        Procedimento que retorna o tipo do valor de entrada, verificando se é
        `float` ou `int`.

        Params: `None`
        -------

        Returns:
        --------
        `float` | `int`
            Tipo do valor de entrada.

        Exemples:
        ---------
        >>> exemple = NumericBase("12.4", 15)
        >>> exemple.type_of_value()
        float

        >>> exemple2 = NumericBase("21", 28)
        >>> exemple2.type_of_value()
        int
        '''
        return float if "." in self.value else int

    def convert_base(self:"NumericBase",
                     initial_base: Base | None = None,
                     final_base: Base=base(10)
        ) -> "NumericBase":
        '''
        Converte o número para uma base numérica diferente. Por padrão,
        a base 10 é considerada a base final, caso não seja fornecida outra.

        Params:
            initial_base: a base numérica inicial do número.
            final_base: a base numérica para a qual o número será convertido.

        Returns:
            Uma nova instância de NumericBase representando o número na nova base.

        Raises:
            ValueError: se a base inicial ou final não estiver no intervalo válido.

        Exemples:
        >>> num = NumericBase(9, "12")
        >>> num.convert_base(initial_base=num.atual_base, final_base=2)
        NumericBase(atual_base=2, value='1100')
        >>>
        >>>
        '''
        if initial_base is None:
            initial_base = self.atual_base

        self.atual_base = final_base
        # Step 1: Separate integer and fractional parts
        if self.type_of_value() is float:
            integer_part, fractional_part = self.value.split('.')
        else:
            integer_part, fractional_part = self.value, ""

        # Step 2: Convert integer part using Horner's method
        def convert_integer_part(
                value:ValueLabel,
                base_from:Base,
                base_to:Base
            ) -> ValueLabel:
            '''
            Converte a parte inteira de um número para uma base diferente.

            Params:
                `value`: ValueLabel | str
                    A parte inteira do número como uma string.
                `base_from`: Base | int
                    A base numérica inicial da parte inteira
                `base_to`: Base | int
                    A base numérica para a qual a parte inteira será convertida.

            Returns:
                `results`: str
                    A parte inteira convertida como uma string.

            Exemples:
            >>> convert_fractional_part("125", 6, 2)
            110101
            '''
            num = 0
            for digit in value:
                num = num * base_from + self.CONVENTIONS.tolist().index(digit)

            # Now convert to target base
            result = ""
            while num > 0:
                remainder = num % base_to
                result = self.CONVENTIONS[remainder] + result
                num //= base_to
            return result or "0"

        # Step 3: Convert fractional part
        def convert_fractional_part(
                value:ValueLabel,
                base_from:Base,
                base_to:Base
            ) -> ValueLabel:
            '''
            Converte a parte fracionária de um número para uma base diferente.

            Params:
                `value`: ValueLabel | str
                    A parte fracionária do número como uma string.
                `base_from`: Base | int
                    A base numérica inicial da parte fracionária.
                `base_to`: Base | int
                    A base numérica para a qual a parte fracionária será convertida.

            Returns:
                `results`: str
                    A parte fracionária convertida como uma string.

            Exemples:
            >>> convert_fractional_part("125", 6, 2)
            110101
            '''
            fraction = 0.0
            power = 1 / base_from
            for digit in value:
                fraction += self.CONVENTIONS.tolist().index(digit) * power
                power /= base_from

            # Convert to target base
            result = ""
            count = 0
            while fraction > 0 and count < 10:  # Limit the length to avoid infinite fractions: limite == 10
                fraction *= base_to
                integer_part = int(fraction)
                result += self.CONVENTIONS[integer_part]
                fraction -= integer_part
                count += 1
            return result

        # Combine integer and fractional parts
        integer_result = convert_integer_part(integer_part, initial_base, final_base)
        fractional_result = convert_fractional_part(fractional_part, initial_base, final_base) if fractional_part else ""

        str_result = integer_result + ('.' + fractional_result if fractional_result else "")
        return NumericBase(final_base, str_result)

    def convert_to_digit(self:"NumericBase", char:Char) -> int:
        '''
        Converte um caractere em um dígito numérico.

        Params:
            `char`: Char | str
                O caractere a ser convertido.

        Returns:
            int
                O dígito numérico correspondente ao caractere.

        Raises:
            `ValueError`: se o caractere não estiver na lista de caracteres válidos.

        Exemples:
        >>> convert_to_digit("A")
        10
        >>> convert_to_digit("C")
        12
        >>> convert_to_digit("1")
        1
        >>> convert_to_digit("2")
        2
        '''
        return self.CONVENTIONS.tolist().index(char)

    def convert_to_char(self:"NumericBase", digit:int) -> Char:
        '''
        Converte um dígito numérico em um caractere.

        Params:
            `digit`: int
                O dígito numérico a ser convertido.

        Returns:
            Char | str
                O caractere correspondente ao dígito numérico.

        Raises:
            `ValueError`: se o dígito numérico estiver fora do intervalo válido.

        Exemples:
        >>> convert_to_char(10)
        "A"
        >>> convert_to_char(13)
        "D"
        >>> convert_to_char(5)
        "5"
        >>> convert_to_char(0)
        "0"
        '''
        return self.CONVENTIONS[digit]
    
    @_Helper.erros_tratament
    def __add__(self:"NumericBase", other:"NumericBase") -> "NumericBase":
        '''
        Soma dois números em uma base numérica (int | float) específica, 
        utilizado a sobrecarga do operador `+`.

        Params:
            `other`: NumericBase
                O outro número a ser somado.

        Returns:
            Uma nova instância de NumericBase representando a soma dos dois números.

        Raises:
            `ValueError`: se as bases dos dois números forem diferentes.

        Exemples:
        >>> num1, num2 = NumericBase(9, "12"), NumericBase(9, "5")
        >>> num1 + num2
        NumericBase(atual_base=9, value='17', erros='strict')
        '''

        base = self.atual_base
        error = self._Helper.get_erros(this=self, other=other)

        # Separar partes inteiras e fracionárias
        int_part1, frac_part1 = self.value.split('.') if '.' in self.value else (self.value, "")
        int_part2, frac_part2 = other.value.split('.') if '.' in other.value else (other.value, "")

        # Adicionar zeros para igualar o comprimento das partes fracionárias
        max_frac_len = max(len(frac_part1), len(frac_part2))
        frac_part1 = frac_part1.ljust(max_frac_len, '0')
        frac_part2 = frac_part2.ljust(max_frac_len, '0')

        # Adicionar a parte fracionária
        result_frac = []
        carry = 0
        for d1, d2 in zip(frac_part1[::-1], frac_part2[::-1]):
            total = self.convert_to_digit(d1) + self.convert_to_digit(d2) + carry
            carry = total // base
            result_frac.append(self.convert_to_char(total % base))
        result_frac = ''.join(result_frac[::-1])

        # Adicionar a parte inteira
        max_int_len = max(len(int_part1), len(int_part2))
        int_part1 = int_part1.zfill(max_int_len)[::-1]
        int_part2 = int_part2.zfill(max_int_len)[::-1]

        result_int = []
        for d1, d2 in zip(int_part1, int_part2):
            total = self.convert_to_digit(d1) + self.convert_to_digit(d2) + carry
            carry = total // base
            result_int.append(self.convert_to_char(total % base))

        if carry > 0:
            result_int.append(self.convert_to_char(carry))
        result_int = ''.join(result_int[::-1])

        # Combinar parte inteira e fracionária
        result_value = result_int + ('.' + result_frac if result_frac else "")

        return NumericBase(base, result_value, error)

    @_Helper.erros_tratament
    def __mul__(self:"NumericBase", other:"NumericBase") -> "NumericBase":
        '''
        Multiplica dois números (int | float) em uma base numérica específica,
        utilizando a sobrecarga do operador `*`.

        Args:
            other: O outro número a ser multiplicado.

        Returns:
            Uma nova instância de NumericBase representando o produto dos dois números.

        Raises:
            ValueError: Se as bases dos dois números forem diferentes.

        Exemples:
        >>> num1, num2 = NumericBase(9, "12"), NumericBase(9, "5")
        >>> num1 * num2
        NumericBase(atual_base=9, value='61', erros='strict')
        '''

        base = self.atual_base
        error = self._Helper.get_erros(this=self, other=other)

        # Separar partes inteiras e fracionárias
        int_part1, frac_part1 = self.value.split('.') if '.' in self.value else (self.value, "")
        int_part2, frac_part2 = other.value.split('.') if '.' in other.value else (other.value, "")

        # Contagem do número total de dígitos fracionários para posicionar o ponto decimal
        total_frac_len = len(frac_part1) + len(frac_part2)

        # Conversão de cada parte para inteiro, acumulando em base
        def to_integer(value:ValueLabel, base:Base) -> int:
            result = 0
            for char in value:
                result = result * base + self.convert_to_digit(char)
            return result

        # Converte as partes inteira e fracionária para um único número inteiro, ignorando temporariamente o ponto decimal
        num1 = to_integer(int_part1 + frac_part1, base) if frac_part1 else to_integer(int_part1, base)
        num2 = to_integer(int_part2 + frac_part2, base) if frac_part2 else to_integer(int_part2, base)

        # Multiplica os valores inteiros resultantes
        int_result = num1 * num2

        # Conversão do resultado para a string na base, incluindo o ponto decimal na posição correta
        result = []
        while int_result > 0:
            result.append(self.convert_to_char(int_result % base))
            int_result //= base
        result = ''.join(result[::-1]).zfill(total_frac_len + 1) if total_frac_len else ''.join(result[::-1])

        # Coloca o ponto decimal na posição correta
        if total_frac_len:
            result_int = result[:-total_frac_len] if total_frac_len < len(result) else "0"
            result_frac = result[-total_frac_len:].rstrip('0')
            result_value = result_int + ('.' + result_frac if result_frac else "")
        else:
            result_value = result

        return NumericBase(base, result_value, error)
    
    @_Helper.erros_tratament
    def __sub__(self:"NumericBase", other:"NumericBase") -> "NumericBase":
        '''
        Subtração de dois números (int | float) em uma base numérica específica, 
        utilizado a sobrecarga do operador `-`.

        Params:
            `other`: NumericBase
                O outro número a ser somado.

        Returns:
            Uma nova instância de NumericBase representando a subtração dos dois números.

        Raises:
            `ValueError`: se as bases dos dois números forem diferentes.
            `NegativeValueError`: se o resultado da opereração resultar em um valor negativo.

        Exemples:
        >>> num1, num2 = NumericBase(9, "12"), NumericBase(9, "5")
        >>> num1 - num2
        NumericBase(atual_base=9, value='6', erros='strict')
        
        >>> num1, num2 = NumericBase(9, "12"), NumericBase(9, "5", "coerce")
        >>> num1 - num2
        NumericBase(atual_base=9, value='6', erros='strict')

        >>> num1, num2 = NumericBase(10, "40.2", "coerce"), NumericBase(8, "0.2", "coerce")
        >>> num1 - num2
        NumericBase(atual_base=10, value='49.95', erros='coerce')
        '''
        base = self.atual_base
        error = self._Helper.get_erros(this=self, other=other)

        # Determina a base alvo: a maior dentre as duas
        target = max(self.atual_base, other.atual_base)

        # Conversão dos operandos para a base 'target'
        int1, frac1 = NumericBase._Helper.convert_number(self.value, self.atual_base, target, precision=10)
        int2, frac2 = NumericBase._Helper.convert_number(other.value, other.atual_base, target, precision=10)

        # Normaliza as partes fracionárias (mesmo número de dígitos)
        frac1, frac2 = NumericBase._Helper.pad_lists(frac1, frac2, left=False)
        # Realiza a subtração da parte fracionária
        frac_result, borrow_frac = NumericBase._Helper.subtract_lists(frac1, frac2, target)

        # Normaliza as partes inteiras (pad à esquerda)
        int1, int2 = NumericBase._Helper.pad_lists(int1, int2, left=True)
        # Ajusta o último dígito da parte inteira de acordo com o borrow oriundo da fração
        int1[-1] = (int1[-1] - borrow_frac) % target
        # Realiza a subtração da parte inteira
        int_result, borrow_int = NumericBase._Helper.subtract_lists(int1, int2, target)
        if borrow_int != 0:
            class NegativeValueError(ValueError):
                pass
            raise NegativeValueError("Subtração resultou em número negativo, não suportado.")

        # Remove zeros supérfluos: zeros à esquerda na parte inteira e à direita na parte fracionária
        while len(int_result) > 1 and int_result[0] == 0:
            int_result.pop(0)
        while frac_result and frac_result[-1] == 0:
            frac_result.pop()

        # Converte as listas de dígitos de volta para string utilizando CONVENTIONS
        int_str_res = ''.join(self.CONVENTIONS[d] for d in int_result)
        frac_str_res = ''.join(self.CONVENTIONS[d] for d in frac_result)
        result_value = int_str_res + ('.' + frac_str_res if frac_str_res else '')
        
        return NumericBase(target, result_value, error)
    
    @_Helper.erros_tratament
    def __truediv__(self:"NumericBase", other:"NumericBase") -> "NumericBase":
        '''
        Divide dois números (int | float) em uma base numérica específica, utilizado a
        sobrecarga do operador `/`.

        Params:
            `other`: NumericBase
                O outro número que será o divisor.

        Returns:
            Uma nova instância de NumericBase representando a divisão dos dois números.

        Raises:
            `ValueError`: se as bases dos dois números forem diferentes.
            `ZeroDivisionError`: se o divisor for zero.

        Exemples:
        >>> num1, num2 = NumericBase(10, "40"), NumericBase(10, "40")
        >>> num1 / num2
        NumericBase(atual_base=40, value='1', erros='strict')
        '''
        error = self._Helper.get_erros(this=self, other=other)
        target = max(self.atual_base, other.atual_base)
        PRECISION = 10  # Número de dígitos fracionários desejados no resultado

        # Conversão dos operandos para a base 'target'
        int1, frac1 = NumericBase._Helper.convert_number(self.value, self.atual_base, target, precision=PRECISION)
        int2, frac2 = NumericBase._Helper.convert_number(other.value, other.atual_base, target, precision=PRECISION)

        # Para a divisão, junta-se a parte inteira e a fracionária (normalizando as frações)
        total_frac_digits = max(len(frac1), len(frac2))
        frac1 += [0] * (total_frac_digits - len(frac1))
        frac2 += [0] * (total_frac_digits - len(frac2))
        num1_full = int1 + frac1
        num2_full = int2 + frac2

        if NumericBase._Helper.compare_lists(num2_full, [0]) == 0:
            raise ZeroDivisionError("Divisão por zero não é permitida.")

        # Realiza a divisão longa
        quotient, _ = NumericBase._Helper.long_division(num1_full, num2_full, target, PRECISION)
        # Separa a parte inteira e fracionária do quociente
        int_part = quotient[:-PRECISION] if PRECISION < len(quotient) else [0]
        frac_part = quotient[-PRECISION:] if PRECISION <= len(quotient) else quotient
        while len(int_part) > 1 and int_part[0] == 0:
            int_part.pop(0)
        while frac_part and frac_part[-1] == 0:
            frac_part.pop()
        int_str_res = ''.join(self.CONVENTIONS[d] for d in int_part)
        frac_str_res = ''.join(self.CONVENTIONS[d] for d in frac_part)
        result_value = int_str_res + ('.' + frac_str_res if frac_str_res else '')
        
        return NumericBase(target, result_value, error)
    
