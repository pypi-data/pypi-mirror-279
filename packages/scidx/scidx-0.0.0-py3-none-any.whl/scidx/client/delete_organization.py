import requests

def delete_organization(self, organization_name: str) -> dict:
    """
    Delete an organization in the sciDX system.

    Parameters
    ----------
    organization_name : str
        The name of the organization to be deleted.

    Returns
    -------
    dict
        A dictionary containing the success message.

    Raises
    ------
    Exception
        If there is an error deleting the organization.
    """
    url = f"{self.api_url}/organization/{organization_name}"
    response = requests.delete(url)
    print(f"Request URL: {url}")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.content}")
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error: {response.json()['detail']}")
