"""This program queries a gRPC server.

An HTTP GET request triggers this program to query a server using gRPC.
In this sample AutoKitteh is querying itself for demonstration purposes,
however this is not required. The host can be any gRPC server.

Starlark is a dialect of Python (see https://bazel.build/rules/language).

For detailed information on gRPC naming conventions see the following link:
https://github.com/grpc/grpc/blob/master/doc/naming.md
"""

load("@grpc", "grpc_conn")

def on_webhook_trigger():
    # The following is equivalent to running this command in the terminal:
    # grpcurl -plaintext localhost:9980 autokitteh.projects.v1.ProjectsService.List
    response = grpc_conn.call(
        target = "localhost:9980",
        service = "autokitteh.projects.v1.ProjectsService",
        method = "List",
    )
    print(response)
