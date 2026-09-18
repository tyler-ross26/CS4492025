import requests
import unittest
from unittest.mock import patch, Mock
import os

print("Saving files to:", os.getcwd())


def search_by_mgp_id(mgp_id):
    url = f"https://www.metabolomicsworkbench.org/rest/gene/mgp_id/{mgp_id}/all"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if isinstance(data, list):
            # Empty result
            return []
        else:
            # Single result
            return [data["gene_id"]]

    else:
        print(
            f"Failed to search by MGP ID {mgp_id}: "
            f"API returned status code {response.status_code}"
        )
        return []


def search_by_symbol(symbol):
    url = f"https://www.metabolomicsworkbench.org/rest/gene/gene_symbol/{symbol}/all"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if isinstance(data, list):
            # Empty result
            return []

        elif "Row1" in data:
            # Multiple results
            gene_ids = []

            for row in data.values():
                gene_ids.append(row["gene_id"])

            return gene_ids

        else:
            # Single result
            return [data["gene_id"]]

    else:
        print(
            f"Failed to search by symbol {symbol}: "
            f"API returned status code {response.status_code}"
        )
        return []


def search_by_name(name):
    url = f"https://www.metabolomicsworkbench.org/rest/gene/gene_name/{name}/all"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if isinstance(data, list):
            # Empty result
            return []

        elif "Row1" in data:
            # Multiple results
            gene_ids = []

            for row in data.values():
                gene_ids.append(row["gene_id"])

            return gene_ids

        else:
            # Single result
            return [data["gene_id"]]

    else:
        print(
            f"Failed to search by name {name}: "
            f"API returned status code {response.status_code}"
        )
        return []


def download_gene(gene_id):
    url = f"https://api.ncbi.nlm.nih.gov/datasets/v2/gene/id/{gene_id}/download"

    response = requests.get(
        url,
        params={"include_annotation_type": "FASTA_GENE"}
    )

    if response.status_code == 200:
        filename = f"gene_{gene_id}.zip"

        with open(filename, "wb") as f:
            f.write(response.content)

        print(f"Downloaded: {filename}")

    else:
        print(
            f"Failed to download gene {gene_id}: "
            f"API returned status code {response.status_code}"
        )


# ---------------------------------------------------------
# Unit Tests
# ---------------------------------------------------------

class TestGeneSearch(unittest.TestCase):

    @patch("requests.get")
    def test_search_by_symbol_single_result(self, mock_get):
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "gene_id": "7157"
        }

        mock_get.return_value = mock_response

        # Call function
        result = search_by_symbol("TP53")

        # Check expected result
        self.assertEqual(result, ["7157"])

        # Verify correct URL was requested
        mock_get.assert_called_once_with(
            "https://www.metabolomicsworkbench.org/rest/gene/gene_symbol/TP53/all"
        )


    @patch("requests.get")
    def test_search_by_mgp_id_api_error(self, mock_get):
        # Mock failed API response
        mock_response = Mock()
        mock_response.status_code = 404

        mock_get.return_value = mock_response

        # Call function
        result = search_by_mgp_id("MGP000001")

        # API error should return an empty list
        self.assertEqual(result, [])


# ---------------------------------------------------------
# Main Program
# ---------------------------------------------------------

def main():
    # Ask user for search type
    print("Search by:")
    print("1. Gene ID")
    print("2. Gene Symbol")
    print("3. Gene Name")
    print("4. MGP ID")

    choice = input("Enter choice (1/2/3/4): ")

    # Get search term
    search_term = input("Enter your search term: ")

    # Search for matching gene IDs based on user choice
    gene_ids = []

    if choice == "1":
        # Gene IDs provided directly
        gene_ids = [gid.strip() for gid in search_term.split(",")]

    elif choice == "2":
        # Search Metabolomics Workbench by gene symbol
        gene_ids = search_by_symbol(search_term)

    elif choice == "3":
        # Search Metabolomics Workbench by gene name
        gene_ids = search_by_name(search_term)

    elif choice == "4":
        # Search Metabolomics Workbench by MGP ID
        gene_ids = search_by_mgp_id(search_term)

    # Download each gene dataset from NCBI
    if not gene_ids:
        print("No genes found matching your search.")

    else:
        print(
            f"\nFound {len(gene_ids)} gene(s). "
            "Starting downloads..."
        )

        for gene_id in gene_ids:
            download_gene(gene_id)

        print("\nAll downloads complete!")


if __name__ == "__main__":
    main()