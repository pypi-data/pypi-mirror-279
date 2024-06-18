import requests

def register_organization(self, name: str, title: str, description: str = "") -> dict:
    """
    Create a new organization in the sciDX REST API.

    Parameters
    ----------
    name : str
        The name of the organization.
    title : str
        The title of the organization.
    description : str
        The description of the organization.

    Returns
    -------
    dict
        A dictionary containing the response from the API.

    Raises
    ------
    HTTPError
        If the API request fails with detailed error information.
    """
    url = f"{self.api_url}/organization"
    payload = {
        "name": name,
        "title": title,
        "description": description
    }
    response = requests.post(url, json=payload)
    if response.status_code == 201:
        return response.json()
    else:
        error_message = (
            f"Failed to create organization. "
            f"Request URL: {url}\n"
            f"Payload: {payload}\n"
            f"Response Status Code: {response.status_code}\n"
            f"Response Content: {response.content.decode('utf-8')}"
        )
        raise requests.exceptions.HTTPError(error_message, response=response)
