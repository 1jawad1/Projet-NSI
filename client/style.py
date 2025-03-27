from tkinter import ttk

def apply_theme(style, theme_name="light"):
    """
    Applique le style sélectionné.
    :param style: L'objet ttk.Style()
    :param theme_name: Nom du thème ("light", "dark", "colorful")
    """

    if theme_name == "light":
        style.configure("TFrame", background="white")
        style.configure("TLabel", font=("Arial", 12), background="white", foreground="black")
        style.configure("Title.TLabel", font=("Arial", 16, "bold"), background="white", foreground="#333")
        style.configure("Subtitle.TLabel", font=("Arial", 14, "italic"), background="white", foreground="#666")
        style.configure("Content.TLabel", font=("Arial", 12), background="white", foreground="#444")

        style.configure("TButton", font=("Arial", 12), padding=10, background="white", foreground="black")
        style.map("TButton", background=[("active", "#e0e0e0")], foreground=[("active", "black")])

        style.configure("TEntry", font=("Arial", 12), padding=5, fieldbackground="white", foreground="black")
        style.configure("TComboBox", font=("Arial", 12), fieldbackground="white", foreground="black")
        style.configure("TSpinbox", font=("Arial", 12), fieldbackground="white", foreground="black")
        style.configure("TScale", font=("Arial", 12), sliderlength=20, background="white", troughcolor="#d3d3d3")

        style.configure("TNotebook", background="white")
        style.configure("TNotebook.Tab", font=("Arial", 12), background="white")
        style.map("TNotebook.Tab", background=[("selected", "#ddd")])

        style.configure("TLabelframe", background="white", font=("Arial", 12, "bold"))
        style.configure("TLabelframe.Label", background="white", font=("Arial", 12, "bold"), foreground="#333")

    elif theme_name == "dark":
        style.configure("TFrame", background="#2C2F33")
        style.configure("TLabel", font=("Arial", 12), background="#2C2F33", foreground="#a0a0a0")
        style.configure("Title.TLabel", font=("Arial", 16, "bold"), background="#2C2F33", foreground="#f5f5f5")
        style.configure("Subtitle.TLabel", font=("Arial", 14, "italic"), background="#2C2F33", foreground="#c5c5c5")
        style.configure("Content.TLabel", font=("Arial", 12), background="#2C2F33", foreground="#a0a0a0")

        style.configure("TButton", font=("Arial", 12), padding=10, background="#23272A", foreground="#a0a0a0")
        style.map("TButton", background=[("active", "#99AAB5")], foreground=[("active", "black")])

        style.configure("TEntry", font=("Arial", 12), padding=5, fieldbackground="#2C2F33", foreground="#a0a0a0")
        style.configure("TComboBox", font=("Arial", 12), fieldbackground="#2C2F33", foreground="#a0a0a0")
        style.configure("TSpinbox", font=("Arial", 12), fieldbackground="#2C2F33", foreground="#a0a0a0")
        style.configure("TScale", font=("Arial", 12), sliderlength=20, background="#2C2F33", troughcolor="#404040")

        style.configure("TNotebook", background="#2C2F33")
        style.configure("TNotebook.Tab", font=("Arial", 12), background="#23272A", foreground="#f5f5f5")
        style.map("TNotebook.Tab", background=[("selected", "#99AAB5")])

        style.configure("TLabelframe", background="#2C2F33", font=("Arial", 12, "bold"), foreground="#f5f5f5")
        style.configure("TLabelframe.Label", background="#2C2F33", font=("Arial", 12, "bold"), foreground="#f5f5f5")

    elif theme_name == "colorful":
        style.configure("TFrame", background="#FFEB3B")  # Jaune vif
        style.configure("TLabel", font=("Arial", 12), background="#FFEB3B", foreground="#00796B")
        style.configure("Title.TLabel", font=("Arial", 16, "bold"), background="#FFEB3B", foreground="#E91E63")
        style.configure("Subtitle.TLabel", font=("Arial", 14, "italic"), background="#FFEB3B", foreground="#1976D2")
        style.configure("Content.TLabel", font=("Arial", 12), background="#FFEB3B", foreground="#00796B")

        style.configure("TButton", font=("Arial", 12), padding=10, background="#00796B", foreground="white")
        style.map("TButton", background=[("active", "#004D40")], foreground=[("active", "white")])

        style.configure("TEntry", font=("Arial", 12), padding=5, fieldbackground="#FFEB3B", foreground="black")
        style.configure("TComboBox", font=("Arial", 12), fieldbackground="#FFEB3B", foreground="black")
        style.configure("TSpinbox", font=("Arial", 12), fieldbackground="#FFEB3B", foreground="black")
        style.configure("TScale", font=("Arial", 12), sliderlength=20, background="#FFEB3B", troughcolor="#0288D1")

        style.configure("TNotebook", background="#FFEB3B")
        style.configure("TNotebook.Tab", font=("Arial", 12), background="#1976D2", foreground="white")
        style.map("TNotebook.Tab", background=[("selected", "#E91E63")])

        style.configure("TLabelframe", background="#FFEB3B", font=("Arial", 12, "bold"), foreground="#00796B")
        style.configure("TLabelframe.Label", background="#FFEB3B", font=("Arial", 12, "bold"), foreground="#00796B")

    else:
        raise ValueError(f"Thème inconnu : {theme_name}")
