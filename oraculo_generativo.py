import openai

# AQUÍ VA LA LLAVE - descomenta la próxima linea
# openai.api_key = ''

from dotenv import load_dotenv
load_dotenv()

import os
# openai.api_key = os.environ['OPENAI_API_KEY']

def gpt_transform_piece(texto, query):
    prompt = f'''Instrucciones:
    - Toma el siguiente texto y utilizalo para desarrollar una respuesta a la consulta de manera abstracta en un largo ensayo poético que es crítico, pésimista, cyborg y feminista. 
    - Utiliza formas complejas y escritura diagramática o poesía caligráfica.
    - Escribe en espaol de méxico usando género neutro (nosotrxs, ellx, ...) o femenino.

    Texto:
    {texto}

    Consulta:
    {query}

    Ensayo:
    '''
    
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=500,
        temperature = 1.1,
        stream=True
    )

    transformed_text = ""
    for chunk in response:
        transformed_text += chunk.to_dict()['choices'][0]['text']

    return transformed_text

if __name__ == '__main__':
    texto = "La tecnología y sus artefactos representan la cristalización del avance del intelecto, dispositivos que posibilitan, restringen y potencia- lizan la actividad humana, creando nuevos contextos partiendo de nuestras capacidades biológicas y creando una simbiosis cognitiva y emocional en la que nuestras características humanas se funden con los avances tecnológicos"
    gpt_transform_piece(texto)