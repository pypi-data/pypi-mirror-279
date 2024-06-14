from synthientpy.models import ActionType, LookupResponse, TokenType


def verify_token(lookup: LookupResponse, token_type: TokenType) -> bool:
    """Verify

    Args:
        lookup (LookupResponse): The response from the lookup endpoint.

    Returns:
        bool: If the token is valid.
    """
    return (
        lookup.consumed is False
        and (lookup.solved if token_type != TokenType.METRICS else True) is True
        and token_type == lookup.token_type
    )


def determine_action(lookup: LookupResponse, token_type: TokenType) -> ActionType:
    """Determine the action to take based on the lookup response.

    Args:
        lookup (LookupResponse): The response from the lookup endpoint.

    Returns:
        str: The action to take.
    """
    if verify_token(lookup, token_type):
        return ActionType(lookup.risk_level)
    return ActionType.BLOCK
