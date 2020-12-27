# Steganograph-App-y

Welcome to the Steganograph-App-y! This is a Python application where you can try out exisiting steganographic algorithms as well as a new algorithm proposed and implemented by me on an easy-to-use GUI.

# Getting Started

To get started with the app, first clone the repo and `cd` into the directory:

```
git clone https://github.com/FaiZaman/Steganograph-app-y.git
cd Steganograph-app-y
```

# Running

To run the application, navigate to the root directory and run the following command:

```
python Main.py
```

Note that your system must be running Python 3.7 or a later version for the application to function properly.

# Using the Graphical User Interface

Click `Embed` or `Extract` for the respective actions.

## Embedding

1) Select an embedding algorithm from the dropdown list.
2) Select the cover image file to embed your message into.
3) Select the message file to embed into the cover image.
4) Enter a secret key based on which the embedding order is determined. Do not lose this key as you need it for extraction.
5) Select the folder where the stego image will be saved.
6) Click `Embed`.

## Extraction

1) Select an embedding algorithm from the dropdown list. This must be the same algorithm you used to embed the message.
2) Select the stego image file to extract your message from.
3) Enter a secret key based on which the extraction order is determined. This must be the same key as the one used in the embedding process.
4) Select the folder where the extracted message will be saved.
5) Click `Extract`.
