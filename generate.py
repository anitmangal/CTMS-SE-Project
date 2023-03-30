import sqlite3
import random
from math import ceil, floor

# Initialize database
def init():
  global sqliteConnect, cursor
  try:
    sqliteConnect = sqlite3.connect('database.db')
  except:
    print('Could not connect to database.')
    exit()
  cursor = sqliteConnect.cursor()
  cursor.execute('CREATE TABLE IF NOT EXISTS TT(ID INTEGER PRIMARY KEY, Teams TEXT UNIQUE)') # Tournament Teams Table
  cursor.execute('CREATE TABLE IF NOT EXISTS MD(ID INTEGER PRIMARY KEY, TeamA INT NOT NULL, TeamB INT NOT NULL, DetailsGenerated BOOLEAN NOT NULL DEFAULT 0, Result INT, BatFirst BOOLEAN, TeamARuns INT, TeamAWickets INT, TeamABalls INT, TeamBRuns INT, TeamBWickets INT, TeamBBalls INT, FOREIGN KEY(TeamA) REFERENCES TT(ID), FOREIGN KEY(TeamB) REFERENCES TT(ID))') # Match Details Table
  cursor.execute('CREATE TABLE IF NOT EXISTS PD(ID INTEGER PRIMARY KEY, Name TEXT, Age INT, Hand BOOLEAN, TeamID NOT NULL, FOREIGN KEY(TeamID) REFERENCES TT(ID))') # Player Details Table
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

# Reset the database
def reset():
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
  MatchArray = cursor.execute('SELECT * FROM MD')
  for i in MatchArray:
    print("Match", i[0], ":", i[1], "vs", i[2])
    
# Tell if the match details are generated
def isGenerated(matchID):
  global sqliteConnect, cursor
  return cursor.execute('SELECT DetailsGenerated FROM MD WHERE ID = ?', (matchID,)).fetchone()[0]

# Get the match details
def getDetails(matchID):
  global sqliteConnect, cursor
  md = cursor.execute('SELECT * FROM MD WHERE ID = ?', (matchID,)).fetchone()
  print("Match", md[0], ":", md[1], "vs", md[2])
  print("Result:")
  if (md[4] == 0):
    print("Tie")
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
  MDArr = cursor.execute(f'SELECT * FROM MD{matchID}').fetchall()
  for i in range(22):
    if (i == 0): print("Team", md[1], ":")
    elif (i == 11): print("Team", md[2], ":")
    print(end="\t")
    print("Player: ", MDArr[i][0], end="\t")
    print("Runs: ", MDArr[i][1], end="\t")
    print("Balls: ", MDArr[i][2], end="\t")
    print("Wickets: ", MDArr[i][3], end="\t")
    print("Balls Bowled: ", MDArr[i][4])
  
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
  # Get the teams playing the match
  cursor.execute(f'SELECT TeamA, TeamB FROM MD WHERE ID = {matchID}')
  matchteams = cursor.fetchall()
  tAid = matchteams[0][0]
  tBid = matchteams[0][1]
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
    cursor.execute(f'INSERT INTO MD{matchID} VALUES(?, ?, ?, ?, ?)', (teamA[i][0], tArsArr[i], tAbfArr[i], tAwtArr[i], tAbbArr[i]))
  for i in range(11):
    cursor.execute(f'INSERT INTO MD{matchID} VALUES(?, ?, ?, ?, ?)', (teamB[i][0], tBrsArr[i], tBbfArr[i], tBwtArr[i], tBbbArr[i]))
  sqliteConnect.commit()
  
# DEBUG
def printTeams():
  global sqliteConnect, cursor
  TeamsArray = cursor.execute('SELECT * FROM TT')
  #TeamsArray = cursor.fetchall()
  for i in TeamsArray:
    print(i)
  PlayersArray = cursor.execute('SELECT * FROM PD')
  for i in PlayersArray:
    print(i)
  for i in range(1, numTeams() + 1):
    TeamArray = cursor.execute(f'SELECT * FROM TD{i}')
    for j in TeamArray:
      print(j)
    
if __name__ == '__main__':
  init()
  choice = input('Do you want to reset? (y/n): ')
  if (choice == 'y' or choice == 'Y'):
    reset()
  if (numTeams() == 0):
    n = int(input('Enter number of teams: '))
    generateTeams(n)
  if (numMatches() == 0):
    generateMatches()
  while (True) :
    print("Matches:")
    printMatches()
    choice = int(input('Enter match number to view details (Enter 0 to exit):'))
    if (choice == 0): exit()
    if (choice > numMatches() or choice < 0):
      print('Invalid match number.')
    if (isGenerated(choice)):
      print('Details already generated.')
      getDetails(choice)
    else:
      genchoice = input("Do you want to generate details? (y/n):")
      if (genchoice == 'y' or genchoice == 'Y'):
        generateDetails(choice)
        print('Details generated.')
        getDetails(choice)