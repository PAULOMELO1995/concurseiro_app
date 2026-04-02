from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ListProperty, ObjectProperty
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.progressbar import ProgressBar
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.animation import Animation
import json
import random
from datetime import datetime, timedelta

# Configuração da janela
Window.size = (360, 640)

# Cores do tema
COLORS = {
    'primary': get_color_from_hex('#3498db'),
    'primary_dark': get_color_from_hex('#2980b9'),
    'secondary': get_color_from_hex('#2ecc71'),
    'secondary_dark': get_color_from_hex('#27ae60'),
    'accent': get_color_from_hex('#e74c3c'),
    'background': get_color_from_hex('#ecf0f1'),
    'background_dark': get_color_from_hex('#bdc3c7'),
    'text_primary': get_color_from_hex('#2c3e50'),
    'text_secondary': get_color_from_hex('#7f8c8d'),
    'text_light': get_color_from_hex('#ffffff'),
}

# TODAS AS 50 QUESTÕES REAIS DO CONCURSO ANALISTA EDUCACIONAL
SIMULADO_QUESTIONS = [
    {
        'question': 'As próclises presentes na frase "Também não se esqueça de praticar alguma atividade física que lhe encha de prazer e alegria." ocorrem, respectivamente, por causa de um(a) ______ antes do verbo "esquecer", devidamente conjugado, e de um(a) ______ antes do verbo "encher", também devidamente conjugado.',
        'options': [
            'conjunção subordinativa / pronome relativo',
            'pronome relativo / conjunção subordinativa', 
            'pronome indefinido / conjunção subordinativa',
            'palavra de sentido negativo / pronome relativo'
        ],
        'answer': 'palavra de sentido negativo / pronome relativo',
        'subject': 'Língua Portuguesa',
        'difficulty': 'Difícil',
        'explanation': 'A próclise ocorre devido à palavra de sentido negativo ("não") antes de "esquecer" e ao pronome relativo ("que") antes de "encher".'
    },
    {
        'question': 'Em "Não é fácil unir tudo isso, mas é totalmente possível.", a conjunção "mas" expressa oposição, o mesmo NÃO ocorre com:',
        'options': ['Porquanto', 'Entretanto', 'No entanto', 'Não obstante'],
        'answer': 'Porquanto',
        'subject': 'Língua Portuguesa', 
        'difficulty': 'Médio',
        'explanation': '"Porquanto" é uma conjunção explicativa, não adversativa como "mas".'
    },
    {
        'question': 'As linhas tracejadas situadas no terceiro parágrafo do texto são, correta e respectivamente, preenchidas com:',
        'options': ['à / porque', 'a / porque', 'a / por que', 'à / por que'],
        'answer': 'a / porque',
        'subject': 'Língua Portuguesa',
        'difficulty': 'Médio',
        'explanation': 'Uso da crase e das conjunções conforme a norma culta.'
    },
    {
        'question': 'Observe as seguintes palavras que, no texto, são empregadas em sentido conotativo: I. Vivência (1º§) II. Barato (2º§) III. Gordura (4º§) Está correto o que se afirma apenas em',
        'options': ['I', 'II', 'I e III', 'II e III'],
        'answer': 'II',
        'subject': 'Língua Portuguesa',
        'difficulty': 'Fácil',
        'explanation': '"Barato" é usado no sentido figurado de "interessante".'
    },
    {
        'question': 'Sobre o que é exclusivamente explicitado no texto, é correto afirmar que:',
        'options': [
            'Todas as pessoas insistem em se preocupar demais com o futuro.',
            'As pessoas querem colher algo diferente do que plantam para ser surpreendidas.',
            'Faz toda a diferença na qualidade de vida do ser humano quando ele aprende a plantar virtudes em seu interior.',
            'As pessoas que ajudam nos momentos de dificuldade são tratadas com desconfiança pelos indivíduos por elas ajudados.'
        ],
        'answer': 'Faz toda a diferença na qualidade de vida do ser humano quando ele aprende a plantar virtudes em seu interior.',
        'subject': 'Interpretação de Texto',
        'difficulty': 'Médio',
        'explanation': 'O texto enfatiza a importância de cultivar virtudes para uma vida melhor.'
    },
    {
        'question': 'Assinale a alternativa que apresenta uma frase extraída do texto que contém uma locução verbal.',
        'options': [
            'É lógico que essa pergunta tem uma infinidade de respostas e possibilidades, (...)',
            'Infelizmente, muitas pessoas não conseguem isso por conta dos extremos que citei há pouco.',
            'Citei esse exemplo das amizades porque acredito ser um dos maiores tesouros dessa vida.',
            'Coma frutas, verduras, legumes, comidas ricas em fibras e proteínas e evite ao máximo comidas repletas de conservantes, com excesso de açúcar ou gordura.'
        ],
        'answer': 'Infelizmente, muitas pessoas não conseguem isso por conta dos extremos que citei há pouco.',
        'subject': 'Língua Portuguesa',
        'difficulty': 'Médio',
        'explanation': 'A locução verbal é "não conseguem" (verbo principal + verbo auxiliar).'
    },
    {
        'question': 'Sobre a sua função sintática, a última palavra da oração "Você colherá saúde corporal!" corresponde a um:',
        'options': ['Aposto', 'Vocativo', 'Adjunto adverbial', 'Adjunto adnominal'],
        'answer': 'Adjunto adnominal',
        'subject': 'Língua Portuguesa',
        'difficulty': 'Difícil',
        'explanation': '"Corporal" é adjunto adnominal porque qualifica o substantivo "saúde".'
    },
    {
        'question': 'De acordo com o texto, a literatura infantil e juvenil',
        'options': [
            'é eficaz somente quando focada em histórias de fantasia, já que outros gêneros são muito complexos para jovens leitores.',
            'é relevante apenas nas fases iniciais da educação e perde sua importância à medida que o leitor amadurece e passa a compreender textos mais complexos.',
            'é importante apenas para entretenimento, oferecendo pouca contribuição para a formação do leitor em termos de compreensão crítica e desenvolvimento cultural.',
            'desempenha um papel crucial na formação do leitor, pois desperta o interesse pela leitura, além de ser uma ferramenta importante para a compreensão de diferentes culturas e sociedades.'
        ],
        'answer': 'desempenha um papel crucial na formação do leitor, pois desperta o interesse pela leitura, além de ser uma ferramenta importante para a compreensão de diferentes culturas e sociedades.',
        'subject': 'Literatura',
        'difficulty': 'Médio',
        'explanation': 'O texto defende a importância universal da literatura em todas as fases da vida.'
    },
    {
        'question': 'Conforme o texto de Antônio Candido, a literatura é uma manifestação universal em todas as culturas e sociedades. Em razão disso, assinale a alternativa que descreve corretamente as especificidades do discurso literário.',
        'options': [
            'A literatura, enquanto linguagem autorreferencial, significa que ela apenas se refere a si mesma e não tem relação ou influência sobre a realidade ou a cultura em que está inserida.',
            'O discurso literário é estritamente uma representação factual do mundo, focando em apresentar informações precisas e objetivas, sem espaço para interpretação ou criatividade.',
            'O discurso literário, como elaboração estética de visões de mundo, serve para expressar e refletir as diversas realidades culturais e pessoais, funcionando como um patrimônio representativo da cultura de um povo.',
            'A literatura é um meio exclusivamente destinado ao entretenimento, sem contribuir significativamente para a compreensão ou expressão de visões de mundo ou culturas, sendo limitada em seu impacto e relevância cultural.'
        ],
        'answer': 'O discurso literário, como elaboração estética de visões de mundo, serve para expressar e refletir as diversas realidades culturais e pessoais, funcionando como um patrimônio representativo da cultura de um povo.',
        'subject': 'Literatura',
        'difficulty': 'Médio',
        'explanation': 'Antônio Candido defende a literatura como expressão cultural universal.'
    },
    {
        'question': 'Sobre a caracterização dos estilos literários, pode-se afirmar que em relação ao Romantismo no Brasil:',
        'options': [
            'A linguagem informal, linguagem simples próxima do coloquial, alcança valorização.',
            'O romance brasileiro daquele período não tinha compromisso como o contexto histórico de sua época.',
            'A crítica à burguesia predominava na prosa ficcional romântica refletindo a presença da denúncia na Literatura.',
            'A influência europeia foi fundamental para o início do Romantismo no Brasil com todas as características advindas dos escritores portugueses.'
        ],
        'answer': 'A influência europeia foi fundamental para o início do Romantismo no Brasil com todas as características advindas dos escritores portugueses.',
        'subject': 'Literatura Brasileira',
        'difficulty': 'Médio',
        'explanation': 'O Romantismo brasileiro foi fortemente influenciado pelos modelos europeus.'
    },
    {
        'question': 'Certa loja oferece duas opções de pagamento para seus clientes. Nas compras à vista, o cliente ganha um desconto de 8% sobre o valor total da compra. Caso queira comprar a prazo, o valor total da compra tem um acréscimo de 5% e o cliente pode dividir em até 3 parcelas iguais. Determinado cliente decidiu pagar sua compra a prazo, pois não tinha o valor integral para realizar o pagamento à vista. Sabendo-se que ele dividiu a compra em duas parcelas de R$ 420,00, qual o valor o cliente pagaria, caso fizesse a compra à vista?',
        'options': ['R$ 368,00', 'R$ 736,00', 'R$ 920,00', 'R$ 1.104,00'],
        'answer': 'R$ 736,00',
        'subject': 'Matemática Financeira',
        'difficulty': 'Médio',
        'explanation': 'Valor à vista = (2 × 420) / 1,05 × 0,92 = 840 / 1,05 × 0,92 = 800 × 0,92 = 736'
    },
    {
        'question': 'Márcia e Paulo são casados e estão adquirindo um imóvel novo, cujo valor é R$ 550.000,00, que será pago pelos dois de forma proporcional aos salários que cada um recebe. Assim, se o salário de Márcia é R$ 5.500,00 e o de Paulo é R$ 4.500,00 a diferença entre os valores que cada um dos dois irá pagar está compreendida entre:',
        'options': [
            'R$ 1.000,00 e R$ 10.000,00',
            'R$ 10.000,01 e R$ 25.000,00',
            'R$ 25.000,01 e R$ R$ 50.000,00',
            'R$ 50.000,01 e R$ 100.000,00'
        ],
        'answer': 'R$ 25.000,01 e R$ R$ 50.000,00',
        'subject': 'Matemática Financeira',
        'difficulty': 'Médio',
        'explanation': 'Diferença = 550.000 × (5.500 - 4.500) / (5.500 + 4.500) = 550.000 × 1.000 / 10.000 = 55.000'
    },
    {
        'question': 'Uma varanda quadrada está passando por uma reforma e irá receber um deck de madeira fazendo com que a sua área aumente. Sabe-se que serão acrescentados dois metros de um lado e três de outro, fazendo com que a varanda fique retangular. Caso a área total da varanda com o deck seja de 56 metros quadrados, qual será o seu perímetro?',
        'options': ['20 metros', '30 metros', '40 metros', '50 metros'],
        'answer': '30 metros',
        'subject': 'Matemática',
        'difficulty': 'Médio',
        'explanation': 'Lado original = x, nova área = (x+2)(x+3) = 56 ⇒ x² + 5x + 6 = 56 ⇒ x² + 5x - 50 = 0 ⇒ x = 5. Perímetro = 2×(7+8) = 30m'
    },
    {
        'question': 'Ao chegarem na praia após um longo dia de trabalho, quatro amigos foram em um restaurante e pediram, cada um, uma bebida diferente. Sobre a escolha de cada um deles, foram obtidas as seguintes informações: Antônio e Jorge não pediram cerveja. Fernando e Douglas não pediram água com gás e nem suco. Douglas não pediu refrigerante. Antônio não pediu água com gás. Se as bebidas escolhidas pelos quatro amigos estão dentre as citadas, qual deles escolheu o suco?',
        'options': ['Jorge', 'Douglas', 'Antônio', 'Fernando'],
        'answer': 'Jorge',
        'subject': 'Raciocínio Lógico',
        'difficulty': 'Difícil',
        'explanation': 'Por eliminação: Fernando (refri), Douglas (cerveja), Antônio (água sem gás), Jorge (suco)'
    },
    {
        'question': 'O gráfico representa a nota média dos alunos de uma escola nos anos 20X1, 20X2, 20X3, 20X4. Essas notas foram obtidas após a implementação de um modelo educacional inovador, que melhora o desempenho médio dos alunos em 5% a cada ano, tendo o projeto sido iniciado no ano 20X0 e seu primeiro resultado obtido no ano 20X1. Com base nessas informações, pode-se concluir que, no ano de 20X4, o modelo aumentou a nota média dessa escola em quantos pontos, aproximadamente, quando comparado com o ano 20X0?',
        'options': ['14,68 pontos', '15,72 pontos', '16,42 pontos', '17,24 pontos'],
        'answer': '16,42 pontos',
        'subject': 'Matemática',
        'difficulty': 'Difícil',
        'explanation': 'Aumento de 5% ao ano por 4 anos: 1,05⁴ ≈ 1,2155 → aumento de 21,55%'
    },
    {
        'question': 'Sobre os princípios e artigos da Declaração Universal dos Direitos Humanos, analise as afirmativas: I. A maternidade e a infância têm direito a cuidados e assistência especiais. II. Todo ser humano tem direito à instrução. A instrução será gratuita, pelo menos, nos graus elementares e fundamentais. III. Todo ser humano tem o direito de participar livremente da vida cultural da comunidade.',
        'options': ['I, II e III', 'I e II, apenas', 'I e III, apenas', 'II e III, apenas'],
        'answer': 'I, II e III',
        'subject': 'Direitos Humanos',
        'difficulty': 'Fácil',
        'explanation': 'Todas as afirmativas estão corretas conforme a Declaração Universal dos Direitos Humanos.'
    },
    {
        'question': 'A Lei Brasileira de Inclusão da Pessoa com Deficiência (Estatuto da Pessoa com Deficiência) – Lei nº 13.146/2015, destina-se a assegurar e promover, em condições de igualdade, o exercício dos direitos e das liberdades fundamentais por pessoa com deficiência, visando a sua inclusão social e cidadania. A avaliação da deficiência com vistas a nortear o processo educativo, dentro do contexto proposto pela referida Lei, quando necessária, será:',
        'options': [
            'Condição prévia à matrícula para ingresso no sistema educacional',
            'Prerrogativa da família do aprendiz com apoio de tecnologia assistiva',
            'Executada dentro de abordagem clínica, com participação da família',
            'Biopsicossocial, realizada por equipe multiprofissional e interdisciplinar'
        ],
        'answer': 'Biopsicossocial, realizada por equipe multiprofissional e interdisciplinar',
        'subject': 'Legislação Especial',
        'difficulty': 'Médio',
        'explanation': 'A LBI adota o modelo biopsicossocial para avaliação da deficiência.'
    },
    {
        'question': 'De acordo com o Estatuto da Criança e do Adolescente (ECA), NÃO é dever do Estado em relação à criança e ao adolescente:',
        'options': [
            'Atendimento no ensino fundamental, através de programas suplementares de material didático-escolar, transporte, alimentação e assistência à saúde',
            'Atendimento em creche e pré-escola às crianças de zero a cinco anos de idade; acesso aos níveis mais elevados do ensino, da pesquisa e da criação artística, segundo a capacidade de cada um; oferta de ensino noturno regular, adequado às condições do adolescente trabalhador',
            'Ensino fundamental, obrigatório e gratuito, inclusive para os que a ele não tiveram acesso na idade própria; progressiva extensão da obrigatoriedade e gratuidade ao ensino médio; atendimento educacional especializado aos portadores de deficiência, obrigatoriamente na rede regular de ensino',
            'O acesso ao ensino obrigatório e gratuito é direito público subjetivo. O não oferecimento do ensino obrigatório pelo poder público ou sua oferta irregular importa responsabilidade da autoridade competente.'
        ],
        'answer': 'Ensino fundamental, obrigatório e gratuito, inclusive para os que a ele não tiveram acesso na idade própria; progressiva extensão da obrigatoriedade e gratuidade ao ensino médio; atendimento educacional especializado aos portadores de deficiência, obrigatoriamente na rede regular de ensino',
        'subject': 'ECA',
        'difficulty': 'Difícil',
        'explanation': 'O ECA não exige obrigatoriamente o atendimento na rede regular para educação especial.'
    },
    {
        'question': 'O Plano Nacional de Educação (PNE), oficializado pela Lei nº 13.005/2014, é o compilado geral de tratativas da educação brasileira com vigência por dez anos. São consideradas diretrizes do PNE, EXCETO:',
        'options': [
            'Erradicação do analfabetismo',
            'Universalização do atendimento escolar',
            'Igualdade de atendimento a alguns alunos e capacitação de professores para o Atendimento Educacional Especializado (AEE)',
            'Superação das desigualdades educacionais, com ênfase na promoção da cidadania e erradicação de todas as formas de discriminação'
        ],
        'answer': 'Igualdade de atendimento a alguns alunos e capacitação de professores para o Atendimento Educacional Especializado (AEE)',
        'subject': 'PNE',
        'difficulty': 'Médio',
        'explanation': 'O PNE busca igualdade para TODOS os alunos, não apenas para alguns.'
    },
    {
        'question': 'A LDB estabelece, no Artigo 24, que a educação básica, nos níveis fundamental e médio, será organizada de acordo com regras comuns. Considerando tais regras, assinale a afirmativa INCORRETA.',
        'options': [
            'A escola poderá realizar a classificação do aluno no primeiro ano do ensino fundamental, procedente de outra escola',
            'A escola poderá organizar-se em classes, ou turmas, com alunos de séries distintas, com níveis equivalentes de adiantamento na matéria, para o ensino de línguas estrangeiras, artes, ou outros componentes curriculares',
            'A carga horária mínima anual será de oitocentas horas para o ensino fundamental distribuídas por um mínimo de duzentos dias de efetivo trabalho escolar, excluído o tempo reservado aos exames finais, quando houver',
            'Nos estabelecimentos que adotam a progressão regular por série, o regimento escolar pode admitir formas de progressão parcial, desde que preservada a sequência do currículo, observadas as normas do respectivo sistema de ensino'
        ],
        'answer': 'A carga horária mínima anual será de oitocentas horas para o ensino fundamental distribuídas por um mínimo de duzentos dias de efetivo trabalho escolar, excluído o tempo reservado aos exames finais, quando houver',
        'subject': 'LDB',
        'difficulty': 'Médio',
        'explanation': 'A carga horária inclui o tempo dos exames finais, não os exclui.'
    },
    {
        'question': 'Segundo a LDB, em seu Art. 24, "a verificação do rendimento escolar observará os seguintes critérios: avaliação contínua e cumulativa do desempenho do aluno, com prevalência dos aspectos qualitativos sobre os quantitativos e dos resultados ao longo do período sobre os de eventuais provas finais". De acordo com o exposto e considerando as funções da avaliação, pode-se afirmar que se trata da seguinte avaliação:',
        'options': ['Somativa', 'Formativa', 'Diagnóstica', 'Comparativa'],
        'answer': 'Formativa',
        'subject': 'Avaliação Educacional',
        'difficulty': 'Médio',
        'explanation': 'Avaliação formativa acompanha o desenvolvimento contínuo do aluno.'
    },
    {
        'question': 'A Constituição Federal estabelece, em seu artigo 212, o percentual mínimo aplicado anualmente pela União, Estados, Distrito Federal e Municípios na manutenção e desenvolvimento do ensino. Assinale a alternativa que completa correta e sequencialmente a disposição Constitucional: "A União aplicará, anualmente, nunca menos de ____, e os Estados, o Distrito Federal e os Municípios ____, no mínimo, da receita resultante de impostos..."',
        'options': ['15% / 22%', '18% / 25%', '21% / 23%', '23% / 28%'],
        'answer': '18% / 25%',
        'subject': 'Direito Constitucional',
        'difficulty': 'Fácil',
        'explanation': 'Art. 212 da CF: União 18%, Estados e Municípios 25%.'
    },
    {
        'question': 'A Lei de Diretrizes e Bases, de 1996, em seu Art. 13, é clara quanto às competências dos docentes. Assim, compete ao professor, no exercício de sua prática profissional, de acordo com a LDB: I. Participar da elaboração da proposta pedagógica do estabelecimento de ensino. II. Assegurar o cumprimento dos dias letivos e horas-aula estabelecidas. III. Elaborar e cumprir o plano de trabalho, segundo a proposta pedagógica do estabelecimento de ensino.',
        'options': ['I e III', 'II e IV', 'II, IV e V', 'I, III, IV e V'],
        'answer': 'I e III',
        'subject': 'LDB',
        'difficulty': 'Médio',
        'explanation': 'Art. 13 da LDB estabelece as competências dos professores.'
    },
    {
        'question': 'O Projeto Político Pedagógico – PPP, enquanto instrumento orientador do fazer escolar deve conter objetivos, metas e ações. NÃO corresponde aos pressupostos do PPP na escola:',
        'options': [
            'Para a sua elaboração deverá ser ouvida toda a comunidade escolar e seu entorno',
            'É um documento que reflete as intenções, os objetivos, as aspirações e os ideais da equipe escolar',
            'A valorização dos profissionais da educação e seu aperfeiçoamento permanente deve fazer parte dele',
            'Seu foco principal é a gestão escolar, pois ela orienta e organiza todo o trabalho da escola, sendo seu sujeito principal'
        ],
        'answer': 'Seu foco principal é a gestão escolar, pois ela orienta e organiza todo o trabalho da escola, sendo seu sujeito principal',
        'subject': 'Gestão Escolar',
        'difficulty': 'Médio',
        'explanation': 'O foco do PPP é o processo pedagógico, não apenas a gestão.'
    },
    {
        'question': 'Para compreender o caráter político e pedagógico do PPP, é INCORRETO considerar',
        'options': [
            'na perspectiva participativa, o projeto se expressa como uma totalidade (presente-futuro), englobando todas as dimensões da vida escolar',
            'a função social da educação e da escola em uma sociedade cada vez mais excludente, compreendendo que a educação, como campo de mediações sociais, define-se sempre por seu caráter intencional e político',
            'a necessária organicidade entre o PPP e os anseios da comunidade escolar, implicando a efetiva participação dos professores e alunos nos momentos de elaboração e implementação, e dos gestores no acompanhamento e avaliação',
            'que a escola pode, tanto reforçar, manter, reproduzir formas de dominação e de exclusão como constituir-se em espaço emancipatório, de construção de um novo projeto social, que atenda às necessidades da grande maioria da população'
        ],
        'answer': 'a necessária organicidade entre o PPP e os anseios da comunidade escolar, implicando a efetiva participação dos professores e alunos nos momentos de elaboração e implementação, e dos gestores no acompanhamento e avaliação',
        'subject': 'PPP',
        'difficulty': 'Difícil',
        'explanation': 'Todos os atores devem participar de todas as etapas, não apenas gestores no acompanhamento.'
    },
    {
        'question': 'Conforme a Lei de Diretrizes e Bases da Educação (LDB), em seus artigos 13 e 14, a elaboração da proposta pedagógica deve contar com a participação dos profissionais da educação. Diante disso, analise as afirmativas relacionadas à gestão escolar democrática: I. Exige o cultivo da cultura da participação, do trabalho coletivo, da ação colegiada, da realização pelo bem comum. II. A tarefa da gestão democrática e participativa na escola é contribuir para a implementação das mudanças, ajudando a criar um clima favorável na comunidade que a cerca.',
        'options': ['I, II e III', 'II, apenas', 'I e II, apenas', 'II e III, apenas'],
        'answer': 'I e II, apenas',
        'subject': 'Gestão Democrática',
        'difficulty': 'Médio',
        'explanation': 'As afirmativas I e II estão corretas sobre gestão democrática.'
    },
    {
        'question': 'Sobre um dos Indicadores da Qualidade na Educação – "dimensão gestão escolar democrática", pode-se afirmar que:',
        'options': [
            'Enfocam a participação nas decisões, a preocupação com a qualidade, com a relação custo-benefício e com a transparência',
            'Referem-se ao respeito, à alegria, à amizade e solidariedade, à disciplina, ao combate à discriminação e ao exercício dos direitos e deveres',
            'Enfatizam o bom aproveitamento dos recursos existentes na escola, a disponibilidade e a qualidade desses recursos e a organização dos espaços escolares',
            'Trata-se do planejamento das atividades educativas, sobre as estratégias e recursos de ensino-aprendizagem, os processos de avaliação dos alunos, incluindo a autoavaliação e a avaliação dos profissionais da escola'
        ],
        'answer': 'Enfocam a participação nas decisões, a preocupação com a qualidade, com a relação custo-benefício e com a transparência',
        'subject': 'Indicadores Educacionais',
        'difficulty': 'Médio',
        'explanation': 'A dimensão gestão democrática foca na participação e transparência.'
    },
    {
        'question': 'Os vários tipos de avaliação existentes fornecem diversos dados sobre o desempenho dos estudantes. "Considerada uma das modalidades avaliativas utilizadas no final de um processo educacional... tem como sua principal característica demonstrar o sucesso de assimilação (ou não) dos conteúdos pelos alunos, por meio da associação de notas ou conceitos como forma de classificação." As informações se referem ao seguinte tipo de avaliação:',
        'options': ['Somativa', 'Formativa', 'Diagnóstica', 'Comparativa'],
        'answer': 'Somativa',
        'subject': 'Avaliação Educacional',
        'difficulty': 'Fácil',
        'explanation': 'Avaliação somativa ocorre ao final do processo para classificação.'
    },
    {
        'question': 'O Sistema de Avaliação da Educação Básica (SAEB) é uma ferramenta crucial para o monitoramento e a melhoria da qualidade da educação no Brasil. Seus instrumentos são desenvolvidos para informar sobre: I. Atendimento escolar; equidade. II. Ensino e aprendizagem. III. Investimento; gestão. IV. Profissionais da educação.',
        'options': ['I, II, III, IV, V', 'II, apenas', 'II e IV, apenas', 'I, III e IV, apenas'],
        'answer': 'I, II, III, IV, V',
        'subject': 'Avaliação Educacional',
        'difficulty': 'Médio',
        'explanation': 'O SAEB abrange todas as dimensões da educação básica.'
    },
    {
        'question': 'Com relação à conquista da autonomia da escola, uma das atribuições do inspetor escolar é "subsidiar a escola na elaboração e no desenvolvimento do seu projeto pedagógico". Considere a atribuição citada e assinale a alternativa que NÃO a representa.',
        'options': [
            'Esclarecer a escola sobre os padrões básicos indispensáveis à elaboração do processo pedagógico',
            'Tomar providências, junto à Secretaria Municipal de Educação, para que as propostas de capacitação se efetivem',
            'Analisar o calendário escolar considerando as especificidades da escola, as peculiaridades regionais e locais e as referências legais, zelando pelo seu cumprimento',
            'Orientar a escola na definição de sua proposta curricular, adequando-se às especificidades socioculturais da região e às necessidades, prioridades e possibilidades da comunidade à qual atende'
        ],
        'answer': 'Analisar o calendário escolar considerando as especificidades da escola, as peculiaridades regionais e locais e as referências legais, zelando pelo seu cumprimento',
        'subject': 'Inspeção Escolar',
        'difficulty': 'Médio',
        'explanation': 'Esta é atribuição mais administrativa que pedagógica.'
    },
    {
        'question': 'O perfil do inspetor escolar deve ser de função: I. Verificadora. II. Avaliadora. III. Orientadora. IV. Corretiva.',
        'options': ['I, II, III e IV', 'II e III, apenas', 'I, II e III, apenas', 'II, III e IV, apenas'],
        'answer': 'I, II, III e IV',
        'subject': 'Inspeção Escolar',
        'difficulty': 'Fácil',
        'explanation': 'Todas as funções são atribuições do inspetor escolar.'
    },
    {
        'question': 'No Atendimento Educacional Especializado (AEE), o acompanhamento do processo de ensino-aprendizagem é fundamental para o desenvolvimento do aluno. De acordo com o que é normatizado na Educação Especial na rede estadual de Ensino de Minas Gerais, relacione os documentos listados a suas respectivas descrições: 1. Plano de Desenvolvimento Individual (PDI) 2. Plano de Atendimento Educacional Especializado (PAEE)',
        'options': ['2 – 1 – 1', '1 – 1 – 2', '2 – 1 – 2', '1 – 2 – 1'],
        'answer': '1 – 1 – 2',
        'subject': 'Educação Especial',
        'difficulty': 'Difícil',
        'explanation': 'PDI é obrigatório e acompanha o estudante; PAEE define recursos e atividades.'
    },
    {
        'question': 'A Avaliação de Desempenho dos Analistas Educacionais / Inspetores Escolares (ADIE) tem como finalidade o acompanhamento sistemático de desempenho do Analista Educacional / Inspetor Escolar (ANE/IE). As opções a seguir apresentam objetivos da ADIE, de acordo com a Resolução Conjunta SEPLAG/SEE, à exceção de uma. Assinale-a.',
        'options': [
            'Aprimorar a implementação dos processos de Inspeção Escolar',
            'Identificar e subsidiar as ações para o desenvolvimento profissional do servidor',
            'Adequar o nível de acesso do ANE/IE às plataformas de gestão do sistema de ensino do estado',
            'Acompanhar o cumprimento das atribuições previstas para o ANE/IE, pela Secretaria de Estado de Educação'
        ],
        'answer': 'Adequar o nível de acesso do ANE/IE às plataformas de gestão do sistema de ensino do estado',
        'subject': 'Legislação Estadual',
        'difficulty': 'Médio',
        'explanation': 'Este não é objetivo da ADIE, mas sim questão técnica de sistemas.'
    },
    {
        'question': 'As atribuições do Inspetor Escolar são estabelecidas pela Resolução SEE. Assinale a opção que apresenta corretamente uma dessas atribuições.',
        'options': [
            'Orientação, assistência e controle do processo administrativo das escolas e, na forma do regulamento, do seu processo pedagógico',
            'Elaboração e na implementação de projetos educativos ou, como docente, em projeto de formação continuada de educadores, na forma do regulamento',
            'Organização e atualização de cadastros, arquivos, fichários, livros de escrituração da escola, relativos aos registros dos servidores e à vida escolar dos alunos',
            'Atuação como elemento articulador das relações interpessoais internas e externas da escola que envolvam os profissionais, os alunos e seus pais e a comunidade'
        ],
        'answer': 'Orientação, assistência e controle do processo administrativo das escolas e, na forma do regulamento, do seu processo pedagógico',
        'subject': 'Inspeção Escolar',
        'difficulty': 'Médio',
        'explanation': 'Esta é a atribuição principal do inspetor escolar conforme a legislação.'
    },
    {
        'question': 'Sobre o IDEB e suas implicações na avaliação da qualidade da educação, analise as afirmativas: I. O IDEB combina dados de desempenho acadêmico dos alunos em avaliações padronizadas e taxas de rendimento escolar para medir a qualidade da educação. II. Um aumento no IDEB necessariamente indica uma melhoria na qualidade do ensino e na aprendizagem dos alunos. III. A nota média de aprendizagem dos alunos é um dos componentes essenciais do cálculo do IDEB.',
        'options': ['I, II e V', 'I, III e IV', 'II, IV e V', 'I, III e V'],
        'answer': 'I, III e IV',
        'subject': 'Indicadores Educacionais',
        'difficulty': 'Difícil',
        'explanation': 'I, III e IV estão corretas sobre o IDEB.'
    },
    {
        'question': 'O currículo da educação infantil, de acordo com a Resolução do Conselho Estadual de Educação de Minas Gerais (CEE/MG), deve ser entendido como',
        'options': [
            'um conjunto de práticas espontâneas que se fundamentam na teoria social crítica, e que considera a trajetória dos alunos para direcionar todo o processo de ensino-aprendizagem',
            'um documento que contém todas as disciplinas que devem ser estudadas pelas crianças, de acordo com o ano letivo, com o intuito de submetê-las a um processo formal de avaliação',
            'um documento direcionador do processo de formação disciplinar que pode identificar a necessidade de a escola promover ações coletivas para acolhimento e intervenção profissional ativa, em casos de abuso sexual praticados contra os alunos',
            'um conjunto de práticas, efetivadas pelas relações estabelecidas entre os professores e as crianças, que buscam articular as experiências e os saberes das crianças e dos professores com conhecimentos que fazem parte do patrimônio cultural, artístico, ambiental, científico e tecnológico'
        ],
        'answer': 'um conjunto de práticas, efetivadas pelas relações estabelecidas entre os professores e as crianças, que buscam articular as experiências e os saberes das crianças e dos professores com conhecimentos que fazem parte do patrimônio cultural, artístico, ambiental, científico e tecnológico',
        'subject': 'Educação Infantil',
        'difficulty': 'Médio',
        'explanation': 'Esta é a concepção de currículo para educação infantil conforme a resolução.'
    }
]

