
# gRPC Sample

This AutoKitteh project demonstrates querying a gRPC server triggered by an HTTP request. In this sample, AutoKitteh is querying itself for demonstration purposes, but any gRPC server can be queried.

## API Documentation

- https://grpc.io/docs/

## Setup Instructions

1. Install and start a
   [self-hosted AutoKitteh server](https://docs.autokitteh.com/get_started/quickstart),
   or use AutoKitteh Cloud.

2. Run these commands to deploy this project's manifest file:

   ```shell
   git clone https://github.com/autokitteh/kittehub.git
   ak deploy --manifest kittehub/samples/grpc/autokitteh.yaml
   ```

3. Look for the following lines in the output of the `ak deploy` command, and
   copy the URL paths for later:

   ```
   [!!!!] trigger "..." created, webhook path is "/webhooks/..."
   ```

> [!TIP]
> If you don't see the output of `ak deploy` anymore, you can run these
> commands instead, and use the webhook slugs from their outputs:
>
> ```shell
> ak trigger get webhook_trigger --project grpc_sample -J
> ```

## Usage Instructions

1. Run this command to trigger gRPC requests:

   ```shell
   curl -i [--get] "http://localhost:9980/webhooks/SLUG1"
   ```

2. The webhook will invoke a gRPC call using AutoKitteh to query its own server for project data:

   ```python
   # The following is equivalent to running this command in the terminal:
   # grpcurl -plaintext localhost:9980 autokitteh.projects.v1.ProjectsService.List
   response = grpc_conn.call(
       target = "localhost:9980",
       service = "autokitteh.projects.v1.ProjectsService",
       method = "List",
   )
   print(response)
   ```

3. Check out the resulting session logs in the AutoKitteh server to see the gRPC queries and responses.
