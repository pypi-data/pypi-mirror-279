# synthientpy

A strongly typed Python client for [Synthient](https://synthient.com).
Supports asynchronous and synchronous requests to the Synthient API.

## Installation

MacOS/Linux
```bash
pip3 install synthientpy
```
Windows
```bat
pip install synthientpy
```

## Usage

Check synthientpy/models for the available fields in the response object.

Client and AsyncClient have the following methods:

```python
class Client:
    def __init__(
        self,
        api_key: str,
        default_timeout: int = DEFAULT_TIMEOUT,
        proxy: Optional[str] = None,
    ) -> None: ...
     def lookup(self, token: str) -> LookupResponse: ...
     def visits(self, session: str) -> VisitsResponse: ...
     def delete(self, token: str) -> DeleteResponse: ...
```

### Synchronous Usage

```python
import synthientpy as synthient
client = synthient.Client(
    api_key=os.getenv("SYNTHIENT_API_KEY"),
)
token = "..."
visitor_info = client.lookup(token)
print(visitor_info)
```

### Asynchronous Usage

```python
import asyncio
import synthientpy as synthient

async def main():
    client = synthient.AsyncClient(
        api_key=os.getenv("SYNTHIENT_API_KEY"),
    )
    token = "..."
    visitor_info = await client.lookup(token)
    print(visitor_info)

asyncio.run(main())
```
### Helper Functions

In addition to the client, there are helper functions that can be used to interact with the Synthient API.

```python
def verify_token(lookup: LookupResponse, token_type: TokenType) -> bool: ...

def determine_action(lookup: LookupResponse, token_type: TokenType) -> str: ...
```
Verify token checks if the token is valid and if the server should reject or accept it.
Determine action checks if the token is valid and returns the action that should be taken based on the token type.
```python
class ActionType(str, Enum):
    """Translates the risk level into an action to take.
    ALLOW - Allow the visitor to continue.
    REDIRECT - Redirect the visitor to a different page. Or have them perform another form of verification.
    BLOCK - Block the visitor from accessing
    """

    ALLOW = 0
    REDIRECT = 1
    BLOCK = 2
```

### Models

Full documentation of the fields and their types can be found in the [Synthient API documentation](https://synthient.com/api). You can also find all the types in the `synthientpy.models` module.


### Issues

For any issues or feature requests, please open an issue on the [GitHub repository](https://github.com/synthient/synthientpy)
