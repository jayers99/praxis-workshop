Feature: Steward Intake
  Intake items from inbox to workshop.

  Scenario: Intake a file from inbox
    Given an initialized workshop
    And a file "my-idea.md" exists in _workshop/1-inbox/
    When I run "steward intake my-idea.md"
    Then the exit code should be 0
    And an item directory exists in _workshop/9-items/ with slug "my-idea"
    And the item contains status.yaml with stage "intake"
    And a symlink exists in _workshop/3-intake/ pointing to the item

  Scenario: Intake a folder from inbox
    Given an initialized workshop
    And a folder "my-project/" exists in _workshop/1-inbox/
    When I run "steward intake my-project/"
    Then the exit code should be 0
    And an item directory exists in _workshop/9-items/ with slug "my-project"
    And a symlink exists in _workshop/3-intake/ pointing to the item

  Scenario: Intake with slugified filename
    Given an initialized workshop
    And a file "My Great Idea.md" exists in _workshop/1-inbox/
    When I run "steward intake 'My Great Idea.md'"
    Then the exit code should be 0
    And an item directory exists in _workshop/9-items/ with slug "my-great-idea"

  Scenario: Intake with custom slug
    Given an initialized workshop
    And a file "my-idea.md" exists in _workshop/1-inbox/
    When I run "steward intake my-idea.md --slug custom-name"
    Then the exit code should be 0
    And an item directory exists in _workshop/9-items/ with slug "custom-name"

  Scenario: Intake with slug collision
    Given an initialized workshop
    And an existing item with slug "my-idea"
    And a file "my-idea.md" exists in _workshop/1-inbox/
    When I run "steward intake my-idea.md"
    Then the exit code should be 0
    And an item directory exists in _workshop/9-items/ with slug "my-idea-2"

  Scenario: Intake non-existent file
    Given an initialized workshop
    When I run "steward intake missing.md"
    Then the exit code should be 66
    And stderr contains "not found"
