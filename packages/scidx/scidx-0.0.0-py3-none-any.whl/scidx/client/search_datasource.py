import requests

def search_datasource(self, dataset_name: str = None, owner_org: str = None, search_term: str = None) -> dict:
    """
    Search for datasets in the sciDX system.

    Parameters
    ----------
    dataset_name : str, optional
        The name of the dataset to search for.
    owner_org : str, optional
        The name of the organization to which the dataset belongs.
    search_term : str, optional
        A term to search for in the dataset's title or description.

    Returns
    -------
    dict
        A dictionary containing the search results.

    Raises
    ------
    Exception
        If there is an error performing the search.
    """
    url = f"{self.api_url}/datasource"
    params = {
        "dataset_name": dataset_name,
        "owner_org": owner_org,
        "search_term": search_term
    }
    response = requests.get(url, params=params)
    print(f"Request URL: {url}")
    print(f"Params: {params}")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.content}")
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()