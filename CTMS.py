import sqlite3
import random
import sys
from math import ceil, floor

# Initialize database
def init():
  global sqliteConnect, cursor
  try:
    sqliteConnect = sqlite3.connect(r'database.db')
  except:
    print('Could not connect to database.')
    sys.exit(0)
  cursor = sqliteConnect.cursor()
  cursor.execute('CREATE TABLE IF NOT EXISTS TT(ID INTEGER PRIMARY KEY, Teams TEXT, MatchesPlayed INTEGER DEFAULT 0, MatchesWon INTEGER DEFAULT 0, HighestRunScorer INT DEFAULT 0, HighestWicketTaker INT DEFAULT 0, Last5Matches TEXT DEFAULT "NA")') # Tournament Teams Table
  cursor.execute('CREATE TABLE IF NOT EXISTS MD(ID INTEGER PRIMARY KEY, TeamA INT NOT NULL, TeamB INT NOT NULL, DetailsGenerated BOOLEAN NOT NULL DEFAULT 0, Result INT, BatFirst BOOLEAN, TeamARuns INT, TeamAWickets INT, TeamABalls INT, TeamBRuns INT, TeamBWickets INT, TeamBBalls INT, FOREIGN KEY(TeamA) REFERENCES TT(ID), FOREIGN KEY(TeamB) REFERENCES TT(ID))') # Match Details Table
  cursor.execute('CREATE TABLE IF NOT EXISTS PD(ID INTEGER PRIMARY KEY, Name TEXT, Age INT, Hand BOOLEAN, TeamID NOT NULL, MatchesPlayed INTEGER DEFAULT 0, RunsScored INTEGER DEFAULT 0, BallsFaced INTEGER DEFAULT 0, BallsBowled INTEGER DEFAULT 0, WicketsTaken INTEGER DEFAULT 0, FOREIGN KEY(TeamID) REFERENCES TT(ID))') # Player Details Table
  sqliteConnect.commit()
    
# Get the number of teams
def numTeams():
  global sqliteConnect, cursor
  try: 
    cursor.execute('SELECT COUNT(*) FROM TT')
    return cursor.fetchone()[0]
  except:
    # If TT table does not exist
    return 0

# Get the number of matches
def numMatches():
  global sqliteConnect, cursor
  try: 
    cursor.execute('SELECT COUNT(*) FROM MD')
    return cursor.fetchone()[0]
  except:
    # If MD table does not exist
    return 0
  
# Get the number of players
def numPlayers():
  global sqliteConnect, cursor
  try:
    cursor.execute('SELECT COUNT(*) FROM PD')
    return cursor.fetchone()[0]
  except:
    # IF PD table does not exist
    return 0

# Reset the database
def resetDB():
  global sqliteConnect, cursor
  numT = numTeams()
  numM = numMatches()
  cursor.execute('DROP TABLE IF EXISTS TT')
  cursor.execute('DROP TABLE IF EXISTS MD')
  cursor.execute('DROP TABLE IF EXISTS PD')
  for i in range(numT):
    cursor.execute(f'DROP TABLE IF EXISTS TD{i + 1}')
  for i in range(numM):
    cursor.execute(f'DROP TABLE IF EXISTS MD{i + 1}')
  sqliteConnect.commit()
  init()

# Generate teams, along with players
def generateTeams(n = 8):
  global sqliteConnect, cursor
  for team in range(n):
    # Create team, decide captain, number of batsmen, allrounders, and wicketkeepers. Bowlers are the rest.
    cursor.execute('INSERT INTO TT(Teams) VALUES(?)', (f'Team {team + 1}',))
    cursor.execute(f'CREATE TABLE TD{team + 1} (PlayerID INT PRIMARY KEY, isCaptain BOOLEAN, isBatsman BOOLEAN, isBowler BOOLEAN, isWK BOOLEAN, FOREIGN KEY(PlayerID) REFERENCES PD(ID))')
    captain = random.randint(0, 11)
    batsmen = random.randint(4, 6) # 4-6 batsmen
    allrounders = random.randint(1,3) # 1-3 allrounders
    wk = random.randint(0, batsmen) # A batsman can be a wicketkeeper only
    for player in range(11):
      # Create player, checking if the player is captain or wicketkeeper
      cursor.execute('INSERT INTO PD(Name, Age, Hand, TeamID) VALUES(?, ?, ?, ?)', (f'{team+1}Player{player + 1}', random.randint(18, 35), True, team + 1))
      playerID = team*11 + player + 1
      iscap = (captain==player)
      iswk = (wk==player)
      # Batsman
      if batsmen > 0:
        cursor.execute(f'INSERT INTO TD{team + 1} VALUES(?, ?, ?, ?, ?)', (playerID, iscap, True, False, iswk))
        batsmen -= 1
      # All rounder, is batsman and bowler
      elif allrounders > 0:
        cursor.execute(f'INSERT INTO TD{team + 1} VALUES(?, ?, ?, ?, ?)', (playerID, iscap, True, True, iswk))
        allrounders -= 1
      # Bowler
      else:
        cursor.execute(f'INSERT INTO TD{team + 1} VALUES(?, ?, ?, ?, ?)', (playerID, iscap, False, True, iswk))
  sqliteConnect.commit()

