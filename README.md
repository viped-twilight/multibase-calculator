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
------
```Python
  >>> from multibase calculator import NumericBase
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

Melhorias
=========
A Operação de divisão por meio da sobrecarga do operado `/` que ocorre do método
`NumericBase.__truediv__` não apresenta desemprenho suficiente para ser utilizada.
Por isso, recomenda-se fortemente substituir, quando possível, a divisão por uma 
operação de multiplicação com o operador `*`.

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
