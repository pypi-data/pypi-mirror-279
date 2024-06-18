import pytest
import uuid
from scidx.client import sciDXClient

# Function to generate a unique organization name
def generate_unique_name(base_name):
    return f"{base_name}_{uuid.uuid4().hex[:6]}"

# Global variables to store IDs and names
api_url = "http://127.0.0.1:8000"
client = sciDXClient(api_url)
organization_name = generate_unique_name("pytest_organization")
organization_data = {
    "name": organization_name,
    "title": "Pytest Organization",
    "description": "Organization created for pytest."
}
dataset_data = {
    "dataset_name": "pytest_dataset",
    "dataset_title": "Pytest Dataset Title",
    "owner_org": organization_name,
    "resource_url": "http://example.com/resource",
    "resource_name": "Pytest Resource Name",
    "dataset_description": "This is a dataset for testing.",
    "resource_description": "This is a resource for testing.",
    "resource_format": "CSV"
}

@pytest.fixture(scope="module", autouse=True)
def setup_and_cleanup():
    global client, organization_name, organization_data, dataset_data

    # Setup: Ensure the organization does not already exist
    print("Setup: Checking if the organization already exists")
    existing_orgs = client.search_organization()
    print(f"Setup: Existing organizations: {existing_orgs}")
    if organization_name in existing_orgs:
        print(f"Setup: Organization {organization_name} already exists")
        client.delete_organization(organization_name)
        print(f"Setup: Deleted existing organization {organization_name}")

    # Run the tests
    yield

    # Cleanup: Delete the organization after tests
    try:
        client.delete_organization(organization_name)
        print(f"Cleanup: Deleted organization {organization_name}")
    except Exception as e:
        print(f"Cleanup: Failed to delete organization {organization_name}. Reason: {str(e)}")

# Test to create an organization
@pytest.mark.order(1)
def test_create_organization():
    global client, organization_data
    response = client.register_organization(**organization_data)
    assert "id" in response
    assert response["message"] == "Organization created successfully"

# Test to register a datasource
@pytest.mark.order(2)
def test_register_datasource():
    global client, dataset_data
    response = client.register_datasource(**dataset_data)
    assert "id" in response
    assert response["id"] is not None

# Test to search for datasource by name
@pytest.mark.order(3)
def test_search_datasource_by_name():
    global client, dataset_data
    response = client.search_datasource(dataset_name=dataset_data["dataset_name"])
    assert len(response) > 0
    assert response[0]["name"] == dataset_data["dataset_name"]

# Test to search for datasource by organization ID
@pytest.mark.order(4)
def test_search_datasource_by_organization():
    global client, dataset_data
    response = client.search_datasource(owner_org=dataset_data["owner_org"])
    assert len(response) > 0
    assert response[0]["owner_org"] == dataset_data["owner_org"]

# Test to search for datasource by search term
@pytest.mark.order(5)
def test_search_datasource_by_term():
    global client
    search_term = "Pytest"
    response = client.search_datasource(search_term=search_term)
    assert len(response) > 0
    assert any(search_term in result["title"] for result in response)

# Test to search for datasource by owner_org and other parameters
@pytest.mark.order(6)
def test_search_datasource_by_owner_org_and_other_params():
    global client, dataset_data
    search_term = "Pytest"
    dataset_name = dataset_data["dataset_name"]
    response = client.search_datasource(
        owner_org=dataset_data["owner_org"],
        dataset_name=dataset_name,
        search_term=search_term
    )
    assert len(response) > 0
    assert all(result["owner_org"] == dataset_data["owner_org"] for result in response)
    assert any(search_term in result["title"] or result["name"] == dataset_name for result in response)
