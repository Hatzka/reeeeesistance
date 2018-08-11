

import telepot
import time
# from roleRules import *
from random import randint
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
groupA = '-1001178944523' #reeeeeeeee
groupB = '-1001208260199' #Testusterus
group = groupB
TOKEN = '537254396:AAEtg-h504Rkvlft1KsVPo5po66B5vGZKDs'
bot = telepot.Bot(TOKEN)


class Player:
    role = ''
    isLeader = False
    username = None
    nr = None

    def __init__(self, name, id):  # , username):
        self.name = name
        self.id = id
        #self.username = username


class Mission:
    nr = None
    isSuccessful = None
    team = []

    def __init__(self, nr, teamSize):
        self.nr = nr
        self.teamSize = teamSize


global name
global usedRoles
global joinedPlayers
global countdownTime
global startingPlayer
global gameInProgress
global gameStartMessage
global playerListMessage
global currentLeader
global index
global knownSpies
global allSpies
global enemySpyList
global allySpyList
global commanderList
global enemySpyList_default
global allySpyList_default
global commanderList_default
global leaderIndex
global currentLeader
global leaderMessage
global leaderText_default
global joinedPlayers
global teamSize
global missionList
global MessageList
global teamString
global teamString_default
global membersInString
global teamListMessage
teamString_default = 'Team:\n'
MessageList = []
TeamList = []
teamSize = {
    5: [2, 3, 2, 3, 3],
    6: [2, 3, 4, 3, 4],
    7: [2, 3, 3, 4, 4],
    8: [3, 4, 4, 5, 5],
    9: [3, 4, 4, 5, 5],
    10: [3, 4, 4, 5, 5],
}
missionList = []
playerList = []
gameInProgress = False
countdownTime = 0
joinedPlayers = 'Joined Players:\n'
roles = (('spy', 'resistance', 'spy', 'resistance', 'resistance', 'resistance', 'spy', 'resistance', 'resistance', 'spy'),
         ['assassin', 'commander', 'false commander', 'bodyguard', 'resistance',
             'resistance', 'deep cover', 'resistance', 'resistance', 'deep agent']
         )
modes = {
    'original': 0,
    'assassin': 1
}
RoleRules = {
    'assassin': 'You are the assassin. Your job is to identify and assassinate the Commander.',
    'false commander': 'You are the False Commander.\nThe Bodyguard will see you as the Commander.',
    'deep cover': 'You are the Deep Cover Spy.\nYou are unknown to the Commander.',
    'deep agent': 'You are the Deep Agent.\nYou are a spy, but you don\'t know who the other spies are.',
    'spy':  'You are a Spy. Fail 3 missions to win.',
    'commander': 'You are the Commander.\nYou know who the Spies are, except for the Deep Cover Spy.',
    'bodyguard': 'You are the Bodyguard.\nYou must protect the Commander.',
    'resistance': 'You are a member of the Resistance. Succeed in 3 missions to win.'
}
RoleImages = {
    # SPY ROLES
    # 'https://i.imgur.com/uhynJ41.png', #'https://i.imgur.com/pV0cUVr.png',
    'assassin': 'https://i.imgur.com/CGzMcgj.png',
    'false commander': 'https://i.imgur.com/ukShyQ7.png',
    'deep cover': 'https://i.imgur.com/DNLJcok.png',
    'deep agent': 'https://i.imgur.com/Y4KaIv1.png',
    # 'https://i.imgur.com/aAd2Pht.png', #'https://vignette.wikia.nocookie.net/town-of-salem/images/3/36/Spy_icon.png/revision/latest/scale-to-width-down/445?cb=20150801162432',
    'spy':  'https://i.imgur.com/pZnjO9f.png',
    # RESISTANCE ROLES
    'commander': 'https://i.imgur.com/JWtB3JU.png',  # 'https://i.i.imgur.com/b0bogdb.png', #'https://lh3.googleusercontent.com/-z1tTXVR9ZHs/U6P4WOTDSpI/AAAAAAAAABE/auScPcEHYGY/s557/fight_the_power_occupy_wall_street_peace_fist_groovy_peace_symbol_sign_cnd_logo_retro_2_united_nations_blue-555px.jpg',
    'bodyguard': 'https://i.imgur.com/wYosC0T.png',
    'resistance': 'https://i.imgur.com/cgqFv8i.png'  # 'https://i.imgur.com/keOmLNV.png'#'https://lh3.googleusercontent.com/-z1tTXVR9ZHs/U6P4WOTDSpI/AAAAAAAAABE/auScPcEHYGY/s557/fight_the_power_occupy_wall_street_peace_fist_groovy_peace_symbol_sign_cnd_logo_retro_2_united_nations_blue-555px.jpg'
}
# ------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------
knownSpies = ('false commander', 'deep agent', 'spy', 'assassin')
allSpies = ('deep cover', 'false commander', 'deep agent', 'spy', 'assassin')
allySpyList_default = "  Other Spies:\n"
enemySpyList_default = "  Known Spies:\n"
commanderList_default = "  The commanders:\n"
allySpyList = allySpyList_default
enemySpyList = enemySpyList_default
commanderList = commanderList_default
leaderText_default = "Current Leader:\n"


