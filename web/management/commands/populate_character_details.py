import requests
import re
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from web.models import Character, Character_Details

class Command(BaseCommand):
    help = 'Populate Character_Details from Avatar Wiki'

    def handle(self, *args, **kwargs):
        # Fetch all existing character names from the database
        characters = Character.objects.all()

        for character in characters:
            character_name = character.name.replace(" ", "_")  # Format name for URL

            # Check if character details already exist
            if Character_Details.objects.filter(character=character).exists():
                self.stdout.write(self.style.SUCCESS(f'Skipping {character_name}, details already filled.'))
                continue  # Skip this character as details already exist

            url = f'https://avatar.fandom.com/wiki/{character_name}'  # Construct the URL

            try:
                # Fetch the page
                response = requests.get(url)
                response.raise_for_status()  # Raise an error for bad responses

                # Parse the HTML content
                soup = BeautifulSoup(response.text, 'html.parser')

                # 1. Add the introduction section
                introduction_section = soup.find('div', class_='pi-data-value')
                if introduction_section:
                    introduction = introduction_section.get_text(strip=True)
                    introduction = re.sub(r'\[\d+\]', '', introduction)  # Remove numerical references
                    character_detail = Character_Details(
                        character=character,
                        number=1,
                        title='Introduction',
                        body=introduction,
                        hide_title=False  # First title
                    )
                    character_detail.save()
                else:
                    self.stderr.write(self.style.ERROR(f'No introduction found for {character_name}'))

                # 2. Add infobox details - Check multiple possible classes
                infobox = soup.find('aside', class_='portable-infobox') or soup.find('aside', class_='pi-item')

                if infobox:
                    for row in infobox.find_all('div', class_='pi-item'):
                        title = row.find('div', class_='pi-item-label')
                        value = row.find('div', class_='pi-item-data')
                        if title and value:
                            title_text = title.get_text(strip=True)
                            title_text = re.sub(r'\[\d+\]', '', title_text)  # Remove numerical references
                            title_text = re.sub(r'\[.*?\]', '', title_text)  # Remove square brackets and their contents

                            value_text = value.get_text(strip=True)
                            value_text = re.sub(r'\[\d+\]', '', value_text)  # Remove numerical references

                            character_detail = Character_Details(
                                character=character,
                                number=1,
                                title=title_text,
                                body=value_text,
                                hide_title=False  # Infobox titles are typically important
                            )
                            character_detail.save()
                        else:
                            self.stderr.write(self.style.ERROR(f'Infobox row missing data for {character_name}'))
                else:
                    self.stderr.write(self.style.ERROR(f'No infobox found for {character_name}'))

                # 3. Add section paragraphs from both h2 and h3 tags
                sections = soup.find_all(['h2', 'h3'])
                for index, section in enumerate(sections):
                    section_title = section.get_text(strip=True)
                    section_title = re.sub(r'\[\d+\]', '', section_title)  # Remove numerical references
                    section_title = re.sub(r'\[.*?\]', '', section_title)  # Remove square brackets and their contents

                    next_elem = section.find_next_sibling()

                    first_paragraph = True  # To track if it's the first paragraph of the section

                    while next_elem and next_elem.name not in ['h2', 'h3']:
                        if next_elem.name == 'p':
                            paragraph_text = next_elem.get_text(strip=True)
                            paragraph_text = re.sub(r'\[\d+\]', '', paragraph_text)  # Remove numerical references
                            if paragraph_text:
                                hide_title = not first_paragraph  # Hide title for all but the first paragraph
                                if first_paragraph:
                                    first_paragraph = False  # Set to False after the first paragraph
                                character_detail = Character_Details(
                                    character=character,
                                    number=index + 2,  # Start numbering from 2 for section paragraphs
                                    title=section_title,
                                    body=paragraph_text,
                                    hide_title=hide_title
                                )
                                character_detail.save()
                        next_elem = next_elem.find_next_sibling()

                self.stdout.write(self.style.SUCCESS(f'Successfully populated data for {character_name}'))

            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Error fetching data for {character_name}: {str(e)}'))
