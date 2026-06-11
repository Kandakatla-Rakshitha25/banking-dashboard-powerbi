# reports/

Place your Power BI files here:

- `Banking_Dashboard.pbix` — Main Power BI Desktop report file
- `Banking_Dashboard.pdf` — Exported PDF snapshot for quick preview

## Note on .pbix files

Power BI `.pbix` files are binary and can be large (50–200 MB). 
If your file exceeds GitHub's 100 MB limit, use Git LFS:

```bash
git lfs install
git lfs track "*.pbix"
git add .gitattributes
```

Or host the file on OneDrive/SharePoint and link to it in the README.
