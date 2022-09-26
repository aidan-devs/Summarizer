import tkinter as tk

# Creates the Window
frame = tk.Tk()
frame.title("Summarizer")
frame.geometry('1280x720')

# This function is called to get the input of the text box
# It currently prints the input under the button, this is where we will eventually call GPT-3
def submitInput():
    inp = inputBox.get(1.0, "end-1c")
    lbl.config(text="Text submitted: " + inp)

# Creates the textbox
inputBox = tk.Text(frame, height=20, width=80)
inputBox.pack()

# Creates submit button
submitButton = tk.Button(frame, text="Submit", command=submitInput)
submitButton.pack()

# Creates the label (blank for now, it changes after it is submitted)
lbl = tk.Label(frame, text="")
lbl.pack()

# Starts the window
frame.mainloop()