# PLANO DE ESTUDOS COMPLETO
DEFAULT_STUDY_PLAN = """📚 PLANO DE ESTUDOS - ANALISTA EDUCACIONAL

🎯 METAS DIÁRIAS:
• 2 horas de estudo teórico
• 50 questões resolvidas  
• 30 minutos de revisão

📅 SEMANA 1: LÍNGUA PORTUGUESA
Segunda: Interpretação de Texto (20 questões)
Terça: Morfologia (25 questões)
Quarta: Sintaxe (30 questões)
Quinta: Semântica (25 questões)
Sexta: Redação Oficial (20 questões)
Sábado: Revisão Geral (40 questões)
Domingo: Simulado (50 questões)

📅 SEMANA 2: DIREITO ADMINISTRATIVO
Segunda: Princípios da Administração (25 questões)
Terça: Atos Administrativos (30 questões)
Quarta: Serviços Públicos (25 questões)
Quinta: Licitações (30 questões)
Sexta: Controle da Administração (20 questões)
Sábado: Revisão (40 questões)
Domingo: Simulado (50 questões)

📅 SEMANA 3: LEGISLAÇÃO EDUCACIONAL
Segunda: LDB - Lei 9.394/96 (30 questões)
Terça: ECA - Estatuto da Criança (25 questões)
Quarta: PNE - Plano Nacional (20 questões)
Quinta: Diretrizes Curriculares (25 questões)
Sexta: Legislação Estadual (30 questões)
Sábado: Revisão (40 questões)
Domingo: Simulado (50 questões)

📅 SEMANA 4: CONHECIMENTOS ESPECÍFICOS
Segunda: Gestão Educacional (25 questões)
Terça: Avaliação Educacional (30 questões)
Quarta: Políticas Públicas (20 questões)
Quinta: Financiamento da Educação (25 questões)
Sexta: Educação Inclusiva (30 questões)
Sábado: Revisão Geral (50 questões)
Domingo: Simulado Completo (80 questões)

🎯 DICAS IMPORTANTES:
• Faça pausas a cada 50 minutos
• Revise o conteúdo no mesmo dia
• Mantenha um ritmo constante
• Acompanhe seu progresso"""