def sendRoleMessages():
    global knownSpies
    global allSpies
    global enemySpyList
    global allySpyList
    global commanderList
    global enemySpyList_default
    global allySpyList_default
    global commanderList_default
    allySpyList = allySpyList_default
    enemySpyList = enemySpyList_default
    commanderList = commanderList_default
    for player in playerList:
        for otherPlayer in playerList:
            if player.role in allSpies:
                # and otherPlayer.id != player.id:
                if otherPlayer.role in allSpies and otherPlayer.role != player.role and player.role != 'deep agent':
                    if otherPlayer.username is None:
                        allySpyList += "  " + otherPlayer.name
                    else:
                        allySpyList += "  " + otherPlayer.name + \
                            ' (@' + otherPlayer.username + ')'
                    # if otherPlayer.role == 'deep agent':
                    #     allySpyList += '(Deep Agent)'
                # make spylist and send to everyone but oberon
            elif player.role == 'commander':
                # make spylist without deep cover
                if otherPlayer.role in knownSpies:
                    if otherPlayer.username is None:
                        enemySpyList += "  " + otherPlayer.name
                    else:
                        enemySpyList += "  " + otherPlayer.name + \
                            ' (@' + otherPlayer.username + ')'
            elif player.role == 'bodyguard':
                # make list of commander and false commander
                if otherPlayer.role in ('commander', 'false commander'):
                    if otherPlayer.username is None:
                        commanderList += "  " + otherPlayer.name
                    else:
                        commanderList += "  " + otherPlayer.name + \
                            ' (@' + otherPlayer.username + ')'
        bot.sendPhoto(
            player.id, RoleImages[player.role], RoleRules[player.role])
        if player.role in allSpies and player.role != "deep agent":
            bot.sendMessage(player.id, allySpyList)
            allySpyList = allySpyList_default
        elif player.role == 'commander':
            bot.sendMessage(player.id, enemySpyList)
            enemySpyList = enemySpyList_default
        elif player.role == 'bodyguard':
            bot.sendMessage(player.id, commanderList)
            commanderList = commanderList_default


