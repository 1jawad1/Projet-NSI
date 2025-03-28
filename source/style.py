from tkinter import ttk

def apply_theme(style, theme_name="light"):
    """
    Applique le style sélectionné.
    :param style: L'objet ttk.Style()
    :param theme_name: Nom du thème ("light", "dark", "colorful")
    """
    if theme_name == "light":
        style.configure("TFrame", background="white", borderwidth=0, relief="flat")
        style.configure("TLabel", font=("Arial", 12), background="#7f8c8d", foreground="black")
        style.configure("Title.TLabel", font=("Arial", 16, "bold"), background="white", foreground="#333")
        style.configure("Subtitle.TLabel", font=("Arial", 14, "italic"), background="white", foreground="#666")
        style.configure("Content.TLabel", font=("Arial", 12), background="white", foreground="#444")

        style.configure("TButton", font=("Arial", 12), padding=3, background="white", foreground="black")
        style.map("TButton", background=[("active", "#e0e0e0")], foreground=[("active", "black")])

        style.configure("TEntry", font=("Arial", 12), padding=5, fieldbackground="white", foreground="black")
        style.configure("TComboBox", font=("Arial", 12), fieldbackground="white", foreground="black")
        style.configure("TSpinbox", font=("Arial", 12), fieldbackground="white", foreground="black")
        style.configure("TScale", font=("Arial", 12), sliderlength=20, background="white", troughcolor="#d3d3d3")

        style.configure("TNotebook", background="white")
        style.configure("TNotebook.Tab", font=("Arial", 12), background="white")
        style.map("TNotebook.Tab", background=[("selected", "#ddd")])

        style.configure("TLabelframe", background="#7f8c8d", font=("Arial", 12, "bold"), borderwidth=0, relief="flat")
        style.configure("TLabelframe.Label", background="#7f8c8d", font=("Arial", 12, "bold"), foreground="#333")

    elif theme_name == "dark":
        style.configure("TFrame", background="#2C2F33", borderwidth=0, relief="flat")
        style.configure("TLabel", font=("Arial", 12), background="#7f8c8d", foreground="#f0f3f4")
        style.configure("Title.TLabel", font=("Arial", 16, "bold"), background="#2C2F33", foreground="#f0f3f4")
        style.configure("Subtitle.TLabel", font=("Arial", 14, "italic"), background="#2C2F33", foreground="#f0f3f4")
        style.configure("Content.TLabel", font=("Arial", 12), background="#2C2F33", foreground="#f0f3f4")

        style.configure("TButton", font=("Arial", 12), padding=3, background="#424949", foreground="black")
        style.map("TButton", background=[("active", "#99AAB5")], foreground=[("active", "black")])

        style.configure("TEntry", font=("Arial", 12), padding=5, fieldbackground="#2C2F33", foreground="#1c2833")
        style.configure("TComboBox", font=("Arial", 12), fieldbackground="#2C2F33", foreground="#1c2833")
        style.configure("TSpinbox", font=("Arial", 12), fieldbackground="#2C2F33", foreground="#1c2833")
        style.configure("TScale", font=("Arial", 12), sliderlength=20, background="#2C2F33", troughcolor="#404040")

        style.configure("TNotebook", background="#424949")
        style.configure("TNotebook.Tab", font=("Arial", 10), background="#a6acaf", foreground="#000000")
        style.map("TNotebook.Tab", background=[("selected", "#616a6b")])

        style.configure("TLabelframe", background="#7f8c8d", font=("Arial", 12, "bold"), foreground="#f0f3f4", borderwidth=0, relief="flat")
        style.configure("TLabelframe.Label", background="#7f8c8d", font=("Arial", 12, "bold"), foreground="#f0f3f4")


    else:
        raise ValueError(f"Thème inconnu : {theme_name}")
