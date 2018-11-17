# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.realestate -t test_real_estate.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.realestate.testing.COLLECTIVE_REALESTATE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/collective/realestate/tests/robot/test_real_estate.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Real estate
  Given a logged-in site administrator
    and an add Real estate form
   When I type 'My Real estate' into the title field
    and I submit the form
   Then a Real estate with the title 'My Real estate' has been created

Scenario: As a site administrator I can view a Real estate
  Given a logged-in site administrator
    and a Real estate 'My Real estate'
   When I go to the Real estate view
   Then I can see the Real estate title 'My Real estate'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Real estate form
  Go To  ${PLONE_URL}/++add++Real estate

a Real estate 'My Real estate'
  Create content  type=Real estate  id=my-real_estate  title=My Real estate

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Real estate view
  Go To  ${PLONE_URL}/my-real_estate
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Real estate with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Real estate title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