# ------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------
# players = [['1', '2', '3', '4', '5'],
#            ['', '', '', '', '', '', '', '', '', ''],
#            []
#            ]
# global playerNr
global playerNR
global playerListMessage
global countdownMessage
playerNR = len(playerList)
# playerNr = len(players[0])
# global playerRoleString


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    text = msg.get("text")
    chatType = msg['chat']['type']
    global gameInProgress
    global joinedPlayers
    global playerNR
    global gameStartMessage
    global playerListMessage
    global leaderIndex
    global currentLeader
    global sage
    global leaderMessage
    global leaderText_default
    global playerList
    global startingPlayerMessageID
    global index
    global MessageList
    global membersInString
    global teamListMessage
    if text == "@vervulfbot":
        bot.sendMessage(group, "Hello")
    if text in ('rolld20', '/rolld20', '/rolld20@vervulfbot'):
        bot.sendMessage(group, randint(1,20))
    if text in ("/forcestart", "/forcestart@vervulfbot"):
        initializeGame()
    if text in ("/stop", "/stop@vervulfbot"):
        if gameInProgress:
            bot.sendMessage(group, "Cancelling Game...")
            playerList = []
            usedRoles = []
            joinedPlayers = "Joined Players:\n"
            bot.deleteMessage((group, gameStartMessage['message_id']))
            bot.deleteMessage((group, playerListMessage['message_id']))
            gameInProgress = False
    if text == "/startgame" or text == "/startgame@vervulfbot":
        if not gameInProgress:
            global index
            membersInString = []
            gameInProgress = True
            startingPlayer = msg['from']['first_name']
            startingPlayerMessageID = msg['message_id']
            index = 1
            playerList = []
            usedRoles = []
            joinedPlayers = "Joined Players:\n"
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text='Join', callback_data='join', url='https://t.me/vervulfbot?start=join')], [InlineKeyboardButton(text='Force Start', callback_data='forcestart'), InlineKeyboardButton(text='Stop', callback_data='stop')], [InlineKeyboardButton(text='Next Leader', callback_data='changeLeader')]])
            gameStartMessage = bot.sendMessage(group, startingPlayer +
                                               ' started a new game.\n Join now!', reply_markup=keyboard)
            playerListMessage = bot.sendMessage(group, joinedPlayers)
            leaderMessage = bot.sendMessage(
                group, leaderText_default)
            MessageList.append(gameStartMessage)
            MessageList.append(playerListMessage)
            MessageList.append(leaderMessage)
            # countdownMessage = bot.sendMessage(group, str(
            #     countdownTime) + ' seconds left to join.')
            # countdownMsgID = (group, countdownMessage['message_id'])
            # countdown(countdownMsgID)
            # initializeGame()
        else:
            bot.sendMessage(group, 'A game is already in progress!')
    elif text == '/playerList' or text == '/players@vervulfbot':
        bot.sendMessage(group, joinedPlayers)
    elif text in ('/extendTimer', '/extendTimer@vervulfbot'):
        extendTimer(30)
    elif text == "/start join" and chatType == 'private' and gameInProgress:
        playerName = msg['from']['first_name']
        # playerUsername = msg['from']['username']
        playerID = str(msg['from']['id'])
        # print(playerName)
        # global joinedPlayers
        playerNR = len(playerList)
        if playerNR < 10:
            print(playerNR)
            bot.sendMessage(playerID, 'You have successfully joined the game.')
            x = Player(playerName, playerID)  # , playerUsername)
            if 'username' in msg['from']:
                x.username = msg['from']['username']
            playerList.append(x)
            if playerNR < 10:
                if x.username is not None:
                    joinedPlayers += str(index) + ". " + \
                        x.name + ' (@' + x.username + ')' + '\n'
                else:
                    # + ' - @' #x.username + '\n'
                    joinedPlayers += str(index) + ". " + x.name + '\n'
            else:
                if x.username is not None:
                    joinedPlayers += str(index) + ". " + \
                        x.name + ' (@' + x.username + ')'
                else:
                    joinedPlayers += str(index) + ". " + x.name
            index += 1
            bot.editMessageText(
                (group, playerListMessage['message_id']), joinedPlayers)
        else:
            bot.sendMessage(playerID, 'The game is full.')


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(
        msg, flavor='callback_query')
    global playerNR
    global playerList
    global playerListMessage
    global gameInProgress
    global index
    global leaderIndex
    global currentLeader
    global sage
    global leaderText_default
    global playerList
    global cancelMessage
    global cancelMessage_
    global startingPlayerMessageID
    global leaderMessage
    global MessageList
    global TeamList
    global teamString
    global teamString_default
    global membersInString
    global teamListMessage
    playerNR = len(playerList)
    if query_data == 'changeLeader':
        changeLeader()
    if query_data == 'stop':
        global gameStartMessage
        global playerListMessage
        cancelMessage = bot.sendMessage(group, "Cancelling Game...")
        stopGame()
        time.sleep(3)
        bot.deleteMessage((group, cancelMessage["message_id"]))
    if query_data == 'forcestart':
        initializeGame()
    if query_data == 'join':
        playerName = msg['from']['first_name']
        # playerUsername = msg['from']['username']
        playerID = str(msg['from']['id'])
        # print(playerName)
        global joinedPlayers
        if playerNR < 10:
            x = Player(playerName, playerID)  # , playerUsername)
            playerList.append(x)
            if playerNR < 10:
                joinedPlayers += str(index) + ". " + \
                    x.name + '\n'  # + ' - @' #x.username + '\n'
            else:
                joinedPlayers += str(index) + ". " + x.name + \
                    ' - @'  # + x.username + ' - ' + x.id
            index += 1
            bot.editMessageText(
                (group, playerListMessage['message_id']), joinedPlayers)
    if str(from_id) == currentLeader.id:
        for player in playerList:
            if query_data == player.nr:
                if len(TeamList) < missionList[missionIndex].teamSize:
                    if player not in TeamList:
                        TeamList.append(player)
                        print(TeamList)
                    else:
                        print('Player already in team.')
                else:
                    print('Team is full.')
                print(player.name + ' - ' + player.nr)
        for teamMember in TeamList:
            if teamMember not in membersInString:
                teamString += teamMember.name + '\n'
                membersInString.append(teamMember)
                bot.editMessageText((currentLeader.id, teamListMessage['message_id']), teamString)
    if query_data == 'passleader':
        changeLeader()
    if query_data == 'teamconfirm':
        #confirm team
        print('confirm team')
    if query_data == 'resetteam':
        TeamList = []
        membersInString = []
        teamString = teamString_default
        bot.editMessageText((currentLeader.id, teamListMessage['message_id']),teamString)
        print(TeamList)


