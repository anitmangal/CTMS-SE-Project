from CTMS import *
#import CTMS
#import sqlite3
#import random
#import sys
#import kivy
from kivymd.app import MDApp
from kivymd import icon_definitions
from kivymd.uix import gridlayout
from kivymd.uix import dropdownitem
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.datatables import MDDataTable
from kivy.uix.spinner import Spinner
from kivy.metrics import dp

#define different screens
class HomeWindow(Screen):
    pass

class AboutUsWindow(Screen):
    pass

class ResetWindow(Screen):
    def press_yes(self):
        resetDB()

class MenuWindow(Screen):
    def genMatches(self):
        if (numMatches() == 0):
            generateMatches()

class ViewTeamsWindow(Screen):
    pass

class TeamDetailsWindow1(Screen):

    def show_playerD1(self):
        
        cursor = returncursor()
        teamID = 1
        playerArray = cursor.execute(f'SELECT PD.ID, PD.Name, TD{teamID}.isCaptain, TD{teamID}.isBatsman, TD{teamID}.isBowler, TD{teamID}.isWK FROM TD{teamID} LEFT JOIN PD ON PD.ID = TD{teamID}.PlayerID WHERE PD.TeamID = ?', (teamID,)).fetchall()
        playerD1_list=[]
        for (i, j, k, l, m, n) in playerArray:
            roleStr=""
            if k:
                roleStr += " (Captain)"
            if l:
                roleStr += " (Batsman)"
            if m:
                roleStr += " (Bowler)"
            if n:
                roleStr += " (Wicketkeeper)"
            PlayerD_tuple = (f"{i}", f"{j}", roleStr)
            playerD1_list.append(PlayerD_tuple)

        self.playerD1Table = MDDataTable(
            disabled=False,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=100,
            size_hint=(1, 1),
            column_data=[
            ("Player ID", dp(100)),
            ('Name', dp(100)),
            ("Team Role", dp(100))
            ],
            row_data=playerD1_list,
            elevation=2,
            background_color_header="#C1D334",
            background_color_cell="#75801F"
            )
        self.back_button = Button(text='[font=assets/fonts/Merriweather-Black]back[/font]', markup=True, bold=True, font_size=25, size_hint=(1, 0.1), halign='center', valign='bottom')
        self.back_button.bind(on_release=lambda backButton: self.back_fromt1PlayerD())
        self.add_widget(self.playerD1Table)
        self.add_widget(self.back_button)

    def back_fromt1PlayerD(self):
        self.remove_widget(self.playerD1Table)
        self.remove_widget(self.back_button)
        
    def show_stats1(self):
        teamID = 1
        cursor = returncursor()
        td = cursor.execute('SELECT * FROM TT WHERE ID = ?', (teamID,)).fetchone()
        highScore = cursor.execute('SELECT PD1.Name, PD1.RunsScored, PD2.Name, PD2.WicketsTaken FROM TT LEFT JOIN PD PD1 ON PD1.ID = TT.HighestRunScorer LEFT JOIN PD PD2 ON PD2.ID = TT.HighestWicketTaker WHERE TT.ID = ?', (teamID,)).fetchone()
        strHighRScore="None"
        strHighWScore="None"
        if(highScore != None):
            strHighRScore = f"{highScore[0]} ({highScore[1]} runs)"
            strHighWScore = f"{highScore[2]} ({highScore[3]} wickets)"

        strResults5 =""
        for j in range(5):
            if (len(td[6]) > j):
                strResults5 += f" {td[6][j]} "

        self.stats1Table = MDDataTable(
            disabled=False,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=100,
            size_hint=(1, 1),
            column_data=[
            (f'Team {td[1]}', dp(100)),
            ('Stats', dp(100))
            ],
            row_data=[
            ("Matches played", td[2]),
            ("Matches won", td[3]),
            ("Highest Run Scorer", strHighRScore),
            ("Highest Wicket Taker", strHighWScore),
            ("Results in last 5 matches", strResults5)
            ],
            elevation=2,
            background_color_header="#C1D334",
            background_color_cell="#75801F"
            )
        self.back_button = Button(text='[font=assets/fonts/Merriweather-Black]back[/font]', markup=True, bold=True, font_size=25, size_hint=(1, 0.1), halign='center', valign='bottom')
        self.back_button.bind(on_release=lambda backButton: self.back_fromt1stats())
        self.add_widget(self.stats1Table)
        self.add_widget(self.back_button)

    def back_fromt1stats(self):
        self.remove_widget(self.stats1Table)
        self.remove_widget(self.back_button)

