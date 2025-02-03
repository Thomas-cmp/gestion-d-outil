
import tkinter as tk
from tkinter import messagebox
import sqlite3
# Page d'affectation d'un outil
from tkinter import ttk, messagebox
import win32com.client as win32  # Pour envoyer des emails via Outlook
from PIL import Image, ImageTk



# Connexion à la base de données
def connect_db():
    return sqlite3.connect("gestion_outils.db")

# Page de connexion

class PageConnexion(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Page de Connexion")
        
        # Couleurs et polices
        self.bg_color = "#AEC6CF"
        self.button_color = "#4CAF50"
        self.font_title = ('Arial', 24, 'bold')
        self.font_label = ('Arial', 14)
        self.font_entry = ('Arial', 12)

        # Application du fond
        self.configure(bg=self.bg_color)

        # Chargement et affichage de l'image
        try:
            image = Image.open("cmp_logo.png")  # Remplacez par le chemin de votre image
            image = image.resize((280, 100), Image.LANCZOS)  # Redimensionnement si nécessaire
            self.photo = ImageTk.PhotoImage(image)

            label_image = tk.Label(self, image=self.photo, bg=self.bg_color)
            label_image.grid(row=0, column=0, columnspan=3, pady=10)
        except Exception as e:
            print(f"Erreur lors du chargement de l'image : {e}")

        # Titre de la page
        title_label = tk.Label(self, text="Connexion Team Leader", font=self.font_title, bg=self.bg_color, fg="white")
        title_label.grid(row=2, column=0, columnspan=3, pady=20)
        
        # Interface de la page de connexion
        label_id = tk.Label(self, text="Scanner badge:", font=self.font_label, bg=self.bg_color, fg="white")
        label_id.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        
        self.entry_id = tk.Entry(self, font=self.font_entry, width=25, show="•")  # Texte masqué par défaut
        self.entry_id.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        
        # Bouton pour afficher/masquer le texte
        self.show_password = False  # État actuel (masqué par défaut)
        self.toggle_button = tk.Button(self, text="Afficher", command=self.toggle_password, bg="#FFC300")
        self.toggle_button.grid(row=3, column=2, padx=5, pady=10)

        # Lier la touche "Entrée" à la méthode `connexion`
        self.entry_id.bind("<Return>", self.handle_enter)

        # Bouton de connexion
        self.bouton_connexion = tk.Button(self, text="Se Connecter", font=self.font_label, command=self.connexion, 
                                          bg=self.button_color, fg="white", width=20, height=2)
        self.bouton_connexion.grid(row=4, column=0, columnspan=3, pady=20)

        # Centrage de la page
        self.pack(expand=True)

    def toggle_password(self):
        """Basculer entre le mode masqué et visible pour le champ de texte."""
        if self.show_password:
            self.entry_id.config(show="•")  # Masquer le texte
            self.toggle_button.config(text="Afficher")
        else:
            self.entry_id.config(show="")  # Afficher le texte
            self.toggle_button.config(text="Masquer")
        self.show_password = not self.show_password

    def handle_enter(self, event):
        """Gérer l'appui sur la touche Entrée."""
        self.connexion()

    def connexion(self):
        id_utilisateur = self.entry_id.get()
        
        # Vérifie si l'utilisateur est un team leader
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM utilisateurs WHERE id = ?", (id_utilisateur,))
        result = cursor.fetchone()
        conn.close()
        
        if result and result[0] == "team_leader":
            messagebox.showinfo("Connexion réussie", "Vous êtes connecté en tant que Team Leader.")
            self.master.show_page(MenuPage)  # Passe à la page suivante
        else:
            messagebox.showerror("Erreur", "ID invalide ou vous n'êtes pas un Team Leader.")


# Page Menu de choix
class MenuPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Menu")
        self.configure(bg="#AEC6CF")

        # Boutons du menu
        bouton_affecter = tk.Button(self, text="Affecter un Outil", font=('Arial', 14), bg="#4CAF50", fg="white", command=self.affecter)
        bouton_affecter.pack(pady=20, ipadx=20, ipady=10)
        
        bouton_retourner = tk.Button(self, text="Retourner un Outil", font=('Arial', 14), bg="#4CAF50", fg="white", command=self.retourner)
        bouton_retourner.pack(pady=20, ipadx=20, ipady=10)

        bouton_gestion = tk.Button(self, text="Gestion des Outils", font=('Arial', 14), bg="#4CAF50", fg="white", command=self.gestion)
        bouton_gestion.pack(pady=20, ipadx=20, ipady=10)

        bouton_gestion_utilisateurs = tk.Button(self, text="Gestion des Utilisateurs", font=('Arial', 14), bg="#4CAF50", fg="white", command=self.gestion_utilisateurs)
        bouton_gestion_utilisateurs.pack(pady=20, ipadx=20, ipady=10)

        # Bouton de déconnexion
        bouton_deconnexion = tk.Button(self, text="Se Déconnecter", font=('Arial', 14), bg="#E74C3C", fg="white", command=self.deconnexion)
        bouton_deconnexion.pack(pady=20, ipadx=20, ipady=10)

        self.pack(expand=True)

    def affecter(self):
        self.master.show_page(AffecterPage)

    def retourner(self):
        self.master.show_page(RetournerPage)

    def gestion(self):
        self.master.show_page(GestionPage)

    def gestion_utilisateurs(self):
        self.master.show_page(GestionUtilisateursPage)

    def deconnexion(self):
        self.master.show_page(PageConnexion)


class AffecterPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Affecter un Outil")

        # Définir les couleurs et les polices
        self.bg_color = "#AEC6CF"
        self.button_color = "#4CAF50"
        self.font_label = ('Arial', 14)
        self.font_button = ('Arial', 12, 'bold')

        # Application du fond
        self.configure(bg=self.bg_color)

        # Titre de la page
        title_label = tk.Label(self, text="Page d'Affectation d'Outil", font=('Arial', 20, 'bold'), bg=self.bg_color, fg="white")
        title_label.grid(row=0, column=0, columnspan=3, pady=20)

        # Interface de saisie pour l'opérateur
        label_nom_operateur = tk.Label(self, text="ID de l'Opérateur :", font=self.font_label, bg=self.bg_color, fg="white")
        label_nom_operateur.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.entree_nom_operateur = tk.Entry(self, font=self.font_label, width=30)
        self.entree_nom_operateur.grid(row=1, column=1, padx=10, pady=10)

        # Liaison de la touche "Entrée" à la recherche
        self.entree_nom_operateur.bind("<Return>", lambda event: self.rechercher_operateur())

        # Bouton rechercher
        self.bouton_rechercher_operateur = tk.Button(
            self, text="Rechercher", font=self.font_button, bg="#2980B9", fg="white", 
            command=self.rechercher_operateur
        )
        self.bouton_rechercher_operateur.grid(row=1, column=2, padx=10, pady=10)

        # Champ pour afficher le résultat de la recherche
        self.label_resultat_recherche = tk.Label(self, text="", font=self.font_label, bg=self.bg_color, fg="white")
        self.label_resultat_recherche.grid(row=2, column=1, padx=10, pady=10)

        # Champ de filtre pour les outils
        label_filtre_outil = tk.Label(self, text="Filtrer les outils :", font=self.font_label, bg=self.bg_color, fg="white")
        label_filtre_outil.grid(row=3, column=0, pady=10, sticky="w")

        self.entree_filtre_outil = tk.Entry(self, font=self.font_label, width=30)
        self.entree_filtre_outil.grid(row=3, column=1, padx=10, pady=10)
        self.entree_filtre_outil.bind("<KeyRelease>", lambda event: self.filtrer_outils())

        # Liste des outils disponibles avec Treeview
        label_select_outil = tk.Label(self, text="Outils Disponibles :", font=self.font_label, bg=self.bg_color, fg="white")
        label_select_outil.grid(row=4, column=0, pady=10)

        self.tree_outils_disponibles = ttk.Treeview(self, columns=("id_outil", "nom_outil"), show="headings", height=6)
        self.tree_outils_disponibles.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        # Configurer les colonnes
        self.tree_outils_disponibles.heading("id_outil", text="ID Outil")
        self.tree_outils_disponibles.heading("nom_outil", text="Nom de l'Outil")
        self.tree_outils_disponibles.column("id_outil", width=100, anchor="center")
        self.tree_outils_disponibles.column("nom_outil", width=200, anchor="center")

        # Bouton d'affectation
        self.bouton_affecter = tk.Button(self, text="Affecter Outil", font=self.font_button, bg=self.button_color, fg="white", command=self.affecter_outil, width=20, height=2)
        self.bouton_affecter.grid(row=6, column=1, pady=20)

        # Liste des outils affectés avec Treeview
        label_outils_affectes = tk.Label(self, text="Outils Affectés :", font=self.font_label, bg=self.bg_color, fg="white")
        label_outils_affectes.grid(row=7, column=0, pady=10)

        self.tree_outils_affectes = ttk.Treeview(self, columns=("id_outil", "nom_outil", "nom_operateur"), show="headings", height=6)
        self.tree_outils_affectes.grid(row=8, column=0, columnspan=3, padx=10, pady=10)

        # Configurer les colonnes
        self.tree_outils_affectes.heading("id_outil", text="ID Outil")
        self.tree_outils_affectes.heading("nom_outil", text="Nom de l'Outil")
        self.tree_outils_affectes.heading("nom_operateur", text="Nom Opérateur")
        self.tree_outils_affectes.column("id_outil", width=100, anchor="center")
        self.tree_outils_affectes.column("nom_outil", width=200, anchor="center")
        self.tree_outils_affectes.column("nom_operateur", width=200, anchor="center")

        # Bouton retour au menu
        self.bouton_retour_menu = tk.Button(self, text="Retour au Menu", font=self.font_button, bg="#f44336", fg="white", command=lambda: self.master.show_page(MenuPage), width=20, height=2)
        self.bouton_retour_menu.grid(row=9, column=1, pady=20)

        # Charger les données initiales
        self.outils_disponibles = []
        self.afficher_outils_disponibles()
        self.afficher_outils_affectes()

    def rechercher_operateur(self):
        """Rechercher l'opérateur par son identifiant et afficher ses informations."""
        nom_operateur = self.entree_nom_operateur.get()

        if not nom_operateur:
            messagebox.showerror("Erreur", "Veuillez entrer l'identifiant ou le nom de l'opérateur.")
            return

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT nom, prenom FROM utilisateurs WHERE id = ? OR nom = ?", (nom_operateur, nom_operateur))
        operateur = cursor.fetchone()
        conn.close()

        if operateur:
            self.label_resultat_recherche.config(text=f"{operateur[0]} {operateur[1]}")
        else:
            self.label_resultat_recherche.config(text="Aucun opérateur trouvé.")

    def afficher_outils_disponibles(self):
        """Afficher les outils disponibles dans le Treeview."""
        for item in self.tree_outils_disponibles.get_children():
            self.tree_outils_disponibles.delete(item)

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id_outil, nom_outil FROM outils WHERE disponible = 1")
        self.outils_disponibles = cursor.fetchall()
        conn.close()

        for outil in self.outils_disponibles:
            self.tree_outils_disponibles.insert("", "end", values=(outil[0], outil[1]))

    def afficher_outils_affectes(self):
        """Afficher les outils affectés dans le Treeview."""
        for item in self.tree_outils_affectes.get_children():
            self.tree_outils_affectes.delete(item)

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT outils.id_outil, outils.nom_outil, affectations.id_utilisateur
            FROM outils
            JOIN affectations ON outils.id_outil = affectations.id_outil
            WHERE affectations.date_retour IS NULL
        """)
        affectations = cursor.fetchall()
        conn.close()

        for affectation in affectations:
            self.tree_outils_affectes.insert("", "end", values=(affectation[0], affectation[1], affectation[2]))

    def filtrer_outils(self):
        """Filtrer la liste des outils disponibles par le nom."""
        filtre = self.entree_filtre_outil.get().lower()
        outils_filtres = [outil for outil in self.outils_disponibles if filtre in outil[1].lower()]

        # Mettre à jour le Treeview
        for item in self.tree_outils_disponibles.get_children():
            self.tree_outils_disponibles.delete(item)

        for outil in outils_filtres:
            self.tree_outils_disponibles.insert("", "end", values=(outil[0], outil[1]))

    def affecter_outil(self):
        """Affecter l'outil sélectionné à un opérateur."""
        selected_item = self.tree_outils_disponibles.selection()
        if not selected_item:
            messagebox.showerror("Erreur", "Veuillez sélectionner un outil.")
            return

        id_outil = self.tree_outils_disponibles.item(selected_item, "values")[0]
        nom_operateur = self.entree_nom_operateur.get()

        if not nom_operateur:
            messagebox.showerror("Erreur", "Le nom de l'opérateur est obligatoire.")
            return

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE outils SET disponible = 0 WHERE id_outil = ?", (id_outil,))
        cursor.execute("INSERT INTO affectations (id_utilisateur, id_outil) VALUES (?, ?)", (nom_operateur, id_outil))
        conn.commit()
        conn.close()

        self.afficher_outils_disponibles()
        self.afficher_outils_affectes()


class RetournerPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Retourner un Outil")
        self.configure(bg="#AEC6CF")

        # Couleurs et polices
        self.button_color = "#4CAF50"
        self.font_label = ('Arial', 14)
        self.font_entry = ('Arial', 12)
        self.bg_color = "#AEC6CF"
        self.font_button = ('Arial', 12, 'bold')

        # Titre de la page
        titre_label = tk.Label(self, text="Retourner un Outil", font=("Arial", 18, "bold"), bg="#AEC6CF")
        titre_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Champ ID de l'Opérateur
        self.label_id_operateur = tk.Label(self, text="ID de l'Opérateur :", font=("Arial", 12), bg="#AEC6CF")
        self.label_id_operateur.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entree_id_operateur = tk.Entry(self, font=("Arial", 12), relief="solid", bd=2, width=30)
        self.entree_id_operateur.grid(row=1, column=1, padx=10, pady=10)

        # Bouton pour rechercher l'utilisateur
        self.bouton_rechercher = tk.Button(self, text="Rechercher l'Utilisateur", font=("Arial", 12, "bold"), bg="#2980B9", fg="white", relief="raised", command=self.rechercher_utilisateur)
        self.bouton_rechercher.grid(row=2, column=0, columnspan=2, pady=10, sticky="nsew")

        # Frame pour afficher les outils de l'utilisateur
        self.frame_outils = tk.Frame(self, bg="#AEC6CF")
        self.frame_outils.grid(row=3, column=0, columnspan=2, pady=20, sticky="nsew")

        # Liste des outils affectés
        label_outils_affectes = tk.Label(self, text="Outils Affectés :", font=self.font_label, bg=self.bg_color, fg="white")
        label_outils_affectes.grid(row=4, column=0, columnspan=2, pady=10)

        self.liste_outils_affectes = tk.Listbox(self, height=6, width=50, font=self.font_entry)
        self.liste_outils_affectes.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        # Bouton retour au menu
        self.bouton_retour_menu = tk.Button(self, text="Retour au Menu", font=self.font_button, bg="#f44336", fg="white", command=lambda: self.master.show_page(MenuPage), width=20, height=2)
        self.bouton_retour_menu.grid(row=8, column=0, columnspan=2, pady=20)

        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        self.pack()

        self.afficher_outils_affectes()

    def afficher_outils_affectes(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(""" 
            SELECT outils.nom_outil, outils.id_outil, affectations.id_utilisateur
            FROM outils 
            JOIN affectations ON outils.id_outil = affectations.id_outil 
            WHERE affectations.date_retour IS NULL
        """)
        affectations = cursor.fetchall()
        conn.close()

        self.liste_outils_affectes.delete(0, tk.END)
        for affectation in affectations:
            self.liste_outils_affectes.insert(tk.END, f"{affectation[0]} (ID: {affectation[1]}) - Opérateur: {affectation[2]}")

    def rechercher_utilisateur(self):
        id_operateur = self.entree_id_operateur.get()

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(""" 
            SELECT outils.id_outil, outils.nom_outil
            FROM outils
            JOIN affectations ON outils.id_outil = affectations.id_outil
            WHERE affectations.id_utilisateur = ? AND affectations.date_retour IS NULL
        """, (id_operateur,))
        outils = cursor.fetchall()
        conn.close()

        if outils:
            self.afficher_outils(outils)
        else:
            messagebox.showerror("Erreur", "Aucun outil trouvé pour cet opérateur ou tous les outils ont déjà été retournés.")

    def afficher_outils(self, outils):
        for widget in self.frame_outils.winfo_children():
            widget.destroy()

        for i, (id_outil, nom_outil) in enumerate(outils):
            bouton_outil = tk.Button(self.frame_outils, text=f"{nom_outil} (ID: {id_outil})", font=("Arial", 12), bg="#2980B9", fg="white", relief="raised", 
                                     command=lambda id_outil=id_outil: self.retourner_outil(id_outil))
            bouton_outil.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            bouton_reparer = tk.Button(self.frame_outils, text="Déclarer à Réparer", font=("Arial", 12), bg="#E67E22", fg="white", relief="raised", 
                                       command=lambda id_outil=id_outil: self.declarer_a_reparer(id_outil))
            bouton_reparer.grid(row=i, column=1, padx=10, pady=5, sticky="w")

    def retourner_outil(self, id_outil):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(""" 
            UPDATE affectations
            SET date_retour = datetime('now') 
            WHERE id_outil = ? AND date_retour IS NULL
        """, (id_outil,))

        cursor.execute(""" 
            UPDATE outils
            SET disponible = 1
            WHERE id_outil = ?
        """, (id_outil,))

        conn.commit()
        conn.close()

        messagebox.showinfo("Succès", f"L'outil (ID: {id_outil}) a été retourné avec succès.")
        self.rechercher_utilisateur()


    def declarer_a_reparer(self, id_outil):
        conn = connect_db()
        cursor = conn.cursor()

        # Mettre à jour l'état de l'outil à "En reparation"
        cursor.execute("""
            UPDATE outils
            SET etat = 'En reparation'
            WHERE id_outil = ?
        """, (id_outil,))

        # Mettre à jour la date de retour dans la table affectations
        cursor.execute("""
            UPDATE affectations
            SET date_retour = datetime('now')
            WHERE id_outil = ? AND date_retour IS NULL
        """, (id_outil,))

        conn.commit()
        conn.close()

        # Afficher un message de succès
        messagebox.showinfo("Succès", f"L'outil (ID: {id_outil}) a été déclaré en réparation, et la liste a été mise à jour.")

        # Rafraîchir les outils affichés dans la liste
        self.rechercher_utilisateur()
        self.afficher_outils_affectes()

        # Envoyer un email à la maintenance pour signaler la déclaration
        self.envoyer_mail_maintenance(id_outil)


    def envoyer_mail_maintenance(self, id_outil):
        conn = connect_db()
        cursor = conn.cursor()

        # Récupérer le nom de l'outil déclaré en réparation
        cursor.execute("SELECT nom_outil FROM outils WHERE id_outil = ?", (id_outil,))
        nom_outil = cursor.fetchone()[0]

        # Récupérer tous les outils actuellement en réparation
        cursor.execute("SELECT id_outil, nom_outil FROM outils WHERE etat = 'En reparation'")
        outils_en_reparation = cursor.fetchall()
        conn.close()

        # Lancer Outlook
        outlook = win32.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0)

        # Sujet de l'email
        mail.Subject = f"Nouvelle déclaration d'outil à réparer : {nom_outil} (ID: {id_outil})"

        # Corps HTML de l'email
        corps_email = f"""
        <p>Bonjour,</p>
        <p>L'outil suivant a été déclaré en réparation :</p>
        <ul>
            <li><b>Nom de l'outil :</b> {nom_outil}</li>
            <li><b>ID de l'outil :</b> {id_outil}</li>
        </ul>
        <p>Voici le tableau récapitulatif de tous les outils actuellement en réparation :</p>
        <table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; width: 100%; font-family: Arial, sans-serif;">
            <thead>
                <tr style="background-color: #f2f2f2; text-align: left;">
                    <th style="padding: 8px;">ID Outil</th>
                    <th style="padding: 8px;">Nom Outil</th>
                </tr>
            </thead>
            <tbody>
        """

        # Ajouter les outils en réparation dans le tableau
        for outil_id, outil_nom in outils_en_reparation:
            corps_email += f"""
            <tr>
                <td style="padding: 8px;">{outil_id}</td>
                <td style="padding: 8px;">{outil_nom}</td>
            </tr>
            """

        corps_email += """
            </tbody>
        </table>
        <p>Cordialement,<br>Service de gestion des outils</p>
        """

        # Ajouter le contenu HTML au corps de l'email
        mail.HTMLBody = corps_email

        # Adresse du destinataire
        mail.To = "tlaguerre@cmp-ams.com"  # Remplacez par l'adresse email réelle de la maintenance

        # Envoyer l'email
        mail.Send()

        # Afficher un message de confirmation
        messagebox.showinfo("Email envoyé", "Un email a été envoyé à la maintenance.")


import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Connexion à la base de données
def connect_db():
    return sqlite3.connect("gestion_outils.db")

class GestionPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Gestion des Outils")
        self.configure(bg="#AEC6CF")

        # Titre de la page
        titre_label = tk.Label(self, text="Gestion des Outils", font=("Arial", 18, "bold"), bg="#AEC6CF", fg="white")
        titre_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Section pour afficher les outils existants
        self.tree_outils = ttk.Treeview(self, columns=("id_outil", "nom_outil", "etat", "disponible", "projet", "station"), show="headings", height=10)
        self.tree_outils.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.tree_outils.heading("id_outil", text="ID Outil")
        self.tree_outils.heading("nom_outil", text="Nom de l'Outil")
        self.tree_outils.heading("etat", text="État")
        self.tree_outils.heading("disponible", text="Disponible")
        self.tree_outils.heading("projet", text="Projet")
        self.tree_outils.heading("station", text="Station")

        self.tree_outils.column("id_outil", width=100, anchor="center")
        self.tree_outils.column("nom_outil", width=200, anchor="w")
        self.tree_outils.column("etat", width=150, anchor="center")
        self.tree_outils.column("disponible", width=100, anchor="center")
        self.tree_outils.column("projet", width=150, anchor="center")
        self.tree_outils.column("station", width=150, anchor="center")

        # Sélection dans la liste
        self.tree_outils.bind("<ButtonRelease-1>", self.selectionner_outil)

        # Section pour ajouter/modifier un outil
        cadre_formulaire = tk.Frame(self, bg="#AEC6CF")
        cadre_formulaire.grid(row=2, column=0, columnspan=2, pady=10)

        # Champ ID Outil
        label_id = tk.Label(cadre_formulaire, text="ID de l'Outil :", font=("Arial", 12), bg="#AEC6CF")
        label_id.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entree_id = tk.Entry(cadre_formulaire, font=("Arial", 12), width=30)
        self.entree_id.grid(row=0, column=1, padx=10, pady=5)

        # Champ Nom Outil
        label_nom = tk.Label(cadre_formulaire, text="Nom de l'Outil :", font=("Arial", 12), bg="#AEC6CF")
        label_nom.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entree_nom = tk.Entry(cadre_formulaire, font=("Arial", 12), width=30)
        self.entree_nom.grid(row=1, column=1, padx=10, pady=5)

        # Champ État Outil
        label_etat = tk.Label(cadre_formulaire, text="État de l'Outil :", font=("Arial", 12), bg="#AEC6CF")
        label_etat.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.entree_etat = ttk.Combobox(cadre_formulaire, values=["Disponible", "En reparation", "Repare"], font=("Arial", 12), width=28)
        self.entree_etat.grid(row=2, column=1, padx=10, pady=5)

        # Champ Projet
        label_projet = tk.Label(cadre_formulaire, text="Projet :", font=("Arial", 12), bg="#AEC6CF")
        label_projet.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.entree_projet = ttk.Combobox(cadre_formulaire, values=self.get_projet(), font=("Arial", 12), width=28)
        self.entree_projet.grid(row=3, column=1, padx=10, pady=5)

        # Champ Station
        label_station = tk.Label(cadre_formulaire, text="Station :", font=("Arial", 12), bg="#AEC6CF")
        label_station.grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.entree_station = tk.Entry(cadre_formulaire, font=("Arial", 12), width=30)
        self.entree_station.grid(row=4, column=1, padx=10, pady=5)

        # Boutons Ajouter/Modifier/Supprimer
        bouton_ajouter = tk.Button(cadre_formulaire, text="Ajouter l'Outil", font=("Arial", 12, "bold"), bg="#27AE60", fg="white", command=self.ajouter_outil)
        bouton_ajouter.grid(row=5, column=0, pady=10)

        bouton_modifier = tk.Button(cadre_formulaire, text="Modifier l'Outil", font=("Arial", 12, "bold"), bg="#2980B9", fg="white", command=self.modifier_outil)
        bouton_modifier.grid(row=5, column=1, pady=10)

        bouton_supprimer = tk.Button(cadre_formulaire, text="Supprimer l'Outil", font=("Arial", 12, "bold"), bg="#C0392B", fg="white", command=self.supprimer_outil)
        bouton_supprimer.grid(row=6, column=0, columnspan=2, pady=10)

        # Bouton retour au menu
        bouton_retour_menu = tk.Button(self, text="Retour au Menu", font=("Arial", 12, "bold"), bg="#C0392B", fg="white", command=lambda: self.master.show_page(MenuPage))
        bouton_retour_menu.grid(row=7, column=0, columnspan=2, pady=20)

        # Charger les outils dès l'ouverture de la page
        self.afficher_outils()
        self.pack()

    def get_projet(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT nom_projet FROM projet")
        projet = [row[0] for row in cursor.fetchall()]
        conn.close()
        return projet

    def selectionner_outil(self, event):
        selected_item = self.tree_outils.selection()
        if selected_item:
            values = self.tree_outils.item(selected_item, "values")
            self.entree_id.delete(0, tk.END)
            self.entree_id.insert(0, values[0])
            self.entree_nom.delete(0, tk.END)
            self.entree_nom.insert(0, values[1])
            self.entree_etat.set(values[2])
            self.entree_projet.set(values[4])
            self.entree_station.delete(0, tk.END)
            self.entree_station.insert(0, values[5])
            self.selected_id = values[0]

    def afficher_outils(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id_outil, nom_outil, etat, disponible, projet, station FROM outils")
        outils = cursor.fetchall()
        conn.close()

        for item in self.tree_outils.get_children():
            self.tree_outils.delete(item)

        for outil in outils:
            self.tree_outils.insert("", "end", values=outil)

    def ajouter_outil(self):
        id_outil = self.entree_id.get().strip()
        nom_outil = self.entree_nom.get().strip()
        etat_outil = self.entree_etat.get().strip()
        projet = self.entree_projet.get().strip() or None
        station = self.entree_station.get().strip() or None

        if not id_outil or not nom_outil or not etat_outil:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs obligatoires.")
            return

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO outils (id_outil, nom_outil, etat, disponible, projet, station) VALUES (?, ?, ?, ?, ?, ?)",
                       (id_outil, nom_outil, etat_outil, 1 if etat_outil == "Disponible" else 0, projet, station))
        conn.commit()
        conn.close()

        self.afficher_outils()

    def modifier_outil(self):
        id_outil = self.selected_id
        nom_outil = self.entree_nom.get().strip()
        etat_outil = self.entree_etat.get().strip()
        projet = self.entree_projet.get().strip() or None
        station = self.entree_station.get().strip() or None

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("UPDATE outils SET nom_outil=?, etat=?, disponible=?, projet=?, station=? WHERE id_outil=?",
                       (nom_outil, etat_outil, 1 if etat_outil == "Disponible" else 0, projet, station, id_outil))
        conn.commit()
        conn.close()

        self.afficher_outils()

    def supprimer_outil(self):
        id_outil = self.selected_id
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM outils WHERE id_outil=?", (id_outil,))
        conn.commit()
        conn.close()

        self.afficher_outils()




class GestionUtilisateursPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("Gestion des Utilisateurs")
        self.configure(bg="#AEC6CF")

        # Titre de la page
        titre_label = tk.Label(self, text="Gestion des Utilisateurs", font=("Arial", 18, "bold"), bg="#AEC6CF", fg="white")
        titre_label.pack(pady=20)

        # Tableau des utilisateurs
        self.tree_utilisateurs = ttk.Treeview(self, columns=("id", "nom", "prenom", "role", "email"), show="headings", height=10)
        self.tree_utilisateurs.pack(pady=10)

        self.tree_utilisateurs.heading("id", text="ID")
        self.tree_utilisateurs.heading("nom", text="Nom")
        self.tree_utilisateurs.heading("prenom", text="Prénom")
        self.tree_utilisateurs.heading("role", text="Rôle")
        self.tree_utilisateurs.heading("email", text="Email")

        self.tree_utilisateurs.column("id", width=50, anchor="center")
        self.tree_utilisateurs.column("nom", width=150, anchor="w")
        self.tree_utilisateurs.column("prenom", width=150, anchor="w")
        self.tree_utilisateurs.column("role", width=100, anchor="center")
        self.tree_utilisateurs.column("email", width=200, anchor="w")

        self.tree_utilisateurs.bind("<<TreeviewSelect>>", self.remplir_champs)

        # Section pour ajouter/modifier un utilisateur
        cadre_formulaire = tk.Frame(self, bg="#AEC6CF")
        cadre_formulaire.pack(pady=20)

        tk.Label(cadre_formulaire, text="ID :", bg="#AEC6CF").grid(row=0, column=0, padx=5, pady=5)
        self.entree_id = tk.Entry(cadre_formulaire)
        self.entree_id.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(cadre_formulaire, text="Nom :", bg="#AEC6CF").grid(row=1, column=0, padx=5, pady=5)
        self.entree_nom = tk.Entry(cadre_formulaire)
        self.entree_nom.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(cadre_formulaire, text="Prénom :", bg="#AEC6CF").grid(row=2, column=0, padx=5, pady=5)
        self.entree_prenom = tk.Entry(cadre_formulaire)
        self.entree_prenom.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(cadre_formulaire, text="Rôle :", bg="#AEC6CF").grid(row=3, column=0, padx=5, pady=5)
        self.entree_role = ttk.Combobox(cadre_formulaire, values=["operateur", "team_leader"], state="readonly")
        self.entree_role.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(cadre_formulaire, text="Email :", bg="#AEC6CF").grid(row=4, column=0, padx=5, pady=5)
        self.entree_email = tk.Entry(cadre_formulaire)
        self.entree_email.grid(row=4, column=1, padx=5, pady=5)

        bouton_ajouter = tk.Button(cadre_formulaire, text="Ajouter", font=("Arial", 12, "bold"), bg="#27AE60", fg="white", command=self.ajouter_utilisateur)
        bouton_ajouter.grid(row=5, column=0, pady=10)

        bouton_modifier = tk.Button(cadre_formulaire, text="Modifier", font=("Arial", 12, "bold"), bg="#2980B9", fg="white", command=self.modifier_utilisateur)
        bouton_modifier.grid(row=5, column=1, pady=10)

        bouton_supprimer = tk.Button(cadre_formulaire, text="Supprimer", font=("Arial", 12, "bold"), bg="#E74C3C", fg="white", command=self.supprimer_utilisateur)
        bouton_supprimer.grid(row=5, column=2, padx=10, pady=10)

        cadre_boutons = tk.Frame(self, bg="#AEC6CF")
        cadre_boutons.pack(pady=10)

        bouton_retour = tk.Button(cadre_boutons, text="Retour au Menu", font=("Arial", 12, "bold"), bg="#E74C3C", fg="white", command=lambda: self.master.show_page(MenuPage))
        bouton_retour.grid(row=0, column=1, padx=10, pady=20)

        self.afficher_utilisateurs()

    def afficher_utilisateurs(self):
        conn = sqlite3.connect("gestion_outils.db")
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, nom, prenom, role, email FROM utilisateurs")
            utilisateurs = cursor.fetchall()
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'accès à la base de données : {e}")
            return
        finally:
            conn.close()

        for item in self.tree_utilisateurs.get_children():
            self.tree_utilisateurs.delete(item)

        for utilisateur in utilisateurs:
            self.tree_utilisateurs.insert("", "end", values=utilisateur)

    def remplir_champs(self, event):
        selection = self.tree_utilisateurs.selection()
        if selection:
            item = self.tree_utilisateurs.item(selection[0])
            valeurs = item["values"]

            self.entree_id.config(state="normal")
            self.entree_id.delete(0, tk.END)
            self.entree_id.insert(0, valeurs[0])

            self.entree_nom.delete(0, tk.END)
            self.entree_nom.insert(0, valeurs[1])

            self.entree_prenom.delete(0, tk.END)
            self.entree_prenom.insert(0, valeurs[2])

            self.entree_role.set(valeurs[3])

            self.entree_email.delete(0, tk.END)
            self.entree_email.insert(0, valeurs[4])

    def ajouter_utilisateur(self):
        id = self.entree_id.get()
        nom = self.entree_nom.get()
        prenom = self.entree_prenom.get()
        role = self.entree_role.get()
        email = self.entree_email.get()

        if not id or not nom or not prenom or not role:
            messagebox.showwarning("Attention", "Veuillez remplir tous les champs obligatoires.")
            return

        conn = sqlite3.connect("gestion_outils.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO utilisateurs (id, nom, prenom, role, email) VALUES (?, ?, ?, ?, ?)", (id, nom, prenom, role, email))
            conn.commit()
            self.afficher_utilisateurs()
            messagebox.showinfo("Succès", "Utilisateur ajouté avec succès.")
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'ajout : {e}")
        finally:
            conn.close()

    def modifier_utilisateur(self):
        id_utilisateur = self.entree_id.get()
        nom = self.entree_nom.get()
        prenom = self.entree_prenom.get()
        role = self.entree_role.get()
        email = self.entree_email.get()

        if not id_utilisateur or not nom or not prenom or not role:
            messagebox.showwarning("Attention", "Veuillez remplir tous les champs obligatoires.")
            return

        conn = sqlite3.connect("gestion_outils.db")
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE utilisateurs SET id = ?, nom = ?, prenom = ?, role = ?, email = ? WHERE id = ?", (id_utilisateur, nom, prenom, role, email, id_utilisateur))
            conn.commit()
            self.afficher_utilisateurs()
            messagebox.showinfo("Succès", "Utilisateur modifié avec succès.")
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la modification : {e}")
        finally:
            conn.close()

    def supprimer_utilisateur(self):
        selection = self.tree_utilisateurs.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un utilisateur à supprimer.")
            return

        utilisateur_id = self.tree_utilisateurs.item(selection[0])["values"][0]
        utilisateur_nom = self.tree_utilisateurs.item(selection[0])["values"][1]
        utilisateur_prenom = self.tree_utilisateurs.item(selection[0])["values"][2]

        confirmation = messagebox.askyesno(
            "Confirmation de suppression",
            f"Êtes-vous sûr de vouloir supprimer l'utilisateur {utilisateur_nom} {utilisateur_prenom} (ID: {utilisateur_id}) ?"
        )

        if not confirmation:
            return

        conn = sqlite3.connect("gestion_outils.db")
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM utilisateurs WHERE id = ?", (utilisateur_id,))
            conn.commit()
            self.afficher_utilisateurs()
            messagebox.showinfo("Succès", "Utilisateur supprimé avec succès.")
        except sqlite3.Error as e:
            messagebox.showerror("Erreur", f"Erreur lors de la suppression : {e}")
        finally:
            conn.close()




# Classe principale pour gérer les pages
class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x700")
        self.title("Gestion des Outils")
        self.configure(bg="#AEC6CF")
        self.frames = {}
        self.show_page(PageConnexion)
    
    def show_page(self, page_class):
        # Effacer tout le contenu de la page actuelle
        for widget in self.winfo_children():
            widget.destroy()

        # Créer et afficher la nouvelle page
        page = page_class(self)
        page.pack()



# Lancer l'application
app = Application()
app.mainloop()