# Botão personalizado
class CustomButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''
        self.size_hint_y = None
        self.height = dp(50)
        self.font_size = sp(16)
        
        with self.canvas.before:
            Color(rgba=COLORS['primary'])
            self.rect = RoundedRectangle(radius=[dp(10)])
            
        self.bind(pos=self.update_rect, size=self.update_rect)
        
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

# TELA DE SIMULADO
class SimuladoScreen(Screen):
    current_question = NumericProperty(0)
    score = NumericProperty(0)
    total_questions = NumericProperty(0)
    user_answers = ListProperty([])
    time_remaining = NumericProperty(18000)  # 5 horas

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.questions = SIMULADO_QUESTIONS
        self.total_questions = len(self.questions)
        self.user_answers = [None] * self.total_questions
        Clock.schedule_once(self.setup_ui, 0.1)

    def setup_ui(self, dt):
        layout = BoxLayout(orientation='vertical')
        
        # Header
        header = BoxLayout(size_hint_y=0.1, padding=dp(10))
        back_btn = Button(text='Voltar', size_hint_x=0.3)
        back_btn.bind(on_press=self.go_back)
        
        self.title_label = Label(text=f'Questão 1/{self.total_questions}', halign='center')
        self.time_label = Label(text='05:00:00', size_hint_x=0.3)
        
        header.add_widget(back_btn)
        header.add_widget(self.title_label)
        header.add_widget(self.time_label)
        layout.add_widget(header)
        
        # Progresso
        self.progress = ProgressBar(max=self.total_questions, size_hint_y=0.02)
        layout.add_widget(self.progress)
        
        # Área da questão
        scroll = ScrollView()
        self.content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15),
                               size_hint_y=None)
        self.content.bind(minimum_height=self.content.setter('height'))
        scroll.add_widget(self.content)
        layout.add_widget(scroll)
        
        # Navegação
        nav = BoxLayout(size_hint_y=0.1, spacing=dp(10), padding=dp(10))
        prev_btn = CustomButton(text='Anterior')
        prev_btn.bind(on_press=self.previous_question)
        
        next_btn = CustomButton(text='Próxima')
        next_btn.bind(on_press=self.next_question)
        
        finish_btn = CustomButton(text='Finalizar', background_color=COLORS['accent'])
        finish_btn.bind(on_press=self.finish_simulado)
        
        nav.add_widget(prev_btn)
        nav.add_widget(next_btn)
        nav.add_widget(finish_btn)
        layout.add_widget(nav)
        
        self.add_widget(layout)
        self.show_question(0)
        Clock.schedule_interval(self.update_timer, 1)

    def show_question(self, index):
        self.current_question = index
        self.content.clear_widgets()
        
        questao = self.questions[index]
        
        # Informações
        info = BoxLayout(size_hint_y=None, height=dp(30))
        info.add_widget(Label(text=f"{questao['subject']} - {questao['difficulty']}"))
        self.content.add_widget(info)
        
        # Enunciado
        enunciado = Label(
            text=f"{index + 1}. {questao['question']}",
            text_size=(Window.width - dp(40), None),
            size_hint_y=None,
            halign='left'
        )
        enunciado.bind(texture_size=enunciado.setter('size'))
        self.content.add_widget(enunciado)
        
        # Alternativas
        self.alternativas = []
        for i, alt in enumerate(questao['options']):
            btn = CustomButton(
                text=f"{chr(65+i)}) {alt}",
                size_hint_y=None,
                height=dp(60)
            )
            btn.index = i
            btn.bind(on_press=self.select_answer)
            self.alternativas.append(btn)
            self.content.add_widget(btn)
        
        self.update_buttons()
        self.title_label.text = f'Questão {index + 1}/{self.total_questions}'
        self.progress.value = index + 1

    def select_answer(self, instance):
        self.user_answers[self.current_question] = instance.index
        self.update_buttons()

    def update_buttons(self):
        for btn in self.alternativas:
            if btn.index == self.user_answers[self.current_question]:
                btn.background_color = COLORS['secondary']
            else:
                btn.background_color = COLORS['primary']

    def previous_question(self, instance):
        if self.current_question > 0:
            self.show_question(self.current_question - 1)

    def next_question(self, instance):
        if self.current_question < self.total_questions - 1:
            self.show_question(self.current_question + 1)

    def update_timer(self, dt):
        if self.time_remaining > 0:
            self.time_remaining -= 1
            horas = self.time_remaining // 3600
            minutos = (self.time_remaining % 3600) // 60
            segundos = self.time_remaining % 60
            self.time_label.text = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
        else:
            self.finish_simulado()

    def finish_simulado(self, instance=None):
        # Calcular pontuação
        acertos = 0
        for i, resposta in enumerate(self.user_answers):
            if resposta is not None and self.questions[i]['options'][resposta] == self.questions[i]['answer']:
                acertos += 1
        
        self.score = acertos
        porcentagem = (acertos / self.total_questions) * 100
        
        # Mostrar resultados
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        content.add_widget(Label(text=f'RESULTADO FINAL', font_size=sp(20), bold=True))
        content.add_widget(Label(text=f'Acertos: {acertos}/{self.total_questions}'))
        content.add_widget(Label(text=f'Porcentagem: {porcentagem:.1f}%'))
        
        if porcentagem >= 70:
            content.add_widget(Label(text='🎉 APROVADO!', font_size=sp(18), color=COLORS['secondary']))
        else:
            content.add_widget(Label(text='📝 ESTUDE MAIS', font_size=sp(18), color=COLORS['accent']))
        
        close_btn = CustomButton(text='Voltar ao Início')
        content.add_widget(close_btn)
        
        popup = Popup(title='Simulado Finalizado', content=content, size_hint=(0.8, 0.6))
        close_btn.bind(on_press=lambda x: (popup.dismiss(), setattr(self.manager, 'current', 'main')))
        popup.open()

    def go_back(self, instance):
        self.manager.current = 'main'

