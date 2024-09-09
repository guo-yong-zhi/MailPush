1. Configure the `src/config.json` file correctly.
2. Use another email address to send an email to the email address you filled in `config.json`.
	- You can choose to add any attachment (e.g. ebooks, photos).
	- Both the subject and the body can be empty.
    - Both the subject and the body can contain multiple lines.
	- A line in the subject or body can be a file download link, or multiple. Multiple links are separated by spaces, pipes `|`, or enclosed by inequalities `<` and `>` respectively. Commas `,` and semicolons `;` are not supported.
	- A line in the subject or body can start with the `saveto` keyword to specify the path or file name downloaded to Kindle. Multiple file names are separated by pipes `|`, or enclosed by inequalities `<` and `>` respectively. Spaces, commas `,` and semicolons `;` are not supported. The default path is configured by the parameter `downloaddir` in `config.json`, which defaults to `/mnt/us/documents/downloads`. Examples:
		> - `saveto abc.pdf`              # means the first file is saved to /mnt/us/documents/downloads/abc.pdf
		> - `saveto books/`               # means the first file is saved to /mnt/us/documents/downloads/books/, the file name remains unchanged
		> - `saveto /mnt/us/123.epub`     # means the first file is saved to /mnt/us/123.epub
		> - `saveto abc.pdf | ../def.pdf` # means the first two files are saved to /mnt/us/documents/downloads/abc.pdf and /mnt/us/documents/def.pdf respectively
3. Click the `Fetch unread emails` button to download all unread emails, or click the `Fetch newest emails` button to get the files in the latest mail. Other email download modes are also provided.
4. After selecting a download mode, wait a little. The books will download.