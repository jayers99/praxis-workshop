Feature: Steward Stage
  Transition items between stages.

  Scenario: Transition item to backlog (standard progression)
    Given an initialized workshop
    And an item "my-feature" exists with stage "intake"
    When I run "steward stage my-feature backlog"
    Then the exit code should be 0
    And the item has stage "backlog"
    And no symlink exists in _workshop/3-intake/
    And a symlink exists in _workshop/5-active/1-backlog/ pointing to the item

  Scenario: Transition item directly to forge (fast-track)
    Given an initialized workshop
    And an item "my-feature" exists with stage "intake"
    When I run "steward stage my-feature forge"
    Then the exit code should be 0
    And the item has stage "forge"
    And a symlink exists in _workshop/5-active/3-forge/ pointing to the item

  Scenario: Transition item to terminal stage (archive) from forge
    Given an initialized workshop
    And an item "my-feature" exists with stage "forge"
    When I run "steward stage my-feature archive"
    Then the exit code should be 0
    And the item has stage "archive"
    And a symlink exists in _workshop/7-exits/3-archive/ pointing to the item

  Scenario: Transition item to terminal stage (trash) from backlog
    Given an initialized workshop
    And an item "my-feature" exists with stage "backlog"
    When I run "steward stage my-feature trash"
    Then the exit code should be 0
    And the item has stage "trash"
    And a symlink exists in _workshop/7-exits/5-trash/ pointing to the item

  Scenario: Transition item to terminal stage (handoff) from review
    Given an initialized workshop
    And an item "my-feature" exists with stage "review"
    When I run "steward stage my-feature handoff"
    Then the exit code should be 0
    And the item has stage "handoff"
    And a symlink exists in _workshop/7-exits/1-handoff/ pointing to the item

  Scenario: Invalid stage transition (skipping stages)
    Given an initialized workshop
    And an item "my-feature" exists with stage "intake"
    When I run "steward stage my-feature review"
    Then the exit code should be 65
    And stderr contains "Cannot transition"

  Scenario: Stage non-existent item
    Given an initialized workshop
    When I run "steward stage nonexistent backlog"
    Then the exit code should be 66
    And stderr contains "No item found"

  Scenario: Stage with ambiguous slug
    Given an initialized workshop
    And an item "my-feature" exists with stage "intake"
    And an item "my-feature-v2" exists with stage "intake"
    When I run "steward stage my-feature forge"
    Then the exit code should be 66
    And stderr contains "Multiple items match"

  Scenario: Stage with invalid stage name
    Given an initialized workshop
    And an item "my-feature" exists with stage "intake"
    When I run "steward stage my-feature invalid-stage"
    Then the exit code should be 65
    And stderr contains "Invalid stage"

  Scenario: Shelving and unshelving
    Given an initialized workshop
    And an item "my-feature" exists with stage "forge"
    When I run "steward stage my-feature shelf"
    Then the exit code should be 0
    And the item has stage "shelf"
    When I run "steward stage my-feature forge"
    Then the exit code should be 0
    And the item has stage "forge"
