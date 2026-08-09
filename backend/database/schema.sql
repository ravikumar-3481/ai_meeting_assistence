create extension if not exists pgcrypto;

create table public.users (
    id uuid primary key references auth.users(id) on delete cascade,
    email varchar(255),                  -- kept in sync via trigger below
    full_name varchar(255),
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer set search_path = public
as $$
begin
    insert into public.users (id, email, full_name)
    values (new.id, new.email, new.raw_user_meta_data ->> 'full_name');
    return new;
end;
$$;

create trigger on_auth_user_created
    after insert on auth.users
    for each row execute procedure public.handle_new_user();

create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
    new.updated_at = now();
    return new;
end;
$$;

create trigger set_updated_at_users
    before update on public.users
    for each row execute procedure public.set_updated_at();

create table public.meetings (
    id varchar(150) primary key,                     -- app-generated meeting_id (e.g. 20260808-title-slug-uuid)
    user_id uuid not null references public.users(id) on delete cascade,
    title varchar(255) not null,
    source_url text,
    language varchar(20) default 'english',
    status varchar(20) default 'ready',       
    pinecone_namespace varchar(150) unique not null, 
    total_chunks int default 0,
    duration_seconds int,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);
create index idx_meetings_user_id on public.meetings(user_id);

create trigger set_updated_at_meetings
    before update on public.meetings
    for each row execute procedure public.set_updated_at();

create table public.meeting_chunks (
    id uuid primary key default gen_random_uuid(),
    meeting_id varchar(150) not null references public.meetings(id) on delete cascade,
    chunk_index int not null,
    vector_id varchar(100) not null,   -- Pinecone vector id
    created_at timestamptz not null default now(),
    unique (meeting_id, chunk_index)
);
create index idx_chunks_meeting_id on public.meeting_chunks(meeting_id);

create table public.meeting_outputs_meta (
    id uuid primary key default gen_random_uuid(),
    meeting_id varchar(150) not null references public.meetings(id) on delete cascade,
    output_type varchar(30) not null, 
    generated_at timestamptz not null default now()
);
create index idx_outputs_meeting_id on public.meeting_outputs_meta(meeting_id);

create table public.action_items (
    id uuid primary key default gen_random_uuid(),
    meeting_id varchar(150) not null references public.meetings(id) on delete cascade,
    task text not null,
    owner varchar(255),
    due_date date,
    status varchar(20) default 'open',
    created_at timestamptz not null default now()
);
create index idx_action_items_meeting_id on public.action_items(meeting_id);

create table public.access_audit_log (
    id bigserial primary key,
    user_id uuid references public.users(id),
    meeting_id varchar(150) references public.meetings(id),
    action varchar(50),
    accessed_at timestamptz not null default now(),
    result varchar(20)  -- allowed | denied
);
create index idx_audit_user_id on public.access_audit_log(user_id);

alter table public.users enable row level security;
alter table public.meetings enable row level security;
alter table public.meeting_chunks enable row level security;
alter table public.meeting_outputs_meta enable row level security;
alter table public.action_items enable row level security;
alter table public.access_audit_log enable row level security;

create policy "users_select_own"
    on public.users for select
    using (auth.uid() = id);

create policy "users_update_own"
    on public.users for update
    using (auth.uid() = id);

create policy "meetings_select_own"
    on public.meetings for select
    using (auth.uid() = user_id);

create policy "meetings_insert_own"
    on public.meetings for insert
    with check (auth.uid() = user_id);

create policy "meetings_update_own"
    on public.meetings for update
    using (auth.uid() = user_id);

create policy "meetings_delete_own"
    on public.meetings for delete
    using (auth.uid() = user_id);

create policy "chunks_select_own"
    on public.meeting_chunks for select
    using (
        exists (
            select 1 from public.meetings m
            where m.id = meeting_chunks.meeting_id
              and m.user_id = auth.uid()
        )
    );

create policy "chunks_insert_own"
    on public.meeting_chunks for insert
    with check (
        exists (
            select 1 from public.meetings m
            where m.id = meeting_chunks.meeting_id
              and m.user_id = auth.uid()
        )
    );

create policy "outputs_select_own"
    on public.meeting_outputs_meta for select
    using (
        exists (
            select 1 from public.meetings m
            where m.id = meeting_outputs_meta.meeting_id
              and m.user_id = auth.uid()
        )
    );

create policy "outputs_insert_own"
    on public.meeting_outputs_meta for insert
    with check (
        exists (
            select 1 from public.meetings m
            where m.id = meeting_outputs_meta.meeting_id
              and m.user_id = auth.uid()
        )
    );

create policy "action_items_select_own"
    on public.action_items for select
    using (
        exists (
            select 1 from public.meetings m
            where m.id = action_items.meeting_id
              and m.user_id = auth.uid()
        )
    );

create policy "action_items_insert_own"
    on public.action_items for insert
    with check (
        exists (
            select 1 from public.meetings m
            where m.id = action_items.meeting_id
              and m.user_id = auth.uid()
        )
    );

create policy "action_items_update_own"
    on public.action_items for update
    using (
        exists (
            select 1 from public.meetings m
            where m.id = action_items.meeting_id
              and m.user_id = auth.uid()
        )
    );

create policy "audit_select_own"
    on public.access_audit_log for select
    using (auth.uid() = user_id);