# Generate matches by round robin method. Match details are not generated here.
def generateMatches():
  global sqliteConnect, cursor
  numT = numTeams()
  TeamsArr = [x for x in range(1, numT+1)]
  # If odd, add a dummy team 0
  if numT%2:
    TeamsArr.append(0)
  # Copy the array
  rotation = list(TeamsArr)
  fixtures = []
  for i in range(0, len(TeamsArr)-1):
    # Record current rotation
    fixtures.append(rotation)
    # Rotate the array, matching the first and last teams
    rotation = [rotation[0]] + [rotation[-1]] + rotation[1:-1]
  for i in fixtures:
    # Get the matches as pairs of teams. If a team is 0, it is a dummy team, so the match is ignored.
    tempArr = zip(*[iter(i)]*2)
    for (a, b) in tempArr:
      if (a == 0 or b == 0):
        continue
      cursor.execute('INSERT INTO MD(TeamA, TeamB) VALUES(?, ?)', (a, b))
  sqliteConnect.commit()
      
# Print the fixtures
def printMatches():
  global sqliteConnect, cursor
  MatchArray = cursor.execute('SELECT MD.ID, T1.Teams, T2.Teams FROM MD LEFT JOIN TT T1 ON MD.TeamA = T1.ID LEFT JOIN TT T2 ON MD.TeamB = T2.ID')
  for i in MatchArray:
    print("Match", i[0], ":", i[1], "vs", i[2])
    
# Print the teams
def printTeams():
  global sqliteConnect, cursor
  TeamArray = cursor.execute('SELECT * FROM TT')
  for i in TeamArray:
    print("Team", i[0], ": ", i[1])

# Print the players
def printPlayers():
  global sqliteConnect, cursor
  PlayerArray = cursor.execute('SELECT ID, Name, TeamID FROM PD').fetchall()
  for i in PlayerArray:
    print("Player", i[0], ": ", i[1], " from team ", end="")
    team = cursor.execute('SELECT Teams FROM TT WHERE ID = ?', (i[2],)).fetchone()
    print(team[0])
    
    
# Tell if the match details are generated
def isGenerated(matchID):
  global sqliteConnect, cursor
  return cursor.execute('SELECT DetailsGenerated FROM MD WHERE ID = ?', (matchID,)).fetchone()[0]

def getTournamentStats():
  global sqliteConnect, cursor
  print("Top 5 Run Scorers:")
  print("Player Name\t\tTeam\t\tRuns Scored")
  runs = cursor.execute('SELECT PD.Name, TT.Teams, PD.RunsScored FROM PD LEFT JOIN TT ON PD.TeamID = TT.ID ORDER BY PD.RunsScored DESC LIMIT 5').fetchall()
  for i in runs:
    print(i[0], "\t\t", i[1], "\t\t", i[2], sep="")
  print()
  print("Top 5 Wicket Takers:")
  print("Player Name\t\tTeam\t\tWickets Taken")
  wickets = cursor.execute('SELECT PD.Name, TT.Teams, PD.WicketsTaken FROM PD LEFT JOIN TT ON PD.TeamID = TT.ID ORDER BY PD.WicketsTaken DESC LIMIT 5').fetchall()
  for i in wickets:
    print(i[0], "\t\t", i[1], "\t\t", i[2], sep="")
  print()

