# Multibase-calculator

Módulo para operações com números em diferentes bases.

![Python](https://img.shields.io/static/v1?label=Python&message=language&color=darkgreen&style=for-the-badge&logo=python)


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
- `CONVENTIONS`: uma lista de caracteres válidos para representar números em diferentes bases (0-9 e A-Z);
- `validate_char()`: função para validar se um caractere é válido para a base numérica;
- `base`, `valueLabel`, `Base`, `ValueLabel`, `Char`: tipos customizados para base e valor do número;
- `NumericBase`: classe principal para representar um número em uma base específica;
- `_Helper`: subclasse de `NumericBase` para armazenamento de métodos úteis e repetitivos.

Funcionalidades
===============
- Representação de números em diferentes bases.
- Conversão entre bases numéricas.
- Operações de adição, subtração, multiplicação e <mark>divisão</mark>* entre números em bases diferentes.
- Validação de caracteres para garantir a integridade da base numérica.
- Formatação de saída em string para exibição.

Finalidade
==========
Este módulo foi criado para facilitar a manipulação de números em diferentes 
bases numéricas, fornecendo uma estrutura de dados e funções para realizar 
operações e conversões de forma eficiente e segura.

Usabilidade:
===========
```Python
  >>> from multibasecalculator import NumericBase
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
```

Convenções
==========

| Label           | Value in Base 10 |
|-----------------|------------------|
| 0               | 0                |
| 1               | 1                |
| 2               | 2                |
| 3               | 3                |
| 4               | 4                |
| 5               | 5                |
| 6               | 6                |
| 7               | 7                |
| 8               | 8                |
| 9               | 9                |
| A               | 10               |
| B               | 11               |
| C               | 12               |
| D               | 13               |
| E               | 14               |
| F               | 15               |
| G               | 16               |
| H               | 17               |
| I               | 18               |
| J               | 19               |
| K               | 20               |
| L               | 21               |
| M               | 22               |
| N               | 23               |
| O               | 24               |
| P               | 25               |
| Q               | 26               |
| R               | 27               |
| S               | 28               |
| T               | 29               |
| U               | 30               |
| V               | 31               |
| W               | 32               |
| X               | 33               |
| Y               | 34               |
| Z               | 35               |

Melhorias
=========
A Operação de divisão por meio da sobrecarga do operado `/` que ocorre do método
`NumericBase.__truediv__` não apresenta desempenho suficiente para ser utilizada.
Por isso, recomenda-se fortemente substituir, quando possível, a divisão por uma 
operação de multiplicação com o operador `*`.

> [!WARNING]
> A Operação de divisão por meio da sobrecarga do operado `/` que ocorre do método
`NumericBase.__truediv__` não apresenta desempenho suficiente para ser utilizada..

TODO
====
* [x] Crição da Subclasse _Helper;
* [x] Implementação de tratamento de erros para operações com bases distrintas;
* [ ] Correção do funcionamento do método `NumericBase.__truediv__`;
* [ ] Implementação de interface Web simples.

Sobre
=====

**Versão:** 1.0.0

**Autor:** Pedro Costa

**Data:** 28/11/2024
