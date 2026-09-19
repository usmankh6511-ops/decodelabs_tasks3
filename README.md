# Project 3: The Data Warehouse — Azure Version

Azure equivalent of the DecodeLabs Cloud Computing Project 3. Same mission
(Interns table, dummy records, persistence proof) using **Azure Database
for MySQL Flexible Server** in place of AWS RDS.

Two paths below:
- **Option A (Public access + firewall rule)** — fastest, good if you're
  close to the deadline. Matches "granular access control" (Security
  Group ⇄ Firewall rule) from the slides.
- **Option B (Private VNet-integrated)** — matches the "private subnet,
  no public endpoint" best practice exactly, needs an extra jump-box VM.

Pick ONE. Option A is enough to satisfy the milestone requirements.

---

## STEP 0 — Install & log in to Azure CLI
```bash
# macOS
brew install azure-cli

# Windows (PowerShell, run as admin)
winget install -e --id Microsoft.AzureCLI

# Linux
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# then log in (opens browser)
az login
```

---

## STEP 1 — Create a Resource Group
```bash
az group create --name interns-rg --location eastus
```

---

## OPTION A — Public access + Firewall rule (recommended, fastest)

### Step 2A — Find your public IP
```bash
curl ifconfig.me
```
Note this IP — you'll use it as the firewall rule source (this is the
Azure equivalent of the "Source: My IP" security group rule in the slides).

### Step 3A — Create the Flexible Server
```bash
az mysql flexible-server create \
  --resource-group interns-rg \
  --name interns-mysql-server \
  --location eastus \
  --admin-user dbadmin \
  --admin-password "YourStrongPassword123!" \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --storage-size 20 \
  --version 8.0 \
  --public-access <YOUR_PUBLIC_IP>
```
Replace `<YOUR_PUBLIC_IP>` with the IP from Step 2A.
(Note: `admin` is a reserved word in Azure MySQL — that's why we use
`dbadmin` as the username.)

This single command also opens the correct firewall rule for your IP.
To add another IP later (e.g. a teammate's):
```bash
az mysql flexible-server firewall-rule create \
  --resource-group interns-rg \
  --name interns-mysql-server \
  --rule-name AllowTeammateIP \
  --start-ip-address <THEIR_IP> \
  --end-ip-address <THEIR_IP>
```

### Step 4A — Create the database
```bash
az mysql flexible-server db create \
  --resource-group interns-rg \
  --server-name interns-mysql-server \
  --database-name internsdb
```

Skip to **STEP 5 — Connect** below.

---

## OPTION B — Private VNet-integrated (matches "isolated network" exactly)

### Step 2B — Create a VNet with a delegated private subnet
```bash
az network vnet create \
  --resource-group interns-rg \
  --name interns-vnet \
  --address-prefix 10.0.0.0/16 \
  --subnet-name db-subnet \
  --subnet-prefix 10.0.1.0/24

az network vnet subnet update \
  --resource-group interns-rg \
  --vnet-name interns-vnet \
  --name db-subnet \
  --delegations Microsoft.DBforMySQL/flexibleServers
```

### Step 3B — Create a Private DNS zone (required for VNet-integrated servers)
```bash
az network private-dns zone create \
  --resource-group interns-rg \
  --name interns-mysql.private.mysql.database.azure.com
```

### Step 4B — Create the Flexible Server with private access
```bash
az mysql flexible-server create \
  --resource-group interns-rg \
  --name interns-mysql-server \
  --location eastus \
  --admin-user dbadmin \
  --admin-password "YourStrongPassword123!" \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --storage-size 20 \
  --version 8.0 \
  --vnet interns-vnet \
  --subnet db-subnet \
  --private-dns-zone interns-mysql.private.mysql.database.azure.com
```
No public endpoint now — the database only resolves inside the VNet.

### Step 5B — Add a public subnet + jump-box VM (bastion equivalent)
```bash
az network vnet subnet create \
  --resource-group interns-rg \
  --vnet-name interns-vnet \
  --name public-subnet \
  --address-prefix 10.0.2.0/24

az vm create \
  --resource-group interns-rg \
  --name jump-box \
  --image Ubuntu2204 \
  --vnet-name interns-vnet \
  --subnet public-subnet \
  --admin-username azureuser \
  --generate-ssh-keys \
  --size Standard_B1s
```
Note the returned `publicIpAddress`. SSH into it, then connect to the DB
from inside (its hostname resolves via the private DNS zone):
```bash
ssh azureuser@<jump-box-public-ip>
sudo apt-get update && sudo apt-get install -y mysql-client
mysql -h interns-mysql-server.mysql.database.azure.com -u dbadmin -p
```

Create the database once connected:
```sql
CREATE DATABASE internsdb;
USE internsdb;
```

---

## STEP 5 — Connect with MySQL Workbench / CLI and run the scripts

Azure requires SSL. Download the CA certificate once:
```bash
curl -o DigiCertGlobalRootCA.crt.pem https://dl.cacerts.digicert.com/DigiCertGlobalRootCA.crt.pem
```

**Option A (public):** In MySQL Workbench, new connection →
- Hostname: `interns-mysql-server.mysql.database.azure.com`
- Port: `3306`
- Username: `dbadmin`
- Password: what you set in Step 3A
- SSL tab → "Use SSL" → CA File: point to `DigiCertGlobalRootCA.crt.pem`

**Option B (private):** connect from inside the jump-box VM instead
(Workbench can't reach a private endpoint from your laptop directly
unless you also set up a VPN/Bastion tunnel — the `mysql` CLI over SSH
from Step 5B is the simplest route).

Then, from the `sql/` folder, run in order:
```sql
source sql/01_create_table.sql;
source sql/02_insert_records.sql;
source sql/03_verify.sql;
```
Screenshot the `SELECT * FROM Interns;` output into `screenshots/`.

---

## STEP 6 — (Bonus) Connect via Python
```bash
cd python
pip install -r requirements.txt
```
Edit the CONFIG section at the top of `connect_db.py`:
- `DB_HOST` → your server's hostname
  (`interns-mysql-server.mysql.database.azure.com`)
- `DB_USER` → `dbadmin`
- `DB_PASSWORD`, `DB_NAME` → yours

Run it:
```bash
python connect_db.py
```
It connects over SSL and prints every row in `Interns`.

---

## STEP 7 — GitHub & Submission Checklist
- [ ] Create a **public** GitHub repo (e.g. `project3-data-warehouse-azure`)
- [ ] Push `sql/`, `python/`, `screenshots/`, `README.md`
- [ ] Include the screenshot of a successful `SELECT * FROM Interns;`
- [ ] Test everything end-to-end before submitting
- [ ] Don't wait for the last day

```bash
cd project3-azure-data-warehouse
git init
git add .
git commit -m "Project 3: The Data Warehouse - Azure MySQL Flexible Server"
git branch -M main
git remote add origin https://github.com/<your-username>/project3-data-warehouse-azure.git
git push -u origin main
```

---

## Cleanup (avoid ongoing charges after you're done)
```bash
az group delete --name interns-rg --yes --no-wait
```
This deletes everything created above (server, VNet, VM) in one shot.

---

## Troubleshooting
- **"Client with IP ... is not allowed to connect"** → your IP changed or
  the firewall rule wasn't added; re-run Step 2A/3A with your current IP.
- **SSL connection error** → make sure you downloaded and pointed to
  `DigiCertGlobalRootCA.crt.pem`.
- **"Access denied for user 'admin'"** → Azure reserves `admin`; use
  `dbadmin` (or whatever non-reserved name you chose) everywhere.
