# Steganograph-App-y

Welcome to Steganograph-App-y! This is a Python application where you can try out exisiting steganographic algorithms as well as different combinations of edge detectors for the purpose of embedding in steganography on an easy-to-use GUI.

# Getting Started

To get started with the app, first clone the repo and `cd` into the directory:

```
git clone https://github.com/FaiZaman/Steganograph-app-y.git
cd Steganograph-app-y
```

# Running

To run the application, navigate to the root directory and run the following command:

```
python app.py
```

Note that your system must be running Python 3.7 or a later version for the application to function properly.

# Using the Graphical User Interface

Click `Embed`/`Hybrid Embed`/`Extract`/`Hybrid Extract` for the respective actions.

## Embedding

1) Select an embedding algorithm from the dropdown list.
2) Select the cover image file to embed your message into.
3) Select the message file to embed into the cover image.
4) Enter a secret key based on which the embedding order is determined (do not lose this key as you need it for extraction!).
5) Select the folder where the stego image will be saved.
6) Click `Embed`.

## Hybrid Embedding

1) Select the first edge detector from the dropdown list.
2) Select the second edge detector from the dropdown list.
3) Select the hybridisation technique from the dropdown list.
4) Select the cover image file to embed your message into.
5) Select the message file to embed into the cover image.
6) Enter a secret key based on which the embedding order is determined. (do not lose this key as you need it for extraction!).
7) Select the folder where the stego image will be saved.
8) Click `Hybrid Embed`

## Extraction

1) Select an embedding algorithm from the dropdown list. This must be the same algorithm you used to embed the message.
2) Select the stego image file to extract your message from.
3) Enter a secret key based on which the extraction order is determined. This must be the same key as the one used in the embedding process.
4) Select the folder where the extracted message will be saved.
5) Click `Extract`.

## Hybrid Extraction

1) Select the first edge detector from the dropdown list. This must be the same detector you used in the embedding process.
2) Select the second edge detector from the dropdown list. This must be the same detector you used in the embedding process.
3) Select the hybridisation technique from the dropdown list. This must be the same hybridisation technique you used in the embedding process
4) Select the stego image file to extract your message from.
6) Enter a secret key based on which the extraction order is determined. This must be the same key as the one used in the embedding process.
7) Select the folder where the extracted message image will be saved.
8) Click `Hybrid Extract`.