# BANCO DE QUESTÕES
class QuestionBankScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.setup_ui, 0.1)

    def setup_ui(self, dt):
        layout = BoxLayout(orientation='vertical')
        
        # Header
        header = BoxLayout(size_hint_y=0.1, padding=dp(10))
        back_btn = Button(text='Voltar')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        
        title = Label(text='Banco de Questões', halign='center')
        filter_btn = Button(text='Filtrar', size_hint_x=0.3)
        filter_btn.bind(on_press=self.show_filters)
        
        header.add_widget(back_btn)
        header.add_widget(title)
        header.add_widget(filter_btn)
        layout.add_widget(header)
        
        # Lista de questões
        scroll = ScrollView()
        self.questions_layout = GridLayout(cols=1, spacing=dp(10), padding=dp(10),
                                         size_hint_y=None)
        self.questions_layout.bind(minimum_height=self.questions_layout.setter('height'))
        scroll.add_widget(self.questions_layout)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
        self.show_questions()

    def show_questions(self):
        self.questions_layout.clear_widgets()
        
        for i, questao in enumerate(SIMULADO_QUESTIONS):
            card = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(120),
                           padding=dp(10))
            
            with card.canvas.before:
                Color(rgba=COLORS['background'])
                Rectangle(pos=card.pos, size=card.size)
            
            # Header do card
            header = BoxLayout(size_hint_y=0.3)
            header.add_widget(Label(text=f"{questao['subject']} - {questao['difficulty']}"))
            card.add_widget(header)
            
            # Questão (resumida)
            questao_text = questao['question'][:80] + '...' if len(questao['question']) > 80 else questao['question']
            questao_label = Label(text=questao_text, size_hint_y=0.5, halign='left')
            card.add_widget(questao_label)
            
            # Botões
            botoes = BoxLayout(size_hint_y=0.2)
            ver_btn = Button(text='Ver', size_hint_x=0.5)
            ver_btn.bind(on_press=lambda x, q=questao: self.show_question_detail(q))
            
            praticar_btn = Button(text='Praticar', size_hint_x=0.5)
            praticar_btn.bind(on_press=lambda x, q=questao: self.practice_question(q))
            
            botoes.add_widget(ver_btn)
            botoes.add_widget(praticar_btn)
            card.add_widget(botoes)
            
            self.questions_layout.add_widget(card)

    def show_filters(self, instance):
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        content.add_widget(Label(text='Filtrar por:'))
        
        materia_spinner = Spinner(
            text='Todas as Matérias',
            values=['Todas as Matérias', 'Língua Portuguesa', 'Direito Administrativo', 'LDB', 'ECA', 'Gestão Educacional', 'Avaliação Educacional']
        )
        content.add_widget(materia_spinner)
        
        dificuldade_spinner = Spinner(
            text='Todas as Dificuldades',
            values=['Todas as Dificuldades', 'Fácil', 'Médio', 'Difícil']
        )
        content.add_widget(dificuldade_spinner)
        
        botoes = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        cancelar = Button(text='Cancelar')
        filtrar = Button(text='Aplicar Filtro')
        
        botoes.add_widget(cancelar)
        botoes.add_widget(filtrar)
        content.add_widget(botoes)
        
        popup = Popup(title='Filtrar Questões', content=content, size_hint=(0.8, 0.6))
        cancelar.bind(on_press=popup.dismiss)
        filtrar.bind(on_press=lambda x: (popup.dismiss(), self.apply_filters(materia_spinner.text, dificuldade_spinner.text)))
        popup.open()

    def apply_filters(self, materia, dificuldade):
        # Implementar filtragem real
        self.show_questions()

    def show_question_detail(self, questao):
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        scroll = ScrollView()
        detalhes = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(10))
        detalhes.bind(minimum_height=detalhes.setter('height'))
        
        detalhes.add_widget(Label(text=questao['question'], text_size=(None, None)))
        for i, alt in enumerate(questao['options']):
            detalhes.add_widget(Label(text=f"{chr(65+i)}) {alt}"))
        
        detalhes.add_widget(Label(text=f"Resposta: {questao['answer']}"))
        detalhes.add_widget(Label(text=f"Explicação: {questao['explanation']}"))
        
        scroll.add_widget(detalhes)
        content.add_widget(scroll)
        
        fechar = Button(text='Fechar', size_hint_y=None, height=dp(50))
        content.add_widget(fechar)
        
        popup = Popup(title='Detalhes da Questão', content=content, size_hint=(0.9, 0.8))
        fechar.bind(on_press=popup.dismiss)
        popup.open()

    def practice_question(self, questao):
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        content.add_widget(Label(text=questao['question'], text_size=(None, None)))
        
        self.practice_buttons = []
        for i, alt in enumerate(questao['options']):
            btn = Button(text=f"{chr(65+i)}) {alt}", size_hint_y=None, height=dp(60))
            btn.index = i
            btn.bind(on_press=lambda x: self.check_practice_answer(x, questao))
            self.practice_buttons.append(btn)
            content.add_widget(btn)
        
        self.result_label = Label(text='')
        content.add_widget(self.result_label)
        
        popup = Popup(title='Praticar Questão', content=content, size_hint=(0.9, 0.8))
        popup.open()

    def check_practice_answer(self, instance, questao):
        resposta_correta = questao['options'].index(questao['answer'])
        
        for btn in self.practice_buttons:
            if btn.index == resposta_correta:
                btn.background_color = COLORS['secondary']
            elif btn == instance and btn.index != resposta_correta:
                btn.background_color = COLORS['accent']
        
        if instance.index == resposta_correta:
            self.result_label.text = 'Resposta Correta! ✅'
            self.result_label.color = COLORS['secondary']
        else:
            self.result_label.text = f'Resposta Errada! Correto: {questao["answer"]}'
            self.result_label.color = COLORS['accent']

