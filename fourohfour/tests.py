"""Tests for the fourohfour app."""

from unittest import TestCase, mock
import string
import random
from wsgi import create_web_app
from http import HTTPStatus as status

from werkzeug.exceptions import default_exceptions


class TestFourOhFour(TestCase):
    """Four oh four abounds."""

    def setUp(self):
        """We have an app and a client."""
        self.app = create_web_app()
        self.client = self.app.test_client()

    def test_returns_404(self):
        """The fourohfour app returns 404."""
        with self.app.app_context():
            response = self.client.get('/')

        self.assertEqual(response.status_code, status.NOT_FOUND,
                         "The root endpoint returns 400")

    def test_returns_404_on_head(self):
        """The fourohfour app returns 404 when you HEAD."""
        with self.app.app_context():
            response = self.client.head('/')

        self.assertEqual(response.status_code, status.NOT_FOUND,
                         "The root endpoint returns 400")


class TestHealthCheck(TestCase):
    """Test the health check endpoint."""

    def setUp(self):
        """We have an app and a client."""
        self.app = create_web_app()
        self.client = self.app.test_client()

    def test_returns_200(self):
        """The health check endpoint returns 200."""
        with self.app.app_context():
            response = self.client.get('/healthz')

        self.assertEqual(response.status_code, status.OK,
                         "The health check endpoint returns 200")


class TestNGINXErrorHandling(TestCase):
    """Propagates errors generated by NGINX."""

    def setUp(self):
        """We have an app and a client."""
        self.app = create_web_app()
        self.client = self.app.test_client()

    def test_echos_error(self):
        """Response status code reflects ``X-Code`` header."""
        with self.app.app_context():
            for code in default_exceptions.keys():
                response = self.client.get('/', headers={'X-Code': code,
                                                         'X-Request-ID': '1'})
                self.assertEqual(response.status_code, code,
                                 'Response status code matches request header')