class TeamDetailsWindow2(Screen):
    def show_playerD(self):
        
        cursor = returncursor()
        teamID = 2
        playerArray = cursor.execute(f'SELECT PD.ID, PD.Name, TD{teamID}.isCaptain, TD{teamID}.isBatsman, TD{teamID}.isBowler, TD{teamID}.isWK FROM TD{teamID} LEFT JOIN PD ON PD.ID = TD{teamID}.PlayerID WHERE PD.TeamID = ?', (teamID,)).fetchall()
        playerD_list=[]
        for (i, j, k, l, m, n) in playerArray:
            roleStr=""
            if k:
                roleStr += " (Captain)"
            if l:
                roleStr += " (Batsman)"
            if m:
                roleStr += " (Bowler)"
            if n:
                roleStr += " (Wicketkeeper)"
            PlayerD_tuple = (f"{i}", f"{j}", roleStr)
            playerD_list.append(PlayerD_tuple)

        self.playerDTable = MDDataTable(
            disabled=False,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=100,
            size_hint=(1, 1),
            column_data=[
            ("Player ID", dp(100)),
            ('Name', dp(100)),
            ("Team Role", dp(100))
            ],
            row_data=playerD_list,
            elevation=2,
            background_color_header="#C1D334",
            background_color_cell="#75801F"
            )
        self.back_button = Button(text='[font=assets/fonts/Merriweather-Black]back[/font]', markup=True, bold=True, font_size=25, size_hint=(1, 0.1), halign='center', valign='bottom')
        self.back_button.bind(on_release=lambda backButton: self.back_fromtPlayerD())
        self.add_widget(self.playerDTable)
        self.add_widget(self.back_button)

    def back_fromtPlayerD(self):
        self.remove_widget(self.playerDTable)
        self.remove_widget(self.back_button)
        
    def show_stats(self):
        teamID = 2
        cursor = returncursor()
        td = cursor.execute('SELECT * FROM TT WHERE ID = ?', (teamID,)).fetchone()
        highScore = cursor.execute('SELECT PD1.Name, PD1.RunsScored, PD2.Name, PD2.WicketsTaken FROM TT LEFT JOIN PD PD1 ON PD1.ID = TT.HighestRunScorer LEFT JOIN PD PD2 ON PD2.ID = TT.HighestWicketTaker WHERE TT.ID = ?', (teamID,)).fetchone()
        strHighRScore="None"
        strHighWScore="None"
        if(highScore != None):
            strHighRScore = f"{highScore[0]} ({highScore[1]} runs)"
            strHighWScore = f"{highScore[2]} ({highScore[3]} wickets)"

        strResults5 =""
        for j in range(5):
            if (len(td[6]) > j):
                strResults5 += f" {td[6][j]} "

        self.statsTable = MDDataTable(
            disabled=False,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=100,
            size_hint=(1, 1),
            column_data=[
            (f'Team {td[1]}', dp(100)),
            ('Stats', dp(100))
            ],
            row_data=[
            ("Matches played", td[2]),
            ("Matches won", td[3]),
            ("Highest Run Scorer", strHighRScore),
            ("Highest Wicket Taker", strHighWScore),
            ("Results in last 5 matches", strResults5)
            ],
            elevation=2,
            background_color_header="#C1D334",
            background_color_cell="#75801F"
            )
        self.back_button = Button(text='[font=assets/fonts/Merriweather-Black]back[/font]', markup=True, bold=True, font_size=25, size_hint=(1, 0.1), halign='center', valign='bottom')
        self.back_button.bind(on_release=lambda backButton: self.back_fromtstats())
        self.add_widget(self.statsTable)
        self.add_widget(self.back_button)

    def back_fromtstats(self):
        self.remove_widget(self.statsTable)
        self.remove_widget(self.back_button)

class TeamDetailsWindow3(Screen):
    def show_playerD(self):
        
        cursor = returncursor()
        teamID = 3
        playerArray = cursor.execute(f'SELECT PD.ID, PD.Name, TD{teamID}.isCaptain, TD{teamID}.isBatsman, TD{teamID}.isBowler, TD{teamID}.isWK FROM TD{teamID} LEFT JOIN PD ON PD.ID = TD{teamID}.PlayerID WHERE PD.TeamID = ?', (teamID,)).fetchall()
        playerD_list=[]
        for (i, j, k, l, m, n) in playerArray:
            roleStr=""
            if k:
                roleStr += " (Captain)"
            if l:
                roleStr += " (Batsman)"
            if m:
                roleStr += " (Bowler)"
            if n:
                roleStr += " (Wicketkeeper)"
            PlayerD_tuple = (f"{i}", f"{j}", roleStr)
            playerD_list.append(PlayerD_tuple)

        self.playerDTable = MDDataTable(
            disabled=False,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=100,
            size_hint=(1, 1),
            column_data=[
            ("Player ID", dp(100)),
            ('Name', dp(100)),
            ("Team Role", dp(100))
            ],
            row_data=playerD_list,
            elevation=2,
            background_color_header="#C1D334",
            background_color_cell="#75801F"
            )
        self.back_button = Button(text='[font=assets/fonts/Merriweather-Black]back[/font]', markup=True, bold=True, font_size=25, size_hint=(1, 0.1), halign='center', valign='bottom')
        self.back_button.bind(on_release=lambda backButton: self.back_fromtPlayerD())
        self.add_widget(self.playerDTable)
        self.add_widget(self.back_button)

    def back_fromtPlayerD(self):
        self.remove_widget(self.playerDTable)
        self.remove_widget(self.back_button)
        
    def show_stats(self):
        teamID = 3
        cursor = returncursor()
        td = cursor.execute('SELECT * FROM TT WHERE ID = ?', (teamID,)).fetchone()
        highScore = cursor.execute('SELECT PD1.Name, PD1.RunsScored, PD2.Name, PD2.WicketsTaken FROM TT LEFT JOIN PD PD1 ON PD1.ID = TT.HighestRunScorer LEFT JOIN PD PD2 ON PD2.ID = TT.HighestWicketTaker WHERE TT.ID = ?', (teamID,)).fetchone()
        strHighRScore="None"
        strHighWScore="None"
        if(highScore != None):
            strHighRScore = f"{highScore[0]} ({highScore[1]} runs)"
            strHighWScore = f"{highScore[2]} ({highScore[3]} wickets)"

        strResults5 =""
        for j in range(5):
            if (len(td[6]) > j):
                strResults5 += f" {td[6][j]} "

        self.statsTable = MDDataTable(
            disabled=False,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=100,
            size_hint=(1, 1),
            column_data=[
            (f'Team {td[1]}', dp(100)),
            ('Stats', dp(100))
            ],
            row_data=[
            ("Matches played", td[2]),
            ("Matches won", td[3]),
            ("Highest Run Scorer", strHighRScore),
            ("Highest Wicket Taker", strHighWScore),
            ("Results in last 5 matches", strResults5)
            ],
            elevation=2,
            background_color_header="#C1D334",
            background_color_cell="#75801F"
            )
        self.back_button = Button(text='[font=assets/fonts/Merriweather-Black]back[/font]', markup=True, bold=True, font_size=25, size_hint=(1, 0.1), halign='center', valign='bottom')
        self.back_button.bind(on_release=lambda backButton: self.back_fromtstats())
        self.add_widget(self.statsTable)
        self.add_widget(self.back_button)

    def back_fromtstats(self):
        self.remove_widget(self.statsTable)
        self.remove_widget(self.back_button)

