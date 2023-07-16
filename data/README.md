[![Supabase Production](https://github.com/0ptim/JellyChat/actions/workflows/supabase_production.yml/badge.svg)](https://github.com/0ptim/JellyChat/actions/workflows/supabase_production.yml)

[![Supabase Staging](https://github.com/0ptim/JellyChat/actions/workflows/supabase_staging.yml/badge.svg)](https://github.com/0ptim/JellyChat/actions/workflows/supabase_staging.yml)

# JellyChat - Data

> https://cofmxsabxteiidryklyg.supabase.co  
> https://iajfqvpslzrtmvekqwpv.supabase.co

We use Supabase to store:

- Users - `users`
  - Used to store the user token
- Messages - `chat_messages`
  - Content
  - Type: human/jelly/tool
- QA data - `qa`
  - Question
  - Asnwer
- Embeddings - `embeddings`
  - Vector
  - Content
  - Metadata

## Technologies

- Supabase
- Postgres
- pgvector

## Local development

First, install the supabase CLI via npm:

```bash
npm install
```

To start supabase locally, make sure you have Docker installed and running. Then run:

```bash
npx supabase start
```

This can take a few minutes to start up. Once it's running, you should see all the containers running in Docker.

Default connection info:

- API URL: http://localhost:54321
- GraphQL URL: http://localhost:54321/graphql/v1
- DB URL: `postgresql://postgres:postgres@localhost:54322/postgres`
- Studio URL: http://localhost:54323
- Inbucket URL: http://localhost:54324
- JWT secret: `super-secret-jwt-token-with-at-least-32-characters-long`
- anon key: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0`
- service_role key: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImV4cCI6MTk4MzgxMjk5Nn0.EGIM96RAZx35lJzdJsyH-qQwv8Hdp7fsn3W0YpN81IU`

To stop supabase, run:

```bash
npx supabase stop
```

Use the `--backup` to stop without resetting the database.

```bash
npx supabase stop --backup
```

## Migrations

To create a new migration, run:

```bash
npx supabase migration new {description}
```

> ℹ `{description}` should be a short description of the migration, e.g. `create_users_table`.

This will create a new migration file in `/migrations`. Insert your SQL there.

To apply the migrations, run:

```bash
npx supabase db reset
```

This will reset the database and apply all migrations. You can also use this command to reset the database to a clean state.

## Deploying to production

Normally, you would need to deploy using the Supabase CLI. However, there's already a GitHub Action set up to deploy the migrations.

The action is triggered on every push to `main`. It will run the migrations and deploy them to production.
