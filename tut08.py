import os
os.chdir('C:\\Users\\dell\\Documents\\GitHub\\2001CB60_2022\\tut08')
from datetime import datetime
start_time = datetime.now()

from platform import python_version
ver = python_version()

import re
if ver == "3.8.10":
	print("Correct Version Installed")
else:
	print("Please install 3.8.10. Instruction are present in the GitHub Repo/Webmail. Url: https://pastebin.com/nvibxmjw")

def scorecard(inns,filename,team):
	# defining each type of variable
	gross_balls=0
	extras=0
	wides_1=0
	total_1=0
	wicket_1=0
	leg_byes_=0
	byes_1=0
	powerplay_runs=0
	maiden_balls=0
	runs_at_fow=[] # lists to store the runs, wickets, over and player name at fall of wicket
	wickets_at_fow=[]
	over_at_fow=[]
	player_=[]
	player=''
	players_batted={} # all players batted in an innings
	players_bowled={} # all players bowled in an innings.
	# reading file to read all lines.
	with open(filename,'r') as f1:
		lines=f1.readlines()
	# storing players' names to a list from teams.txt
	with open('teams.txt','r') as f2:
		pak_players=f2.readlines()[inns] # since team names are in different rows, we extract using indexing a/c to whose innings we are writing currently.
		team_list=pak_players.split(',')
		team_list[0]=team_list[0].split(':')
		team_list[0]=team_list[0][1]
		team_list[-1]=team_list[-1][:-1]
	# for one line in all lines
	for line in lines:
		pattern=re.compile(r'\d{1,6}(\s[A-Z][a-z]+)?(\s[A-Z][a-z]+)\sto(\s[A-Z][a-z]+)?(\s[A-Z][a-z]+)')  # finding the format '1.6 bowler to batsman'
		pattern2=re.compile(r'[\.|!]\s([A-Z][a-z]+\s)?([A-Z][a-z]+\s)([A-Z a-z]*b\s[A-Z a-z]+)\s(\d{0,9})\((\d{0,9})\)([\[\(a-z0-9- \)\]]*)') # finding the format '. Batsman c catcher b bowler run(ball) [4s-fours 6s- sixes]'
		pattern3=re.compile(r'\sto(\s[A-Z][a-z]+)?(\s[A-Z][a-z]+),\s([no|1|2|3|5|wide]+)') # finding the format ' to batsman, runs given/wide'
		pattern4=re.compile(r'\sto(\s[A-Z][a-z]+)?(\s[A-Z][a-z]+),\s([2|3|4|5])\s[wides]+,') # finding the format ' to batsman, 2/3/4/5 wides,'
		pattern5=re.compile(r'(\s[a-z]+)?(\s[A-Z][a-z]+),\s([SIX|FOUR]+)') # finding the format ' batsman, SIX/FOUR'
		pattern6=re.compile(r'\d{0,9}?\d{0,9}\(') # finding the format 'runs(' which would indicate that a wicket is taken.
		pattern7=re.compile(r'(\d{1,9}\.\d{1,6})') # finding the format of current over and ball e.g. '1.6'
		pattern8=re.compile(r'\sto(\s[A-Z][a-z]+)?(\s[A-Z][a-z]+),[ leg byes| byes]+,\s([FOUR|1|2|3]+),?\s') # finding the format ' to batsman, leg byes/byes, 1/2/3/FOUR ,'
		pattern9=re.compile(r'\sto(\s[A-Z][a-z]+)?(\s[A-Z][a-z]+),(\s[no|1|2|3|4|5]+)?([ wide| run]+)s?,') # finding the format ' to batsman, no/1/2/3/4/5 runs/wide'

		player_inn=pattern.finditer(line) # respective matches.
		outs=pattern2.finditer(line)
		run1_inn=pattern3.finditer(line)
		run2_inn=pattern4.finditer(line)
		run3_inn=pattern5.finditer(line)
		wicket_inn=pattern6.finditer(line)
		over_inn=pattern7.finditer(line)
		leg_byes=pattern8.finditer(line)
		wides_inn=pattern9.finditer(line)

		for pl in player_inn: # if match found, but one of group(3) and group(4) is None, add the other to string player and add player name to players_batted.
			if (pl.group(3)!=None) and (pl.group(4)!=None):
				player=pl.group(3)+pl.group(4)
				players_batted.update({pl.group(3)+pl.group(4):['',0,0,0,0,0]}) # each value in list corresponds to the required info for a batter (as present in the scorecard)
			elif (pl.group(3)!=None) and (pl.group(4)==None):
				player=pl.group(3)
				players_batted.update({pl.group(3):['',0,0,0,0,0]})
			elif (pl.group(3)==None) and (pl.group(4)!=None):
				player=pl.group(4)
				players_batted.update({pl.group(4):['',0,0,0,0,0]})
			 # if match found, but one of group(1) and group(2) is None, add the other to string player and add player name to player_bowled.
			if (pl.group(1)!=None) and (pl.group(2)!=None):
				players_bowled.update({pl.group(1)+pl.group(2):[0,0,0,0,0,0]}) # each value in list corresponds to the required info for a bowler (as present in the scorecard)
			elif (pl.group(1)!=None) and (pl.group(2)==None):
				players_bowled.update({pl.group(1):[0,0,0,0,0,0]})
			elif (pl.group(1)==None) and (pl.group(2)!=None):
				players_bowled.update({pl.group(2):[0,0,0,0,0,0]})
			gross_balls+=1
		for run1 in run1_inn: # if matched, increment respective variables to score.
			if run1.group(3)=='1':
				total_1+=1
			elif run1.group(3)=='2':
				total_1+=2
			elif run1.group(3)=='3':
				total_1+=3
			elif run1.group(3)=='5':
				total_1+=5
			elif run1.group(3)=='wide':
				total_1+=1
				extras+=1
				wides_1+=1

		for run2 in run2_inn: # increment extras
			extras+=int(run2.group(3))
			wides_1+=int(run2.group(3))

		for run3 in run3_inn: # increment boundaries to score
			if run3.group(3)=='FOUR':
				total_1+=4
			if run3.group(3)=='SIX':
				total_1+=6
		for wicket in wicket_inn: # increment wickets
			wicket_1+=1
		for over in over_inn: # increment over by matching the starting of a line.
			total_over=over.group(1)
			if total_over=='5.6': # get powerplay runs at end of 6 overs.
				powerplay_runs=total_1
		for leg in leg_byes: # increment legbyes or byes to score and respective extras.
			if leg.group(3)!='FOUR':  
				total_1+=int(leg.group(3))
				extras+=int(leg.group(3))
				leg_byes_+=int(leg.group(3))
			if leg.group(3)=='FOUR':
				leg_byes_+=4
				extras+=4
				total_1+=4
		for out in outs: # if wicket taken, update to output Fall of Wickets.
			over_at_fow.append(total_over)
			wickets_at_fow.append(wicket_1)
			runs_at_fow.append(total_1)
			player_.append(player)
	bowl_list=list(players_bowled.keys()) # convert players_bowled keys to list.

	with open('scorecard.txt','a') as f1: # headers of output file (formatting done for notepad only).
		f1.write(f"{team:<5}{'Innings':^10}{' ':^10}{' ':^88}{total_1:^1}{'-':^1}{wicket_1:^1}{' (':^1}{total_over:^1}{' Ov)':>2}")
		f1.write('\n')
		f1.write(f"{'Batter': <25}{' ': ^50}{'R': ^10}{'B': ^10}{'4s': ^10}{'6s': ^10}{'SR': >14}")
		f1.write('\n')

	for line in lines: # again run on line in lines.
		pattern=re.compile(r'\sto(\s[A-Z][a-z]+)?(\s[A-Z][a-z]+)') # finding the pattern ' to batsman'
		pattern2=re.compile(r'[\.|!]\s([A-Z][a-z]+\s)?([A-Z][a-z]+\s)([A-Z a-z]*b\s[A-Z a-z]+)\s(\d{0,9})\((\d{0,9})\)([\[\(a-z0-9- \)\]]*)') # finding the format '. Batsman c catcher b bowler run(ball) [4s-fours 6s- sixes]'
		pattern5=re.compile(r'(\s[a-z]+)?(\s[A-Z][a-z]+),\s([SIX|FOUR]+)') # finding the format ' batsman, SIX/FOUR'
		pattern6=re.compile(r'\d{0,9}?\d{0,9}\(') # finding the format 'runs(' which would indicate that a wicket is taken.
		pattern7=re.compile(r'(\d{1,9}\.\d{1,6})') # finding the format of current over and ball e.g. '1.6'
		pattern8=re.compile(r'\sto(\s[A-Z][a-z]+)?(\s[A-Z][a-z]+),[ leg byes| byes]+,\s([FOUR|1|2|3]+),?\s') # finding the format ' to batsman, leg byes/byes, 1/2/3/FOUR ,'
		pattern9=re.compile(r'\sto(\s[A-Z][a-z]+)?(\s[A-Z][a-z]+),(\s[no|1|2|3|4|5]+)?([ wide| run]+)s?,') # finding the format ' to batsman, no/1/2/3/4/5 runs/wide ,' 

		players=pattern.finditer(line) # respective matches.
		outs=pattern2.finditer(line)
		run3_inn=pattern5.finditer(line)
		wicket_inn=pattern6.finditer(line)
		over_inn=pattern7.finditer(line)
		leg_byes=pattern8.finditer(line)
		wides_inn=pattern9.finditer(line)

		for plyr in players: # if match found, but one of group(1) and group(2) is None, add the other to string player
			if (plyr.group(1)!=None) and (plyr.group(2)!=None):
				player=plyr.group(1)+plyr.group(2)
			elif (plyr.group(1)!=None) and (plyr.group(2)==None):
				player=plyr.group(1)
			elif (plyr.group(1)==None) and (plyr.group(2)!=None):
				player=plyr.group(2)
		# variables to store the fours and sixes of a player
		fours=0
		sixes=0
		for out in outs: # finding the no. of sixes and fours by a player that is given when he gets out.
			if ('4s-' in out.group(6)) and ('6s-'not in out.group(6)): # finding '4s-' or '6s-' in out.group(6) and respectively update fours/sixes.
				fours=int(out.group(6)[5])
			elif ('4s-' not in out.group(6)) and ('6s-' in out.group(6)):
				sixes=int(out.group(6)[5])
			elif ('4s-' in out.group(6)) and ('6s-' in out.group(6)):
				fours=int(out.group(6)[5])
				sixes=int(out.group(6)[10])
			sr=(float(out.group(4))/float(out.group(5)))*100 # output strike rate by rounding off 
			sr=round(sr,2) 
			for item in team_list:
				if player in item:
					players_batted[player][0]=out.group(3)
					players_batted[player][1]=out.group(4)
					players_batted[player][2]=out.group(5)
					players_batted[player][3]=fours
					players_batted[player][4]=sixes
					players_batted[player][5]=sr
			
		bat_list=list(players_batted.keys()) # players_batted keys as a list.
		for wide_run in wides_inn: # increment wide/runs for a bowler.
				for item in bowl_list:  # iterate over each player in bowl_list to match the one in the present line.
					index=line.find(',')
					if (item in line[:index]): # matching player name with name of player in beginning of line.
						if wide_run.group(4)==' wide': # if wide given:
							maiden_balls=0 # maiden balls set to 0 once wide given.
							if wide_run.group(3)!=None: # if more than 1 wides given,
								players_bowled[item][2]+=int(wide_run.group(3)[1:])
								players_bowled[item][5]+=int(wide_run.group(3)[1:])
								break
							else: # if only 1 wide
								players_bowled[item][2]+=1
								players_bowled[item][5]+=1
								break
						elif wide_run.group(4)==' run': # if run (other than fours and sixes) given (including dot ball)
							if wide_run.group(3)==' no': # if no run given
								maiden_balls+=1 # maiden balls increments.
								players_bowled[item][0]+=1
								break
							else:
								players_bowled[item][1]=0
								players_bowled[item][0]+=1
								players_bowled[item][2]+=int(wide_run.group(3)[1:])
								break
				break
		for boundary in run3_inn: # increment boundary runs for a bowler
			for item in bowl_list:  # iterate over each player in bowl_list to match the one in the present line.
				maiden_balls=0 # in case of boundary, maiden balls is set to 0.
				index=line.find(',')
				if item in line[:index]:
					if boundary.group(3)=='FOUR':
						players_bowled[item][0]+=1
						players_bowled[item][2]+=4
						break
					elif boundary.group(3)=='SIX':
						players_bowled[item][0]+=1
						players_bowled[item][2]+=6
						break
			break
		for leg in leg_byes: # increment balls for leg byes/byes but not runs.
			for item in bowl_list: # iterate over each player in bowl_list to match the one in the present line.
				maiden_balls=0
				index=line.find(',')
				if (item in line[:index]):
					players_bowled[item][0]+=1
					break
			break
		for wicket in wicket_inn: # increment balls for wickets.
			for item in bowl_list: # iterate over each player in bowl_list to match the one in the present line.
				maiden_balls+=1 # a wicket is a maiden ball
				index=line.find(',')
				if item in line[:index]:
					players_bowled[item][0]+=1
					players_bowled[item][3]+=1
					break
			break

		for over_ in over_inn: # this is for updating maiden overs of a bowler
			if ('.6' in over_.group(1)) and (maiden_balls==6): # if maiden balls==6 and it is the final ball of the over: 
				for item in bowl_list:
					index=line.find(',')
					if (item in line[:index]):
						players_bowled[item][1]+=1 # add to the corresponding value i.e. index 1 in that player's key-value. 
						maiden_balls=0
						break

	for i in range(len(players_batted)): # code to write the batter's info in the 'scorecard.txt' file.
		for item in team_list:
			if bat_list[i] in item:
				if players_batted[bat_list[i]][0]!='': # if player has been out (found by checking if c... b... is present in the respective key-value.)
					with open('scorecard.txt','a') as f:
						f.write(f"{bat_list[i][1:]:<25}{players_batted[bat_list[i]][0]:^50}{players_batted[bat_list[i]][1]:^10}{players_batted[bat_list[i]][2]:^10}{players_batted[bat_list[i]][3]:^10}{players_batted[bat_list[i]][4]:^10}{players_batted[bat_list[i]][5]:>14}\n")
				else: # write using a not_outs function.
					not_outs(bat_list[i],players_batted,lines)
	with open('scorecard.txt','a') as f:# code to write the total runs, wickets and total overs.
		f.write(f"{'Extras':<25}{' ':^54}{f'{extras}(b {byes_1}, lb {leg_byes_}, w {wides_1}, nb {0}, p {0})':>28}\n")
		f.write(f"{'Total':<25}{' ':^54}{f'{total_1} ({wicket_1} wkts, {total_over} Ov)':>22}\n")
		j=0
		for item in team_list: # code to write the did not bat line:
			for i in range(len(players_batted)):
				if bat_list[i] in item: # for each item in team_list, if bat_list player is also in item, break
					break
				else: # (if the player batted, his name would be in bat_list, else this would automatically run.)
					if i!=len(players_batted)-1: # examine until the last element of bat_list 
						continue
					else: # if still not found till the last, this condition runs and the player's name gets added.
						j+=1
						if j==1:
							f.write(f"{'Did Not Bat':<35}{item:^{len(item)-1}}")
						else:
							f.write(f"{' ,':^2}{item:>{len(item)-1}}")
		f.write('\n')
		f.write('\nFall of wickets\n') # writing the fall of wickets data we collected above.
		for i in range(len(wickets_at_fow)):
			for item in team_list:
				if player_[i] in item:
					if i==0:
						f.write(f'{runs_at_fow[i]}-{wickets_at_fow[i]} ({item[1:]}, {over_at_fow[i]})')
					else:
						if i==4 or i==9:
							f.write(f', {runs_at_fow[i]}-{wickets_at_fow[i]} ({item[1:]}, {over_at_fow[i]})\n')
						else:
							f.write(f', {runs_at_fow[i]}-{wickets_at_fow[i]} ({item[1:]}, {over_at_fow[i]})')
		if i!=4 or i!=9:
			f.write('\n')
		# writing the bowler info part
		f.write(f"{'Bowler':<30}{'O':^15}{'M':^15}{'R':^15.5}{'W':^14}{'NB':^13}{'WD':^18}{'ECO':^15}\n") 
		
		for item in bowl_list: # run for each item in ball_list ( which is basically the keys of players_bowled.)
			eco=players_bowled[item][2]/float(to_over(players_bowled[item][0])) # economy of the bowler.
			eco=str(round(eco,1))+'0'
			# when writing the bowler's info, we write the overs by calling the function to_over.
			f.write(f"{item[1:]:<30}{to_over(players_bowled[item][0]):^15}{players_bowled[item][1]:^15}{players_bowled[item][2]:^15}{players_bowled[item][3]:^13}{players_bowled[item][4]:^16}{players_bowled[item][5]:^16}{eco:^15}\n")
		f.write(f"\n{'Powerplays':<45}{'Overs':^42}{'Runs':>42}\n") # write powerplay status, overs and runs.
		f.write(f"{'Mandatory':<45}{'0.1-6':^42}{powerplay_runs:>42}\n\n\n")

