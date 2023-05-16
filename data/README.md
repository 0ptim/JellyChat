# Database

This directory contains the database schema and migrations for Supabase.

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

> `{description}` should be a short description of the migration, e.g. `create_users_table`.

```bash
supabase migration new {description}
```

This will create a new migration file in `/migrations`. Insert your SQL there.

To apply the migrations, run:

```bash
supabase db reset
```

This will reset the database and apply all migrations. You can also use this command to reset the database to a clean state.

## Deploying to production

Normally, you would need to deploy using the Supabase CLI. However, there's already a GitHub Action set up to deploy the migrations.

The action is triggered on every push to `main`. It will run the migrations and deploy them to production.