def getTeamDetails(teamID):
  global sqliteConnect, cursor
  td = cursor.execute('SELECT * FROM TT WHERE ID = ?', (teamID,)).fetchone()
  print("Team", td[1])
  print("Players:")
  playerArray = cursor.execute(f'SELECT PD.ID, PD.Name, TD{teamID}.isCaptain, TD{teamID}.isBatsman, TD{teamID}.isBowler, TD{teamID}.isWK FROM TD{teamID} LEFT JOIN PD ON PD.ID = TD{teamID}.PlayerID WHERE PD.TeamID = ?', (teamID,)).fetchall()
  for (i, j, k, l, m, n) in playerArray:
    print("Player", i, ":", j, end="")
    if k:
      print(" (Captain)", end="")
    if l:
      print(" (Batsman)", end="")
    if m:
      print(" (Bowler)", end="")
    if n:
      print(" (Wicketkeeper)", end="")
    print()
  print("Statistics:")
  print("Matches Played:", td[2])
  print("Matches Won:", td[3])
  highScore = cursor.execute('SELECT PD1.Name, PD1.RunsScored, PD2.Name, PD2.WicketsTaken FROM TT LEFT JOIN PD PD1 ON PD1.ID = TT.HighestRunScorer LEFT JOIN PD PD2 ON PD2.ID = TT.HighestWicketTaker WHERE TT.ID = ?', (teamID,)).fetchone()
  if (highScore == None):
    print("Highest Run Scorer: None")
    print("Highest Wicket Taker: None")
  else:
    print("Highest Run Scorer:", highScore[0], "(", highScore[1],"runs )")
    print("Highest Wicket Taker:", highScore[2], "(", highScore[3],"wickets )")
  print("Results in last 5 matches:", end=" ")
  for i in range(5): 
    if (len(td[6]) > i):
      print(td[6][i], end="")
  print()
  
  
# Get the match details
def getMatchDetails(matchID):
  global sqliteConnect, cursor
  md = cursor.execute('SELECT MD.ID, T1.Teams, T2.Teams, MD.DetailsGenerated, MD.Result, MD.BatFirst, MD.TeamARuns, MD.TeamAWickets, MD.TeamABalls, MD.TeamBRuns, MD.TeamBWickets, MD.TeamBBalls FROM MD LEFT JOIN TT T1 ON T1.ID=MD.TeamA LEFT JOIN TT T2 ON T2.ID=MD.TeamB WHERE MD.ID = ?', (matchID,)).fetchone()
  print("Match", md[0], ":", md[1], "vs", md[2])
  print("Result:")
  if (md[4] == 0):
    print("Draw")
  elif (md[4] == 1):
    print("Team", md[1], " wins")
  else:
    print("Team", md[2], " wins")
  if (md[5] == 0):
    print("Team", md[1], " batted first.")
  else:
    print("Team", md[2], " batted first.")
  print("Team", md[1], ":", md[6], "/", md[7], "(", floor(md[8]/6) + float(md[8]%6)/10, "overs )")
  print("Team", md[2], ":", md[9], "/", md[10], "(", floor(md[11]/6) + float(md[11]%6)/10, "overs )")
  print("Match Scorecard:")
  MDArr = cursor.execute(f'SELECT PD.Name, MD{matchID}.RunsScored, MD{matchID}.BallsFaced, MD{matchID}.WicketsTaken, MD{matchID}.BallsBowled FROM MD{matchID} LEFT JOIN PD ON PD.ID=MD{matchID}.PlayerID').fetchall()
  for i in range(22):
    if (i == 0): print("Team", md[1], ":")
    elif (i == 11): print("Team", md[2], ":")
    print(end="\t")
    print("Player: ", MDArr[i][0], end="\t")
    print("Runs: ", MDArr[i][1], end="\t")
    print("Balls: ", MDArr[i][2], end="\t")
    print("Wickets: ", MDArr[i][3], end="\t")
    print("Balls Bowled: ", MDArr[i][4])
    
def getPlayerDetails(playerID):
  global sqliteConnect, cursor
  pd = cursor.execute('SELECT * FROM PD WHERE ID = ?', (playerID,)).fetchone()
  print("Player Name: ", pd[1])
  print("Player Age: ", pd[2])
  if (pd[3] == 1): print("Right-Handed")
  else: print("Left-Handed")
  print("Team: ", pd[4])
  print("Player Statistics:")
  print("Matches Played: ", pd[5])
  print("Runs Scored: ", pd[6])
  if (pd[7] != 0): print("Strike Rate: ", pd[6]*100/pd[7])
  else: print("Strike Rate: 0")
  print("Wickets Taken: ", pd[9])
  
