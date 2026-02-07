-- Pocket Empire Database Schema

-- 1. Leads Table
create table if not exists leads (
  id uuid default uuid_generate_v4() primary key,
  business_name text not null,
  industry text,
  website text,
  email text,
  phone text,
  address text,
  status text default 'New', -- New, Contacted, Sold, Dead
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  last_contacted timestamp with time zone,
  notes text,
  data jsonb, -- Full lead object
  user_id uuid references auth.users(id)
);

-- 2. Invoices Table
create table if not exists invoices (
  id text primary key, -- e.g. INV-2024-1001
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  client_name text not null,
  amount numeric(10, 2) not null,
  status text default 'Sent', -- Sent, Paid, Overdue
  origin text,
  destination text,
  load_ref text,
  pdf_url text, -- Link to stored PDF
  data jsonb, -- Store full JSON object for app compatibility (line items, etc)
  user_id uuid references auth.users(id)
);

-- 3. Wealth Snapshots
create table if not exists wealth_snapshots (
  id uuid default uuid_generate_v4() primary key,
  date date not null,
  total_net_worth numeric(12, 2) not null,
  cash numeric(12, 2) default 0,
  investments numeric(12, 2) default 0,
  debt numeric(12, 2) default 0,
  assets numeric(12, 2) default 0,
  user_id uuid references auth.users(id)
);

-- 4. Reminders / Tasks
create table if not exists reminders (
  id uuid default uuid_generate_v4() primary key,
  title text not null,
  due_date date,
  category text, -- Bill, Compliance, Follow-up
  status text default 'Pending', -- Pending, Completed
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  user_id uuid references auth.users(id)
);

-- 5. Company Settings
create table if not exists company_settings (
  id integer primary key generated always as identity,
  company_name text,
  address text,
  phone text,
  email text,
  mc_number text,
  dot_number text,
  user_id uuid references auth.users(id)
);

-- Enable RLS (Row Level Security)
alter table leads enable row level security;
alter table invoices enable row level security;
alter table wealth_snapshots enable row level security;
alter table reminders enable row level security;
alter table company_settings enable row level security;

-- Create Policies (Allow users to see only their own data)
create policy "Users can view own data" on leads for select using (auth.uid() = user_id);
create policy "Users can insert own data" on leads for insert with check (auth.uid() = user_id);
create policy "Users can update own data" on leads for update using (auth.uid() = user_id);

-- 6. App Data (Key-Value Store for Wealth/Leads JSON blobs)
create table if not exists app_data (
  key text primary key, -- e.g., 'wealth_myself', 'leads_history'
  value jsonb,
  updated_at timestamp with time zone default timezone('utc'::text, now()) not null,
  user_id uuid references auth.users(id)
);

-- Enable RLS
alter table app_data enable row level security;
create policy "Users can view own app data" on app_data for select using (auth.uid() = user_id);
create policy "Users can update own app data" on app_data for all using (auth.uid() = user_id);
