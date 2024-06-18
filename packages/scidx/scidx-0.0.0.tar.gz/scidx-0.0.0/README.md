# scidx

scidx is a Python library that allows you to interact with the sciDX REST API for managing datasets and organizations. This library provides a convenient way to create, search, and manage datasets and organizations using simple Python functions.

## Features

- Register organizations
- Register datasets
- Search organizations
- Search datasets
- Delete organizations

## Installation

To install the library, you can use pip:

```
pip install scidx
```

For detailed installation instructions and dependencies, see [installation](docs/installation.md).

## Configuration

To configure the library, you need to set the API URL for your sciDX REST API instance. This can be done by initializing the `sciDXClient` with the appropriate URL:

```python
from scidx.client import sciDXClient

api_url = "http://your-api-url.com"
client = sciDXClient(api_url)
```

For detailed configuration instructions, see [Configuration](docs/configuration.md).

## Usage

Here is a quick example of how to use the library:

```python
from scidx.client import sciDXClient

# Initialize the client
api_url = "http://your-api-url.com"
client = sciDXClient(api_url)

# Register an organization
response = client.register_organization(
    name="example_org",
    title="Example Organization",
    description="This is an example organization."
)
print(response)

# Register a dataset
dataset_data = {
    "dataset_name": "example_dataset",
    "dataset_title": "Example Dataset Title",
    "owner_org": "example_org",
    "resource_url": "http://example.com/resource",
    "resource_name": "Example Resource Name",
    "dataset_description": "This is a dataset for testing.",
    "resource_description": "This is a resource for testing.",
    "resource_format": "CSV"
}
response = client.register_datasource(**dataset_data)
print(response)

# Search for organizations
organizations = client.search_organization()
print(organizations)

# Search for datasets
datasets = client.search_datasources(dataset_name="example_dataset")
print(datasets)
```

For more usage examples and detailed explanations, see [Usage](docs/usage.md).

## Testing

To run the tests for this project, you can use pytest:

```bash
pytest
```

For detailed testing instructions, see [Testing](docs/testing.md).

## Contributing

We welcome contributions to the sciDX-PY project. To contribute, please follow the guidelines in [Contributing](docs/contributing.md).

## License

This project is licensed under the MIT License. See [LICENSE.md](docs/LICENSE.md) for more details.

## Contact

For any questions or suggestions, please open an [issue](/docs/issues.md) on GitHub.
