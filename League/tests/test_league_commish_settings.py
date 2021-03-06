from FantasyWeb.baseTest import BaseTestCase, add_league_member, is_on_page

class LeagueCommishSettingsTestCase(BaseTestCase):
	def setUp(self):
		self.response = None
		self.test_url = "/league/%s/commish_settings" % self.league.pk

		self.login_user1()

	def test001_league_commish_settings_without_login(self):
		"""Tests how the server handles viewing the league commish settings screen without first logging in"""
		add_league_member(self.user, self.league, "team1")
		self.logout_user1()
		self.helper_test_unauthenticated_page_access(self.test_url)

	def test002_league_commish_settings_no_membership(self):
		"""Tests how the server handles viewing the league commish settings screen without being a member"""
		response = self.client.get(self.test_url, follow=True)
		self.assertFalse(is_on_page(response, 'League: league_name1'))
		self.assertTrue(is_on_page(response, 'Fantasy Web - Home'))

	def test003_league_commish_settings_membership_no_commish(self):
		"""Tests how the server handles viewing the league commish settings screen without being a commish"""
		add_league_member(self.user, self.league, "team1")
		response = self.client.get(self.test_url, follow=True)

		self.assertFalse(is_on_page(response, 'Commish Settings'))
		self.assertTrue(is_on_page(response, 'League: league_name1'))
		self.assertTrue(is_on_page(response, 'Standings'))

	def test004_league_settings_page_view_as_commish(self):
		"""Tests how the server handles viewing the league settings screen without being a member"""
		add_league_member(self.user, self.league, "team1", commish=True)
		response = self.client.get(self.test_url, follow=True)

		self.assertTrue(is_on_page(response, 'League: league_name1'))
		self.assertTrue(is_on_page(response, '<p>Commish Settings</p>'))
		self.assertTrue(is_on_page(response, 'Commish Settings'))

		# abc123 invite id from baseTest league creation
		self.assertTrue(is_on_page(response, 'https://fantasyfootballelites.com/invite/abc123'))


		commish_settings_nav_active = '<a class="nav-link white-text league-active" '
		commish_settings_nav_active += 'href="/league/%s/commish_settings">Commish Settings</a>' % self.league.pk
		self.assertTrue(is_on_page(response, commish_settings_nav_active))
