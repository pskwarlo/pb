Konfiguracja:
```
curl -fsSL https://ollama.com/install.sh | sh
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
docker exec -it ollama ollama pull llama3
docker exec -it ollama ollama run llama3
```

Instalacja wymaganych bibliotek:
```
cd pb
python3 -m venv venv 
pip install -r requirements.txt
```

Otwieramy plik config.py i ustawiamy parametr
```
DATA_PATH = "sources/" -> ścieżka do dokumentów (dodawane rekursywnie) 
```

Po przygotowaniu pliku konfiguracyjnego:
```
python3 caretaker.py (--reset -> rebuild db)
streamlit run app.py (defaults to localhost:8501)
```
