import click
import requests
from bs4 import BeautifulSoup
from rich.console import Console

# @click.group()
# def find_rasifal():
#     """A CLI tool to fetch and display Horoscope"""
#     pass

console = Console()

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


HOROSCOPE_TIME = {
    'd':'daily',    
    'w':'weekly', 
    'm':'monthly',
    'y':'yearly',
}

def parse_content(soup):
    """Parses the HTML content and prints the horoscope."""

    desc = soup.find('div', class_="desc").find("p").text
    # click.echo(desc)
    click.echo(click.style(desc, fg="green", bold=True))



@click.command()
@click.option('--sign', '-s',type=click.Choice(HOROSCOPE_MAP.keys(), case_sensitive=False), prompt='Your horoscope sign please ?', help='Your horoscope name. Eg: Dhanu, Mesh, etc.')
@click.option('--time', '-t', type=click.Choice(HOROSCOPE_TIME.keys(), case_sensitive=False),prompt="Time of horoscope", help='Time of horoscope. Eg: daily, weekly, monthly, yearly', default='d')
def fetch_content(sign, time='daily'):
    """Fetches and displays content from the specified website."""
    try:
        url =  f"https://www.hamropatro.com/rashifal/{HOROSCOPE_TIME[time]}/{sign}"
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