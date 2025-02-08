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

**Versão:** 1.0.0

**Autor:** Pedro Costa

**Data:** 28/11/2024
"""
