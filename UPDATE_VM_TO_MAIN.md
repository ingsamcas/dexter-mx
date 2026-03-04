# Update VM to Production (main branch)

## What Changed

The `develop` branch has been merged into `main` via squash commit.

**Main branch now includes**:
- ✅ Full DataBursatil API v2 integration
- ✅ 7 tools for Mexican market analysis
- ✅ Fixed ticker handling (no .MX for DataBursatil)
- ✅ Enhanced prompts with provider-specific rules
- ✅ Testing suite and documentation

## Update Instructions for VM

### Step 1: Pull Latest Main Branch

```bash
cd ~/dexter-free
git fetch origin
git checkout main
git pull origin main
```

You should see:

```
From https://github.com/ingsamcas/dexter-mx
 * branch            main       -> FETCH_HEAD
Updating 8b31566..51e1699
Fast-forward
 .github/GIT_FLOW.md                            |  96 +++++++++++++++
 TESTING_DATABURSATIL.md                        | 161 +++++++++++++++++++++++++
 src/dexter/prompts.py                          |  23 +++-
 src/dexter/tools/databursatil/__init__.py      |   8 +-
 src/dexter/tools/databursatil/api.py           |  42 ++++---
 src/dexter/tools/databursatil/db_financials.py | 102 ++++++++++------
 src/dexter/tools/databursatil/db_metrics.py    |  93 ++++++++++++--
 src/dexter/tools/databursatil/db_prices.py     | 105 ++++++++++++----
 test_databursatil.py                           |  74 ++++++++++++
 9 files changed, 609 insertions(+), 95 deletions(-)
```

### Step 2: Rebuild Docker Image (Production)

```bash
docker build --no-cache -t dexter-mx .
```

### Step 3: Verify Production Version

```bash
./dexter.sh
# Inside container:
uv run python test_databursatil.py
```

Expected output:
```
==========================================================
Testing DataBursatil API Integration
==========================================================

1. Searching for LASITE...
Result: {'data_source': 'databursatil', 'search': 'LASITE', ...}

2. Getting LASITE company info...
Result: {'data_source': 'databursatil', 'ticker': 'LASITE', ...}

3. Getting LASITE current price...
Result: {'data_source': 'databursatil', 'ticker': 'LASITE', ...}

4. Getting LASITE historical prices (last 7 days)...
Result: {'data_source': 'databursatil', 'ticker': 'LASITE', ...}

5. Getting LASITE income statements (Q4 2024)...
Result: {'data_source': 'databursatil', 'ticker': 'LASITE', ...}

==========================================================
Test complete!
==========================================================
```

### Step 4: Run Production Agent

```bash
./dexter.sh compare
```

Test with the same query:

```
I own 250 shares of LASITE at $4.27 cost basis. Should I sell, buy more, or maintain?
```

You should get a complete analysis without critical errors.

## Differences from Develop Branch

None. The `main` branch now contains all the same code as `develop`.

**Git log**:
```
commit 51e1699 (HEAD -> main, tag: v1.0.0, origin/main)
feat: DataBursatil integration for Mexican market (v1.0.0)

commit a18cb4b (origin/develop, develop)
docs: add DataBursatil testing guide

commit d7553f7
fix: reimplemented DataBursatil API client per official docs
```

## Next Steps

### Option A: Continue using `main` (Recommended for stability)
```bash
git checkout main
```

### Option B: Continue development on `develop`
```bash
git checkout develop
# develop already has all the changes from main
```

### Option C: Start working on private features
After validating `main` works correctly, you can create a private fork for:
- Lápiz API integration
- PDF export
- WhatsApp bot
- REST API service

## Verification Checklist

- [ ] VM is on `main` branch
- [ ] Docker image rebuilt with `--no-cache`
- [ ] `test_databursatil.py` passes all tests
- [ ] Agent completes LASITE analysis successfully
- [ ] Data source shows "DATABURSATIL" as primary
- [ ] No "Data not found" errors for LASITE

## Troubleshooting

### Issue: "Already up to date" after git pull
**Solution**: You're already on the latest version. Proceed to rebuild Docker.

### Issue: Docker build fails
**Solution**: 
```bash
# Clean Docker cache
docker system prune -a
# Rebuild
docker build --no-cache -t dexter-mx .
```

### Issue: Changes not reflected in container
**Solution**: Make sure you rebuilt the image after pulling from main.

---

**Current Version**: v1.0.0  
**Branch**: main  
**Tag**: v1.0.0  
**Commit**: 51e1699
