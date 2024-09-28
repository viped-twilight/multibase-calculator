import streamlit as st
import numpy as np

# Conjunto de caracteres para conversão entre bases
conventions = np.array([*"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"], dtype=np.str_)

# Função para converter números com base para decimal
def convert_to_decimal(number_with_base:str) -> str:
    try:
        number, base = number_with_base.split('_')
        return str(int(number, base=int(base)))
    except ValueError:
        st.error(f"""
        O valor {number_with_base} possui uma base inválida ou incompatível [{base}].
        Certifique-se que a base está entre 2 e 36 e que os algarismos do número
        são válidos para a base selecionada.
        """)
        return None

# Função para converter de decimal para qualquer base
def convert_from_decimal(number_in_decimal:int, new_base:int) -> str:
    if number_in_decimal == 0:
        return "0"
    else:
        return (convert_from_decimal(number_in_decimal // new_base, new_base)) + str(conventions[number_in_decimal % new_base])

# Função principal da calculadora
def calculate(equation, new_base):
    try:
        # Manipulação dos dados de entrada
        equation_per_item = equation.split(" ")
        operandos = equation_per_item[0::2]

        # Converter cada operando para decimal
        operandos_convertidos = [convert_to_decimal(num) for num in operandos]

        # Checar se alguma conversão falhou
        if any(op is None for op in operandos_convertidos):
            return None, None

        # Substituir os operandos convertidos na equação
        equation_per_item[0::2] = operandos_convertidos
        equation_in_decimal = " ".join(equation_per_item)

        # Avaliar a equação em decimal
        result_in_decimal = eval(equation_in_decimal)

        # Converter o resultado para a base escolhida
        result_in_choice_base = convert_from_decimal(result_in_decimal, new_base)

        return result_in_decimal, result_in_choice_base

    except Exception as e:
        st.error(f"Ocorreu um erro ao calcular a equação: {e}")
        return None, None

# Configuração da interface com Streamlit
st.set_page_config(page_title="Calculadora de Bases", layout="centered")

st.title("Calculadora de Bases Numéricas")
st.write("Insira uma equação, incluindo os operandos com suas respectivas bases (ex: `1010_2 + 15_10`) e escolha uma base para o resultado.")

# Caixa de entrada para a equação
equation = st.text_input("Digite a equação:")

# Seleção da base para o resultado
new_base = st.number_input("Digite a base do resultado (entre 2 e 36):", min_value=2, max_value=36, value=10)

# Botão para calcular
if st.button("Calcular"):
    if equation:
        result_in_decimal, result_in_choice_base = calculate(equation, new_base)
        
        if result_in_decimal is not None and result_in_choice_base is not None:
            st.success(f"{equation} = {st.latex(f'{result_in_decimal}_{10}')} = {st.latex(f'{result_in_choice_base}_{new_base}')}")
    else:
        st.error("Por favor, insira uma equação válida.")

# Estilizando a interface
st.markdown("""
    <style>
    .stButton button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        padding: 8px 16px;
    }
    .stTextInput input {
        font-size: 18px;
    }
    .stNumberInput input {
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)