class TeamDetailsWindow4(Screen):
    def show_playerD(self):
        
        cursor = returncursor()
        teamID = 4
        playerArray = cursor.execute(f'SELECT PD.ID, PD.Name, TD{teamID}.isCaptain, TD{teamID}.isBatsman, TD{teamID}.isBowler, TD{teamID}.isWK FROM TD{teamID} LEFT JOIN PD ON PD.ID = TD{teamID}.PlayerID WHERE PD.TeamID = ?', (teamID,)).fetchall()
        playerD_list=[]
        for (i, j, k, l, m, n) in playerArray:
            roleStr=""
            if k:
                roleStr += " (Captain)"
            if l:
                roleStr += " (Batsman)"
            if m:
                roleStr += " (Bowler)"
            if n:
                roleStr += " (Wicketkeeper)"
            PlayerD_tuple = (f"{i}", f"{j}", roleStr)
            playerD_list.append(PlayerD_tuple)

        self.playerDTable = MDDataTable(
            disabled=False,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=100,
            size_hint=(1, 1),
            column_data=[
            ("Player ID", dp(100)),
            ('Name', dp(100)),
            ("Team Role", dp(100))
            ],
            row_data=playerD_list,
            elevation=2,
            background_color_header="#C1D334",
            background_color_cell="#75801F"
            )
        self.back_button = Button(text='[font=assets/fonts/Merriweather-Black]back[/font]', markup=True, bold=True, font_size=25, size_hint=(1, 0.1), halign='center', valign='bottom')
        self.back_button.bind(on_release=lambda backButton: self.back_fromtPlayerD())
        self.add_widget(self.playerDTable)
        self.add_widget(self.back_button)

    def back_fromtPlayerD(self):
        self.remove_widget(self.playerDTable)
        self.remove_widget(self.back_button)
        
    def show_stats(self):
        teamID = 4
        cursor = returncursor()
        td = cursor.execute('SELECT * FROM TT WHERE ID = ?', (teamID,)).fetchone()
        highScore = cursor.execute('SELECT PD1.Name, PD1.RunsScored, PD2.Name, PD2.WicketsTaken FROM TT LEFT JOIN PD PD1 ON PD1.ID = TT.HighestRunScorer LEFT JOIN PD PD2 ON PD2.ID = TT.HighestWicketTaker WHERE TT.ID = ?', (teamID,)).fetchone()
        strHighRScore="None"
        strHighWScore="None"
        if(highScore != None):
            strHighRScore = f"{highScore[0]} ({highScore[1]} runs)"
            strHighWScore = f"{highScore[2]} ({highScore[3]} wickets)"

        strResults5 =""
        for j in range(5):
            if (len(td[6]) > j):
                strResults5 += f" {td[6][j]} "

        self.statsTable = MDDataTable(
            disabled=False,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=100,
            size_hint=(1, 1),
            column_data=[
            (f'Team {td[1]}', dp(100)),
            ('Stats', dp(100))
            ],
            row_data=[
            ("Matches played", td[2]),
            ("Matches won", td[3]),
            ("Highest Run Scorer", strHighRScore),
            ("Highest Wicket Taker", strHighWScore),
            ("Results in last 5 matches", strResults5)
            ],
            elevation=2,
            background_color_header="#C1D334",
            background_color_cell="#75801F"
            )
        self.back_button = Button(text='[font=assets/fonts/Merriweather-Black]back[/font]', markup=True, bold=True, font_size=25, size_hint=(1, 0.1), halign='center', valign='bottom')
        self.back_button.bind(on_release=lambda backButton: self.back_fromtstats())
        self.add_widget(self.statsTable)
        self.add_widget(self.back_button)

    def back_fromtstats(self):
        self.remove_widget(self.statsTable)
        self.remove_widget(self.back_button)

class TeamDetailsWindow5(Screen):
    def show_playerD(self):
        
        cursor = returncursor()
        teamID = 5
        playerArray = cursor.execute(f'SELECT PD.ID, PD.Name, TD{teamID}.isCaptain, TD{teamID}.isBatsman, TD{teamID}.isBowler, TD{teamID}.isWK FROM TD{teamID} LEFT JOIN PD ON PD.ID = TD{teamID}.PlayerID WHERE PD.TeamID = ?', (teamID,)).fetchall()
        playerD_list=[]
        for (i, j, k, l, m, n) in playerArray:
            roleStr=""
            if k:
                roleStr += " (Captain)"
            if l:
                roleStr += " (Batsman)"
            if m:
                roleStr += " (Bowler)"
            if n:
                roleStr += " (Wicketkeeper)"
            PlayerD_tuple = (f"{i}", f"{j}", roleStr)
            playerD_list.append(PlayerD_tuple)

        self.playerDTable = MDDataTable(
            disabled=False,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=100,
            size_hint=(1, 1),
            column_data=[
            ("Player ID", dp(100)),
            ('Name', dp(100)),
            ("Team Role", dp(100))
            ],
            row_data=playerD_list,
            elevation=2,
            background_color_header="#C1D334",
            background_color_cell="#75801F"
            )
        self.back_button = Button(text='[font=assets/fonts/Merriweather-Black]back[/font]', markup=True, bold=True, font_size=25, size_hint=(1, 0.1), halign='center', valign='bottom')
        self.back_button.bind(on_release=lambda backButton: self.back_fromtPlayerD())
        self.add_widget(self.playerDTable)
        self.add_widget(self.back_button)

    def back_fromtPlayerD(self):
        self.remove_widget(self.playerDTable)
        self.remove_widget(self.back_button)
        
    def show_stats(self):
        teamID = 5
        cursor = returncursor()
        td = cursor.execute('SELECT * FROM TT WHERE ID = ?', (teamID,)).fetchone()
        highScore = cursor.execute('SELECT PD1.Name, PD1.RunsScored, PD2.Name, PD2.WicketsTaken FROM TT LEFT JOIN PD PD1 ON PD1.ID = TT.HighestRunScorer LEFT JOIN PD PD2 ON PD2.ID = TT.HighestWicketTaker WHERE TT.ID = ?', (teamID,)).fetchone()
        strHighRScore="None"
        strHighWScore="None"
        if(highScore != None):
            strHighRScore = f"{highScore[0]} ({highScore[1]} runs)"
            strHighWScore = f"{highScore[2]} ({highScore[3]} wickets)"

        strResults5 =""
        for j in range(5):
            if (len(td[6]) > j):
                strResults5 += f" {td[6][j]} "

        self.statsTable = MDDataTable(
            disabled=False,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=100,
            size_hint=(1, 1),
            column_data=[
            (f'Team {td[1]}', dp(100)),
            ('Stats', dp(100))
            ],
            row_data=[
            ("Matches played", td[2]),
            ("Matches won", td[3]),
            ("Highest Run Scorer", strHighRScore),
            ("Highest Wicket Taker", strHighWScore),
            ("Results in last 5 matches", strResults5)
            ],
            elevation=2,
            background_color_header="#C1D334",
            background_color_cell="#75801F"
            )
        self.back_button = Button(text='[font=assets/fonts/Merriweather-Black]back[/font]', markup=True, bold=True, font_size=25, size_hint=(1, 0.1), halign='center', valign='bottom')
        self.back_button.bind(on_release=lambda backButton: self.back_fromtstats())
        self.add_widget(self.statsTable)
        self.add_widget(self.back_button)

    def back_fromtstats(self):
        self.remove_widget(self.statsTable)
        self.remove_widget(self.back_button)

