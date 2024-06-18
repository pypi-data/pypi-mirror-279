import requests

def register_datasource(self, dataset_name: str, dataset_title: str, owner_org: str,
                      resource_url: str, resource_name: str, dataset_description: str = "",
                      resource_description: str = "", resource_format: str = "CSV") -> dict:
    """
    Create a new data source in the sciDX system.

    Parameters
    ----------
    dataset_name : str
        The name of the dataset.
    dataset_title : str
        The title of the dataset.
    owner_org : str
        The name of the organization.
    resource_url : str
        The URL of the resource.
    resource_name : str
        The name of the resource.
    dataset_description : str, optional
        The description of the dataset (default is an empty string).
    resource_description : str, optional
        The description of the resource (default is an empty string).
    resource_format : str, optional
        The format of the resource (default is "CSV").

    Returns
    -------
    dict
        A dictionary containing the response from the API.

    Raises
    ------
    HTTPError
        If the API request fails with detailed error information.
    """
    url = f"{self.api_url}/datasource"
    payload = {
        "dataset_name": dataset_name,
        "dataset_title": dataset_title,
        "owner_org": owner_org,
        "resource_url": resource_url,
        "resource_name": resource_name,
        "dataset_description": dataset_description,
        "resource_description": resource_description,
        "resource_format": resource_format
    }
    response = requests.post(url, json=payload)
    print(f"Request URL: {url}")
    print(f"Payload: {payload}")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.content.decode('utf-8')}")
    if response.status_code == 201:
        return response.json()
    else:
        error_message = (
            f"Failed to create datasource. "
            f"Request URL: {url}\n"
            f"Payload: {payload}\n"
            f"Response Status Code: {response.status_code}\n"
            f"Response Content: {response.content.decode('utf-8')}"
        )
        raise requests.exceptions.HTTPError(error_message, response=response)