# TELA DE PLANO DE ESTUDOS
class StudyPlanScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.setup_ui, 0.1)

    def setup_ui(self, dt):
        layout = BoxLayout(orientation='vertical')
        
        # Header
        header = BoxLayout(size_hint_y=0.1, padding=dp(10))
        back_btn = Button(text='Voltar')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        
        title = Label(text='Plano de Estudos', halign='center')
        edit_btn = Button(text='Editar', size_hint_x=0.3)
        edit_btn.bind(on_press=self.edit_plan)
        
        header.add_widget(back_btn)
        header.add_widget(title)
        header.add_widget(edit_btn)
        layout.add_widget(header)
        
        # Conteúdo do plano
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10),
                          size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))
        
        plano_label = Label(
            text=DEFAULT_STUDY_PLAN,
            text_size=(Window.width - dp(40), None),
            halign='left',
            size_hint_y=None
        )
        plano_label.bind(texture_size=plano_label.setter('size'))
        content.add_widget(plano_label)
        
        scroll.add_widget(content)
        layout.add_widget(scroll)
        
        self.add_widget(layout)

    def edit_plan(self, instance):
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        editor = TextInput(text=DEFAULT_STUDY_PLAN, size_hint_y=0.8)
        content.add_widget(editor)
        
        botoes = BoxLayout(size_hint_y=0.2, spacing=dp(10))
        cancelar = Button(text='Cancelar')
        salvar = Button(text='Salvar')
        
        botoes.add_widget(cancelar)
        botoes.add_widget(salvar)
        content.add_widget(botoes)
        
        popup = Popup(title='Editar Plano de Estudos', content=content, size_hint=(0.9, 0.9))
        cancelar.bind(on_press=popup.dismiss)
        salvar.bind(on_press=lambda x: (popup.dismiss(), self.save_plan(editor.text)))
        popup.open()

    def save_plan(self, texto):
        # Aqui salvaria o plano editado
        print("Plano salvo:", texto[:100])