class TeamDetailsWindow6(Screen):
    def show_playerD(self):
        
        cursor = returncursor()
        teamID = 6
        playerArray = cursor.execute(f'SELECT PD.ID, PD.Name, TD{teamID}.isCaptain, TD{teamID}.isBatsman, TD{teamID}.isBowler, TD{teamID}.isWK FROM TD{teamID} LEFT JOIN PD ON PD.ID = TD{teamID}.PlayerID WHERE PD.TeamID = ?', (teamID,)).fetchall()
        playerD_list=[]
        for (i, j, k, l, m, n) in playerArray:
            roleStr=""
            if k:
                roleStr += " (Captain)"
            if l:
                roleStr += " (Batsman)"
            if m:
                roleStr += " (Bowler)"
            if n:
                roleStr += " (Wicketkeeper)"
            PlayerD_tuple = (f"{i}", f"{j}", roleStr)
            playerD_list.append(PlayerD_tuple)

        self.playerDTable = MDDataTable(
            disabled=False,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=100,
            size_hint=(1, 1),
            column_data=[
            ("Player ID", dp(100)),
            ('Name', dp(100)),
            ("Team Role", dp(100))
            ],
            row_data=playerD_list,
            elevation=2,
            background_color_header="#C1D334",
            background_color_cell="#75801F"
            )
        self.back_button = Button(text='[font=assets/fonts/Merriweather-Black]back[/font]', markup=True, bold=True, font_size=25, size_hint=(1, 0.1), halign='center', valign='bottom')
        self.back_button.bind(on_release=lambda backButton: self.back_fromtPlayerD())
        self.add_widget(self.playerDTable)
        self.add_widget(self.back_button)

    def back_fromtPlayerD(self):
        self.remove_widget(self.playerDTable)
        self.remove_widget(self.back_button)
        
    def show_stats(self):
        teamID = 6
        cursor = returncursor()
        td = cursor.execute('SELECT * FROM TT WHERE ID = ?', (teamID,)).fetchone()
        highScore = cursor.execute('SELECT PD1.Name, PD1.RunsScored, PD2.Name, PD2.WicketsTaken FROM TT LEFT JOIN PD PD1 ON PD1.ID = TT.HighestRunScorer LEFT JOIN PD PD2 ON PD2.ID = TT.HighestWicketTaker WHERE TT.ID = ?', (teamID,)).fetchone()
        strHighRScore="None"
        strHighWScore="None"
        if(highScore != None):
            strHighRScore = f"{highScore[0]} ({highScore[1]} runs)"
            strHighWScore = f"{highScore[2]} ({highScore[3]} wickets)"

        strResults5 =""
        for j in range(5):
            if (len(td[6]) > j):
                strResults5 += f" {td[6][j]} "

        self.statsTable = MDDataTable(
            disabled=False,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=100,
            size_hint=(1, 1),
            column_data=[
            (f'Team {td[1]}', dp(100)),
            ('Stats', dp(100))
            ],
            row_data=[
            ("Matches played", td[2]),
            ("Matches won", td[3]),
            ("Highest Run Scorer", strHighRScore),
            ("Highest Wicket Taker", strHighWScore),
            ("Results in last 5 matches", strResults5)
            ],
            elevation=2,
            background_color_header="#C1D334",
            background_color_cell="#75801F"
            )
        self.back_button = Button(text='[font=assets/fonts/Merriweather-Black]back[/font]', markup=True, bold=True, font_size=25, size_hint=(1, 0.1), halign='center', valign='bottom')
        self.back_button.bind(on_release=lambda backButton: self.back_fromtstats())
        self.add_widget(self.statsTable)
        self.add_widget(self.back_button)

    def back_fromtstats(self):
        self.remove_widget(self.statsTable)
        self.remove_widget(self.back_button)

