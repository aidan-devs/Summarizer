from tkinter import *
from tkinter import ttk
import tkinter
import sv_ttk
import openai
from threading import *
from bs4 import BeautifulSoup
import requests

"""
READ:
This program was written for a class that required the use of GPT-3. I would rather have trained my own neural network
but OpenAI's GPT-3 works fairly well for this application anyway.

I also wanted to make the program as easy to read as possible, meaning some obvious optimizations (ex. using loops for
radio buttons) have been purposefully avoided

The professor also prefers Java so I used camelCase to be funny.
"""

# PUT YOUR OPEN AI KEY HERE, DELETE BEFORE COMMITTING TO GITHUB
# This will also charge your account, be careful and use test strings if possible
openai.api_key = ""

# Creates the window
window = tkinter.Tk()
window.title("Summarizer")
window.geometry('750x850')
frame = Frame(window)

# Centers all widgets
frame.grid(row=0, column=0, sticky="N")
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# Initializes the style
style = ttk.Style()

# Initializes a variable for summarizer type
sumType = tkinter.IntVar()
sumType.set(1)

# Initializes a variable for input type
inputType = tkinter.IntVar()
inputType.set(1)

# Creates a thread in order to prevent window from freezing while waiting for text to generate
def apiResponseThread():
    # Prevents button from being pressed while loading
    # Also gives a visual indicator for the program loading
    submitButton.config(state="disabled", text="Loading")

    if openai.api_key == "":
        outputBox.delete(1.0, END)
        outputBox.insert(INSERT, "No API key provided. Please exit and provide an API key.")
        return

    # Calls the submitInput() function in a thread
    t1 = Thread(target=submitInput)
    t1.start()


# This function is called to process the input of the text box in the previously mentioned thread
def submitInput():

    inp = inputBox.get(1.0, "end-1c")

    # Returns if the user inputs too little text to summarize
    if len(inp) < 50 and inputType.get() != 2:
        outputBox.delete(1.0, END)
        outputBox.insert(INSERT, "Please enter more text")
        submitButton.config(state="active", text="Submit")
        return

    errorURLSubmit = False
    errorMsg = ''

    # Only runs when the URL option is selected
    if inputType.get() == 2:
        # Header that contains fake user information so request is less likely to be denied
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        # Requests URL data
        try:
            htmlData = requests.get(inp, headers=headers).text
        except requests.exceptions.HTTPError:
            errorURLSubmit = True
            errorMsg = "HTTP Error"
        except requests.exceptions.ConnectionError:
            errorURLSubmit = True
            errorMsg = "Connection Error"
        except requests.exceptions.Timeout:
            errorURLSubmit = True
            errorMsg = "Timeout Error"
        except requests.exceptions.RequestException:
            errorURLSubmit = True
            errorMsg = "An error has occured"

        # If there was an error, it displays the error message and returns
        if errorURLSubmit:
            outputBox.delete(1.0, END)
            outputBox.insert(INSERT, errorMsg)
            submitButton.config(state="active", text="Submit")
            return

        # Parses all <p> from the HTML document (important information is usually contained in paragraphs)
        soupParser = BeautifulSoup(htmlData, 'html.parser')
        data = ''
        inp = ''
        for data in soupParser.find_all("p"):
            inp = inp + data.getText()

    # Creates the prompt for GPT-3
    prompt = ""
    if sumType.get() == 1:
        prompt = "Summarize the following with bullet points:\n\n" + inp
    if sumType.get() == 2:
        prompt = "Summarize the following in a paragraph:\n\n" + inp
    if sumType.get() == 3:
        prompt = inp + "\n\n" + "Answer the following question using the text above: " + questionBox.get()

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
        submitButton.config(state="active", text="Submit")
        return
    except openai.error.InvalidRequestError:
        outputBox.delete(1.0, END)
        outputBox.insert(INSERT, "Too much input data provided. Use smaller text/website.")
        submitButton.config(state="active", text="Submit")
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
    submitButton.config(state="active", text="Submit")

    # Shows the text
    outputBox.delete(1.0, END)
    outputBox.insert(INSERT, recData)


# Adds or removes the question box depending on if it is selected
def outputSelected():

    if sumType.get() == 3:
        questionFrame.grid(row=3, column=0, columnspan=2)
        questionLabel.grid(row=0, column=0)
        questionBox.grid(row=1, column=0, pady=10)
    else:
        questionBox.delete(0, END)
        questionFrame.grid_forget()


# GUI Setup
title = ttk.Label(frame, text="Summarizer")
title.config(font=('Small Fonts',30))
title.grid(row=1, column=0)

frameOptions = Frame(frame)
frameOptions.grid(row=2, column=0)

inputTypeFrame = ttk.LabelFrame(frameOptions, text="Choose input type:", padding=(20, 10))
inputTypeFrame.grid(row=0, column=0, padx=10, pady=10)

ttk.Radiobutton(inputTypeFrame, text="Plain Text", variable=inputType, value=1).pack(anchor=W)
ttk.Radiobutton(inputTypeFrame, text="URL (Beta)", variable=inputType, value=2).pack(anchor=W)

outputTypeFrame = ttk.LabelFrame(frameOptions, text="Choose output type:", padding=(20, 10))
outputTypeFrame.grid(row=0, column=1, padx=10, pady=10)

ttk.Radiobutton(outputTypeFrame, text="Bullet Points", variable=sumType, value=1, command=outputSelected).pack(anchor=W)
ttk.Radiobutton(outputTypeFrame, text="Paragraph", variable=sumType, value=2, command=outputSelected).pack(anchor=W)
ttk.Radiobutton(outputTypeFrame, text="Answer", variable=sumType, value=3, command=outputSelected).pack(anchor=W)

questionFrame = Frame(frameOptions)

questionLabel = tkinter.Label(questionFrame, text="Type question here:")
questionLabel.config(font=('Helvatical bold',10))

questionBox = ttk.Entry(questionFrame)
questionBox.config(width=50)

inputBox = tkinter.Text(frame, height=18, width=80)
inputBox.grid(row=5, column=0)

submitButton = ttk.Button(frame, text="Submit", command=apiResponseThread)
submitButton.grid(row=9, column=0, pady=10)

outputBox = tkinter.Text(frame, height=18, width=80)
outputBox.insert(INSERT, "")
outputBox.grid(row=10, column=0)

scrollbarOutput = ttk.Scrollbar(frame, orient='vertical', command=outputBox.yview)
scrollbarOutput.grid(row=10, column=1, sticky=tkinter.NS)
outputBox['yscrollcommand'] = scrollbarOutput.set
scrollbarInput = ttk.Scrollbar(frame, orient='vertical', command=inputBox.yview)
scrollbarInput.grid(row=5, column=1, sticky=tkinter.NS)
inputBox['yscrollcommand'] = scrollbarInput.set

# Sets theme
sv_ttk.set_theme("dark")

# Starts the window
window.mainloop()