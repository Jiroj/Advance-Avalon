import os
import random
import shutil
import sys

def main():

        players = ["Bacon", "Choki", "Ferlyn", "Geo", "Hish", "Kappy", "Karina", "Montana", "Nobie", "Jay"]

        if not (len(players) is 10):
                print("Invalid number of players")
                exit(1)
                
        num_players = len(players)
        players = set(players) # use as set to avoid duplicate players
        players = list(players) # convert to list
        random.shuffle(players) # ensure random order, though set should already do that

        if len(players) != num_players:
                print("No duplicate player names")
                exit(1)

        # choose 3 players
        three_players = random.sample(players, 3)

        # first two proppose for the first mission, last is starting player of second round
        first_mission_proposers = three_players[:2]
        second_mission_starter = three_players[2]

        all_good_roles_in_order = ["Percival", "Merlin", "Galahad", "Tristan", "Iseult", "Uther", "Arthur", "Lancelot", "Guinevere", "Ygraine", "Gawain", "Titania"]
        all_evil_roles_in_order = ["Mordred", "Morgana", "Maleagant", "Agravaine", "Colgrevance", "Oberon"]

        # assign the roles in the game
        good_roles = ["Percival", "Merlin", "Tristan", "Iseult", "Arthur", "Lancelot", "Guinevere", "Gawain", "Titania"]
        evil_roles = ["Mordred", "Morgana", "Maleagant", "Agravaine", "Colgrevance", "Oberon"]

        # shuffle the roles
        random.shuffle(good_roles)
        random.shuffle(evil_roles)

        # determine the number of roles in the game
        if num_players == 10:
                num_evil = 4
                num_good = 6
        elif num_players == 9:
                num_evil  = 3
                num_good = 4
        elif num_players == 7 or num_players == 8:
                num_evil = 3
                num_good = num_players - num_evil
        else: # 5 or 6
                num_evil = 2
                num_good = num_players - num_evil

        # assign players to teams
        assignments = {}
        reverse_assignments = {}
        good_roles_in_game = set()
        evil_roles_in_game = set()
        good_players = players[:num_good]
        evil_players = players[num_good:num_good + num_evil]

        # assign good roles
        for good_player in good_players:
                player_role = good_roles.pop()
                assignments[good_player] = player_role
                reverse_assignments[player_role] = good_player
                good_roles_in_game.add(player_role)

        # assign evil roles
        for evil_player in evil_players:
                player_role = evil_roles.pop()
                assignments[evil_player] = player_role
                reverse_assignments[player_role] = evil_player
                evil_roles_in_game.add(player_role)

        # lone tristan
        if ("Tristan" in good_roles_in_game and "Iseult" not in good_roles_in_game and num_players >= 7):
                good_roles_in_game.remove("Tristan")
                good_roles_in_game.add("Uther")
                tristan_player = reverse_assignments["Tristan"]
                assignments[tristan_player] = "Uther"
                del reverse_assignments["Tristan"]
                reverse_assignments["Uther"] = tristan_player

        # lone iseult
        if ("Iseult" in good_roles_in_game and "Tristan" not in good_roles_in_game and num_players >= 7):
                good_roles_in_game.remove("Iseult")
                good_roles_in_game.add("Uther")
                iseult_player = reverse_assignments["Iseult"]
                assignments[iseult_player] = "Uther"
                del reverse_assignments["Iseult"]
                reverse_assignments["Uther"] = iseult_player
                
        # lone guinevere -> ygraine
        if ("Guinevere" in good_roles_in_game and "Lancelot" not in good_roles_in_game and "Arthur" not in good_roles_in_game and "Maleagant" not in evil_roles_in_game and num_players >= 7):
                good_roles_in_game.remove("Guinevere")
                good_roles_in_game.add("Ygraine")
                guinevere_player = reverse_assignments["Guinevere"]
                assignments[guinevere_player] = "Ygraine"
                del reverse_assignments["Guinevere"]
                reverse_assignments["Ygraine"] = guinevere_player
                
        # lone percival -> galahad
        if ("Percival" in good_roles_in_game and "Merlin" not in good_roles_in_game and "Morgana" not in evil_roles_in_game and num_players >= 7):
                good_roles_in_game.remove("Percival")
                good_roles_in_game.add("Galahad")
                percival_player = reverse_assignments["Percival"]
                assignments[percival_player] = "Galahad"
                del reverse_assignments["Percival"]
                reverse_assignments["Galahad"] = percival_player

        # delete and recreate game directory
        if os.path.isdir("game"):
                shutil.rmtree("game")
        os.mkdir("game")

        # make every role's file
        # Merlin sees: Morgana, Maleagant, Oberon, Agravaine, Colgrevance, Lancelot* as evil
        if "Merlin" in good_roles_in_game:
                # determine who Merlin sees
                seen = []
                for evil_player in evil_players:
                        if assignments[evil_player] != "Mordred":
                                seen.append(evil_player)
                                
                if "Lancelot" in good_roles_in_game:
                        seen.append(reverse_assignments["Lancelot"])
                        
                random.shuffle(seen)
                
                # and write this info to Merlin's file
                player_name = reverse_assignments["Merlin"]
                filename = "game/" + player_name + ".txt"
                with open(filename, "w") as file:
                        file.write("You are Merlin.\n")
                        for seen_player in seen:
                                file.write("You see " + seen_player + " as evil (or Lancelot).\n")

        # Percival sees Merlin, Morgana* as Merlin
        if "Percival" in good_roles_in_game:
                # determine who Percival sees
                seen = []

                if "Merlin" in good_roles_in_game:
                        seen.append(reverse_assignments["Merlin"])
                if "Morgana" in evil_roles_in_game:
                        seen.append(reverse_assignments["Morgana"])

                random.shuffle(seen)
                
                # and write this info to Percival's file
                player_name = reverse_assignments["Percival"]
                filename = "game/" + player_name + ".txt"
                with open(filename, "w") as file:
                        file.write("You are Percival.\n")
                        for seen_player in seen:
                                file.write("You see " + seen_player + " as Merlin (or Morgana).\n")

        if "Tristan" in good_roles_in_game:
                # write the info to Tristan's file
                player_name = reverse_assignments["Tristan"]
                filename = "game/" + player_name + ".txt"
                with open(filename, "w") as file:
                        file.write("You are Tristan.\n")
                        # write Iseult's info to file
                        if "Iseult" in good_roles_in_game:
                                iseult_player = reverse_assignments["Iseult"]
                                if "Oberon" in evil_roles_in_game:
                                        player_name = reverse_assignments["Oberon"]
                                        if (random.choice([True, False])):
                                                file.write(player_name + " is your lover.\n")
                                                file.write(iseult_player + " is your lover.\n")
                                        else:
                                                file.write(iseult_player + " is your lover.\n")
                                                file.write(player_name + " is your lover.\n")
                                else:
                                        file.write(iseult_player + " is your lover.\n")
                        else:
                                file.write("Nobody loves you. Not even your cat.\n")

        if "Iseult" in good_roles_in_game:
                # write this info to Iseult's file
                player_name = reverse_assignments["Iseult"]
                filename = "game/" + player_name + ".txt"
                with open(filename, "w") as file:
                        file.write("You are Iseult.\n")
                        # write Tristan's info to file
                        if "Tristan" in good_roles_in_game:
                                tristan_player = reverse_assignments["Tristan"]
                                if "Oberon" in evil_roles_in_game:
                                        player_name = reverse_assignments["Oberon"]
                                        if (random.choice([True, False])):
                                                file.write(player_name + " is your lover.\n")
                                                file.write(tristan_player + " is your lover.\n")
                                        else:
                                                file.write(tristan_player + " is your lover.\n")
                                                file.write(player_name + " is your lover.\n")
                                else:
                                        file.write(tristan_player + " is your lover.\n")
                        else:
                                file.write("Nobody loves you.\n")
                                
        if "Lancelot" in good_roles_in_game:
                # write ability to Lancelot's file
                player_name = reverse_assignments["Lancelot"]
                filename = "game/" + player_name + ".txt"
                with open(filename, "w") as file:
                        file.write("You are Lancelot. You are on the Good team. \n\n")
                        file.write("Ability: Reversal \n")
                        file.write("You are able to play Reversal cards while on missions. A Reversal card inverts the result of a mission; a mission that would have succeeded now fails and vice versa. \n \n")

        if "Guinevere" in good_roles_in_game:
                # guinevere sees two random "rumors"
                # rumors currently are only player knowledge (e.g. A sees B)
                rumors = []
                truths = []
                lies = []
                connections = []

                not_guin = list(set(players) - set([reverse_assignments["Guinevere"]]))
                if "Mordred" in evil_roles_in_game:
                        not_guin.remove(reverse_assignments["Mordred"])

                for player in not_guin:
                        other_players = list(set(not_guin)-set([player]))
                        for other_player in other_players:
                                connections.append([player,other_player])

                #lies = list(set(connections)-set(truths))
                #lies = connections.remove(set(truths))
                evil_players_no_obemord = list(set(evil_players))
                evil_players_no_mordred = list(set(evil_players))

                if "Mordred" in evil_roles_in_game:
                        evil_players_no_obemord.remove(reverse_assignments["Mordred"])

                if "Oberon" in evil_roles_in_game:
                        evil_players_no_obemord.remove(reverse_assignments["Oberon"])

                #if "Colgrevance" in evil_roles_in_game:
                #        evil_players_no_obemord.remove(reverse_assignments["Colgrevance"])

                # rumor generation here
                for evil_player in evil_players_no_obemord:
                        other_evil_players = list(set(evil_players_no_obemord) - set([evil_player]))
                        for evil_player_two in other_evil_players:
                                truths.append([evil_player,evil_player_two])

                if "Oberon" in evil_roles_in_game:
                        oberon = reverse_assignments["Oberon"]
                        for evil_player_not_oberon in evil_players_no_obemord:
                                truths.append([oberon,evil_player_not_oberon])

                if "Merlin" in good_roles_in_game:
                        merlin = reverse_assignments["Merlin"]
                        for evil_player_not_mordred in evil_players_no_mordred:
                                truths.append([merlin,evil_player_not_mordred])
                        if "Lancelot" in good_roles_in_game:
                                lancelot = reverse_assignments["Lancelot"]
                                truths.append([merlin,lancelot])

                if "Percival" in good_roles_in_game:
                        percival = reverse_assignments["Percival"]
                        if "Merlin" in good_roles_in_game:
                                merlin = reverse_assignments["Merlin"]
                                truths.append([percival,merlin])
                        if "Morgana" in evil_roles_in_game:
                                morgana = reverse_assignments["Morgana"]
                                truths.append([percival,morgana])

                if "Tristan" in good_roles_in_game:
                        tristan = reverse_assignments["Tristan"]
                        if "Iseult" in good_roles_in_game:
                                iseult = reverse_assignments["Iseult"]
                                truths.append([tristan,iseult])
                                truths.append([iseult,tristan])

                if "Arthur" in good_roles_in_game:
                        arthur = reverse_assignments["Arthur"]
                        guinevere = reverse_assignments["Guinevere"]
                        good_players_no_arthur = list(set(good_players) - set([arthur,guinevere]))
                        for good_player in good_players_no_arthur:
                                truths.append([arthur,good_player])

                lies = [lie for lie in connections if lie not in truths]
                random.shuffle(truths)
                random.shuffle(lies)
                guin_truths = []
                guin_lies = []

                if len(truths) > 0:
                        new_truth = truths.pop(0)
                        converse_truth = [new_truth[1],new_truth[0]]
                        lies = [lie for lie in lies if lie != converse_truth]
                        truths = [truth for truth in truths if truth != converse_truth]
                        rumors.append(new_truth)
                        guin_truths.append(new_truth)
                        new_lie = lies.pop(0)
                        converse_lie = [new_lie[1],new_lie[0]]
                        lies = [lie for lie in lies if lie != converse_lie]
                        truths = [truth for truth in truths if truth != converse_lie]
                        rumors.append(new_lie)
                        guin_lies.append(new_lie)

                if len(truths) > 0 and (num_players >= 7):
                        new_truth = truths.pop(0)
                        converse_truth = [new_truth[1],new_truth[0]]
                        lies = [lie for lie in lies if lie != converse_truth]
                        truths = [truth for truth in truths if truth != converse_truth]
                        rumors.append(new_truth)
                        guin_truths.append(new_truth)

                random.shuffle(rumors)
                # and write this info to Guinevere's file
                player_name = reverse_assignments["Guinevere"]
                filename = "game/" + player_name + ".txt"

                with open(filename, "w") as file:
                        file.write("You are Guinevere.\n\n")
                        for rumor in rumors:
                                file.write("{} knows something about {}.\n".format(rumor[0],rumor[1]))
                                
        if "Arthur" in good_roles_in_game:
                # determine which roles Arthur sees
                seen = []
                for good_role in good_roles_in_game:
                        seen.append(good_role)
                random.shuffle(seen)

                # and write this info to Arthur's file
                player_name = reverse_assignments["Arthur"]
                filename = "game/" + player_name + ".txt"

                with open(filename, "w") as file:
                        file.write("You are Arthur.\n\n")
                        file.write("The following good roles are in the game:\n")
                        for seen_role in seen:
                                if seen_role != "Arthur":
                                        file.write(seen_role + "\n")
                        file.write("\n")
                        file.write("Ability: Proclamation\n")
                        file.write("Once 2 quests have failed. You may formally decare yourself as Arthur and guaranteed good, you will no longer be a target for assasination\n")
                        file.write("OR\n")
                        file.write("In the event that evil wins by questing, you will select 4 players to execute. If you correctly name the entire evil team, Good wins the game.\n")
                        
        if "Gawain" in good_roles_in_game:

                # determine what Gawain sees
                seen = []
                player_name = reverse_assignments["Gawain"]
                good_players_no_gawain = set(good_players) - set([player_name])

                # guaranteed see a good player
                seen_good = random.sample(good_players_no_gawain, 1)
                seen.append(seen_good[0])

                # choose two other players randomly
                remaining_players = set(players) - set([player_name]) - set(seen_good)
                seen += random.sample(remaining_players, 2)
                random.shuffle(seen)

                # write info to Gawain's file
                filename = "game/" + player_name + ".txt"
                with open(filename, "w") as file:
                        file.write("You are Gawain.\n\n")
                        file.write("The following players are not all evil:\n")
                        for seen_player in seen:
                                file.write(seen_player + "\n")
                        file.write("\nAbility: Whenever a mission (other than the 1st) is sent, you may declare as Gawain to reveal a single person's played mission card. The mission card still affects the mission. (This ability functions identically to weak Inquisition and occurs after regular Inquisitions.) If the card you reveal is a Success, you are immediately 'Exiled' and may not go on missions for the remainder of the game, although you may still vote and propose missions.\n\n")
                        file.write("You may use this ability once per mission as long as you are not 'Exiled'. You may choose to not use your ability on any round, even if you would be able to use it.\n");

        stalked_good = None;

        if "Uther" in good_roles_in_game:
                # write this info to Uther's file
                player_name = reverse_assignments["Uther"]
                filename = "game/" + player_name + ".txt"
                good_players_no_uther = set(good_players) - set([player_name])
                stalked_good = random.sample(good_players_no_uther, 1)[0]

                with open(filename, "w") as file:
                        file.write("You are Uther.\n")
                        file.write("You are stalking " + stalked_good + "; they are also good.\n")
                        # write Uther's info to file

        stalked_evil = None;
        if "Ygraine" in good_roles_in_game:
                # write this info to Ygraine's file
                player_name = reverse_assignments["Ygraine"]
                filename = "game/" + player_name + ".txt"
                evil_players_no_mordred = set(evil_players)

                if "Mordred" in evil_roles_in_game:
                        evil_players_no_mordred = set(evil_players) - set(reverse_assignments["Mordred"])

                stalked_evil = random.sample(evil_players_no_mordred, 1)[0]

                with open(filename, "w") as file:
                        file.write("You are Ygraine.\n")
                        file.write("You are stalking " + stalked_evil + "; they are evil.\n")
                        file.write("\n (The following roles are not in the game: Guinevere, Lancelot, Arthur, and Maleagant.)\n")

        if "Galahad" in good_roles_in_game:
                # determine which roles Galahad sees
                seen = []
                for evil_role in evil_roles_in_game:
                        seen.append(evil_role)
                random.shuffle(seen)

                # and write this info to Arthur's file
                player_name = reverse_assignments["Galahad"]
                filename = "game/" + player_name + ".txt"

                with open(filename, "w") as file:
                        file.write("You are Galahad.\n\n")
                        file.write("The following evil roles are in the game:\n")
                        for seen_role in seen:
                                        file.write(seen_role + "\n")
                        file.write("\n (The following roles are not in the game: Percival, Merlin, and Morgana.)\n")

        if "Titania" in good_roles_in_game:
                player_name = reverse_assignments["Titania"]
                filename = "game/" + player_name + ".txt"
                if "Colgrevance" in evil_roles_in_game:
                  with open(filename, "w") as file:
                    file.write("You are Titania. You are on the Good team.\n")
                    file.write("\nyou have left your changeling in the court of Colgrevance. Enjoy your mischief.\n\n")
                else:
                  with open(filename, "w") as file:
                    file.write("You are Titania. You are on the Good team.\n")
                    file.write("\nAbility: Sleep. Once a game, after the first quest is complete you may Declare as Titania to cause one player on an approved team to fall asleep and forget to quest.\n")
                    file.write("Note: You must act prior to the member actually questing, if planning to use your ability declare with a mod when you vote on the team.\n\n")

        # make list of evil players seen to other evil
        evil_players_no_oberon_or_colgrevance = list(set(evil_players))
        if "Oberon" in evil_roles_in_game:
                evil_players_no_oberon_or_colgrevance = list(set(evil_players_no_oberon_or_colgrevance) - set([reverse_assignments["Oberon"]]))
                
        if "Colgrevance" in evil_roles_in_game:
                evil_players_no_oberon_or_colgrevance = list(set(evil_players_no_oberon_or_colgrevance) - set([reverse_assignments["Colgrevance"]]))

        random.shuffle(evil_players_no_oberon_or_colgrevance)

        if "Mordred" in evil_roles_in_game:
                player_name = reverse_assignments["Mordred"]
                filename = "game/" + player_name + ".txt"
                with open(filename, "w") as file:
                        file.write("You are Mordred.\n")
                        for evil_player in evil_players_no_oberon_or_colgrevance:
                                if evil_player != player_name:
                                        file.write(evil_player + " is a fellow member of the evil council.\n")
                        if "Oberon" in evil_roles_in_game:
                                file.write("There is an Oberon lurking in the shadows.\n")
                        if "Colgrevance" in evil_roles_in_game:
                                file.write("Colgrevance is watching you.\n")
                                
        if "Morgana" in evil_roles_in_game:
                player_name = reverse_assignments["Morgana"]
                filename = "game/" + player_name + ".txt"
                with open(filename, "w") as file:
                        file.write("You are Morgana.\n")
                        for evil_player in evil_players_no_oberon_or_colgrevance:
                                if evil_player != player_name:
                                        file.write(evil_player + " is a fellow member of the evil council.\n")
                        if "Oberon" in evil_roles_in_game:
                                file.write("There is an Oberon lurking in the shadows.\n")
                        if "Colgrevance" in evil_roles_in_game:
                                file.write("Colgrevance is watching you.\n")

                        choice = random.choice(['1', '2', '3', '4'])

                        file.write("\nAbility: Once per game, when it is your turn to propose a team you may instead declare as Morgana and give up your turn to:\n")
                        if choice is '1':
                                file.write("\nFlip. The next team is made by the person who appears last on the list, and will then proceed up the list towards the first team Leader.\n")
                        elif choice is '2':
                                file.write("\nReverse. The next team is made by the player who led the last completed mission. Play proceeds in reverse order (back up the list towards the first team Leader).\n")
                        elif choice is '3':
                                file.write("\nShuffle. A completely new leader order will be created randomly, the old list will no longer apply.\n")
                        elif choice is '4':
                                file.write("\nMorgana\'s choice. You will be allowed to choose to either Flip, Reverse or Shuffle player order.\n")
                                
        if "Oberon" in evil_roles_in_game:
                player_name = reverse_assignments["Oberon"]
                filename = "game/" + player_name + ".txt"
                with open(filename, "w") as file:
                        file.write("You are Oberon.\n\n")
                        for evil_player in evil_players_no_oberon_or_colgrevance:
                                file.write(evil_player + " is a member of the evil council.\n\n")
                        if "Tristan" in good_roles_in_game and "Iseult" in good_roles_in_game:
                                file.write("you have dosed the lovers with a potion of your own making. They both love you. Enjoy your mischief.\n\n")
                        else:
                                file.write("Ability: You may, onece in the game after the first quest is complete, declare yourself in order to block the next team leader from making a team. The proposal will go to the next player in the list.\n")
                                file.write("Note: Once team is made the ability may not be used, if planning to use the ability declare with the mod when you vote on the quest.\n")
                        if "Colgrevance" in evil_roles_in_game:
                                file.write("Colgrevance is watching you.\n")
        if "Agravaine" in evil_roles_in_game:
                player_name = reverse_assignments["Agravaine"]
                filename = "game/" + player_name + ".txt"
                with open(filename, "w") as file:
                        file.write("You are Agravaine.\n")
                        for evil_player in evil_players_no_oberon_or_colgrevance:
                                if evil_player != player_name:
                                        file.write(evil_player + " is a fellow member of the evil council.\n")
                        if "Oberon" in evil_roles_in_game:
                                file.write("There is an Oberon lurking in the shadows.\n")
                        if "Colgrevance" in evil_roles_in_game:
                                file.write("Colgrevance is watching you.\n")
                        file.write("\nAbility: On any mission you are on, after the mission cards have been revealed, should the mission not result in a Fail (such as via a Reversal, requiring 2 fails, or other mechanics), you may formally declare as Agravaine to force the mission to Fail anyway.\n\n");
                        file.write("Drawback: You may only play Fail cards while on missions.\n\n");
                        file.write("Note: Ability to declare is only valid after the first quest and until 2 quests have failed\n")
                        
        if "Maleagant" in evil_roles_in_game:
                # write ability to Maleagant's file
                player_name = reverse_assignments["Maleagant"]
                filename = "game/" + player_name + ".txt"
                with open(filename, "w") as file:
                        file.write("You are Maleagant. \n\n")
                        for evil_player in evil_players_no_oberon_or_colgrevance:
                                if evil_player != player_name:
                                        file.write(evil_player + " is a fellow member of the evil council.\n")
                        if "Oberon" in evil_roles_in_game:
                                file.write("There is an Oberon lurking in the shadows.\n")
                        if "Colgrevance" in evil_roles_in_game:
                                file.write("Colgrevance is watching you.\n")
                        file.write("\nAbility: Reversal \n")
                        file.write("You are able to play Reversal cards while on missions. A Reversal card inverts the result of a mission; a mission that would have succeeded now fails and vice versa. \n \n")
                        
        if "Colgrevance" in evil_roles_in_game:
                player_name = reverse_assignments["Colgrevance"]
                filename = "game/" + player_name + ".txt"
                Colgrevance_Truth = []
                Colgrevance_Lies = []
                if "Titania" in good_roles_in_game:
                        with open(filename, "w") as file:
                                file.write("You are Colgrevance.\n")
                                randomPlayer = random.randint(0, num_evil-1)
                                randomGoodPlayer = random.randint(0, num_good-1)
                                counter = 0
                                for evil_player in evil_players:
                                        if evil_player != player_name:
                                                if counter is randomPlayer:
                                                        file.write(good_players[randomGoodPlayer] + " is " + assignments[evil_player] + ".\n")
                                                        counter += 1
                                                        Colgrevance_Lies.append([good_players[randomGoodPlayer], assignments[evil_player]])
                                                else:
                                                        file.write(evil_player + " is " + assignments[evil_player] + ".\n")
                                                        Colgrevance_Truth.append([evil_player, assignments[evil_player]])
                                                        counter += 1
                                file.write("\nYour information may be corrupted by Titania\n")
                else:
                        with open(filename, "w") as file:
                                file.write("You are Colgrevance.\n")
                                for evil_player in evil_players:
                                        if evil_player != player_name:
                                                file.write(evil_player + " is " + assignments[evil_player] + ".\n")

        # TODO: pelinor + questing beast
        if num_players == 9:
                # write pelinor's information
                pelinor_filename = "game/" + pelinor + ".txt"
                with open(pelinor_filename, "w") as file:
                        file.write("You are Pelinor.\n\n")
                        file.write("You win if one of the following conditions are met:\n")
                        file.write("[1]: No Questing Beast Was Here cards are played.\n")
                        file.write("[2]: You are on a mission where a Questing Beast Was Here Card is played, and three missions succeed.\n")
                        file.write("[3]: If neither of the previous two conditions are met at the end of the game, you declare as Pelinor prior to Assassination and name the person you believe to be the Questing Beast. You are told if you are correct at the conclusion of any other post-game phases. If you are correct, you win.\n")

                questing_beast_filename = "game/" + questing_beast + ".txt"
                with open(questing_beast_filename, "w") as file:
                        file.write("You are the Questing Beast.\n")
                        file.write("You must play the 'Questing Beast Was Here' card on missions. Once per game, you can play a Success card instead of a Questing Beast Was Here card.\n\n")
                        file.write("You win if all of the following conditions are met:\n")
                        file.write("[1]: You play at least one Questing Beast Was Here card.\n")
                        file.write("[2]: Either a) Pelinor is never on a mission where a Questing Beast Was Here card is played; or b) 3 Quests fail.\n\n")
                        file.write("[3]: Pelinor fails to identify you after the conclusion of the game.\n\n")
                        file.write(pelinor + " is Pelinor.\n")
        # hijack
        bonus_ability_hijack = 0
        if (num_players >= 7):
                if "Mordred" in evil_roles_in_game:
                        evil_players_no_mordred = list(set(evil_players) - set([reverse_assignments["Mordred"]]))
                else:
                        evil_players_no_mordred = list(set(evil_players))
                random.shuffle(evil_players_no_mordred)
                bonus_ability_hijack = evil_players_no_mordred[0]
                bonus_hijack_filename = "game/" + bonus_ability_hijack + ".txt"

                with open(bonus_hijack_filename, "a") as file:
                        file.write("\n \n \nYou also have the following ability, in addition to any other abilities you may possess.")
                        file.write("\nAbility: Should any mission get to the last proposal of the round, after the people on the mission have been named, you may declare as Evil to replace one person on that mission with yourself.\n\n")
                        file.write("Note: You may not use this ability after two missions have already failed. Furthermore, you may only use this ability once per game.\n");

        # write start file
        with open("game/start.txt", "w") as file:
                file.write("The players proposing teams for the first mission are:\n")
                team_lead = players
                
                for first_mission_proposer in first_mission_proposers:
                        file.write(first_mission_proposer + "\n")
                        team_lead.remove(first_mission_proposer)

                file.write("\n" + second_mission_starter + " is the starting player of the 2nd round.\n")
                team_lead.remove(second_mission_starter)
                random.shuffle(team_lead)
                file.write("\nThe next team lead will be the following:\n")
                counter = 3
                
                for leader in team_lead:
                        file.write("[Mission {}] {} \n".format(counter, leader))
                        counter += 1

        # write do not open
        with open("game/DoNotOpen.txt", "w") as file:
                file.write("Player -> Role\n\nGOOD TEAM:\n")
                for role in all_good_roles_in_order:
                        if role in reverse_assignments:
                                file.write(reverse_assignments[role] + " -> " + role + "\n")

                file.write("\n\nEVIL TEAM:\n")
                for role in all_evil_roles_in_order:
                        if role in reverse_assignments:
                                file.write(reverse_assignments[role] + " -> " + role + "\n")

                file.write("\n\nMISCELLANEOUS:\n")
                file.write("[Mission 1] {}, {}\n".format(first_mission_proposers[0],first_mission_proposers[1]))
                file.write("[Mission 2] {} \n".format(second_mission_starter))

                counter = 3
                for leader in team_lead:
                        file.write("[Mission {}] {} \n".format(counter, leader))
                        counter += 1

                if bonus_ability_hijack:
                        file.write("[Hijack] " + bonus_ability_hijack + "\n")

                if "Guinevere" in good_roles_in_game:
                        for truth in guin_truths:
                                file.write("[Guinevere: Truth] {} -> {}\n".format(truth[0],truth[1]))
                        for lie in guin_lies:
                                file.write("[Guinevere: Lie] {} -> {}\n".format(lie[0],lie[1]))

                if "Colgrevance" in evil_roles_in_game:
                        for truth in Colgrevance_Truth:
                                file.write("[Colgrevance: Truth] {} -> {}\n".format(truth[0], truth[1]))
                        for lie in Colgrevance_Lies:
                                file.write("[Colgrevance: Lie] {} -> {}\n".format(lie[0], lie[1]))

if __name__ == "__main__":
        main()
