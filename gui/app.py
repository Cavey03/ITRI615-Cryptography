import os
from tkinter import filedialog, messagebox

import customtkinter as ctk

from ciphers import substitution, vigenere, transposition, vernam
from utils.file_handler import read_bytes, write_text, suggest_output_path

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

CIPHERS = {
    "Substitution": substitution,
    "Vigenère": vigenere,
    "Transposition": transposition,
    "Vernam": vernam,
}


class CipherTab(ctk.CTkFrame):
    def __init__(self, parent, cipher_module, **kwargs):
        super().__init__(parent, **kwargs)
        self.cipher = cipher_module
        self.input_file_path = None
        self._full_output = ""
        self._last_mode = "encrypt"
        self._build()

    def _build(self):
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(1, weight=1)

        # ── Top bar: mode toggle + key ────────────────────────────────────────
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(16, 8))

        ctk.CTkLabel(top, text="Mode:", font=ctk.CTkFont(size=13)).pack(side="left", padx=(0, 6))
        self.mode_var = ctk.StringVar(value="Text")
        ctk.CTkSegmentedButton(
            top, values=["Text", "File"],
            variable=self.mode_var, command=self._toggle_mode, width=160
        ).pack(side="left")

        ctk.CTkLabel(top, text="Key:", font=ctk.CTkFont(size=13)).pack(side="left", padx=(28, 6))
        self.key_entry = ctk.CTkEntry(top, placeholder_text="Enter cipher key…", width=280)
        self.key_entry.pack(side="left")

        # ── Input column ──────────────────────────────────────────────────────
        in_col = ctk.CTkFrame(self, fg_color="transparent")
        in_col.grid(row=1, column=0, sticky="nsew", padx=(20, 8), pady=8)
        in_col.grid_rowconfigure(1, weight=1)
        in_col.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            in_col, text="Input", font=ctk.CTkFont(size=13, weight="bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 6))

        self.input_box = ctk.CTkTextbox(in_col, font=ctk.CTkFont(size=13), wrap="word")
        self.input_box.grid(row=1, column=0, sticky="nsew")

        # File picker panel (hidden until File mode selected)
        self.file_frame = ctk.CTkFrame(in_col, corner_radius=10)
        ctk.CTkLabel(
            self.file_frame, text="Select an input file",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(36, 6))
        self.file_label = ctk.CTkLabel(
            self.file_frame, text="No file chosen",
            font=ctk.CTkFont(size=12), text_color="gray", wraplength=320
        )
        self.file_label.pack(padx=16, pady=(0, 14))
        ctk.CTkButton(
            self.file_frame, text="Browse…", width=150, command=self._browse
        ).pack()

        # ── Output column ─────────────────────────────────────────────────────
        out_col = ctk.CTkFrame(self, fg_color="transparent")
        out_col.grid(row=1, column=1, sticky="nsew", padx=(8, 20), pady=8)
        out_col.grid_rowconfigure(1, weight=1)
        out_col.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            out_col, text="Output", font=ctk.CTkFont(size=13, weight="bold")
        ).grid(row=0, column=0, sticky="w", pady=(0, 6))
        self.output_box = ctk.CTkTextbox(
            out_col, font=ctk.CTkFont(size=13), wrap="word", state="disabled"
        )
        self.output_box.grid(row=1, column=0, sticky="nsew")

        # ── Button bar ────────────────────────────────────────────────────────
        btns = ctk.CTkFrame(self, fg_color="transparent")
        btns.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=(4, 18))

        ctk.CTkButton(btns, text="Encrypt", width=130, command=self._encrypt).pack(side="left", padx=(0, 8))
        ctk.CTkButton(
            btns, text="Decrypt", width=130,
            fg_color=("gray70", "gray30"), hover_color=("gray60", "gray40"),
            text_color=("gray10", "white"), command=self._decrypt
        ).pack(side="left")

        ctk.CTkButton(
            btns, text="Save", width=110,
            fg_color="#2a5c24", hover_color="#376b2f", command=self._save
        ).pack(side="right", padx=(8, 0))
        ctk.CTkButton(btns, text="Copy", width=110, command=self._copy).pack(side="right")

    # ── Mode toggle ───────────────────────────────────────────────────────────

    def _toggle_mode(self, value):
        if value == "File":
            self.input_box.grid_remove()
            self.file_frame.grid(row=1, column=0, sticky="nsew")
        else:
            self.file_frame.grid_remove()
            self.input_box.grid(row=1, column=0, sticky="nsew")

    def _browse(self):
        path = filedialog.askopenfilename()
        if path:
            self.input_file_path = path
            self.file_label.configure(text=os.path.basename(path), text_color="white")

    # ── Output helpers ────────────────────────────────────────────────────────

    def _set_output(self, text):
        self.output_box.configure(state="normal")
        self.output_box.delete("1.0", "end")
        self.output_box.insert("1.0", text)
        self.output_box.configure(state="disabled")

    def _get_output(self):
        self.output_box.configure(state="normal")
        text = self.output_box.get("1.0", "end-1c")
        self.output_box.configure(state="disabled")
        return text

    # ── Cipher operations ─────────────────────────────────────────────────────

    def _run(self, mode):
        key = self.key_entry.get().strip()
        if not key:
            messagebox.showwarning("No Key", "Please enter a cipher key.")
            return
        try:
            fn = self.cipher.encrypt if mode == "encrypt" else self.cipher.decrypt
            self._last_mode = mode

            if self.mode_var.get() == "Text":
                text = self.input_box.get("1.0", "end-1c")
                if not text.strip():
                    messagebox.showwarning("No Input", "Please enter some text.")
                    return
                self._full_output = fn(text, key)
                self._set_output(self._full_output)

            else:
                if not self.input_file_path:
                    messagebox.showwarning("No File", "Please select a file first.")
                    return
                raw = read_bytes(self.input_file_path)
                text = raw.decode("utf-8", errors="replace")
                self._full_output = fn(text, key)

                # Show a preview only — dumping megabytes into the textbox freezes the UI
                preview_limit = 500
                preview = self._full_output[:preview_limit]
                suffix = "..." if len(self._full_output) > preview_limit else ""
                size_kb = len(self._full_output) / 1024
                self._set_output(
                    f"[File {mode}ed — {size_kb:.1f} KB total]\n"
                    f"Use Save to write the full output to disk.\n\n"
                    f"Preview:\n{preview}{suffix}"
                )

        except NotImplementedError as e:
            messagebox.showinfo("Not Implemented Yet", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _encrypt(self): self._run("encrypt")
    def _decrypt(self): self._run("decrypt")

    # ── Output actions ────────────────────────────────────────────────────────

    def _copy(self):
        if not self._full_output:
            messagebox.showwarning("Nothing to Copy", "Output is empty.")
            return
        self.clipboard_clear()
        self.clipboard_append(self._full_output)
        messagebox.showinfo("Copied", "Output copied to clipboard.")

    def _save(self):
        if not self._full_output:
            messagebox.showwarning("Nothing to Save", "Output is empty.")
            return

        if self._last_mode == "encrypt":
            # Encrypted output is always hex text — force .txt
            base = os.path.splitext(self.input_file_path)[0] if self.input_file_path else "output"
            initial = os.path.basename(base) + "_encrypted.txt"
            default_ext = ".txt"
            filetypes = [("Text files", "*.txt"), ("All files", "*.*")]
        else:
            # Decrypted output — restore the original file type
            # Strip _encrypted suffix and recover original extension if possible
            base = os.path.splitext(self.input_file_path)[0] if self.input_file_path else "output"
            base = base.replace("_encrypted", "")
            orig_ext = os.path.splitext(self.input_file_path)[1] if self.input_file_path else ".txt"
            if orig_ext.lower() == ".txt":
                orig_ext = ".txt"
            initial = os.path.basename(base) + "_decrypted" + orig_ext
            default_ext = orig_ext
            filetypes = [("All files", "*.*"), ("Text files", "*.txt")]

        path = filedialog.asksaveasfilename(
            initialfile=initial,
            defaultextension=default_ext,
            filetypes=filetypes,
        )
        if path:
            write_text(path, self._full_output)
            messagebox.showinfo("Saved", f"Saved to {os.path.basename(path)}")


class CryptoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ITRI615 — Classical Cryptography")
        self.geometry("1100x750")
        self.minsize(900, 600)
        self._build()

    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Header bar
        header = ctk.CTkFrame(self, corner_radius=0, fg_color=("gray85", "gray17"))
        header.grid(row=0, column=0, sticky="ew")
        ctk.CTkLabel(
            header,
            text="  Classical Cryptography Tool",
            font=ctk.CTkFont(size=22, weight="bold"),
            anchor="w",
        ).pack(side="left", padx=16, pady=14)
        ctk.CTkLabel(
            header,
            text="ITRI 615  |  2026",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            anchor="e",
        ).pack(side="right", padx=20)

        # Tab view — one tab per cipher
        tabs = ctk.CTkTabview(self, anchor="nw")
        tabs.grid(row=1, column=0, sticky="nsew", padx=16, pady=(8, 16))

        for name, module in CIPHERS.items():
            tabs.add(name)
            CipherTab(tabs.tab(name), module, fg_color="transparent").pack(fill="both", expand=True)
