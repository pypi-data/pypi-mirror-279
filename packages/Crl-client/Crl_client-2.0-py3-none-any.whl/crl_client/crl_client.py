import os
import sys
import json
import tarfile
import zipfile
import subprocess
import requests
import argparse
import psycopg2
from urllib.parse import urlparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread  # Ensure Thread is imported
from pathlib import Path

class CrlBrowserHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"CRL Browser HTTP Server is running")

class CrlBrowser:
    def __init__(self):
        # Main crlnet directory
        self.crlnet_directory = str(Path.home())  # Get home directory path

        # Create directory if it doesn't exist
        if not os.path.exists(self.crlnet_directory):
            os.makedirs(self.crlnet_directory)

        # File path to store user info
        self.user_info_file = os.path.join(self.crlnet_directory, "loginusers/users.json")  # Path for user info relative to home directory
        self.load_user_info()

        # PostgreSQL database connection
        self.db_connection = psycopg2.connect(
            dbname="crlnet",
            user="postgres",
            password="goychay_23",
            host="192.168.0.105",
            port="5432"
        )

        # Start HTTP server
        self.server_thread = Thread(target=self.start_server)
        self.server_thread.start()

    def start_server(self):
        server_address = ('', 8080)
        httpd = HTTPServer(server_address, CrlBrowserHTTPRequestHandler)
        print("HTTP Server running on port 8080")
        httpd.serve_forever()

    def load_user_info(self):
        # Load user info
        if os.path.exists(self.user_info_file):
            with open(self.user_info_file, "r") as file:
                self.user_info = json.load(file)
        else:
            self.user_info = {}

    def search_sites(self, search_term):
        print(f"Searching for '{search_term}'...")

        # Search domains in the database
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT name FROM domains WHERE name ILIKE %s", ('%' + search_term + '%',))
        found_sites = cursor.fetchall()

        if found_sites:
            print("Results found:")
            for site in found_sites:
                print(site[0])  # Fetch the domain name from the tuple
                # Get and display site content if available
                site_content = self.get_site_content(site[0])
                if site_content:
                    self.display_site_content(site_content)
                else:
                    print("No site content available.")
        else:
            print("No results found.")

    def get_site_content(self, site_name):
        site_path = os.path.join(self.crlnet_directory, site_name)
        supported_extensions = ['.html', '.php', '.pl', '.txt']
        try:
            for root, _, files in os.walk(site_path):
                for file in files:
                    if any(file.endswith(ext) for ext in supported_extensions):
                        file_path = os.path.join(root, file)
                        with open(file_path, "r") as f:
                            return f.read()
        except Exception as e:
            print(f"Failed to read file: {e}")
        return None

    def display_site_content(self, content):
        print("Site Content:")
        print(content)

    def save_search_term(self, search_term):
        # Load saved search terms
        search_terms_file = os.path.join(self.crlnet_directory, "search_terms.json")
        if os.path.exists(search_terms_file):
            with open(search_terms_file, "r") as file:
                search_terms = json.load(file)
        else:
            search_terms = []

        # Add new search term
        search_terms.append(search_term)

        # Save search terms to file
        with open(search_terms_file, "w") as file:
            json.dump(search_terms, file)

    def ddns_manager(self):
        subprocess.run("ddns.exe")

    def download_source(self, domain):
        # Check if domain contains an HTTP link
        if not domain.startswith("http://") and not domain.startswith("https://"):
            domain = f"http://{domain}"

        response = requests.get(domain)
        if response.status_code == 200:
            # Check if there are any downloadable files
            if "Content-Disposition" in response.headers:
                filename = self.get_filename_from_cd(response.headers.get("Content-Disposition"))
                if filename:
                    destination = os.path.join(self.crlnet_directory, filename)
                    with open(destination, 'wb') as f:
                        f.write(response.content)
                    print(f"Downloaded {filename} to {self.crlnet_directory}")
                else:
                    print("No downloadable file found.")
            else:
                print("No downloadable file found.")
        else:
            print(f"Failed to download from {domain}. Status code: {response.status_code}")

    def get_filename_from_cd(self, cd):
        """
        Get filename from Content-Disposition header.
        """
        if not cd:
            return None
        fname = re.findall('filename=(.+)', cd)
        if len(fname) == 0:
            return None
        return fname[0]

    def display_html_content(self, domain):
        # Check if domain contains an HTTP link
        if not domain.startswith("http://") and not domain.startswith("https://"):
            domain = f"http://{domain}"

        response = requests.get(domain)
        if response.status_code == 200:
            print("HTML Content:")
            print(response.text)
        else:
            print(f"Failed to fetch HTML content from {domain}. Status code: {response.status_code}")

    def run_source(self, domain):
        # Check if domain contains an HTTP link
        if not domain.startswith("http://") and not domain.startswith("https://"):
            domain = f"http://{domain}"

        response = requests.get(domain)
        if response.status_code == 200:
            # Check if it's a tar.gz file
            if response.headers.get('content-type') == 'application/x-gzip':
                filename = os.path.basename(urlparse(domain).path)
                destination = os.path.join(self.crlnet_directory, filename)
                with open(destination, 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded {filename} to {self.crlnet_directory}")

                # Extract and run executable if it's a tar.gz file
                if filename.endswith('.tar.gz'):
                    with tarfile.open(destination, 'r:gz') as tar:
                        tar.extractall(self.crlnet_directory)
                        extracted_dir = tar.getnames()[0]  # Assumes a single root directory
                        executable_path = os.path.join(self.crlnet_directory, extracted_dir)
                        self.run_executable(executable_path)
                else:
                    print(f"Unsupported archive format: {filename}")
            else:
                print("Not a valid tar.gz file.")
        else:
            print(f"Failed to download from {domain}. Status code: {response.status_code}")

    def run_executable(self, path):
        if os.path.isfile(path):
            subprocess.run(path, shell=True)
        else:
            print(f"Executable not found in {path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CRL Browser Command Line Tool")
    parser.add_argument('--downloader', type=str, help='Domain URL to download files')
    parser.add_argument('--data', type=str, help='Domain URL to display HTML content')
    parser.add_argument('--source', type=str, help='Domain URL containing tar.gz files to execute')

    args = parser.parse_args()
    browser = CrlBrowser()

    if args.downloader:
        browser.download_source(args.downloader)
    elif args.data:
        browser.display_html_content(args.data)
    elif args.source:
        browser.run_source(args.source)
    else:
        while True:
            print("\nOptions:")
            print("1. Search")
            print("2. Run DDNS Manager")
            print("3. Exit")
            choice = input("Enter your choice: ").strip()

            if choice == '1':
                search_term = input("Enter search term: ").strip().lower()
                browser.search_sites(search_term)
            elif choice == '2':
                browser.ddns_manager()
            elif choice == '3':
                print("Exiting...")
                sys.exit()
            else:
                print("Invalid choice. Please try again.")
