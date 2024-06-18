import requests

def search_organization(self) -> list:
    """
    List all organizations in the sciDX system.

    Returns
    -------
    list
        A list of dictionaries representing the organizations.

    Raises
    ------
    Exception
        If there is an error retrieving the organizations.
    """
    url = f"{self.api_url}/organization"
    response = requests.get(url)
    print(f"Request URL: {url}")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.content}")
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.json()['detail']}")
