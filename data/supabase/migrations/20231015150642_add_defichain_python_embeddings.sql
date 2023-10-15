-- Create a table to store embeddings
create table embeddings_defichain_python (
  id UUID primary key,
  content text, -- corresponds to Document.pageContent
  metadata jsonb, -- corresponds to Document.metadata
  embedding vector(1536) -- 1536 works for OpenAI embeddings, change if needed
);

-- Create a function to search for embeddings
create function match_embeddings_defichain_python (
  query_embedding vector(1536),
  match_count int default null,
  filter jsonb DEFAULT '{}'
) returns table (
  id uuid,
  content text,
  metadata jsonb,
  similarity float
)
language plpgsql
as $$
#variable_conflict use_column
begin
  return query
  select
    id,
    content,
    metadata,
    1 - (embeddings_defichain_python.embedding <=> query_embedding) as similarity
  from embeddings_defichain_python
  where metadata @> filter
  order by embeddings_defichain_python.embedding <=> query_embedding
  limit match_count;
end;
$$;