def assignRoles(mode):
    global playerNR
    usedRoles = []
    playerNR = len(playerList)
    i = 0
    while i < playerNR:
        rrole = randint(0, playerNR - 1)
        if rrole not in usedRoles:
            playerList[i].role = rrole
            usedRoles.append(rrole)
            i += 1
    for player in playerList:
        player.role = roles[modes[mode]][player.role]
        # print(player.id + ' - ' + player.name + ' - ' + player.role)


def createMissionList():
    global missionIndex
    missionIndex = 0
    for i in range(5):
        x = Mission(i + 1, teamSize[playerNR][i])
        missionList.append(x)


def nextMission():
    global missionIndex
    missionIndex += 1
    print('Current Mission: ', missionList[missionIndex].nr,
          '\n', 'Team Size: ', missionList[missionIndex].teamSize)


def chooseLeader():
    global leaderIndex
    global currentLeader
    global leaderMessage
    global leaderText_default
    global playerList
    global leaderText_final
    global teamSelectMessage
    global teamString
    global teamString_default
    global teamListMessage
    teamString = teamString_default
    leaderIndex = randint(0, len(playerList) - 1)
    currentLeader = playerList[leaderIndex]
    if currentLeader.username is not None:
        leaderText_final = leaderText_default + \
            currentLeader.name + ' (@' + currentLeader.username + ')'
    else:
        leaderText_final = leaderText_default + currentLeader.name
    bot.editMessageText(
        (group, leaderMessage['message_id']), leaderText_final)
    generateTeamSelectKeyboard()


def generateTeamSelectKeyboard():
    global playerList
    global pListInlineKeyboard
    global teamSelectKeyboard
    global teamSelectMessage
    global teamListMessage
    for i in range(len(playerList)):
        playerList[i].nr = 'P' + str(i + 1) + ') '
    pListInlineKeyboard = []
    for player in playerList:
        pListInlineKeyboard.append([InlineKeyboardButton(
            text=player.nr + player.name, callback_data=player.nr)])
    pListInlineKeyboard.append([InlineKeyboardButton(text='Pass Leader', callback_data='passleader')])
    pListInlineKeyboard.append([InlineKeyboardButton(text='Reset Selection', callback_data='resetteam'),InlineKeyboardButton(text='Confirm Team', callback_data='teamconfirm')])
    teamSelectKeyboard = InlineKeyboardMarkup(
        inline_keyboard=pListInlineKeyboard)
    teamSelectMessage = bot.sendMessage(
        currentLeader.id, 'Select a team to go on the mission: ', reply_markup=teamSelectKeyboard)
    teamListMessage = bot.sendMessage(currentLeader.id, teamString_default)