class TeamDetailsWindow7(Screen):
    def show_playerD(self):
        
        cursor = returncursor()
        teamID = 7
        playerArray = cursor.execute(f'SELECT PD.ID, PD.Name, TD{teamID}.isCaptain, TD{teamID}.isBatsman, TD{teamID}.isBowler, TD{teamID}.isWK FROM TD{teamID} LEFT JOIN PD ON PD.ID = TD{teamID}.PlayerID WHERE PD.TeamID = ?', (teamID,)).fetchall()
        playerD_list=[]
        for (i, j, k, l, m, n) in playerArray:
            roleStr=""
            if k:
                roleStr += " (Captain)"
            if l:
                roleStr += " (Batsman)"
            if m:
                roleStr += " (Bowler)"
            if n:
                roleStr += " (Wicketkeeper)"
            PlayerD_tuple = (f"{i}", f"{j}", roleStr)
            playerD_list.append(PlayerD_tuple)

        self.playerDTable = MDDataTable(
            disabled=False,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=100,
            size_hint=(1, 1),
            column_data=[
            ("Player ID", dp(100)),
            ('Name', dp(100)),
            ("Team Role", dp(100))
            ],
            row_data=playerD_list,
            elevation=2,
            background_color_header="#C1D334",
            background_color_cell="#75801F"
            )
        self.back_button = Button(text='[font=assets/fonts/Merriweather-Black]back[/font]', markup=True, bold=True, font_size=25, size_hint=(1, 0.1), halign='center', valign='bottom')
        self.back_button.bind(on_release=lambda backButton: self.back_fromtPlayerD())
        self.add_widget(self.playerDTable)
        self.add_widget(self.back_button)

    def back_fromtPlayerD(self):
        self.remove_widget(self.playerDTable)
        self.remove_widget(self.back_button)
        
    def show_stats(self):
        teamID = 7
        cursor = returncursor()
        td = cursor.execute('SELECT * FROM TT WHERE ID = ?', (teamID,)).fetchone()
        highScore = cursor.execute('SELECT PD1.Name, PD1.RunsScored, PD2.Name, PD2.WicketsTaken FROM TT LEFT JOIN PD PD1 ON PD1.ID = TT.HighestRunScorer LEFT JOIN PD PD2 ON PD2.ID = TT.HighestWicketTaker WHERE TT.ID = ?', (teamID,)).fetchone()
        strHighRScore="None"
        strHighWScore="None"
        if(highScore != None):
            strHighRScore = f"{highScore[0]} ({highScore[1]} runs)"
            strHighWScore = f"{highScore[2]} ({highScore[3]} wickets)"

        strResults5 =""
        for j in range(5):
            if (len(td[6]) > j):
                strResults5 += f" {td[6][j]} "

        self.statsTable = MDDataTable(
            disabled=False,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=100,
            size_hint=(1, 1),
            column_data=[
            (f'Team {td[1]}', dp(100)),
            ('Stats', dp(100))
            ],
            row_data=[
            ("Matches played", td[2]),
            ("Matches won", td[3]),
            ("Highest Run Scorer", strHighRScore),
            ("Highest Wicket Taker", strHighWScore),
            ("Results in last 5 matches", strResults5)
            ],
            elevation=2,
            background_color_header="#C1D334",
            background_color_cell="#75801F"
            )
        self.back_button = Button(text='[font=assets/fonts/Merriweather-Black]back[/font]', markup=True, bold=True, font_size=25, size_hint=(1, 0.1), halign='center', valign='bottom')
        self.back_button.bind(on_release=lambda backButton: self.back_fromtstats())
        self.add_widget(self.statsTable)
        self.add_widget(self.back_button)

    def back_fromtstats(self):
        self.remove_widget(self.statsTable)
        self.remove_widget(self.back_button)

class TeamDetailsWindow8(Screen):
    def show_playerD(self):
        
        cursor = returncursor()
        teamID = 8
        playerArray = cursor.execute(f'SELECT PD.ID, PD.Name, TD{teamID}.isCaptain, TD{teamID}.isBatsman, TD{teamID}.isBowler, TD{teamID}.isWK FROM TD{teamID} LEFT JOIN PD ON PD.ID = TD{teamID}.PlayerID WHERE PD.TeamID = ?', (teamID,)).fetchall()
        playerD_list=[]
        for (i, j, k, l, m, n) in playerArray:
            roleStr=""
            if k:
                roleStr += " (Captain)"
            if l:
                roleStr += " (Batsman)"
            if m:
                roleStr += " (Bowler)"
            if n:
                roleStr += " (Wicketkeeper)"
            PlayerD_tuple = (f"{i}", f"{j}", roleStr)
            playerD_list.append(PlayerD_tuple)

        self.playerDTable = MDDataTable(
            disabled=False,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=100,
            size_hint=(1, 1),
            column_data=[
            ("Player ID", dp(100)),
            ('Name', dp(100)),
            ("Team Role", dp(100))
            ],
            row_data=playerD_list,
            elevation=2,
            background_color_header="#C1D334",
            background_color_cell="#75801F"
            )
        self.back_button = Button(text='[font=assets/fonts/Merriweather-Black]back[/font]', markup=True, bold=True, font_size=25, size_hint=(1, 0.1), halign='center', valign='bottom')
        self.back_button.bind(on_release=lambda backButton: self.back_fromtPlayerD())
        self.add_widget(self.playerDTable)
        self.add_widget(self.back_button)

    def back_fromtPlayerD(self):
        self.remove_widget(self.playerDTable)
        self.remove_widget(self.back_button)
        
    def show_stats(self):
        teamID = 8
        cursor = returncursor()
        td = cursor.execute('SELECT * FROM TT WHERE ID = ?', (teamID,)).fetchone()
        highScore = cursor.execute('SELECT PD1.Name, PD1.RunsScored, PD2.Name, PD2.WicketsTaken FROM TT LEFT JOIN PD PD1 ON PD1.ID = TT.HighestRunScorer LEFT JOIN PD PD2 ON PD2.ID = TT.HighestWicketTaker WHERE TT.ID = ?', (teamID,)).fetchone()
        strHighRScore="None"
        strHighWScore="None"
        if(highScore != None):
            strHighRScore = f"{highScore[0]} ({highScore[1]} runs)"
            strHighWScore = f"{highScore[2]} ({highScore[3]} wickets)"

        strResults5 =""
        for j in range(5):
            if (len(td[6]) > j):
                strResults5 += f" {td[6][j]} "

        self.statsTable = MDDataTable(
            disabled=False,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=100,
            size_hint=(1, 1),
            column_data=[
            (f'Team {td[1]}', dp(100)),
            ('Stats', dp(100))
            ],
            row_data=[
            ("Matches played", td[2]),
            ("Matches won", td[3]),
            ("Highest Run Scorer", strHighRScore),
            ("Highest Wicket Taker", strHighWScore),
            ("Results in last 5 matches", strResults5)
            ],
            elevation=2,
            background_color_header="#C1D334",
            background_color_cell="#75801F"
            )
        self.back_button = Button(text='[font=assets/fonts/Merriweather-Black]back[/font]', markup=True, bold=True, font_size=25, size_hint=(1, 0.1), halign='center', valign='bottom')
        self.back_button.bind(on_release=lambda backButton: self.back_fromtstats())
        self.add_widget(self.statsTable)
        self.add_widget(self.back_button)

    def back_fromtstats(self):
        self.remove_widget(self.statsTable)
        self.remove_widget(self.back_button)

