# Contributing to pyvisjs

Welcome to pyvisjs! We're glad you're interested in contributing. Please take a moment to review the following guidelines to ensure a smooth and effective contribution process.

## How to Contribute

We welcome contributions in the following areas:

- Reporting bugs
- Submitting feature requests
- Writing code improvements
- Providing documentation updates

Please follow these steps when contributing:

- **Create an Issue (Optional)**: Before making changes, consider creating an issue (Plan -> Issues -> New issue) to discuss and track the proposed changes. This step helps ensure that your contributions align with the project's goals and can provide helpful context for your merge request. Simple requirements specification format could be:
> As a [role],  
> I want [feature/desire]  
> so that [rationale/benefit].  
> For example: [example]

- **Clone the Repository**: Clone the repository to your local machine using the ```git clone``` command.

- **Create a Branch**: Create a new branch for your changes using the ```git checkout -b feature-name``` command, replacing feature-name with a descriptive name for your branch.

- **Create a virtual environment** ```py -m venv .venv```

- **Activate the vitrual environment**: ```.venv\Scripts\activate```

- **Install requirements**: ```py -m pip install -r requirements.txt```

- **Install pyvisjs**: Install pyvisjs package as a local project in “editable” mode ```py -m pip install -e .```

- **Make sure tests are good**: Run ```pytest```

- **Make Changes**: Make your desired changes to the codebase, committing them to your branch with ```git commit -m "your commit message here"```.

- **Push Changes**: Push your changes to the repository on GitLab using ```git push origin feature-name```.

- **Create Merge Request**: Navigate to the project repository and switch to the branch you pushed your changes to. Click on the "Merge Requests" tab and then on the "New merge request" button.

- **Select Source and Target Branches**: Choose the branch containing your changes as the "source branch" and ```dev``` branch as the "target branch."

- **Fill in Merge Request Details**: Provide a title and description for your merge request, detailing the changes you made and why they are necessary.

- **Submit Merge Request**: Once you're satisfied with your changes and the merge request details, submit the merge request.

- **Monitor and Respond to Feedback**: Keep an eye on your merge request for any comments or feedback from project maintainers. Make any requested changes and update the merge request accordingly.

- **Merge Changes**: Once your merge request has been approved, a project maintainer will merge your changes into the main branch of the repository.


## Do not forget
> you can use the following keywords followed by #issue_number in your commit message or merge request subject! 

- Close, Closes, Closed, Closing, close, closes, closed, closing

- Fix, Fixes, Fixed, Fixing, fix, fixes, fixed, fixing
- Resolve, Resolves, Resolved, Resolving, resolve, resolves, resolved, resolving

for example ```This commit is also related to #17 and fixes #18, #19```


## The terminal part from above in short
```
git clone https://gitlab.com/22kittens/pyvisjs.git
cd pyvisjs
git checkout dev
git checkout -b feature-name
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
py -m pip install -e .
pytest
<< make your changes >>
pytest
git add .
git commit -m "Fixes issue #12"
git push origin feature-name
<< create a Pull Request >>

```

## Branching Strategy
```main```:

- **Purpose**: This branch holds the production-released code.
- **Protection**: Set as a protected branch to prevent direct commits. Only allow merge requests (MRs) from ```dev``` after code reviews and CI checks.
- **Deployment**: Deployments to production are triggered from this branch.

```dev```:

- **Purpose**: This branch holds the current or in-progress code.
- **Protection**: Also set as a protected branch to prevent direct commits. Similar to the ```main``` branch, only allow MRs.
- **Integration**: Regularly integrated from ```feature-branches``` to keep it up-to-date with the latest changes.


```feature-branches```:

 - **Purpose**: For developing new features, bug fixes, or any changes.
- **Naming Convention**: Use a consistent naming convention like feature-name or bug-description.
- **Lifecycle**: These branches are short-lived and should be merged back into ```dev``` upon completion.


## Community Guidelines

We value a respectful and inclusive community. Please adhere to the following guidelines when interacting with others in the pyvisjs community:

- Be respectful and considerate of others' opinions and contributions.
- Avoid offensive language, harassment, or discrimination of any kind.
- Help create a welcoming and inclusive environment for all community members.

## Contact

If you have any questions or need assistance, feel free to contact the project owner at andrey@morozov.lv.

Thank you for contributing to pyvisjs! We appreciate your support and contributions.