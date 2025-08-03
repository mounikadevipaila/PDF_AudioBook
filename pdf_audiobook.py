import pyttsx3
import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading

# === Init === #
engine = pyttsx3.init()
extracted_text = ""
is_reading = False
last_position = 0

def threaded_read(start_pos=0):
    global is_reading, last_position
    is_reading = True
    text_to_read = extracted_text[start_pos:]
    engine.say(text_to_read)
    engine.runAndWait()
    is_reading = False
    last_position = start_pos + len(text_to_read)

def read_pdf():
    global extracted_text, is_reading, last_position
    filepath = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if not filepath:
        return

    try:
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            extracted_text = ""

            for page in reader.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"

        if not extracted_text.strip():
            messagebox.showwarning("No Text Found", "This PDF has no readable text.")
            return

        # Show in textbox
        text_box.config(state=tk.NORMAL)
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, extracted_text)
        text_box.config(state=tk.DISABLED)

        # Reset position & start reading
        last_position = 0
        threading.Thread(target=threaded_read, args=(0,), daemon=True).start()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to read PDF: {e}")

def stop_reading():
    global is_reading
    if is_reading:
        engine.stop()
        is_reading = False
        messagebox.showinfo("Stopped", "Reading stopped.")

def continue_reading():
    global is_reading, last_position
    if not extracted_text.strip():
        messagebox.showwarning("No PDF", "Please open a PDF first.")
        return
    if is_reading:
        messagebox.showinfo("Already Reading", "Text is already being read.")
        return

    threading.Thread(target=threaded_read, args=(last_position,), daemon=True).start()

# === GUI === #
root = tk.Tk()
root.title("📖 PDF Audiobook Converter")
root.geometry("700x600")
root.config(bg="#121212")

title_label = tk.Label(root, text="PDF Audiobook Generator", font=("Helvetica", 20, "bold"),
                       fg="#00FFC6", bg="#121212")
title_label.pack(pady=20)

btn_frame = tk.Frame(root, bg="#121212")
btn_frame.pack(pady=10)

read_btn = tk.Button(btn_frame, text="📂 Open PDF & Read", command=read_pdf,
                     font=("Arial", 12), bg="#1DB954", fg="white", padx=15, pady=6)
read_btn.grid(row=0, column=0, padx=10)

stop_btn = tk.Button(btn_frame, text="🛑 Stop Reading", command=stop_reading,
                     font=("Arial", 12), bg="#EF4444", fg="white", padx=15, pady=6)
stop_btn.grid(row=0, column=1, padx=10)

continue_btn = tk.Button(btn_frame, text="▶️ Continue Reading", command=continue_reading,
                         font=("Arial", 12), bg="#3B82F6", fg="white", padx=15, pady=6)
continue_btn.grid(row=0, column=2, padx=10)

text_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas", 12),
                                     bg="#1E1E1E", fg="#EEEEEE", insertbackground="white")
text_box.config(state=tk.DISABLED)
text_box.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

footer = tk.Label(root, text="Built with 💙 by Mounika", font=("Arial", 10),
                  bg="#121212", fg="#888888")
footer.pack(pady=10)

root.mainloop()