class TeamDetailsWindow9(Screen):
    def show_playerD(self):
        
        cursor = returncursor()
        teamID = 9
        playerArray = cursor.execute(f'SELECT PD.ID, PD.Name, TD{teamID}.isCaptain, TD{teamID}.isBatsman, TD{teamID}.isBowler, TD{teamID}.isWK FROM TD{teamID} LEFT JOIN PD ON PD.ID = TD{teamID}.PlayerID WHERE PD.TeamID = ?', (teamID,)).fetchall()
        playerD_list=[]
        for (i, j, k, l, m, n) in playerArray:
            roleStr=""
            if k:
                roleStr += " (Captain)"
            if l:
                roleStr += " (Batsman)"
            if m:
                roleStr += " (Bowler)"
            if n:
                roleStr += " (Wicketkeeper)"
            PlayerD_tuple = (f"{i}", f"{j}", roleStr)
            playerD_list.append(PlayerD_tuple)

        self.playerDTable = MDDataTable(
            disabled=False,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=100,
            size_hint=(1, 1),
            column_data=[
            ("Player ID", dp(100)),
            ('Name', dp(100)),
            ("Team Role", dp(100))
            ],
            row_data=playerD_list,
            elevation=2,
            background_color_header="#C1D334",
            background_color_cell="#75801F"
            )
        self.back_button = Button(text='[font=assets/fonts/Merriweather-Black]back[/font]', markup=True, bold=True, font_size=25, size_hint=(1, 0.1), halign='center', valign='bottom')
        self.back_button.bind(on_release=lambda backButton: self.back_fromtPlayerD())
        self.add_widget(self.playerDTable)
        self.add_widget(self.back_button)

    def back_fromtPlayerD(self):
        self.remove_widget(self.playerDTable)
        self.remove_widget(self.back_button)
        
    def show_stats(self):
        teamID = 9
        cursor = returncursor()
        td = cursor.execute('SELECT * FROM TT WHERE ID = ?', (teamID,)).fetchone()
        highScore = cursor.execute('SELECT PD1.Name, PD1.RunsScored, PD2.Name, PD2.WicketsTaken FROM TT LEFT JOIN PD PD1 ON PD1.ID = TT.HighestRunScorer LEFT JOIN PD PD2 ON PD2.ID = TT.HighestWicketTaker WHERE TT.ID = ?', (teamID,)).fetchone()
        strHighRScore="None"
        strHighWScore="None"
        if(highScore != None):
            strHighRScore = f"{highScore[0]} ({highScore[1]} runs)"
            strHighWScore = f"{highScore[2]} ({highScore[3]} wickets)"

        strResults5 =""
        for j in range(5):
            if (len(td[6]) > j):
                strResults5 += f" {td[6][j]} "

        self.statsTable = MDDataTable(
            disabled=False,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=100,
            size_hint=(1, 1),
            column_data=[
            (f'Team {td[1]}', dp(100)),
            ('Stats', dp(100))
            ],
            row_data=[
            ("Matches played", td[2]),
            ("Matches won", td[3]),
            ("Highest Run Scorer", strHighRScore),
            ("Highest Wicket Taker", strHighWScore),
            ("Results in last 5 matches", strResults5)
            ],
            elevation=2,
            background_color_header="#C1D334",
            background_color_cell="#75801F"
            )
        self.back_button = Button(text='[font=assets/fonts/Merriweather-Black]back[/font]', markup=True, bold=True, font_size=25, size_hint=(1, 0.1), halign='center', valign='bottom')
        self.back_button.bind(on_release=lambda backButton: self.back_fromtstats())
        self.add_widget(self.statsTable)
        self.add_widget(self.back_button)

    def back_fromtstats(self):
        self.remove_widget(self.statsTable)
        self.remove_widget(self.back_button)

class TeamDetailsWindow10(Screen):
    def show_playerD(self):
        
        cursor = returncursor()
        teamID = 10
        playerArray = cursor.execute(f'SELECT PD.ID, PD.Name, TD{teamID}.isCaptain, TD{teamID}.isBatsman, TD{teamID}.isBowler, TD{teamID}.isWK FROM TD{teamID} LEFT JOIN PD ON PD.ID = TD{teamID}.PlayerID WHERE PD.TeamID = ?', (teamID,)).fetchall()
        playerD_list=[]
        for (i, j, k, l, m, n) in playerArray:
            roleStr=""
            if k:
                roleStr += " (Captain)"
            if l:
                roleStr += " (Batsman)"
            if m:
                roleStr += " (Bowler)"
            if n:
                roleStr += " (Wicketkeeper)"
            PlayerD_tuple = (f"{i}", f"{j}", roleStr)
            playerD_list.append(PlayerD_tuple)

        self.playerDTable = MDDataTable(
            disabled=False,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=100,
            size_hint=(1, 1),
            column_data=[
            ("Player ID", dp(100)),
            ('Name', dp(100)),
            ("Team Role", dp(100))
            ],
            row_data=playerD_list,
            elevation=2,
            background_color_header="#C1D334",
            background_color_cell="#75801F"
            )
        self.back_button = Button(text='[font=assets/fonts/Merriweather-Black]back[/font]', markup=True, bold=True, font_size=25, size_hint=(1, 0.1), halign='center', valign='bottom')
        self.back_button.bind(on_release=lambda backButton: self.back_fromtPlayerD())
        self.add_widget(self.playerDTable)
        self.add_widget(self.back_button)

    def back_fromtPlayerD(self):
        self.remove_widget(self.playerDTable)
        self.remove_widget(self.back_button)
        
    def show_stats(self):
        teamID = 10
        cursor = returncursor()
        td = cursor.execute('SELECT * FROM TT WHERE ID = ?', (teamID,)).fetchone()
        highScore = cursor.execute('SELECT PD1.Name, PD1.RunsScored, PD2.Name, PD2.WicketsTaken FROM TT LEFT JOIN PD PD1 ON PD1.ID = TT.HighestRunScorer LEFT JOIN PD PD2 ON PD2.ID = TT.HighestWicketTaker WHERE TT.ID = ?', (teamID,)).fetchone()
        strHighRScore="None"
        strHighWScore="None"
        if(highScore != None):
            strHighRScore = f"{highScore[0]} ({highScore[1]} runs)"
            strHighWScore = f"{highScore[2]} ({highScore[3]} wickets)"

        strResults5 =""
        for j in range(5):
            if (len(td[6]) > j):
                strResults5 += f" {td[6][j]} "

        self.statsTable = MDDataTable(
            disabled=False,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=100,
            size_hint=(1, 1),
            column_data=[
            (f'Team {td[1]}', dp(100)),
            ('Stats', dp(100))
            ],
            row_data=[
            ("Matches played", td[2]),
            ("Matches won", td[3]),
            ("Highest Run Scorer", strHighRScore),
            ("Highest Wicket Taker", strHighWScore),
            ("Results in last 5 matches", strResults5)
            ],
            elevation=2,
            background_color_header="#C1D334",
            background_color_cell="#75801F"
            )
        self.back_button = Button(text='[font=assets/fonts/Merriweather-Black]back[/font]', markup=True, bold=True, font_size=25, size_hint=(1, 0.1), halign='center', valign='bottom')
        self.back_button.bind(on_release=lambda backButton: self.back_fromtstats())
        self.add_widget(self.statsTable)
        self.add_widget(self.back_button)

    def back_fromtstats(self):
        self.remove_widget(self.statsTable)
        self.remove_widget(self.back_button)