def changeLeader():
    global leaderIndex
    global currentLeader
    global leaderMessage
    global leaderText_default
    global playerList
    global teamSelectMessage
    global teamString
    global teamString_default
    global teamListMessage
    global TeamList
    global membersInString
    teamString = teamString_default
    TeamList = []
    membersInString = []
    bot.deleteMessage((currentLeader.id, teamSelectMessage['message_id']))
    bot.deleteMessage((currentLeader.id, teamListMessage['message_id']))
    if leaderIndex == len(playerList) - 1:
        leaderIndex = 0
    else:
        leaderIndex += 1
    lastLeader = currentLeader
    currentLeader = playerList[leaderIndex]
    try:
        if currentLeader.name != lastLeader.name:
            bot.editMessageText(
                (group, leaderMessage['message_id']), leaderText_default + currentLeader.name)
        teamSelectMessage = bot.sendMessage(
            currentLeader.id, 'Select a team to go on the mission: ', reply_markup=teamSelectKeyboard)
        teamListMessage = bot.sendMessage(currentLeader.id, teamString_default)
    except Exception as e:
        print(e)


def initializeGame():
    global knownSpies
    global allSpies
    global enemySpyList
    global allySpyList
    global commanderList
    global enemySpyList_default
    global allySpyList_default
    global commanderList_default
    global cancelMessage
    global cancelMessage_
    global playerNR
    # try
    playerNR = len(playerList)
    if playerNR >= 5:
        assignRoles('normal')
        sendRoleMessages()
        chooseLeader()
        createMissionList()
    else:
        cancelMessage_ = bot.sendMessage(
            group, 'Not enough players. Cancelling game.')
        stopGame()
        time.sleep(3)
        bot.deleteMessage((group, cancelMessage_["message_id"]))
    # except:
    #     bot.sendMessage(group, 'Something came up...')


def stopGame():
    try:
        global gameStartMessage
        global playerListMessage
        global gameInProgress
        global joinedPlayers
        global playerList
        global leaderMessage
        global startingPlayerMessageID
        global MessageList
        if gameInProgress:
            gameInProgress = False
            playerList = []
            usedRoles = []
            joinedPlayers = "Joined Players:\n"

            bot.deleteMessage((group, startingPlayerMessageID))
            for mesaj in MessageList:
                bot.deleteMessage((group, mesaj['message_id']))
            MessageList = []
    except Exception as e:
        print(e)
        # bot.sendMessage(group, 'Something came up...')


def countdown(msg_id):
    countdownTime = 30
    while countdownTime >= 0:
        playerNR = len(playerList)
        countdownTime -= 1
        if countdownTime in (60, 45, 30, 15, 10, 5, 4, 3, 2):
            bot.editMessageText(msg_id,  str(
                countdownTime) + ' seconds left to join.')
        elif countdownTime == 1:
            bot.editMessageText(msg_id,  str(
                countdownTime) + ' second left to join.')
        elif countdownTime == 0:
            bot.deleteMessage((msg_id))
        time.sleep(1)


def MissionSuccess():
    missionList[missionIndex].isSuccessful = True
    nextMission()


def MissionFail():
    missionList[missionIndex].isSuccessful = False
    nextMission()


def CheckMissionState():
    if True:
        MissionSuccess()
    else:
        MissionFail()


def extendTimer(x):
    if x in range(1, 91):
        countdownTime += x

try:
    print('Running...')
    MessageLoop(bot, {'chat': on_chat_message,
                      'callback_query': on_callback_query}).run_as_thread()

    # while 1:
    #     initializeGame()

except:
    print('Something came up.')


try:
    while 1:
        time.sleep(10)
except:
    print('Program Stopped')