def to_over(balls): # converts balls to overs format and returns it as a string. 
	over=str(int(balls//6))
	ball=str(balls%6)
	return over+'.'+ball

def not_outs(player_,list2,lines): # function to write the not out batters info
	for line in lines: # for each line in lines (lines was all the lines that we got previously from reading the innnings file.)
		pattern3=re.compile(r'\sto(\s[A-Z a-z]+),\s([no|1|2|3|5|FOUR|SIX|leg|byes]+)[ runs| run|,]') # find only the runs in a line.
		runs=pattern3.finditer(line)
		for run in runs: # when run/runs is found in a line:
			if player_ in run.group(1): # if the corresponding player's name in group(1)
				if run.group(2)=='no' or run.group(2)=='no' or run.group(2)=='no': # if no runs increase player's balls
					list2[player_][2]+=1
				elif run.group(2)=='FOUR': # if four or six, increase runs of that player by 4 or 6 respectively.
					list2[player_][1]+=4
					list2[player_][3]+=1
					list2[player_][2]+=1
				elif run.group(2)=='SIX':
					list2[player_][1]+=6
					list2[player_][4]+=1
					list2[player_][2]+=1
				else: # for 1/2/3/5 runs, increment runs accordingly.
					list2[player_][1]+=int(run.group(2))
					list2[player_][2]+=1
	with open('scorecard.txt','a') as f: # write the not out player's info in the file.
		sr=(float(list2[player_][1])/float(list2[player_][2]))*100 # strike rate of the not out player
		sr=round(sr,2)
		f.write(f"{player_[1:]:<25}{'not out':^50}{list2[player_][1]:^10}{list2[player_][2]:^10}{list2[player_][3]:^10}{list2[player_][4]:^10}{sr:>14}\n")

try:
	list_dir=os.listdir() # list the directory
	if 'scorecard.txt' in list_dir: # check if the scorecard.txt already exists, if yes remove it.
		os.remove('scorecard.txt')
	scorecard(0,'pak_inns1.txt','Pakistan') # calling the function twice to write pakistan innings and india innings.
	scorecard(2,'india_inns2.txt','India')
	print('Use notepad to read the .txt files as the output is formatted for notepad.')
except:
	print('Please check if input files exist in the folder.')

#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