class ViewPlayerDetailsWindow(Screen):

    def view_playerID(self):
        cursor = returncursor()
        PlayerArray = cursor.execute('SELECT ID, Name, TeamID FROM PD').fetchall()
        player_list=[]
        for i in PlayerArray:
            team = cursor.execute('SELECT Teams FROM TT WHERE ID = ?', (i[2],)).fetchone()
            player_tuple =(f"Player {i[0]}", i[1], team[0])
            player_list.append(player_tuple)

        self.PIDTable = MDDataTable(
            disabled=False,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=100,
            size_hint=(1, 1),
            use_pagination = True,
            rows_num=10,
            pagination_menu_height='240dp',
            column_data=[
            (f'Player ID', dp(100)),
            ('Name', dp(100)),
            ('Team', dp(100))
            ],
            row_data=player_list,
            elevation=2,
            background_color_header="#C1D334",
            background_color_cell="#75801F"
            )
        self.back_button = Button(text='[font=assets/fonts/Merriweather-Black]back[/font]', markup=True, bold=True, font_size=25, size_hint=(1, 0.1), halign='center', valign='bottom')
        self.back_button.bind(on_release=lambda backButton: self.back_fromPID())
        self.add_widget(self.PIDTable)
        self.add_widget(self.back_button)

    def back_fromPID(self):
        self.remove_widget(self.PIDTable)
        self.remove_widget(self.back_button)

    def select_playerID(self):
        playerID = self.ids.input_id.text
        cursor = returncursor()
        pd = cursor.execute('SELECT * FROM PD WHERE ID = ?', (playerID,)).fetchone()
        hand=""
        if(pd[3]==1):
            hand="Right-handed"
        else:
            hand="left-handed"

        striker=0
        if(pd[7]!=0):
            striker=pd[6]*100/pd[7]

        self.PDTable = MDDataTable(
            disabled=False,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=100,
            size_hint=(1, 1),
            column_data=[
            (f'Player {pd[1]}', dp(100)),
            ('Stats', dp(100))
            ],
            row_data=[
            ("Player age", pd[2]),
            ("Handedness", hand),
            ("Team", pd[4]),
            ("Matches played", pd[5]),
            ("Runs scored", pd[6]), 
            ("Strike Rate", striker), 
            ("Wickets taken", pd[9])
            ],
            elevation=2,
            background_color_header="#C1D334",
            background_color_cell="#75801F"
            )
        self.back_button = Button(text='[font=assets/fonts/Merriweather-Black]back[/font]', markup=True, bold=True, font_size=25, size_hint=(1, 0.1), halign='center', valign='bottom')
        self.back_button.bind(on_release=lambda backButton: self.back_fromPD())
        self.add_widget(self.PDTable)
        self.add_widget(self.back_button)

    def back_fromPD(self):
        self.remove_widget(self.PDTable)
        self.remove_widget(self.back_button)
        
