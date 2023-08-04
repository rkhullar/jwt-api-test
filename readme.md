## JWT API Test

### Overview
Testing AWS API Gateway integration with custom JSON Web Tokens. HTTP APIs can use builtin JWT authorizers to validate
tokens before application code is invoked. With this API there are three major endpoints:
- `POST /sign`
  - send arbitrary data to the server in exchange for an access token in the JWT format
  - optionally define metadata like the active token duration or the token audience
- `GET /public-keys`
  - meant to be called by the AWS JWT authorizer
  - provides the public JSON Web Keys that should be used to verify the JWT signature
- `GET /.well-known/openid-configuration`
  - meant to be called by the AWS JWT authorizer
  - defines the endpoints relevant to the auth flow
    - `issuer`: where the api is deployed 
    - `jwks_uri`: `{issuer}/public-keys`

### Database
The complete JWKs including the private key values are first generated and then loaded into MongoDB Atlas. Okta can be used
to generate the JWK by creating a service app integration [[link][okta-create-service-app]]. You can generate the private keys
and save both the JWK and PEM versions locally. You can remove the service app integration after that, since we only needed
it to generate the keys.

### Deployment for Auth Server
1. build the lambda layer package with `docker-compose up`
2. build the lambda function package with `./build.sh`
3. create an IAM role for the lambda function with`AWSLambdaBasicExecutionRole` managed policy
4. create the lambda function
   - python 3.11 runtime with arm64 architecture
   - environment variables for `ATLAS_HOST`, `PROJECT`, and `ENVIRONMENT`
5. create the HTTP API gateway
   - integrate with the lambda function
   - add route for `GET /{proxy+}`
   - optionally add route for `POST /{proxy+}` behind another JWT authorizer
   - disable the default execution endpoint
   - map to your custom domain, optionally under a path like `jwt-server`

### Deployment for Testing
1. create another HTTP API gateway
   - setup another integration like a hello world lambda function
   - create JWT authorizer with the following example config
     - `name`: `jwt-api-dev`
     - `issuer`: `https://{host}/jwt-server`
     - `audience`: `api://default`
   - add route for `GET /{proxy+}` behind the JWT authorizer

### Testing
1. use postman to call your test endpoint without any auth. it should respond with 401 Unauthorized
2. generate the custom JWT
   - do this locally only, unless you added the secure POST route in the auth server deployment
3. add bearer token authorization to your postman request, and include the generated token. now it should respond with 200

### Practical Use Cases
The concept for the custom JWT server can be useful for situations where efficient trust is needed between a client and server
but the data in question needs to be customized.

#### Auth Exchange
You need to create an application workflow and support login with from a third party. For example, you want to support login
via Twitter. The oauth for Twitter free tier is heavily rate limited at 25 requests per user per 24 hours. So you can have the
user login, but you cannot verify their access token for each request to your backend.

This is where the custom JWT could help. If you build an endpoint to exchange the user's Twitter access token for a JWT
specific to your application, then you can avoid the rate limit issue while maintaining security on your endpoint. During
the exchange you call the Twitter api once to load the user's profile data like their name, id, and username. Then you
include that profile data as claims in the custom JWT. When the user interacts with the frontend of your application,
each client side request to your backend can be verified with your AWS JWT authorizer.

#### Trusted Uploads
Your application has functionality for users to upload pictures or documents. The frontend calls your backend endpoint
with an access token from an identity management service like okta, auth0, or cognito. The backend responds with an AWS
presigned s3 post, and the frontend that to perform the upload directly to the s3 bucket.

For this use case the concept of the custom JWT can add additional security in the opposite direction. We want to reassure
users of our application that their uploads are going to the correct location. So if we JWT encode the AWS presigned post,
and sign with our JWK, then the frontend can verify the JWT signature and trust that the post data has not been modified.

### Caveats
#### Production Grade Availability
The custom server needs to deployed such that the oidc config endpoint and jwks url are highly available. If you deploy them
with lambda, you may need to enable provisioned concurrency to optimize the response times on those endpoints. You may also
want to consider other architecture components like cloudfront, alb, and ecs fargate. And some other consideration would
be around multi region deployments and security measures like AWS WAF and Shield.

#### Refresh Tokens
This prototype did not cover refresh tokens. I'd imagine that it might be possible to implement, but it would be significantly
more complex. It would probably mean implementing more oidc discovery endpoints, like `authorization_endpoint`, `token_endpoint`,
and `token_endpoint`. [Authlib][authlib-pypi] could probably help with this. They have documentation for how to create
oauth / oidc servers [here][authlib-flask-oidc].

[okta-create-service-app]: https://developer.okta.com/docs/guides/implement-oauth-for-okta-serviceapp/main/#create-a-service-app-integration
[authlib-pypi]: https://pypi.org/project/Authlib
[authlib-flask-oidc]: https://docs.authlib.org/en/latest/flask/2/index.html
