# DNS Migration Guide: deeperpoint.com + deeperpoint.ca → GitHub Pages

## Architecture Overview

```
deeperpoint.com  ──→  GitHub Pages (primary custom domain)
                       └── deeperpoint.github.io
deeperpoint.ca   ──→  AWS S3 redirect bucket ──→ deeperpoint.com
```

GitHub Pages only supports **one custom domain per repository**. So:
- **`deeperpoint.com`** → configured as the primary custom domain in GitHub Pages
- **`deeperpoint.ca`** → redirects to `deeperpoint.com` via an S3 redirect bucket

> [!IMPORTANT]
> Both AWS accounts can be configured independently. The `deeperpoint.com` Route 53 hosted zone doesn't need to be in the same AWS account as `deeperpoint.ca`.

---

## Part 1: Configure GitHub Pages Custom Domain

### Step 1.1 — Add CNAME file to the repository

Create a file called `CNAME` (no extension) in the repo root containing only:

```
deeperpoint.com
```

This tells GitHub Pages which custom domain to serve.

### Step 1.2 — Enable HTTPS in GitHub repo settings

1. Go to **Settings → Pages** in the `deeperpoint.github.io` repo
2. Under "Custom domain", enter `deeperpoint.com`
3. Check **Enforce HTTPS** (GitHub provides a free TLS certificate via Let's Encrypt)

> [!NOTE]
> The HTTPS certificate may take a few minutes to provision after DNS records are configured.

---

## Part 2: Route 53 — deeperpoint.com (DeeperPoint AWS Account)

### Step 2.1 — Replace the old WordPress DNS records

In the Route 53 hosted zone for `deeperpoint.com`, **delete** any existing A records or CNAME records that currently point to the WordPress site.

### Step 2.2 — Create A records (apex domain → GitHub Pages)

Create **four A records** for the apex domain (`deeperpoint.com`):

| Type | Name              | Value              |
|------|-------------------|--------------------|
| A    | deeperpoint.com   | 185.199.108.153    |
| A    | deeperpoint.com   | 185.199.109.153    |
| A    | deeperpoint.com   | 185.199.110.153    |
| A    | deeperpoint.com   | 185.199.111.153    |

In Route 53, this is a single A record with **four values** (one per line in the value field).

### Step 2.3 — Create AAAA records (IPv6)

Create **four AAAA records** for IPv6 support:

| Type | Name              | Value                          |
|------|-------------------|--------------------------------|
| AAAA | deeperpoint.com  | 2606:50c0:8000::153            |
| AAAA | deeperpoint.com  | 2606:50c0:8001::153            |
| AAAA | deeperpoint.com  | 2606:50c0:8002::153            |
| AAAA | deeperpoint.com  | 2606:50c0:8003::153            |

Again, a single AAAA record with four values.

### Step 2.4 — Create CNAME for www subdomain

| Type  | Name                  | Value                     |
|-------|-----------------------|---------------------------|
| CNAME | www.deeperpoint.com   | deeperpoint.github.io.   |

> [!TIP]
> The trailing dot after `deeperpoint.github.io.` is required in Route 53 to indicate a fully qualified domain name.

### Summary — deeperpoint.com Hosted Zone

After these changes, the hosted zone should contain:

| Record Type | Name                | Value                                                                                          |
|-------------|---------------------|------------------------------------------------------------------------------------------------|
| NS          | deeperpoint.com     | *(keep existing — AWS name servers)*                                                          |
| SOA         | deeperpoint.com     | *(keep existing)*                                                                             |
| A           | deeperpoint.com     | 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153                           |
| AAAA        | deeperpoint.com     | 2606:50c0:8000::153, 2606:50c0:8001::153, 2606:50c0:8002::153, 2606:50c0:8003::153          |
| CNAME       | www.deeperpoint.com | deeperpoint.github.io.                                                                        |

---

## Part 3: Route 53 — deeperpoint.ca (Personal AWS Account)

Since GitHub Pages only supports one custom domain, `deeperpoint.ca` needs to **redirect** to `deeperpoint.com`. The cleanest AWS approach uses an **S3 static website redirect bucket**.

### Step 3.1 — Create S3 redirect bucket

In **your personal AWS account** (same account as the Route 53 hosted zone for `deeperpoint.ca`):

1. Create an S3 bucket named exactly **`deeperpoint.ca`**
   - Region doesn't matter — pick `us-east-1` for simplicity
2. Go to **Properties → Static website hosting**
3. Select **Redirect requests for an object**
4. Set:
   - **Host name**: `deeperpoint.com`
   - **Protocol**: `https`
5. Save

> [!WARNING]
> The bucket name **must** match the domain name exactly for the Route 53 alias to work.

### Step 3.2 — Create Route 53 alias for deeperpoint.ca

In the Route 53 hosted zone for `deeperpoint.ca`:

1. Create an **A record** (or edit the existing one)
2. Toggle **Alias** to **Yes**
3. Route traffic to: **S3 website endpoint**
4. Choose the region where you created the bucket
5. Select the `deeperpoint.ca` bucket from the dropdown

| Type | Name            | Alias Target                                              |
|------|-----------------|-----------------------------------------------------------|
| A    | deeperpoint.ca  | s3-website-us-east-1.amazonaws.com (alias to S3 bucket)   |

### Step 3.3 — (Optional) Handle www.deeperpoint.ca

Repeat the same S3 redirect pattern:

1. Create an S3 bucket named `www.deeperpoint.ca`
2. Configure it to redirect to `https://deeperpoint.com`
3. Create a Route 53 A record (alias) for `www.deeperpoint.ca` → the new S3 bucket

---

## Part 4: Verification Checklist

After all changes propagate (typically 5–60 minutes):

- [ ] `https://deeperpoint.com` → loads the GitHub Pages site
- [ ] `https://www.deeperpoint.com` → redirects to `https://deeperpoint.com`
- [ ] `http://deeperpoint.com` → redirects to `https://deeperpoint.com`
- [ ] `https://deeperpoint.github.io` → redirects to `https://deeperpoint.com`
- [ ] `http://deeperpoint.ca` → redirects to `https://deeperpoint.com`
- [ ] GitHub Pages shows a valid TLS certificate for `deeperpoint.com`

### DNS Verification Commands

```bash
# Verify A records
dig deeperpoint.com A +short
# Should return: 185.199.108.153, etc.

# Verify CNAME
dig www.deeperpoint.com CNAME +short
# Should return: deeperpoint.github.io.

# Verify redirect
curl -I http://deeperpoint.ca
# Should return: HTTP/1.1 301 → https://deeperpoint.com
```

---

## Important Notes

> [!CAUTION]
> **Before deleting old WordPress records**: If you're still running the WordPress site, note that changing the A record will immediately stop serving it. Make sure you have a backup of any WordPress content you want to preserve.

- The S3 redirect buckets do **not** need to be in the same AWS account as the Route 53 hosted zone, but it's simpler if they are.
- S3 website redirect only handles **HTTP** (port 80). If you need HTTPS on `deeperpoint.ca` before the redirect, you'd need a CloudFront distribution in front of the S3 bucket with an ACM certificate. For most purposes, the HTTP→redirect→HTTPS flow is acceptable.
- GitHub's IP addresses are stable but could theoretically change. GitHub's documentation at [docs.github.com/pages](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site) is the authoritative source.
