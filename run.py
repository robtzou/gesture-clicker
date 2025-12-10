import requests
from bs4 import BeautifulSoup

def print_secret_message(doc_url):
    """
    Fetches a published Google Doc, parses the character grid data,
    and prints the secret message.
    """
    try:
        # Fetch the content of the Google Doc
        response = requests.get(doc_url)
        response.raise_for_status()

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the first table in the document
        table = soup.find('table')
        if not table:
            print("No table found in the provided Google Doc.")
            return

        rows = table.find_all('tr')
        if not rows:
            print("Table is empty.")
            return

        # Identify column indices from the header row
        headers = [cell.get_text().strip().lower() for cell in rows[0].find_all(['td', 'th'])]
        
        # dynamic column finding
        try:
            x_idx = next(i for i, h in enumerate(headers) if 'x-coordinate' in h)
            y_idx = next(i for i, h in enumerate(headers) if 'y-coordinate' in h)
            char_idx = next(i for i, h in enumerate(headers) if 'character' in h)
        except StopIteration:
            print("Could not identify necessary columns (x-coordinate, y-coordinate, Character) in the header.")
            return

        # Parse the data rows
        grid_data = []
        max_x = 0
        max_y = 0

        for row in rows[1:]:
            cells = row.find_all('td')
            # Ensure the row has enough columns
            if len(cells) <= max(x_idx, y_idx, char_idx):
                continue
            
            try:
                x = int(cells[x_idx].get_text().strip())
                y = int(cells[y_idx].get_text().strip())
                char = cells[char_idx].get_text().strip()
                
                grid_data.append((x, y, char))
                max_x = max(max_x, x)
                max_y = max(max_y, y)
            except ValueError:
                # Skip rows that don't have valid integer coordinates
                continue

        # Initialize the grid with spaces
        # Dimensions are (max_y + 1) rows and (max_x + 1) columns
        grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

        # Populate the grid
        for x, y, char in grid_data:
            grid[y][x] = char

        # Print the grid
        # Since (0,0) is the bottom-left, we print from the top row (max_y) down to 0
        for y in range(max_y, -1, -1):
            print("".join(grid[y]))

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage (commented out):
print_secret_message('https://docs.google.com/document/d/e/2PACX-1vRPzbNQcx5UriHSbZ-9vmsTow_R6RRe7eyAU60xIF9Dlz-vaHiHNO2TKgDi7jy4ZpTpNqM7EvEcfr_p/pub')
