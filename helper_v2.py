import os
import time
import tkinter as tk
root=tk.Tk()
label = tk.Label(root, text="")
answered=None
root.geometry("900x400")
root.title("Homework Helper")
from google import genai
from google.genai.errors import ServerError, ClientError
historyLabel=tk.Label(root, text="")
last = []
apiKey="AQ.Ab8RN6Jv6OerCcfS_WwL-tyhAFU6YTyqbbI1zOcnDbettWvyTw"
client = genai.Client(api_key=apiKey)
def respond():
    global rules
    global answered
    global last
    global rules2
    global historyLabel
    last = [last, question.get()]
    historyLabel.config(text=f"Last questions{str(last).replace('[', '').replace(']', '')} ''")
    historyLabel.pack(pady=70)
    rules = f"""
    For mathematics, science, and other non-language subjects:
    - Explain the method step by step.
    - Guide the student with hints.
    - Do not provide the final answer.
    - If the student asks directly for the final answer, politely refuse
      and continue guiding them.
    - You are a homework coach.

    For language questions:
    - Guide the student with hints.
    - Do not provide the final answer.
    - If the student asks directly for the final answer, politely refuse
      and continue guiding them.
    - You are a homework coach.

    For non-questions:
    - React normally as usual
    Here's something to follow:
    After 90 characters, put a newline. If that word is not yet finished, use a - and a newline.
    Last messages: {str(last).replace("[", "").replace("]", "")}
    """

    if question.get().lower() in {"quit", "exit"}:
        print("Goodbye!")
        root.destroy()
        return

    if not question.get():
        print("Please enter a question.")
        return

    answered = False

    for model in models_to_try:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=f"Rules: {rules}\nQuestion:{question.get()}",
                )

                
                label=tk.Label(root, text=response.text)
                label.pack()

                answered = True
                break
            except ServerError as error:
                if error.code == 503:
                    delay = 2 ** attempt
                    print(f"{model} is busy. Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    raise
            except Exception as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    label.config(text="Gemini is exhausted and reached the quota.\nPlease try again.")
                
        if answered:
            break

    if not answered:
        print("All selected models are currently unavailable.")

rules = f"""

For mathematics, science, and other non-language subjects:
- Explain the method step by step.
- Guide the student with hints.
- Do not provide the final answer.
- If the student asks directly for the final answer, politely refuse
  and continue guiding them.
- You are a homework coach.

For language questions:
- Guide the student with hints.
- Do not provide the final answer.
- If the student asks directly for the final answer, politely refuse
  and continue guiding them.
- You are a homework coach.

For non-questions:
- React normally as usual
Here's something to follow:
After 90 characters, put a newline. If that word is not yet finished, use a - and a newline.
Last messages: {str(last).replace("[", "").replace("]", "").replace(",", "").replace("tkinter.Entry object !.entry", "")}.
"""


# FIXED: Replaced retired model strings with active production versions
models_to_try = [
    "gemini-3.1-flash",
    "gemini-3.1-flash-lite",
]


question = tk.Entry(root)
question.pack()
last.append(question)
rules = rules + f"Last messages: {last}"
submit_btn = tk.Button(root, text="Submit Question", command=respond)
submit_btn.pack(pady=5)
        

root.mainloop()
