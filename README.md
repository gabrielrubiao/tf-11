# Relatório Técnico - Object Calisthenics (TF-11)

1. **Normalização:** Consiste em armazenar cada informação em um único lugar, permitindo que outros pontos apenas apontem para ela por referência. Na loja, resolveu o problema da duplicação dos dados da cliente Ana e dos produtos, garantindo que alterações reflitam centralmente.
2. **Obsessão por tipos primitivos:** O CPF virou classe para encapsular regras de validação e impedir valores inválidos no domínio. O programa ganhou robustez e previsibilidade. O Dinheiro armazena centavos como inteiros para evitar imprecisões matemáticas comuns em pontos flutuantes (como `0.1 + 0.2`).
3. **Diga, não pergunte:** A lógica de pagamento foi transferida para dentro do objeto `Pedido` através de métodos de comportamento (`pagar()`), eliminando consultas externas de estado e mantendo o encapsulamento seguro.
4. **Fail first:** O hadouken da loja feia estava concentrado em condicionais aninhadas de validação e status. O uso de retorno antecipado e polimorfismo substituiu os blocos `else`/`elif`, reduzindo a complexidade ciclomática.
5. **Modularização:** 
   - `Cpf`: Valida o formato do documento.
   - `Email`: Valida a presença de '@' e não-nulidade.
   - `Cep`: Valida o formato postal.
   - `Dinheiro`: Gerencia valores monetários em centavos.
   - `Status`: Controla estados e descrições do pedido.
   - `TipoNormal`, `TipoVip`, `TipoFuncionario`: Aplicam regras polimórficas de desconto.
   - `Pessoa`: Agrupa dados de identificação pessoal.
   - `Endereco`: Agrupa dados de localização geográfica.
   - `Cliente`: Agrupa pessoa, endereço e tipo comercial.
   - `Produto`: Armazena nome e preço unitário.
   - `ItemDoPedido`: Agocia produto e quantidade.
   - `ItensDoPedido`: Coleção de primeira classe para a lista de itens.
   - `Pedido`: Gerencia o estado e o cálculo financeiro do pedido.
   - `Pedidos`: Coleção de primeira classe para o repositório global de pedidos.
6. **Dívida técnica:** A regra mais difícil foi eliminar totalmente os getters aplicando rigorosamente a Lei de Demeter nas impressões de relatórios encadeados, exigindo o redesenho cuidadoso da delegação de responsabilidades entre as entidades.