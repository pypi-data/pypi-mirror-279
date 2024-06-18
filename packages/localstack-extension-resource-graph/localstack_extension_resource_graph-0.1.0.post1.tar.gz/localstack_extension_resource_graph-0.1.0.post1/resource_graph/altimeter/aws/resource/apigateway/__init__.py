"""Base class for APIGateway resources."""

from resource_graph.altimeter.aws.resource.resource_spec import AWSResourceSpec


class APIGatewayResourceSpec(AWSResourceSpec):
    """Base class for APIGateway resources."""

    service_name = "apigateway"
