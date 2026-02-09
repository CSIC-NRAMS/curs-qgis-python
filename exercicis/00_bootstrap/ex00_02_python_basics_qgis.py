"""Exercici 0.2 — Python bàsic a QGIS (ràpid i didàctic).

Objectiu:
- Veure exemples curts de tipatge dinàmic, llistes/dict/tuple i funció vs mètode.
- Executar codi dins el Script Editor de QGIS.
"""

# (Primer cop: variable) Una variable guarda un valor i li posem un nom.
# --- Tipatge dinàmic (una variable pot canviar de tipus) ---
valor = 10
print("OK -> valor (int):", valor)

valor = 3.5
print("OK -> valor (float):", valor)

valor = "hola"
print("OK -> valor (str):", valor)

# --- Estructures bàsiques ---
# (Primer cop: llista/diccionari/tupla) Són contenidors per guardar més d'un valor.
llista = ["Olot", "Girona", "Barcelona"]
diccionari = {"estacio": "EMA 0250", "pluja_mm": 12.4}
tupla = (2024, 10, 3)

print("OK -> llista:", llista)
print("OK -> diccionari:", diccionari)
print("OK -> tupla:", tupla)

# Funció vs mètode
# (Primer cop: funcio) Una funcio es un bloc reutilitzable que pots cridar per nom.
# - Una funció és una cosa que crides amb parèntesis: len(llista)
# - Un mètode és una funció lligada a un objecte: llista.append("...")
print("OK -> len(llista):", len(llista))
llista.append("Tarragona")
print("OK -> llista després d'append:", llista)

# --- Funcions simples ---
# Definim funcions per separar la logica en peces petites i clares.

def suma(a, b):
    """Suma dos valors i retorna el resultat."""
    return a + b


def missatge_benvinguda(nom):
    """Retorna un missatge simpàtic per a l'usuari."""
    return f"Benvingut/da, {nom}!"


def es_valid(x):
    """Comprova si un valor és numèric i positiu."""
    # (Primer cop: try/except) Ens permet capturar errors sense aturar el programa.
    try:
        return float(x) >= 0
    except Exception:
        return False


print("OK -> suma(2, 3):", suma(2, 3))
print("OK -> missatge:", missatge_benvinguda("Anna"))
print("OK -> es_valid(5):", es_valid(5))
print("OK -> es_valid('text'):", es_valid("text"))

print("OK -> Exercici 0.2 completat.")