def updateHighScores(teamID):
  global sqliteConnect, cursor
  highScore = cursor.execute('SELECT PD1.RunsScored, PD2.WicketsTaken FROM TT LEFT JOIN PD PD1 ON PD1.ID = TT.HighestRunScorer LEFT JOIN PD PD2 ON PD2.ID = TT.HighestWicketTaker WHERE TT.ID = ?', (teamID,)).fetchone()
  teamHighRuns = cursor.execute('SELECT PD.ID, PD.RunsScored FROM TT LEFT JOIN PD ON PD.TeamID = TT.ID WHERE TT.ID = ? ORDER BY PD.RunsScored DESC LIMIT 1', (teamID,)).fetchone()
  teamHighWickets = cursor.execute('SELECT PD.ID, PD.WicketsTaken FROM TT LEFT JOIN PD ON PD.TeamID = TT.ID WHERE TT.ID = ? ORDER BY PD.WicketsTaken DESC LIMIT 1', (teamID,)).fetchone()
  print("HIGH", highScore, teamHighRuns, teamHighWickets)
  if (highScore[0] == None):
    cursor.execute('UPDATE TT SET HighestRunScorer = ? WHERE ID = ?', (teamHighRuns[0], teamID))
    cursor.execute('UPDATE TT SET HighestWicketTaker = ? WHERE ID = ?', (teamHighWickets[0], teamID))
    sqliteConnect.commit()
    return
  if (teamHighRuns[1] > highScore[0]):
    cursor.execute('UPDATE TT SET HighestRunScorer = ? WHERE ID = ?', (teamHighRuns[0], teamID))
  if (teamHighWickets[1] > highScore[1]):
    cursor.execute('UPDATE TT SET HighestWicketTaker = ? WHERE ID = ?', (teamHighWickets[0], teamID))
  sqliteConnect.commit()

