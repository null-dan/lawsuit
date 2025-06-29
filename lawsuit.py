import re
import requests # You need to install this library: pip install requests
from bs4 import BeautifulSoup # Good practice for parsing HTML, though regex might suffice for this specific case

def extract(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        html_content = response.text

        # Using BeautifulSoup to more robustly find the span, then regex on its text
        soup = BeautifulSoup(html_content, 'html.parser')
        progress_span = soup.find('span', class_='progress-meter_progressBarHeading__Nxc77')

        if progress_span:
            # The actual amount is in a nested span. Let's be more precise.
            amount_span = progress_span.find('span', class_='') # Assuming the inner span has an empty class as in your example
            if amount_span:
                # We can still use the regex for validation or to ensure format
                match = re.search(r'\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)', amount_span.get_text())
                if match:
                    extracted_text = match.group(0)
                    return extracted_text
                else:
                    print(f"No amount found in the expected format for {url}")
                    return None
            else:
                print(f"Could not find the inner amount span for {url}")
                return None
        else:
            print(f"Could not find the progress bar heading for {url}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred for {url}: {e}")
        return None


denims_url = "https://www.gofundme.com/f/denims-v-ethan-klein-fair-use-lawsuit-defense-fund"
frogans_url = "https://www.gofundme.com/f/frogans-lawsuit-defense-fund"
kaceytron_url = "https://www.gofundme.com/f/support-kaceytrons-legal-battle-fund"

print("Fetching Denims amount...")
denims_amount = extract(denims_url)
print("Fetching Frogans amount...")
frogans_amount = extract(frogans_url)
print("Fetching Kaceytron amount...")
kaceytron_amount = extract(kaceytron_url)

print(f"\nDenim's: {denims_amount if denims_amount else 'N/A'}")
print(f"Frogan's: {frogans_amount if frogans_amount else 'N/A'}")
print(f"Kaceytron's: {kaceytron_amount if kaceytron_amount else 'N/A'}")
