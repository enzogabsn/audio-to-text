# Audio to text

**Audio to text** é o meu projeto com Python onde você coloca um caminho com uma pasta de áudios, mas esses áudios tem que ser em wav ou em mp3, desta forma:

![image](https://github.com/user-attachments/assets/9798133c-a370-489b-81a5-7ec64f8cc3cd)

Depois, você deve colocar o caminho de uma pasta onde ficarão os textos, ou seja, quando os áudios forem transcrevidos o texto dos áudios ficarão em uma pasta, dessa forma:

![image](https://github.com/user-attachments/assets/14648c72-7718-4a91-be0d-79135d2c471c)

No caso, só irá aparecer os textos quando o áudio ser transcrevido.

Nesse projeto, utilizei uma API Key na OpenAI com o Modelo GPT-3.5-turbo, mas é bem simples de fazer. Caso você seja experiente com a API, você pode criar uma sozinho, mas caso não saiba recomendo ver um tutorial de como criar a sua chave API. Mas com a sua chave API criada, você cria um arquivo fora das pastas chamado `.env`, e coloque dentro dele assim:

```env

OPENAI_API_KEY=SUA_CHAVE_API
```

Lembrando que você deve criar uma chave API e também deve ter créditos para utilizá-la

Agora basta você executar o arquivo python e ele vai transcrever os áudios para texto.

### Requerimentos

- Python instalado na máquina
- Ter o Visual Studio Code
- Ter a extensão do Visual Studio Code de Python, basta pesquisar Python e baixar a primeira opção da Microsoft
- Ter uma pasta de destino para os áudios
- Ter uma pasta de destino para os textos