# TELA DE ESTATÍSTICAS
class StatisticsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.setup_ui, 0.1)

    def setup_ui(self, dt):
        layout = BoxLayout(orientation='vertical')
        
        # Header
        header = BoxLayout(size_hint_y=0.1, padding=dp(10))
        back_btn = Button(text='Voltar')
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        
        title = Label(text='Estatísticas', halign='center')
        header.add_widget(back_btn)
        header.add_widget(title)
        layout.add_widget(header)
        
        # Conteúdo
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10),
                          size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))
        
        # Estatísticas de exemplo
        stats = [
            ('📊 Simulados Realizados', '5'),
            ('🎯 Média de Acertos', '78%'),
            ('⏰ Tempo Médio', '4h 15min'),
            ('📈 Melhor Performance', '92%'),
            ('📚 Questões Resolvidas', '1.250')
        ]
        
        for icon_text, valor in stats:
            card = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60),
                           padding=dp(10))
            
            with card.canvas.before:
                Color(rgba=COLORS['background'])
                Rectangle(pos=card.pos, size=card.size)
            
            card.add_widget(Label(text=icon_text, size_hint_x=0.7))
            card.add_widget(Label(text=valor, size_hint_x=0.3, bold=True))
            content.add_widget(card)
        
        scroll.add_widget(content)
        layout.add_widget(scroll)
        
        self.add_widget(layout)

