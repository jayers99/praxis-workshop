Feature: Steward Init
  Initialize workshop directory structure.

  Scenario: Initialize workshop directory structure
    Given PRAXIS_HOME is set to a valid directory
    And _workshop/ does not exist
    When I run "steward init"
    Then the exit code should be 0
    And _workshop/1-inbox/ directory exists
    And _workshop/3-intake/ directory exists
    And _workshop/5-active/1-backlog/ directory exists
    And _workshop/5-active/3-forge/ directory exists
    And _workshop/5-active/5-review/ directory exists
    And _workshop/5-active/7-shelf/ directory exists
    And _workshop/7-exits/1-handoff/ directory exists
    And _workshop/7-exits/3-archive/ directory exists
    And _workshop/7-exits/5-trash/ directory exists
    And _workshop/8-epics/ directory exists
    And _workshop/9-items/ directory exists
    And .gitignore contains "_workshop/*" pattern

  Scenario: Init when workshop already exists
    Given PRAXIS_HOME is set to a valid directory
    And _workshop/ already exists
    When I run "steward init"
    Then the exit code should be 73
    And stderr contains "already exists"

  Scenario: Init when PRAXIS_HOME not set
    Given PRAXIS_HOME environment variable is not set
    When I run "steward init"
    Then the exit code should be 78
    And stderr contains "PRAXIS_HOME"