class ViewMatchesWindow(Screen):
    def view_matchD(self):
        cursor = returncursor()
        MatchArray = cursor.execute('SELECT MD.ID, T1.Teams, T2.Teams FROM MD LEFT JOIN TT T1 ON MD.TeamA = T1.ID LEFT JOIN TT T2 ON MD.TeamB = T2.ID')
        match_list=[]
        for i in MatchArray:
            match_tuple =(f"Match {i[0]}", i[1], i[2])
            match_list.append(match_tuple)

        self.MDTable = MDDataTable(
            disabled=False,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=100,
            size_hint=(1, 1),
            use_pagination = True,
            rows_num=10,
            pagination_menu_height='240dp',
            column_data=[
            ('Match ID', dp(100)),
            ('Team A', dp(100)),
            ('Team B', dp(100))
            ],
            row_data=match_list,
            elevation=2,
            background_color_header="#C1D334",
            background_color_cell="#75801F"
            )
        self.back_button = Button(text='[font=assets/fonts/Merriweather-Black]back[/font]', markup=True, bold=True, font_size=25, size_hint=(1, 0.1), halign='center', valign='bottom')
        self.back_button.bind(on_release=lambda backButton: self.back_fromMD())
        self.add_widget(self.MDTable)
        self.add_widget(self.back_button)

    def back_fromMD(self):
        self.remove_widget(self.MDTable)
        self.remove_widget(self.back_button)


    def view_matchResult(self):
        matchID = self.ids.input_matchid.text
        if(not isGenerated(matchID)):
            generateDetails(matchID)
        cursor = returncursor()
        md = cursor.execute('SELECT MD.ID, T1.Teams, T2.Teams, MD.DetailsGenerated, MD.Result, MD.BatFirst, MD.TeamARuns, MD.TeamAWickets, MD.TeamABalls, MD.TeamBRuns, MD.TeamBWickets, MD.TeamBBalls FROM MD LEFT JOIN TT T1 ON T1.ID=MD.TeamA LEFT JOIN TT T2 ON T2.ID=MD.TeamB WHERE MD.ID = ?', (matchID,)).fetchone()
        res=""
        res_actor_s=""
        if (md[4] == 0):
            res="Draw"
            res_actor_s=f"{md[1]} & {md[2]}"
        elif (md[4] == 1):
            res="Wins"
            res_actor_s=f"{md[1]}"
        else:
            res="Wins"
            res_actor_s=f"{md[2]}"
        bat_actor=""
        if (md[5] == 0):
            bat_actor=f"{md[1]}"
        else:
            bat_actor=f"{md[2]}"
        score_a=f"{md[6]}/{md[7]} ({floor(md[8]/6) + float(md[8]%6)/10} overs)"
        score_b=f"{md[9]}/{md[10]} ({floor(md[11]/6) + float(md[11]%6)/10} overs)"
        
        self.PDTable = MDDataTable(
            disabled=False,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=100,
            size_hint=(1, 1),
            column_data=[
            ('Metric', dp(100)),
            ('Result', dp(100))
            ],
            row_data=[
            (res, res_actor_s),
            ("Batted first", bat_actor),
            (f"Team {md[1]}", score_a),
            (f"Team {md[2]}", score_b)
            ],
            elevation=2,
            background_color_header="#C1D334",
            background_color_cell="#75801F"
            )
        self.back_button = Button(text='[font=assets/fonts/Merriweather-Black]back[/font]', markup=True, bold=True, font_size=25, size_hint=(1, 0.1), halign='center', valign='bottom')
        self.back_button.bind(on_release=lambda backButton: self.back_fromPD())
        self.add_widget(self.PDTable)
        self.add_widget(self.back_button)

    def back_fromPD(self):
        self.remove_widget(self.PDTable)
        self.remove_widget(self.back_button)

    def view_matchScorecard(self):
        matchID = self.ids.input_matchid.text
        if(not isGenerated(matchID)):
            generateDetails(matchID)
        cursor=returncursor()
        md = cursor.execute('SELECT MD.ID, T1.Teams, T2.Teams, MD.DetailsGenerated, MD.Result, MD.BatFirst, MD.TeamARuns, MD.TeamAWickets, MD.TeamABalls, MD.TeamBRuns, MD.TeamBWickets, MD.TeamBBalls FROM MD LEFT JOIN TT T1 ON T1.ID=MD.TeamA LEFT JOIN TT T2 ON T2.ID=MD.TeamB WHERE MD.ID = ?', (matchID,)).fetchone()
        MDArr = cursor.execute(f'SELECT PD.Name, MD{matchID}.RunsScored, MD{matchID}.BallsFaced, MD{matchID}.WicketsTaken, MD{matchID}.BallsBowled FROM MD{matchID} LEFT JOIN PD ON PD.ID=MD{matchID}.PlayerID').fetchall()
        
        match_score_list=[]
        for i in range(22):
            team=""
            if(i>=0 and i<11):
                team=md[1]
            else:
                team=md[2]
            score_tuple = (team, MDArr[i][0], MDArr[i][1], MDArr[i][2], MDArr[i][3], MDArr[i][4])
            match_score_list.append(score_tuple)
        self.MSTable = MDDataTable(
            disabled=False,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=100,
            size_hint=(1, 1),
            use_pagination = True,
            rows_num=10,
            pagination_menu_height='240dp',
            column_data=[
            ('Team', dp(100)),
            ('Player', dp(100)),
            ('Runs', dp(100)),
            ('Balls received', dp(100)),
            ('Wickets', dp(100)),
            ('Balls Bowled', dp(100))
            ],
            row_data=match_score_list,
            elevation=2,
            background_color_header="#C1D334",
            background_color_cell="#75801F"
            )
        self.back_button = Button(text='[font=assets/fonts/Merriweather-Black]back[/font]', markup=True, bold=True, font_size=25, size_hint=(1, 0.1), halign='center', valign='bottom')
        self.back_button.bind(on_release=lambda backButton: self.back_fromMS())
        self.add_widget(self.MSTable)
        self.add_widget(self.back_button)

    def back_fromMS(self):
        self.remove_widget(self.MSTable)
        self.remove_widget(self.back_button)

class ViewTournamentStatistics(Screen):

    def show_toprun(self):
        #global cursor
        cursor = returncursor()
        runs = cursor.execute('SELECT PD.Name, TT.Teams, PD.RunsScored FROM PD LEFT JOIN TT ON PD.TeamID = TT.ID ORDER BY PD.RunsScored DESC LIMIT 5').fetchall()
        run_records = []
        for i in runs:
            record = (i[0], i[1], i[2])
            run_records.append(record)

        self.toprun_table = MDDataTable(
            disabled=False,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=50,
            size_hint=(1, 1),
            column_data=[
            ('Player Name', dp(100)),
            ('Team', dp(100)),
            ('Runs Scored', dp(100))
            ],
            row_data=run_records,
            elevation=2,
            background_color_header="#5F209D",
            background_color_cell="#330E57"
            )
        self.back_button = Button(text='[font=assets/fonts/Merriweather-Black]back[/font]', markup=True, bold=True, font_size=25, size_hint=(1, 0.1), halign='center', valign='bottom')
        self.back_button.bind(on_release=lambda backButton: self.back_fromrunt())
        self.add_widget(self.toprun_table)
        self.add_widget(self.back_button)

    def show_topwicket(self):
        global cursor
        cursor = returncursor()
        wickets = cursor.execute('SELECT PD.Name, TT.Teams, PD.WicketsTaken FROM PD LEFT JOIN TT ON PD.TeamID = TT.ID ORDER BY PD.WicketsTaken DESC LIMIT 5').fetchall()
        wicket_records = []
        for i in wickets:
            record = (i[0], i[1], i[2])
            wicket_records.append(record)

        self.topwicket_table = MDDataTable(
            disabled=False,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            padding=50,
            size_hint=(1, 1),
            column_data=[
            ('Player Name', dp(100)),
            ('Team', dp(100)),
            ('Wickets Taken', dp(100))
            ],
            row_data=wicket_records,
            elevation=2,
            background_color_header="#5F209D",
            background_color_cell="#330E57",
            )
        self.back_button = Button(text='[font=assets/fonts/Merriweather-Black]back[/font]', markup=True, bold=True, font_size=25, size_hint=(1, 0.1), halign='center', valign='bottom')
        self.back_button.bind(on_release=lambda backButton: self.back_fromwickett())
        self.add_widget(self.topwicket_table)
        self.add_widget(self.back_button)

    def back_fromrunt(self):
        self.remove_widget(self.toprun_table)
        self.remove_widget(self.back_button)

    def back_fromwickett(self):
        self.remove_widget(self.topwicket_table)
        self.remove_widget(self.back_button)
        #App.get_running_app().root.get_screen('menuw').add_widget(self.ids.menu_box)


class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("main.kv")

class CTMSApp(MDApp):
    def build(self):
        init()
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Indigo"
        #Window.clearcolor = (8/255.0, 53/255.0, 3/255.0, 1)
        return kv

if __name__ == '__main__':
    CTMSApp().run()
    closeConn()