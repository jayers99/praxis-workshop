Feature: Steward Sync
  Regenerate symlinks from status.yaml files.

  Scenario: Regenerate all symlinks
    Given an initialized workshop
    And an item "feature-a" exists with stage "forge"
    And an item "feature-b" exists with stage "backlog"
    And the symlinks are cleared
    When I run "steward sync"
    Then the exit code should be 0
    And the output contains "Sync complete"
    And a symlink exists in _workshop/5-active/3-forge/ for "feature-a"
    And a symlink exists in _workshop/5-active/1-backlog/ for "feature-b"

  Scenario: Sync removes orphaned symlinks
    Given an initialized workshop
    And an item "my-feature" exists with stage "forge"
    And an orphaned symlink exists in _workshop/3-intake/ for "my-feature"
    When I run "steward sync"
    Then the exit code should be 0
    And no symlink exists in _workshop/3-intake/ for "my-feature"
    And a symlink exists in _workshop/5-active/3-forge/ for "my-feature"
