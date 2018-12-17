# Chicago Alderman Campaign Finance

FEO stands for Fair Elections Ordinance.

Teams at Reclaim Chicago's Fair Elections Taskforce have been working to pass a fair elections ordinance in the city. This project creates infographics showing where aldermen's money is coming from.

## Requirements

*   [Ruby version 2.2.5 or above](https://www.ruby-lang.org/en/downloads/)
*   [Ruby Gems](https://rubygems.org/pages/download)
*   [Jekyll](https://jekyllrb.com/)
*   [NPM](https://www.npmjs.com/get-npm)
*   [Gulp](https://gulpjs.com)

## Installation

1. Clone the repository.
    ```
    git clone https://github.com/ryantimjohn/chicago_aldermen_campaign_finance.git
    ```

2. Navigate to the project directory
   ```
   cd chicago_aldermen_campaign_finance
   ```

3. Install Node Packages
    ```
    npm install
    ```

## Running Project Locally

1. Navigate to the project directory
    ```
    cd chicago_aldermen_campaign_finance
    ```

2. Serve your new Jekyll project on a local server
   ```
   bundle exec jekyll serve
   ```
   Open http://localhost:4000 in your browser to view your new site.

## Usage

### Add a ward

1. Create a mark down file in `_ward` directory and name as with the ward number

2. Add YAML header at the start of the file and fill in the values for the following keys if appropriate
    ```
    ---
    name:
    ward_number:
    alderman_first_name:
    alderman_middle_name:
    alderman_last_name:
    headline:
    lead:
    description:
    img_src:
    ---
    ```

### Edit a ward

1. Navigate to the  `_ward` directory and find the ward you want to edit

2. Edit the ward's information in the YAML header

### Add a team member
1. Create a mark down file in `_team` directory and name as with the team member's name

2. Add YAML header at the start of the file and fill in the values for the following keys if appropriate
    ```
    ---
    name:
    first_name
    last_name:
    contribution:
    description:
    twitter_handle:
        - id: Cam__Cunningham
    website:
        url: https://www.facebook.com/CordobaChi/
        text: Cordoba
    facebook:
    linkedin:
    email:
    ---
    ```
3. add image to `assets/src/images/team` of the team member. Title the image `[first name here]-[last name here].jpg`
The image must have a jpg file extension.

### Edit a team member

1. Navigate to the  `_team` directory and find the team member you want to edit

2. Edit the team member's information in the YAML header

### Add a partner
1. Create a mark down file in `_partners` directory and name as with the team partners's name

2. Add YAML header at the start of the file and fill in the values for the following keys if appropriate
    ```
    ---
    name:
    website:
    button:
    description:
    ---
    ```
3. add image to `assets/src/images/partners` of the partners. Title the image `[partners name here].jpg`
The image must have a jpg file extension.

### Edit a partner

1. Navigate to the  `_partners` directory and find the team member you want to edit

2. Edit the partners's information in the YAML header


## Deployment
TBD after release

## Contributing

1. Find an open issue or submit and issue. Leave a message about what you want to work on 📝
2. Fork it! 🍴
3. Create your feature branch: `git checkout -b my-new-feature`
4. Commit your changes: `git commit -am 'Add some feature'`
5. Push to the branch: `git push origin my-new-feature`
6. Submit a pull request 🛬😊