Feature: Steward List
  List items in the workshop.

  Scenario: List all items
    Given an initialized workshop
    And an item "feature-a" exists with stage "forge"
    And an item "feature-b" exists with stage "backlog"
    When I run "steward list"
    Then the exit code should be 0
    And the output contains "feature-a"
    And the output contains "feature-b"

  Scenario: List items filtered by stage
    Given an initialized workshop
    And an item "feature-a" exists with stage "forge"
    And an item "feature-b" exists with stage "backlog"
    When I run "steward list --stage forge"
    Then the exit code should be 0
    And the output contains "feature-a"
    And the output does not contain "feature-b"

  Scenario: List with no items
    Given an initialized workshop
    When I run "steward list"
    Then the exit code should be 0
    And the output contains "No items found"
