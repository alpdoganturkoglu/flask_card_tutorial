from tests.base import BaseTest
from app.models import Cards


# TO-DO: optimize login and create card


class CardFTest(BaseTest):

    def test_create_card(self):
        with self.client as client:
            # login
            client.post('/login', data=self.def_user)

            resp = client.get('/create_card')
            self.assertTrue('<label for="topic" class="form-label">Topic</label>' in resp.get_data(as_text=True))

            test_card = {'topic': 'test', 'question': 'test', 'typ': 'general'}
            resp = client.post('/create_card', data=test_card, follow_redirects=True)

            # tests if cards created and page redirected
            self.assertTrue(Cards.query.filter_by(id=1).first() is not None)
            self.assertTrue('<h1 align="center">Cards</h1>' in resp.get_data(as_text=True))

    def test_update_card(self):
        with self.client as client:
            # login
            client.post('/login', data=self.def_user)

            # create card
            test_card = {'topic': 'test', 'question': 'test', 'typ': 'general'}
            client.post('/create_card', data=test_card, follow_redirects=True)

            resp = client.get('/1/update')
            self.assertTrue('<label for="topic" class="form-label">Topic</label>' in resp.get_data(as_text=True))

            test_card = {'topic': 'test', 'question': 'test', 'typ': 'code'}
            resp = client.post('/1/update', data=test_card, follow_redirects=True)

            card_value = Cards.query.filter_by(id=1).first()
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(card_value.typ, 'code')
            self.assertTrue('<h1 align="center">Cards</h1>' in resp.get_data(as_text=True))

    def test_update_card_wrong_data(self):
        with self.client as client:
            # login
            client.post('/login', data=self.def_user)

            # create card
            test_card = {'topic': 'test', 'question': 'test', 'typ': 'general'}
            client.post('/create_card', data=test_card, follow_redirects=True)

            # get page
            resp = client.get('/1/update')
            self.assertTrue('<label for="topic" class="form-label">Topic</label>' in resp.get_data(as_text=True))

            test_card = {'topic': 'test', 'question': '', 'typ': 'code'}
            resp = client.post('/1/update', data=test_card, follow_redirects=True)
            self.assertEqual(resp.status_code, 400)

    def test_update_card_no_card(self):
        with self.client as client:
            # login
            client.post('/login', data=self.def_user)

            # get page
            resp = client.get('/1/update')
            self.assertEqual(resp.status_code, 404)

    def test_delete_card(self):
        with self.client as client:
            # login
            client.post('/login', data=self.def_user)

            # create card
            test_card = {'topic': 'test', 'question': 'test', 'typ': 'general'}
            client.post('/create_card', data=test_card, follow_redirects=True)

            resp = client.get('/1/delete', follow_redirects=True)
            card_value = Cards.query.filter_by(id=1).first()
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(card_value, None)

    def test_delete_no_card(self):
        with self.client as client:
            # login
            client.post('/login', data=self.def_user)

            resp = client.get('/1/delete', follow_redirects=True)
            self.assertEqual(resp.status_code, 404)

    def test_show_card(self):
        with self.client as client:
            # login
            client.post('/login', data=self.def_user)

            # create card
            test_card = {'topic': 'test', 'question': 'test', 'typ': 'general'}
            client.post('/create_card', data=test_card, follow_redirects=True)

            # look for the card
            resp = client.get('/cards', data=test_card, follow_redirects=True)
            self.assertTrue('<h2 class="card-title">test</h2>' in resp.get_data(as_text=True))
