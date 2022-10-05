from tkinter import *
import tkinter as tk
import openai
from threading import *

# PUT YOUR OPEN AI KEY HERE, DELETE BEFORE COMMITTING TO GITHUB
# This will also charge your account, be careful and use test strings if possible
openai.api_key = ""

# Creates the window
window = tk.Tk()
window.title("Summarizer")
window.geometry('750x850')
frame = Frame(window)

# Centers all widgets
frame.grid(row=0, column=0, sticky="N")
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
frame.grid(row=0, column=0, sticky="N")

# Initializes a variable for summarizer type
sumType = tk.IntVar()
sumType.set(1)

# Creates a thread in order to prevent window from freezing while waiting for text to generate
def apiResponseThread():
    # Prevents button from being pressed while loading
    # Also gives a visual indicator for the program loading
    submitButton.config(bg="#DBDBDB", state="disabled", text="Loading")

    if openai.api_key == "":
        outputBox.delete(1.0, END)
        outputBox.insert(INSERT, "No API key provided. Please exit and provide an API key.")
        return

    # Calls the submitInput() function in a thread
    t1 = Thread(target=submitInput)
    t1.start()


# This function is called to process the input of the text box in the previously mentioned thread
def submitInput():
    # Gets the text from the input box
    inp = inputBox.get(1.0, "end-1c")

    if len(inp) < 50:
        outputBox.delete(1.0, END)
        outputBox.insert(INSERT, "Please enter more text")
        submitButton.config(bg="white", state="active", text="Submit")
        return

    # Creates the prompt for GPT-3
    prompt = ""
    if sumType.get() == 1:
        prompt = "Summarize the following with bullet points:\n\n" + inp
    if sumType.get() == 2:
        prompt = "Summarize the following in a paragraph:\n\n" + inp

    # The API request to generate the response
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
    except openai.error.AuthenticationError:
        outputBox.delete(1.0, END)
        outputBox.insert(INSERT, "Issue authenticating with OpenAI. Do you have a valid API key?")
        submitButton.config(bg="white", state="active", text="Submit")
        return

    # Gets the text from the response
    recData = response['choices'][0]['text']

    # Deletes whitespace in the beginning of the text
    while recData.find("\n", 0) == 0:
        index = recData.find("\n", 0)
        recData = list(recData)
        recData.remove("\n")
        recData = ''.join(recData)

    # Adds space between each line for readability
    index = 0
    while True:
        index = recData.find("\n", index)
        if index == -1:
            break
        recData = list(recData)
        recData.insert(index, "\n")
        recData = ''.join(recData)
        index = index + 2

    # Changes the submit button back to its original state
    submitButton.config(bg="white", state="active", text="Submit")

    # Shows the text
    outputBox.delete(1.0, END)
    outputBox.insert(INSERT, recData)


# Creates title
title = tk.Label(frame, text="Summarizer")
title.config(font=('Helvatical bold',30))
title.grid(row=1, column=0)

# Creates subtitle
subtitle = tk.Label(frame, text="Input text below:")
subtitle.config(font=('Helvatical bold',15))
subtitle.grid(row=2, column=0)

# Creates the textbox
inputBox = tk.Text(frame, height=20, width=80)
inputBox.grid(row=3, column=0)

# Creates a label for summarizer type
typeLabel = tk.Label(frame, text="Choose summarizer type:")
typeLabel.grid(row=4, column=0)

# Creates radio buttons for summarizer selection
tk.Radiobutton(frame, text="Bullet Points",padx = 20, variable=sumType, value=1).grid(row=5, column=0)
tk.Radiobutton(frame, text="Paragraph    ",padx = 20, variable=sumType, value=2).grid(row=6, column=0)

# Creates submit button
submitButton = tk.Button(frame, text="Submit", command=apiResponseThread)
submitButton.grid(row=7, column=0)

# Creates the display box for the summarized content (blank for now, it changes after it is submitted)
outputBox = tk.Text(frame, height=20, width=80)
outputBox.insert(INSERT, "")
outputBox.grid(row=8, column=0)

# Adds a scrollbar to the input and output boxes, along with the window
scrollbarOutput = tk.Scrollbar(frame, orient='vertical', command=outputBox.yview)
scrollbarOutput.grid(row=8, column=1, sticky=tk.NS)
outputBox['yscrollcommand'] = scrollbarOutput.set
scrollbarInput = tk.Scrollbar(frame, orient='vertical', command=inputBox.yview)
scrollbarInput.grid(row=3, column=1, sticky=tk.NS)
inputBox['yscrollcommand'] = scrollbarInput.set

# Starts the window
frame.mainloop()
