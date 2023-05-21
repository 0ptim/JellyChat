[![Apply supabase migrations](https://github.com/0ptim/JellyChat/actions/workflows/supabase.yml/badge.svg)](https://github.com/0ptim/JellyChat/actions/workflows/supabase.yml)

# JellyChat - Data

> https://cofmxsabxteiidryklyg.supabase.co

We use Supabase to store all questions and final answers together with their rating.

## Technologies

- Supabase
- Postgres

## Local development

To start supabase locally, make sure you have Docker installed and running. Then run:

```bash
supabase start
```

This can take a few minutes to start up. Once it's running, you should see all the containers running in Docker.

You'll find the dashboard at: `http://localhost:54323/`

To stop supabase, run:

```bash
supabase stop
```

Use the `--backup` to stop without resetting the database.

```bash
supabase stop --backup
```

## Migrations

To create a new migration, run:

```bash
supabase migration new {description}
```

> ℹ `{description}` should be a short description of the migration, e.g. `create_users_table`.

This will create a new migration file in `/migrations`. Insert your SQL there.

To apply the migrations, run:

```bash
supabase db reset
```

This will reset the database and apply all migrations. You can also use this command to reset the database to a clean state.

## Deploying to production

Normally, you would need to deploy using the Supabase CLI. However, there's already a GitHub Action set up to deploy the migrations.

The action is triggered on every push to `main`. It will run the migrations and deploy them to production.