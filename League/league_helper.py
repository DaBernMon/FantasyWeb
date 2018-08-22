import datetime
import json
import uuid

from .models import League, League_Member, League_Setting, Player, Player_Contract

def get_league(league_id):
	return League.objects.filter(pk=league_id).first()


def get_league_member(user, league_id):
	username = user.username
	league_member = League_Member.objects.filter(member__username=username, league__pk=league_id).first()

	return league_member

def get_free_agents(league_id):
	taken_players = Player_Contract.objects.filter(league__id=league_id).values_list('player__id', flat=True)
	free_agents = Player.objects.filter().exclude(id__in=taken_players)

	return free_agents

def get_all_league_members(league_id):
	return League_Member.objects.filter(league__pk=league_id)

def get_league_setting_values(league_id):
	return League_Setting.objects.filter(league__id=league_id)

def create_new_league(user, league_name, owner_limit):
	league = League(name=league_name, invite_id=None,
		year_created=datetime.date.today().year)
	league.save()

	# Update the league's invite id
	league.invite_id = "%s%s" % (league.pk, str(uuid.uuid4()))
	league.save()

	# Set all default settings for the league
	set_league_defaults(league.pk)

	league_setting = League_Setting.objects.filter(league=league, name="owner_limit").first()
	if league_setting is None:
		league_setting = League_Setting(league=league, name="owner_limit",
			value=owner_limit)
	else:
		league_setting.value = owner_limit
	league_setting.save()
	league_member = League_Member(
		league=league,
		member=user,
		team_name="%s's team" % user.username,
		is_commish=True
	)
	league_member.save()

def set_league_defaults(league_id):
	league = League.objects.filter(id=league_id).first()

	with open('FantasyWeb/league_settings_values.json') as settings_file:
		data = json.load(settings_file)
		for name,inner_dict in data.items():
			if name == "flex":
				name = "flex_1"
			league_setting = League_Setting(league=league, name=name, value=inner_dict["default"])
			league_setting.save()
