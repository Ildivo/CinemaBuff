console.log('Привет от JavaScript!');
const data = JSON.parse(document.getElementById('my-data').dataset.json);
console.log(data);

const questions = [
  {
    question: "Какого типа данные представляет строка?",
    choices: ["Число", "Логическое значение", "Текст", "Объект"],
    correctAnswer: 2
  },
  // Добавьте сюда остальные вопросы
];

let currentQuestion = 0;
let score = 0;

// Функция для отображения вопроса
function showQuestion() {
  const questionElement = document.getElementById('question');
  const choicesElement = document.getElementById('choices');   


  questionElement.textContent = questions[currentQuestion].question;

  choicesElement.innerHTML   
 = '';
  questions[currentQuestion].choices.forEach((choice, index) => {
    const button = document.createElement('button');
    button.textContent = choice;   

    button.addEventListener('click', () => {
      checkAnswer(index);
    });
    choicesElement.appendChild(button);   

  });
}

// Функция для проверки ответа
function checkAnswer(selected) {
  if (selected === questions[currentQuestion].correctAnswer) {
    score++;
    
  }

  currentQuestion++;
  if (currentQuestion < questions.length) {
    showQuestion();
  } else {
    showResults();   

  }
}

// Функция для отображения результатов
function showResults() {
  const resultsElement = document.getElementById('results');
  resultsElement.textContent = `Вы набрали ${score} из ${questions.length} баллов!`;
}

// Начальная инициализация
showQuestion();