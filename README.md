Інструкція для запуску Streamlit-додатку “Екологічна аналітика”

Клонування репозиторію
Відкрити CMD або PowerShell та виконати:

git clone https://github.com/OoverHeaven/ekologichna_analityka.git
cd ekologichna_analityka


Створення віртуального середовища

python -m venv env


Активація віртуального середовища

env\Scripts\activate.bat


Після цього перед шляхом у CMD з’явиться (env).

Встановлення залежностей

pip install -r requirements.txt


Встановлюються всі необхідні бібліотеки (streamlit, pandas, plotly, folium, scikit-learn, streamlit-folium).

Запуск додатку

streamlit run app.py


Відкриється браузер із веб-додатком.

Карта показує Кам’янець-Подільський, графік трендів PM2.5 та прогноз на 10 годин вперед.

Зупинка додатку

У CMD натиснути Ctrl + C.

Примітки

Додаток використовує демонстраційні дані у data/air_quality.csv.

Якщо PowerShell блокує скрипти, тимчасово дозволити виконання:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