# Generate the match details
def generateDetails(matchID):
  global sqliteConnect, cursor
  # Decide who bats first
  batFirst = random.randint(0, 1)
  teamAruns = 0
  teamAballs = 0
  teamAwickets = 0
  teamBruns = 0
  teamBwickets = 0
  teamBballs = 0
  winner = 0
  # Decide the details of the first batting team. If the team is all out, the number of balls is decided randomly.
  # Then, decide the details of the second batting team. Decide number of balls and wickets carefully.
  # If A scores more, it wins (1). If B scores more, it wins(2). If A and B score the same, it is a tie(0).
  if (batFirst == 0):
    teamAruns = random.randint(80, 200)
    teamAwickets = random.randint(0, 10)
    teamAballs = 0
    if (teamAwickets == 10):
      teamAballs = random.randint(round(teamAruns/6), 120)
    else:
      teamAballs = 120
    teamBruns = random.randint(60, teamAruns+6)
    if (teamBruns > teamAruns):
      teamBwickets = random.randint(0, 9)
      teamBballs = random.randint(round(teamBruns/6), 120)
      winner = 2
    elif (teamBruns < teamAruns):
      teamBwickets = random.randint(0, 10)
      winner = 1
      if (teamBwickets == 10):
        teamBballs = random.randint(round(teamBruns/6), 120)
      else:
        teamBballs = 120
    else:
      teamBwickets = random.randint(0, 9)
      winner = 0
      teamBballs = random.randint(round(teamBruns/6), 120)
  else:
    teamBruns = random.randint(80, 200)
    teamBwickets = random.randint(0, 10)
    teamBballs = 0
    if (teamBwickets == 10):
      teamBballs = random.randint(round(teamBruns/6), 120)
    else:
      teamBballs = 120
    teamAruns = random.randint(0, teamBruns+6)
    if (teamAruns > teamBruns):
      teamAwickets = random.randint(0, 9)
      teamAballs = random.randint(round(teamAruns/6), 120)
      winner = 1
    elif (teamAruns < teamBruns):
      teamAwickets = random.randint(0, 10)
      winner = 2
      if (teamAwickets == 10):
        teamAballs = random.randint(round(teamAruns/6), 120)
      else:
        teamAballs = 120
    else:
      teamAwickets = random.randint(0, 9)
      winner = 0
      teamAballs = random.randint(round(teamAruns/6), 120)
  cursor.execute('UPDATE MD SET DetailsGenerated = 1, BatFirst = ?, TeamARuns = ?, TeamABalls = ?, TeamAWickets = ?, TeamBRuns = ?, TeamBBalls = ?, TeamBWickets = ?, Result = ? WHERE ID = ?', (batFirst, teamAruns, teamAballs, teamAwickets, teamBruns, teamBballs, teamBwickets, winner, matchID))
  # Get the teams playing the match
  cursor.execute(f'SELECT TeamA, TeamB FROM MD WHERE ID = {matchID}')
  matchteams = cursor.fetchall()
  tAid = matchteams[0][0]
  tBid = matchteams[0][1]
  cursor.execute('UPDATE TT SET MatchesPlayed = MatchesPlayed + 1 WHERE ID = ?', (tAid,))
  cursor.execute('UPDATE TT SET MatchesPlayed = MatchesPlayed + 1 WHERE ID = ?', (tBid,))
  if (winner == 1):
    cursor.execute('UPDATE TT SET MatchesWon = MatchesWon + 1 WHERE ID = ?', (tAid,))
    tAlast5 = cursor.execute('SELECT Last5Matches FROM TT WHERE ID = ?', (tAid,)).fetchone()[0]
    if (tAlast5 == "NA"): tAlast5 = ""
    if (len(tAlast5) == 5): tAlast5 = tAlast5[1:]+'W'
    else: tAlast5 += 'W'
    cursor.execute('UPDATE TT SET Last5Matches = ? WHERE ID = ?', (tAlast5, tAid))
    tBlast5 = cursor.execute('SELECT Last5Matches FROM TT WHERE ID = ?', (tBid,)).fetchone()[0]
    if (tBlast5 == "NA"): tBlast5 = ""
    if (len(tBlast5) == 5): tBlast5 = tBlast5[1:]+'L'
    else: tBlast5 += 'L'
    cursor.execute('UPDATE TT SET Last5Matches = ? WHERE ID = ?', (tBlast5, tBid))
  elif (winner == 2):
    cursor.execute('UPDATE TT SET MatchesWon = MatchesWon + 1 WHERE ID = ?', (tBid,))
    tAlast5 = cursor.execute('SELECT Last5Matches FROM TT WHERE ID = ?', (tAid,)).fetchone()[0]
    if (tAlast5 == "NA"): tAlast5 = ""
    if (len(tAlast5) == 5): tAlast5 = tAlast5[1:]+'L'
    else: tAlast5 += 'L'
    cursor.execute('UPDATE TT SET Last5Matches = ? WHERE ID = ?', (tAlast5, tAid))
    tBlast5 = cursor.execute('SELECT Last5Matches FROM TT WHERE ID = ?', (tBid,)).fetchone()[0]
    if (tBlast5 == "NA"): tBlast5 = ""
    if (len(tBlast5) == 5): tBlast5 = tBlast5[1:]+'W'
    else: tBlast5 += 'W'
    cursor.execute('UPDATE TT SET Last5Matches = ? WHERE ID = ?', (tBlast5, tBid))
  else:
    tAlast5 = cursor.execute('SELECT Last5Matches FROM TT WHERE ID = ?', (tAid,)).fetchone()[0]
    if (tAlast5 == "NA"): tAlast5 = ""
    if (len(tAlast5) == 5): tAlast5 = tAlast5[1:]+'D'
    else: tAlast5 += 'D'
    cursor.execute('UPDATE TT SET Last5Matches = ? WHERE ID = ?', (tAlast5, tAid))
    tBlast5 = cursor.execute('SELECT Last5Matches FROM TT WHERE ID = ?', (tBid,)).fetchone()[0]
    if (tBlast5 == "NA"): tBlast5 = ""
    if (len(tBlast5) == 5): tBlast5 = tBlast5[1:]+'D'
    else: tBlast5 += 'D'
    cursor.execute('UPDATE TT SET Last5Matches = ? WHERE ID = ?', (tBlast5, tBid))
  # Create the table for the match scorecard
  cursor.execute(f'CREATE TABLE MD{matchID} (PlayerID INTEGER PRIMARY KEY, RunsScored INTEGER, BallsFaced INTEGER, WicketsTaken INTEGER, BallsBowled INTEGER, FOREIGN KEY(PlayerID) REFERENCES PD(ID))')
  sqliteConnect.commit()
  # Arrays to hold the runs scored, balls faced, wickets taken, balls bowled by each player
  tArsArr = []
  tBrsArr = []
  tAbfArr = []
  tBbfArr = []
  tAwtArr = []
  tBwtArr = []
  tAbbArr = []
  tBbbArr = []
  # RUNS SCORED (Weight reduces as we go down the order)
  # Team A
  sumA = 0
  for i in range(11):
    if (i <= teamAwickets): tArsArr.append(random.randint(0, 200-11*i))
    else: tArsArr.append(0)
    sumA += tArsArr[i]
  tempsum = 0
  for i in range(11):
    tArsArr[i] = round(tArsArr[i]*teamAruns/sumA)
    tempsum += tArsArr[i]
  if (tempsum != teamAruns):
    tArsArr[0] += teamAruns - tempsum
  # Team B
  sumB = 0
  for i in range(11):
    if (i<= teamBwickets): tBrsArr.append(random.randint(0, 200-11*i))
    else: tBrsArr.append(0)
    sumB += tBrsArr[i]
  tempsum = 0
  for i in range(11):
    tBrsArr[i] = round(tBrsArr[i]*teamBruns/sumB)
    tempsum += tBrsArr[i]
  if (tempsum != teamBruns):
    tBrsArr[0] += teamBruns - tempsum
  # BALLS FACED
  # Team A
  sumA = 0
  for i in range(11):
    tAbfArr.append(random.randint(ceil(tArsArr[i]/6), tArsArr[i]))
    sumA += tAbfArr[i]
  tempsum = 0
  for i in range(11):
    tAbfArr[i] = ceil(tAbfArr[i]*teamAballs/sumA)
    tempsum += tAbfArr[i]
  if (tempsum < teamAballs):
    tAbfArr[0] += teamAballs - tempsum
  elif (tempsum > teamAballs):
    max_val = max(tAbfArr)
    max_ind = tAbfArr.index(max_val)
    tAbfArr[max_ind] += teamAballs - tempsum
  # Team B
  sumB = 0
  for i in range(11):
    tBbfArr.append(random.randint(ceil(tBrsArr[i]/6), tBrsArr[i]))
    sumB += tBbfArr[i]
  tempsum = 0
  for i in range(11):
    tBbfArr[i] = ceil(tBbfArr[i]*teamBballs/sumB)
    tempsum += tBbfArr[i]
  if (tempsum < teamBballs):
    tBbfArr[0] += teamBballs - tempsum
  elif (tempsum > teamBballs):
    max_val = max(tBbfArr)
    max_ind = tBbfArr.index(max_val)
  # Get if player is a bowler or not
  cursor.execute(f'SELECT PlayerID, isBowler FROM TD{tAid}')
  teamA = cursor.fetchall()
  cursor.execute(f'SELECT PlayerID, isBowler FROM TD{tBid}')
  teamB = cursor.fetchall()
  # WICKETS TAKEN
  # Team A
  sumA = 0
  for i in range(11):
    if(teamA[i][1] == 1): tAwtArr.append(random.randint(0, 10))
    else: tAwtArr.append(0)
    sumA += tAwtArr[i]
  tempsum = 0
  for i in range(11):
    if (tempsum < teamAwickets): tAwtArr[i] = floor(tAwtArr[i]*teamBwickets/sumA)
    else: tAwtArr[i] = 0
    tempsum += tAwtArr[i]
  if (tempsum != teamBwickets):
    tAwtArr[10] += teamBwickets - tempsum
  # Team B
  sumB = 0
  for i in range(11):
    if(teamB[i][1] == 1): tBwtArr.append(random.randint(0, 10))
    else: tBwtArr.append(0)
    sumB += tBwtArr[i]
  tempsum = 0
  for i in range(11):
    if (tempsum < teamBwickets): tBwtArr[i] = floor(tBwtArr[i]*teamAwickets/sumB)
    else: tBwtArr[i] = 0
    tempsum += tBwtArr[i]
  if (tempsum != teamAwickets):
    tBwtArr[10] += teamAwickets - tempsum
  # BALLS BOWLED (Max 30 balls per bowler)
  # Team A
  sumA = 0
  for i in range(11):
    if(teamA[i][1] == 1): tAbbArr.append(random.randint(6, 120))
    else: tAbbArr.append(0)
    sumA += tAbbArr[i]
  tempsum = 0
  for i in range(11):
    tAbbArr[i] = floor(tAbbArr[i]*teamBballs/sumA/6)*6
    if (tAbbArr[i] > 30): tAbbArr[i] = 30
    tempsum += tAbbArr[i]
  if (tempsum != teamBballs):
    tAbbArr[10] += teamBballs - tempsum
  # Team B
  sumB = 0
  for i in range(11):
    if(teamB[i][1] == 1): tBbbArr.append(random.randint(6, 120))
    else: tBbbArr.append(0)
    sumB += tBbbArr[i]
  tempsum = 0
  for i in range(11):
    tBbbArr[i] = floor(tBbbArr[i]*teamAballs/sumB/6)*6
    if (tBbbArr[i] > 30): tBbbArr[i] = 30
    tempsum += tBbbArr[i]
  if (tempsum != teamAballs):
    tBbbArr[10] += teamAballs - tempsum
  # Store the data in the MD table
  for i in range(11):
    cursor.execute(f'UPDATE PD SET MatchesPlayed = MatchesPlayed + 1, RunsScored = RunsScored + {tArsArr[i]}, BallsFaced = BallsFaced + {tAbfArr[i]}, WicketsTaken = WicketsTaken + {tAwtArr[i]}, BallsBowled = BallsBowled + {tAbbArr[i]} WHERE ID = {teamA[i][0]}')
    cursor.execute(f'INSERT INTO MD{matchID} VALUES(?, ?, ?, ?, ?)', (teamA[i][0], tArsArr[i], tAbfArr[i], tAwtArr[i], tAbbArr[i]))
  for i in range(11):
    cursor.execute(f'UPDATE PD SET MatchesPlayed = MatchesPlayed + 1, RunsScored = RunsScored + {tBrsArr[i]}, BallsFaced = BallsFaced + {tBbfArr[i]}, WicketsTaken = WicketsTaken + {tBwtArr[i]}, BallsBowled = BallsBowled + {tBbbArr[i]} WHERE ID = {teamB[i][0]}')
    cursor.execute(f'INSERT INTO MD{matchID} VALUES(?, ?, ?, ?, ?)', (teamB[i][0], tBrsArr[i], tBbfArr[i], tBwtArr[i], tBbbArr[i]))
  updateHighScores(tAid)
  updateHighScores(tBid)
  sqliteConnect.commit()
  
