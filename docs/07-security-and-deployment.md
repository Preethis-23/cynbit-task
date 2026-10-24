# Phase 7: Security and Deployment

Prepare the prototype for safe demonstration and possible internal pilot use.

## Objective

Make client-document handling, configuration, and deployment responsible and understandable.

## Tasks

1. Remove secrets from code and logs.
2. Add environment-based provider configuration.
3. Avoid permanent storage of uploaded documents by default.
4. Add file-size and file-type limits.
5. Sanitize displayed content where relevant.
6. Document external model-provider data handling assumptions.
7. Add basic dependency and error-handling guidance.
8. Provide local and Streamlit deployment instructions.

## Human control

The system must clearly state that it is decision support. A human must approve estimates, pricing, proposals, and project acceptance.

## Completion criteria

- A new developer can configure and run the app.
- Sensitive values are supplied through environment variables.
- Security limitations are documented.
- The deployment process is reproducible.
