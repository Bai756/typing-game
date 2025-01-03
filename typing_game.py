import time
import random
import pandas as pd
import tkinter as tk
from tkinter import messagebox

def generate_words(mode):
    words = pd.read_csv("words.csv")
    words = words["Words"].tolist()

    if mode == "10 words":
        words = random.sample(words, 10)
    elif mode == "30 words":
        words = random.sample(words, 30)
    elif mode == "10 seconds":
        words = random.sample(words, 70)
    elif mode == "30 seconds":
        words = random.sample(words, 200)

    for i in range(9, len(words), 10):
        words[i] = words[i] + "\n"

    return words

def start_game(mode):
    start_button.pack_forget()
    results_label.pack_forget()
    display_words.pack(pady=10)
    typing_area.pack(pady=10)

    typing_area.focus_set()
    typing_area.config(state=tk.NORMAL)
    typing_area.delete(1.0, tk.END)

    word_label.config(text="Type the following words:")
    words = generate_words(mode)

    word_count = 0
    def update_words(event):
        typed_text = typing_area.get("1.0", "end-1c").strip()
        typed_words = typed_text.split()
        displayed_words = display_words.get("1.0", "end-1c").strip().split()

        display_words.config(state=tk.NORMAL)
        display_words.delete("1.0", tk.END)

        for i, word in enumerate(displayed_words):
            if i < len(typed_words):
                for j in range(len(word)):
                    if j < len(typed_words[i]):
                        if typed_words[i][j] == word[j]:
                            display_words.insert(tk.END, word[j], "correct")
                        else:
                            display_words.insert(tk.END, word[j], "incorrect")
                    else:
                        display_words.insert(tk.END, word[j], "neutral")
                display_words.insert(tk.END, " ")
            else:
                display_words.insert(tk.END, word + " ", "neutral")
            if i % 10 == 9:
                display_words.insert(tk.END, "\n")

        display_words.config(state=tk.DISABLED)

    def type_word(event):
        nonlocal word_count
        word_count += 1

        if (word_count) % 10 == 0:
            display_words.config(state=tk.NORMAL)
            display_words.delete("1.0", tk.END)
            display_words.insert(tk.END, " ".join(words[word_count:word_count + 20]))
            display_words.config(state=tk.DISABLED)


    if mode == "10 words" or mode == "30 words":
        start_time = time.time()

        display_words.config(state=tk.NORMAL)
        display_words.delete("1.0", tk.END)
        display_words.insert(tk.END, " ".join(words[:20]))
        display_words.config(state=tk.DISABLED)

        typing_area.bind("<KeyRelease>", update_words)
        typing_area.bind("<space>", type_word)
        typing_area.bind("<Return>", lambda event: check_typing(words, start_time, mode))

    elif mode == "10 seconds" or mode == "30 seconds":
        start_time = time.time()

        display_words.config(state=tk.NORMAL)
        display_words.delete("1.0", tk.END)
        display_words.insert(tk.END, " ".join(words[:20]))
        display_words.config(state=tk.DISABLED)


        typing_area.bind("<KeyRelease>", update_words)
        typing_area.bind("<space>", type_word)
        
        window.after(int(mode.split()[0]) * 1000, lambda: check_typing(words, start_time, mode)) # ends after 10 or 30 seconds

def check_typing(words, start_time, mode):
    typed_words = typing_area.get("1.0", "end-1c")

    end_time = time.time()

    typing_area.config(state=tk.DISABLED)
    typing_area.unbind("<Return>")
    typing_area.unbind("<Space>")
    typing_area.unbind("<KeyRelease>")
    display_words.pack_forget()
    typing_area.pack_forget()

    time_taken = end_time - start_time

    original_words = words
    typed_words_list = typed_words.split()

    if mode == "10 words" or mode == "30 words":
        error = 0
        for i in range(len(original_words)):
            if i + 1 > len(typed_words_list):
                error += len(original_words[i])
            else:
                for j in range(len(original_words[i])):
                    if j + 1 > len(typed_words_list[i]):
                        error += 1
                    elif original_words[i][j] != typed_words_list[i][j]:
                        error += 1
        
        num_characters = 0
        for i in range(len(original_words)):
            for j in range(len(original_words[i])):
                num_characters += 1
    
    elif mode == "10 seconds" or mode == "30 seconds":
        error = 0
        for i in range(len(typed_words_list)):
            if i + 1 > len(original_words):
                error += len(typed_words_list[i])
            else:
                for j in range(len(typed_words_list[i])):
                    if j + 1 > len(original_words[i]):
                        error += 1
                    elif typed_words_list[i][j] != original_words[i][j]:
                        error += 1
        
        num_characters = 0
        for i in range(len(typed_words_list)):
            for j in range(len(typed_words_list[i])):
                num_characters += 1
    
    if num_characters == 0:
        accuracy = 0
    else:
        accuracy = (num_characters - error) / num_characters * 100

    wpm = len(typed_words_list) / (time_taken / 60)

    window.update()

    results_label.config(text=f"Your WPM is {wpm:.1f}.\nYour accuracy was {accuracy:.1f}%.")
    results_label.pack(pady=10)
    start_button.pack(pady=20)


window = tk.Tk()
window.title("Typing Speed Game")

w = 800
h = 500
ws = window.winfo_screenwidth()
hs = window.winfo_screenheight() 
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
window.geometry("%dx%d+%d+%d" % (w, h, x, y))
window.lift()
window.focus_force()

welcome_label = tk.Label(window, text="Welcome to the Typing Speed Game!", font=("Helvetica", 20))
welcome_label.pack(pady=20)

mode_var = tk.StringVar(window)
mode_var.set("Choose Game Mode")
mode_menu = tk.OptionMenu(window, mode_var, "10 words", "30 words", "10 seconds", "30 seconds")
mode_menu.pack(pady=10)

word_label = tk.Label(window, text="", font=("Helvetica", 18))
word_label.pack(pady=10)

display_words = tk.Text(window, font=("Helvetica", 14), height=5, width=60, wrap="word")
display_words.pack(pady=10)
display_words.config(state=tk.DISABLED)

display_words.tag_configure("correct", foreground="green")
display_words.tag_configure("incorrect", foreground="red")
display_words.tag_configure("neutral", foreground="white")
display_words.pack_forget()

typing_area = tk.Text(window, font=("Helvetica", 14), height=5, width=50, wrap="word")

def on_start_button_click():
    mode = mode_var.get()
    if mode == "Choose Game Mode":
        messagebox.showwarning("Selection Error", "Please select a game mode!")
        return
    start_game(mode)

start_button = tk.Button(window, text="Start Game", font=("Helvetica", 18), command=on_start_button_click)
start_button.pack(pady=20)

results_label = tk.Label(window, text="", font=("Helvetica", 16), wraplength=600)
results_label.pack(pady=10)

window.mainloop()
