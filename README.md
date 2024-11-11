# GitHack - Generate Fake GitHub Contributions

This script creates fake GitHub contributions by generating random commit dates and times within a specified date range and pushing them to a repository. Use this to make your GitHub profile appear more active with numerous commits across various dates!

**⚠️ Disclaimer:** This script is intended for educational purposes only. Use responsibly and respect GitHub's Terms of Service.

## Features
- Randomly generated commits within a specified date range
- Flexible control over the number of commits per day
- Automatically pushes contributions to the main branch
- Clears the contribution file after pushing, keeping the repository clean

## Requirements
- **Git**: Make sure Git is installed and configured on your system.
- **Python 3.x**: This script uses Python’s `datetime` and `subprocess` modules.

## Customize the Date Range

Set the desired range of dates for the contributions by modifying the `start_date` and `end_date` variables. The default date range is from `2023-11-11` to `2024-08-31`.

## To Run
```bash
python Hack.py
```
## Ending

Once you've configured everything and run the script, it will generate and push fake contributions to your GitHub repository. Afterward, the script will clear the `contribution.txt` file and push the empty file to keep your repository clean.

**⚠️ Use responsibly:** This script is intended for educational purposes only. Misuse may violate GitHub’s Terms of Service. Always respect the platform's policies.

## Acknowledgments

- **Python** for providing a powerful scripting environment.
- **Git** for version control and enabling automated commits.
- **GitHub** for offering a platform to showcase projects and contributions.
- Any contributors who improve this project through issues or pull requests.

If you have any suggestions or improvements, feel free to open an issue or contribute by submitting a pull request!
