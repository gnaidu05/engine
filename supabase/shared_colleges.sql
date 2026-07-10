-- Team-shared college additions for the College Priority Dashboard.
-- Run once in the Supabase SQL editor (or with `supabase db push`).
--
-- NIRF and NBA columns are text because the workbook accepts bands like
-- "101-150" and "-" as well as plain numbers; the dashboard converts
-- numeric strings back to numbers when it loads rows.

create table if not exists public.shared_colleges (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  name text not null,
  loc text not null,
  type text,
  year int,
  div text,
  nirf25 text,
  nirf24 text,
  nirf23 text,
  naac text,
  nba text,
  avg numeric,
  med numeric,
  eng text,
  cg text not null default 'NA'
);

create unique index if not exists shared_colleges_name_key
  on public.shared_colleges (lower(name));

alter table public.shared_colleges enable row level security;

-- The dashboard talks to this table with the project's public anon key, so
-- anyone who can open the page can read and write rows. That matches an
-- internal team tool. If you later add Supabase Auth, change `to anon`
-- below to `to authenticated` and have the page sign users in.
create policy "anon read"   on public.shared_colleges for select to anon using (true);
create policy "anon insert" on public.shared_colleges for insert to anon with check (true);
create policy "anon update" on public.shared_colleges for update to anon using (true);
create policy "anon delete" on public.shared_colleges for delete to anon using (true);
