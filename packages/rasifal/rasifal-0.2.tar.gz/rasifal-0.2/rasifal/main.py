import click
import requests
from bs4 import BeautifulSoup

# @click.group()
# def find_rasifal():
#     """A CLI tool to fetch and display Horoscope"""
#     pass

HOROSCOPE_MAP = {
    'mesh': 'Aries',
    'brish': 'Taurus',
    'mithun': 'Gemini',
    'karkat': 'Cancer',
    'singha': 'Leo',
    'kanya': 'Virgo',
    'tula': 'Libra',
    'brishchik': 'Scorpio',
    'dhanu': 'Sagittarius',
    'makar': 'Capricorn',
    'kumbha': 'Aquarius',
    'min': 'Pisces',
}

def parse_content(soup):
    """Parses the HTML content and prints the horoscope."""

    desc = soup.find('div', class_="desc").find("p").text
    print(desc)





@click.command()
@click.option('--sign', '-s',type=click.Choice(HOROSCOPE_MAP.keys(), case_sensitive=False), prompt='Your horoscope sign please ?', help='Your horoscope name. Eg: Dhanu, Mesh, etc.')
def fetch_content(sign):
    """Fetches and displays content from the specified website."""
    try:
        url =  f"https://www.hamropatro.com/rashifal/daily/{sign}"
        response = requests.get(url)
        response.raise_for_status() 

    except requests.exceptions.RequestException as e:
        click.echo(f"Error fetching the URL: {e}")
        return

    # Set the encoding to handle Nepali content properly
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.content, 'html.parser')
    parse_content(soup)




# find_rasifal.add_command(fetch_content)

def main():
    # find_rasifal()
    fetch_content()

if __name__ == '__main__':
    main()