def closeConn():
  sqliteConnect.close()
  sys.exit(0)
    
if __name__ == '__main__':
  init()
  choice = input('Do you want to reset? (y/n): ')
  if (choice == 'y' or choice == 'Y'):
    resetDB()
  if (numTeams() == 0):
    n = int(input('Enter number of teams: '))
    while(n<=1 or n>12):
      print('Number of teams cannot be less than 2 or more than 12')
      n = int(input('Enter number of teams: '))
    generateTeams(n)
  if (numMatches() == 0):
    generateMatches()
  while (True) :
    caseChoice = int(input('Enter 1 to view teams, 2 to view matches, 3 to view player details, 4 to view tournament statistics, 0 to exit: '))
    if (caseChoice == 0): closeConn()
    elif (caseChoice == 1):
      print("Teams:")
      printTeams()
      choice = int(input('Enter team ID to view details (Enter 0 to go back):'))
      if (choice == 0): continue
      if (choice > numTeams() or choice < 0):
        print('Invalid team ID.')
        continue
      getTeamDetails(choice)
    elif (caseChoice == 2):
      print("Matches:")
      printMatches()
      choice = int(input('Enter match number to view details (Enter 0 to go back):'))
      if (choice == 0): continue
      if (choice > numMatches() or choice < 0):
        print('Invalid match number.')
        continue
      if (isGenerated(choice)):
        print('Details already generated.')
        getMatchDetails(choice)
      else:
        genchoice = input("Do you want to generate details? (y/n):")
        if (genchoice == 'y' or genchoice == 'Y'):
          generateDetails(choice)
          print('Details generated.')
          getMatchDetails(choice)
    elif (caseChoice == 3):
      print("Players:")
      printPlayers()
      choice = int(input('Enter player ID to view details (Enter 0 to to go back):'))
      if (choice == 0): continue
      if (choice > numPlayers() or choice < 0):
        print('Invalid player ID.')
        continue
      getPlayerDetails(choice)
    elif (caseChoice == 4):
      getTournamentStats()
    else:
      print("Invalid choice.")
