Feature: Bin Wrapper
  The bin/steward wrapper activates the correct virtualenv.

  Scenario: bin/steward wrapper works
    Given PRAXIS_HOME is set to a valid directory
    When I run the steward wrapper with "--version"
    Then the output contains "steward"
    And the exit code should be 0