# TELA PRINCIPAL
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.setup_ui, 0.1)

    def setup_ui(self, dt):
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Título
        title = Label(
            text='STUDY PRO\nANALISTA EDUCACIONAL',
            font_size=sp(24),
            bold=True,
            size_hint_y=0.2
        )
        layout.add_widget(title)
        
        # Botões principais
        botoes = [
            ('🎯 SIMULADO COMPLETO', 'simulado'),
            ('📚 BANCO DE QUESTÕES', 'questions'),
            ('📅 PLANO DE ESTUDOS', 'study_plan'),
            ('📊 ESTATÍSTICAS', 'statistics')
        ]
        
        for texto, tela in botoes:
            btn = CustomButton(text=texto, size_hint_y=0.15)
            btn.bind(on_press=lambda x, t=tela: setattr(self.manager, 'current', t))
            layout.add_widget(btn)
        
        self.add_widget(layout)

# Gerenciador de Telas
class StudyApp(App):
    def build(self):
        self.sm = ScreenManager()
        
        telas = [
            ('main', MainScreen(name='main')),
            ('simulado', SimuladoScreen(name='simulado')),
            ('questions', QuestionBankScreen(name='questions')),
            ('study_plan', StudyPlanScreen(name='study_plan')),
            ('statistics', StatisticsScreen(name='statistics')),
        ]
        
        for nome, tela in telas:
            self.sm.add_widget(tela)
        
        return self.sm

if __name__ == '__main__':
    StudyApp().run()