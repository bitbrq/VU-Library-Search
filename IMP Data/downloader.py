import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def download_pdf(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        return
    except Exception as e:
        print(f"Error occurred: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all links on the page
    links = soup.find_all('a', href=True)
    
    # Iterate through links to find PDFs
    for link in links:
        href = link['href']
        # Check if the link points to a PDF
        if href.endswith('.pdf'):
            # Construct absolute URL if link is relative
            pdf_url = urljoin(url, href)
            # Download the PDF
            download_pdf_file(pdf_url)

def download_pdf_file(pdf_url):
    try:
        response = requests.get(pdf_url)
        response.raise_for_status()
    except requests.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        return
    except Exception as e:
        print(f"Error occurred: {e}")
        return

    # Extract filename from URL
    filename = urlparse(pdf_url).path.split('/')[-1]
    # Save the PDF
    with open(filename, 'wb') as f:
        f.write(response.content)
    print(f"PDF downloaded: {filename}")

# Example usage
url = "https://vukhanpur.com/VUHandouts.php"
download_pdf(url)