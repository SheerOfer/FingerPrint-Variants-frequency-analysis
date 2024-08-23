import requests
from bs4 import BeautifulSoup
import pandas as pd


""" Given a list with all the variants that patient have, import the relevant data from mitomap co-ocuuarnce tool """
def query_mitomap_covariants(input_variants):
    url = "https://www.mitomap.org/cgi-bin/covariants"

    # First, get the form page
    session = requests.Session()
    response = session.get(url)

    if response.status_code != 200:
        return f"Error: Unable to fetch the form. Status code: {response.status_code}"

    # Parse the form to get any hidden fields
    soup = BeautifulSoup(response.text, 'html.parser')
    form = soup.find('form', {'name': 'covariants'})

    if not form:
        return "Error: Couldn't find the form on the page."

    # Prepare the data for POST request
    variants = "\n".join(input_variants)
    data = {
        'data': '1',  # This was a hidden field in the original form
        'variants': variants
    }

    # Add any other hidden fields if present
    for hidden in form.find_all("input", type="hidden"):
        data[hidden['name']] = hidden['value']

    # Set headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': url,
        'Origin': 'https://www.mitomap.org',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # Send POST request
    response = session.post(url, data=data, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        return f"Error: Received status code {response.status_code}"


def parse_covariant_data(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table')

    if not table:
        return "Error: Could not find the data table in the HTML."

    # Extract variants
    variants = [th.text.split('\n')[0] for th in table.find_all('th')]
    num_of_variants = (len(variants)-2) // 2
    variants = variants[2:2+num_of_variants]

    data = []
    row_num = 0
    prev_var = ""
    for row in table.find_all('tr')[1:]:  # Skip the header row
        cells = row.find_all(['th', 'td'])
        if len(cells) > 2:
            if row_num % 2 == 0:
                variant = cells[0].text.split('\n')[0]
                prev_var = variant
            else:
                cells.insert(0, prev_var)
                variant = prev_var
            with_without = cells[1].text
            counts = [cell.text.split('\n')[0] for cell in cells[2:]]
            row_num += 1
            for i in range(len(counts)):
                cell = counts[i]
                if cell == "NA":
                    continue
                else:
                    amount = int(cell.split('(')[0])
                    counts[i] = str(amount) + ' (' + str(amount / 61134*100)[:6] + '%)'   # split the results in 61134 (mitomap DB size) to be proportional to all the data
            data.append([variant, with_without] + counts)

    # Create DataFrame
    df = pd.DataFrame(data, columns=['Variant', 'Co-occurrence'] + variants)

    """the first data frame contains all the variants,
        the second df contains only variants with count smaller then 500 i.e the rare variants"""
    unique_variants = []
    print("mitomap overall frequency for variants with count smaller then 500:")
    for var in variants:
        var_lst = var.split('(')
        var_count = int(var_lst[1][:-1])
        if var_count < 500:
            var_freq = var_count / 61134 * 100
            print(var_lst[0] + " overall frequency - " + str(var_freq)[:6] + "% (" + str(var_count) + "/61134)")
            unique_variants.append(var)

    relevant_columns = ['Variant', 'Co-occurrence']
    relevant_columns.extend(unique_variants)
    subset_df = df[relevant_columns]
    subset_df = subset_df[subset_df['Variant'].isin(unique_variants)]

    return subset_df



