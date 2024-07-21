# Bitwarden Password Analyzer

> This is a complete rewrite that just contains an HTML file and uses JavaScript for removing the duplaces. For the old version see the branch [html-generator-python](https://github.com/elias123tre/bitwarden_find_duplicates/tree/html-generator-python).

Find duplicate logins based on domain, from Bitwarden export.
Always read through webpages and scripts before you open them as you are handling sensitive information.

## How to use

0. Export your Bitwarden vault under *Tools -> Export Vault* to a `.json` file (**NOT** the encrypted one).

1. Download the file [`index.html`](https://github.com/elias123tre/bitwarden_find_duplicates/blob/master/index.html) (see "Download raw file" in the top right corner).

2. Open it in your preferred browser.

3. Open your Bitwarden export file on the page.

4. Delete the duplicate entries.

5. Download the updated Bitwarden export file (with the removed logins deleted).

6. Delete your Bitwarden vault under *Settings -> My account -> Empty vault* (at the bottom of the danger zone). THIS WILL DELETE ALL YOUR PASSWORDS IN BITWARDEN, MAKE SURE YOU HAVE AT LEAST ONE EXPORT OR BACKUP!

7. Import the updated file into Bitwarden under *Tools -> Import data -> Bitwarden (json)*.

8. IMPORTANT: Delete all created json files as they contain all your passwords in plain text (they can be read by any program or user!). It is best to open them with an editor (notepad for example), delete the contents and overwrite them again before you move them to the trash.

> Tip: you can upload your new updated Bitwarden export file again to further remove duplicates.

## Run the hosted index.html file from GitHub Pages)

0. Export your Bitwarden vault under *Tools -> Export Vault* to a `.json` file (**NOT** the encrypted one).

1. Go to https://elias123tre.github.io/bitwarden_find_duplicates/ (hosted on GitHub Pages, mirrors the exact [`index.html`](https://github.com/elias123tre/bitwarden_find_duplicates/blob/master/index.html) file in this repository's main branch).

3. Do steps **3-8** from the instructions above.

## Alternatives

- [Bitwarden-Vault-Cleaner](https://github.com/qyqsoft/Bitwarden-Vault-Cleaner)
- [bitwarden_duplicate_cleaner.py](https://gist.github.com/jwmcgettigan/0bf7cd39947764896735997056ca74d7)
- [bitwarden-deduplicate](https://gitlab.com/sundbp/bitwarden-deduplicate)
- [bwclean2.py](https://gist.github.com/serif/a1281c676cf5a1f77af6ff1a25255a85)

## Discussions

- [Official forum post for a duplicate removal feature](https://community.bitwarden.com/t/duplicate-removal-tool-report-including-merge/648) (you can find more scripts and alternatives there)
- [General Reddit discussion on different ways to remove duplicates in Bitwarden](https://www.reddit.com/r/Bitwarden/comments/sdxzpd/what_is_the_best_way_to_remove_duplicates_from_my/)
- [Reddit thread for a script that solves this](https://www.reddit.com/r/Bitwarden/comments/aon967/bitwarden_duplicate_entries_remover/)