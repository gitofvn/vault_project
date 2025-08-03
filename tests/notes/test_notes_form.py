from django.test import TestCase

from notes.forms import NoteForm


class TestNotesForm(TestCase):
    def setUp(self):
        self.data = {
            'title': 'Test Title',
            'content': 'Test Content',
        }

    def test__form_is_valid__expect_success(self):
        form = NoteForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test__title_is_missing__expect_required_message(self):
        self.data['title'] = ''
        form = NoteForm(data=self.data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertEqual(form.errors['title'][0], 'This field is required.')

    def test__title_with_less_than_three_characters__expect_custom_message(self):
        self.data['title'] = 'Hi'
        form = NoteForm(data=self.data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertEqual(form.errors['title'][0], 'Title must be at least 3 characters long.')

    def test__content_is_missing__expect_required_message(self):
        self.data['content'] = ''
        form = NoteForm(data=self.data)
        self.assertFalse(form.is_valid())
        self.assertIn('content', form.errors)
        self.assertEqual(form.errors['content'][0], 'This field is required.')

