import tkinter as tk
import openai
from threading import *

# PUT YOUR OPEN AI KEY HERE, DELETE BEFORE COMMITTING TO GITHUB
# This will also charge your account, be careful and use test strings if possible
openai.api_key = ""

# Creates the window
frame = tk.Tk()
frame.title("Summarizer")
frame.geometry('1280x720')


# Creates a thread in order to prevent window from freezing while waiting for text to generate
def apiResponseThread():
    # Prevents button from being pressed while loading
    # Also gives a visual indicator for the program loading
    submitButton.config(bg="#DBDBDB", state="disabled", text="Loading")

    # Calls the submitInput() function in a thread
    t1 = Thread(target=submitInput)
    t1.start()


# This function is called to process the input of the text box in the previously mentioned thread
def submitInput():
    # Gets the text from the input box
    inp = inputBox.get(1.0, "end-1c")

    # Creates the prompt for GPT-3
    prompt = "Summarize the following with bullet points:\n\n" + inp

    # The API request to generate the response
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    # Gets the text from the response
    recData = response['choices'][0]['text']

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

    # Changes the submit button back to it's original state
    submitButton.config(bg="white", state="active", text="Submit")

    # Shows the text
    lbl.config(text=recData, anchor="w")


# Creates the textbox
inputBox = tk.Text(frame, height=20, width=80)
inputBox.pack()

# Creates submit button
submitButton = tk.Button(frame, text="Submit", command=apiResponseThread)
submitButton.pack()

# Creates the label (blank for now, it changes after it is submitted)
lbl = tk.Label(frame, text="", wraplength=720, anchor="w")
lbl.pack()

# Starts the window
frame.mainloop()
