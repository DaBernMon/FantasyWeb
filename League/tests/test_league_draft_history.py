from FantasyWeb.baseTest import BaseTestCase, add_league_member, is_on_page

class LeagueDraftHistoryTestCase(BaseTestCase):
	def setUp(self):
		self.response = None
		self.test_url = "/league/%s/draft_history" % self.league.pk

		self.login_user1()

	def test001_league_draft_history_without_login(self):
		"""Tests how the server handles viewing the league draft history screen without first logging in"""
		add_league_member(self.user, self.league, "team1")
		self.logout_user1()
		self.helper_test_unauthenticated_page_access(self.test_url)

	def test002_league_draft_history_no_membership(self):
		"""Tests how the server handles viewing the league draft history screen without being a member"""
		response = self.client.get(self.test_url, follow=True)

		self.assertFalse(is_on_page(response, 'League: league_name1'))
		self.assertTrue(is_on_page(response, 'Fantasy Web - Home'))

	def test003_league_draft_history_page_view(self):
		"""Tests how the server handles viewing the league draft history screen without being a member"""
		add_league_member(self.user, self.league, "team1")
		response = self.client.get(self.test_url, follow=True)

		self.assertTrue(is_on_page(response, 'League: league_name1'))
		self.assertTrue(is_on_page(response, '<p>Draft History</p>'))
		self.assertFalse(is_on_page(response, 'Commish Settings'))

		draft_history_nav_active = '<a class="nav-link white-text league-active" '
		draft_history_nav_active += 'href="/league/%s/draft_history">Draft History</a>' % self.league.pk
		self.assertTrue(is_on_page(response, draft_history_nav_active))

	def test004_league_draft_history_page_view_as_commish(self):
		"""Tests how the server handles viewing the league draft history screen without being a member"""
		add_league_member(self.user, self.league, "team1", commish=True)
		response = self.client.get(self.test_url, follow=True)

		self.assertTrue(is_on_page(response, 'League: league_name1'))
		self.assertTrue(is_on_page(response, '<p>Draft History</p>'))
		self.assertTrue(is_on_page(response, 'Commish Settings'))

		draft_history_nav_active = '<a class="nav-link white-text league-active" '
		draft_history_nav_active += 'href="/league/%s/draft_history">Draft History</a>' % self.league.pk
		self.assertTrue(is_on_page(response, draft_history_nav_active))
