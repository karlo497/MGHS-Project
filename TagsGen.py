import tkinter as tk
from tkinter import messagebox
import random
import os
from pytrends.request import TrendReq

def generate_tags():
    pytrends = TrendReq(hl='en-US', tz=360)

    topics = topics_entry.get().split(',')
    keywords = keywords_entry.get().split(',')
    for i, v in enumerate(keywords):
        keywords[i] = v.strip()
    for i, v in enumerate(topics):
        topics[i] = v.strip()

    if remove_duplicate_tags_var.get() == 1:
        remove_duplicate_tags = True
    else:
        remove_duplicate_tags = False

    generated = []
    for i in range(int(generate_amount_entry.get())):
        if tag_type_var.get() == 1:
            generated.append(generate_hashtag(topics, keywords))
        else:
            generated.append(generate_tag(topics, keywords))

    if remove_duplicate_tags:
        generated = list(set(generated))

    if tag_type_var.get() == 1:
        generated = [v.replace(" ", "") for v in generated]

    output = '\n'.join(generated)

    if output_form_var.get() == 'txt':
        file_path = os.path.join(os.getcwd(), "generated_tags.txt")
        with open(file_path, 'w') as f:
            f.write(output)
        messagebox.showinfo("File Generated", f"File generated with name 'generated_tags.txt' in {os.getcwd()}")
    elif output_form_var.get() == 'printlist':
        result_text.config(state=tk.NORMAL)
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, output)
        result_text.config(state=tk.DISABLED)
    else:
        messagebox.showinfo("Generated Tags", output)

def generate_tag(topics, keywords):
    topic = random.choice(topics)
    keyword = random.choice(keywords)
    return f"{topic} {keyword}"

def generate_hashtag(topics, keywords):
    topic = random.choice(topics)
    keyword = random.choice(keywords)
    return f"#{topic}{keyword}"

def get_trending_topics():
    pytrends = TrendReq(hl='en-US', tz=360)
    trending = pytrends.trending_searches(pn='united_states')
    return trending

root = tk.Tk()
root.title("YouTube Tag Generator")
for i in range(3):
    root.columnconfigure(i, weight=1, minsize=75)
    root.rowconfigure(i, weight=1, minsize=50)

tag_type_var = tk.IntVar()
tk.Label(root, text="Type:").grid(row=0, column=0)
tk.Radiobutton(root, text="Tags", variable=tag_type_var, value=0).grid(row=0, column=1)
tk.Radiobutton(root, text="Hashtags", variable=tag_type_var, value=1).grid(row=0, column=2)

topics_label = tk.Label(root, text="Enter video topics (separate with commas):")
topics_label.grid(row=1, column=0, padx=5, pady=5)
topics_entry = tk.Entry(root)
topics_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

keywords_label = tk.Label(root, text="Enter keywords (separate with commas):")
keywords_label.grid(row=2, column=0, padx=5, pady=5)
keywords_entry = tk.Entry(root)
keywords_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5)

remove_duplicate_tags_var = tk.IntVar()
tk.Checkbutton(root, text="Remove duplicate tags", variable=remove_duplicate_tags_var).grid(row=3, column=1, columnspan=2, padx=5, pady=5)

generate_amount_label = tk.Label(root, text="Amount to generate:")
generate_amount_label.grid(row=4, column=0, padx=5, pady=5)
generate_amount_entry = tk.Entry(root)
generate_amount_entry.grid(row=4, column=1, columnspan=2, padx=5, pady=5)

output_form_var = tk.StringVar()
output_form_var.set("print")
output_form_label = tk.Label(root, text="Output format:")
output_form_label.grid(row=5, column=0, padx=5, pady=5)
output_form_options = ["txt", "printlist", "print"]
output_form_menu = tk.OptionMenu(root, output_form_var, *output_form_options)
output_form_menu.grid(row=5, column=1, columnspan=2, padx=5, pady=5)

generate_button = tk.Button(root, text="Generate Tags", command=generate_tags)
generate_button.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

result_text = tk.Text(root, height=10, width=50)
result_text.grid(row=7, column=0, columnspan=3, padx=5, pady=5)
result_text.config(state=tk.DISABLED)

#trending_topics = get_trending_topics()
#print(trending_topics)  # You can use this list of trending topics to populate your entry fields or for other purposes

root.mainloop()
