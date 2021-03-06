from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from League.league_helper import get_league_member, get_league, get_free_agents, get_player_contracts,\
							get_all_league_members, get_league_setting_values, get_league_min_max,\
							get_draft_bid_and_nomination_players
from League.models import League_Setting


@login_required(login_url="/login")
def get_league_standings(request, league_id):
	league_member = get_league_member(request.user, league_id)
	if not league_member:
		return HttpResponseRedirect('/')

	league = get_league(league_id)
	league_members = get_all_league_members(league_id)

	context = {"league_id": league_id, "league_name": league.name,
			   "league_members": league_members,
	           "active": "standings", "is_commish": league_member.is_commish}
	return render(request, 'league_standings.html', context=context)


@login_required(login_url="/login")
def get_league_my_team(request, league_id):
	league_member = get_league_member(request.user, league_id)
	if not league_member:
		return HttpResponseRedirect('/')

	league = get_league(league_id)

	player_contracts = get_player_contracts(league, request.user)

	context = {"league_id": league_id, "league_name": league.name,
	           "active": "my_team",
	           "player_contracts": player_contracts,
	           "is_commish": league_member.is_commish}
	return render(request, 'league_my_team.html', context=context)

@login_required(login_url="/login")
def get_league_schedule(request, league_id):
	league_member = get_league_member(request.user, league_id)
	if not league_member:
		return HttpResponseRedirect('/')

	league = get_league(league_id)

	context = {"league_id": league_id, "league_name": league.name,
	           "active": "schedule", "is_commish": league_member.is_commish}
	return render(request, 'league_schedule.html', context=context)

@login_required(login_url="/login")
def get_league_free_agents(request, league_id):
	league_member = get_league_member(request.user, league_id)
	if not league_member:
		return HttpResponseRedirect('/')

	league = get_league(league_id)
	player_list = get_free_agents(league_id)

	free_agents = []
	for player in player_list:
		p = {}
		p["name"] = player.name
		p["team"] = player.team
		p["number"] = player.number
		p["position"] = player.position
		p["status"] = player.status
		p["height"] = player.height
		p["weight"] = player.weight
		p["dob"] = player.dob
		p["experience"] = player.experience
		p["college"] = player.college

		free_agents.append(p)

	context = {"league_id": league_id, "league_name": league.name, "free_agents": free_agents,
	           "active": "free_agents", "is_commish": league_member.is_commish}
	return render(request, 'league_free_agents.html', context=context)

@login_required(login_url="/login")
def get_league_trade_block(request, league_id):
	league_member = get_league_member(request.user, league_id)
	if not league_member:
		return HttpResponseRedirect('/')

	league = get_league(league_id)

	context = {"league_id": league_id, "league_name": league.name,
	           "active": "trade_block", "is_commish": league_member.is_commish}
	return render(request, 'league_trade_block.html', context=context)

@login_required(login_url="/login")
def get_league_draft(request, league_id):
	league_member = get_league_member(request.user, league_id)
	if not league_member:
		return HttpResponseRedirect('/')

	league = get_league(league_id)

	bid_players_list,nominate_players_list = get_draft_bid_and_nomination_players(league, league_member)
	player_nomination_count = League_Setting.objects.filter(league=league, name="nominations_per_period").first()
	if player_nomination_count is None:
		player_nomination_count = "0"
	else:
		player_nomination_count = player_nomination_count.value

	context = {"league_id": league_id, "league_name": league.name, "bid_players": bid_players_list,
	           "active": "draft", "is_commish": league_member.is_commish,
			   "player_nomination_count": player_nomination_count,
			   "nomination_players": nominate_players_list}
	return render(request, 'league_draft.html', context=context)

@login_required(login_url="/login")
def get_league_forums(request, league_id):
	league_member = get_league_member(request.user, league_id)
	if not league_member:
		return HttpResponseRedirect('/')

	league = get_league(league_id)

	context = {"league_id": league_id, "league_name": league.name,
	           "active": "forums", "is_commish": league_member.is_commish}
	return render(request, 'league_forums.html', context=context)

@login_required(login_url="/login")
def get_league_settings(request, league_id):
	league_member = get_league_member(request.user, league_id)
	if not league_member:
		return HttpResponseRedirect('/')

	league = get_league(league_id)

	context = {"league_id": league_id, "league_name": league.name,
			   "league_settings": get_league_setting_values(league_id),
	           "active": "settings", "is_commish": league_member.is_commish}

	return render(request, 'league_settings.html', context=context)

@login_required(login_url="/login")
def get_league_commish_settings(request, league_id):
	league_member = get_league_member(request.user, league_id)
	if not league_member:
		return HttpResponseRedirect('/')

	if not league_member.is_commish:
		return HttpResponseRedirect('/league/%s' % league_id)

	league = get_league(league_id)
	league_min, league_max = get_league_min_max()

	# Process any settings updates
	if request.method == 'POST':
		# Updates to roster or draft settings
		if request.POST['form_type'] in ['draft-settings-form', 'roster-settings-form']:
			for setting_name in request.POST:
				league_setting_update = League_Setting.objects.filter(league=league, name=setting_name).first()

				if league_setting_update is None or setting_name not in league_min or setting_name not in league_max\
						or float(request.POST[setting_name]) < float(league_min[setting_name])\
						or float(request.POST[setting_name]) > float(league_max[setting_name]):
					continue

				league_setting_update.value = request.POST[setting_name]
				league_setting_update.save()
		# Updates to the draft time
		elif request.POST['form_type'] == 'set-draft-time-form' and 'datetime' in request.POST:
			draft_time = datetime.strptime(request.POST['datetime'], '%m/%d/%Y %I:%M %p')

			draft_time_setting = League_Setting.objects.filter(league=league, name="draft_time").first()
			if draft_time_setting is None:
				draft_time_setting = League_Setting(league=league, name="draft_time", value=str(draft_time))

			draft_time_setting.value = str(draft_time)
			draft_time_setting.save()

	context = {"league_id": league_id, "league_name": league.name,
			   "league_settings": get_league_setting_values(league_id),
	           "active": "commish_settings", "league_minimums": league_min, "league_maximums": league_max,
	           "invite_link": "https://fantasyfootballelites.com/invite/%s" % league.invite_id,
	           "is_commish": league_member.is_commish}
	return render(request, 'league_commish_settings.html', context=context)
