from views.views import View
from models.player import Player
from tinydb import TinyDB, Query, where

class Controller:

    """ ----- ----- Menu ----- ----- """
    def __init__(self):
        """ Initialise les valeurs du Conbtroller via le constructeur __init__ """
        self.players_list = []
        self.db = TinyDB("data/players/db.json")
        self.players_table = self.db.table("Players")
        self.view = View()
        self.user = Query()

    def display_title(self):
        """ Fait appraître le titre """
        welcom_title = "Bienvenue dans l'application de tournois d'echecs ♟️"
        self.view.message(welcom_title)
        self.display_menu()

    def display_menu(self):
        """ Fait appraître le menu """
        user_choice = self.view.menu()
        if user_choice == 1:
            self.new_player()
        if user_choice == 2:
            self.display_player_list()
        if user_choice == 3:
            self.upgrade_rank()
        if user_choice == 4:
            self.tournament_roster()


    """ ----- ----- Joueur ----- ----- """
    def new_player(self):
        """ Créer un nouveau Joueur """
        player_creation_title = "Création d'un nouveau joueur 🙋"
        self.view.message(player_creation_title)
        data_player = self.view.new_player()
        first_name = data_player[0]
        last_name = data_player[1]
        dath_of_birth = data_player[2]
        rank = data_player[3]

        """ On viens vérifier si le joueur n'existe pas déjà """
        same_name = self.players_table.search(self.user.first_name == first_name)
        same_last_name = self.players_table.search(self.user.last_name == last_name)
        if same_last_name and same_name:
            error_message = "Ce joueur est déjà enregistrer ⚠️"
            self.view.message(error_message)
            self.display_menu()

        player = Player(last_name, first_name, dath_of_birth, rank)
        self.add_player_in_file(player.__dict__)
        new_player_again = input("Voulez vous enregistrer un autre joueur ? 🔄 (Y/N) :")
        if (new_player_again == "Y"):
            self.new_player()
        else:
            self.display_menu()

    def players_roster(self):
        """ Création d'une liste contenant les joueurs enregistrés """
        players = self.players_table.all()
        players = sorted(players, key=lambda player: player['last_name'])
        player_roster = []
        for people in players:
            player = Player(
                people["last_name"],
                people["first_name"],
                people["dath_of_birth"],
                people["rank"],
            ).__dict__
            player_roster.append(player)
        return player_roster

    def add_player_in_file(self, data):
        """ Enregistre le joueur dans le fichier JSON """
        self.players_table.insert(data)
        add_player_in_file_title = "Joueur bien enregistrer 🎉"
        self.view.message(add_player_in_file_title)

    def display_player_list(self):
        """ Affiche la liste des joueurs enregistrer par ordre alphabétique (Nom) """
        list_title = "Liste des joueurs enregistrés 📃"
        self.view.message(list_title)
        players = sorted(self.players_table, key=lambda player: player['last_name'])
        self.view.display_player_list(players)

    def upgrade_rank(self):
        """ Modifie le classement d'un joueur """
        rank_title = " Modification de classement 🏆"
        self.view.message(rank_title)
        datas_to_modify = self.view.modify_rank()
        last_name = datas_to_modify[0]
        first_name = datas_to_modify[1]
        rank = int(datas_to_modify[2])
        player_to_modify = self.players_table.search(self.user.last_name == last_name and self.user.first_name == first_name)

    """ ----- ----- TOURNOI ----- ----- """
    def new_tournament(self):
        """ Créer un Tournoi """
        tournament_creation_title = "Création d'un nouveau tournoi 🏁"
        self.view.message(tournament_creation_title)
        tournament_data = self.view.new_tournament()
        name = tournament_data[0]
        place = tournament_data[1]
        start_date = tournament_data[2]
        end_date = tournament_data[3]
        round = tournament_data[4]
        description = tournament_data[5]
        self.db_tournament = TinyDB(f"data/tournaments/{name}.json")
        self.tournament_table = self.db_tournament.table(f"{name}")

    def tournament_roster(self):
        roster_title = " Veuillez choisir les joueurs participants au tournoi 🏆"
        self.view.message(roster_title)
        players = self.players_roster()
        self.view.tournament_roster(players)










