*** Settings ***
Documentation     Test suite for validating the DeviceServiceMonitor logs.
...               This suite connects to a remote machine, checks for service stability,
...               and then validates log content based on the Pytest suite.

# Using a direct relative path to the NEW Robot-specific library.
Library           ../src/RobotRemoteLibrary.py    WITH NAME    RemoteSSH

# These keywords will run once before and after all test cases in this file.
Suite Setup       Connect And Prepare Log Streaming
Suite Teardown    Disconnect From Server


*** Variables ***
# Connection Details
${HOST}           172.23.36.12
${USERNAME}       root
${PASSWORD}       TiaspftVix

# Log Details
${LOG_PATH}       /var/opt/htm/log
${LOG_NAME}       DeviceServiceMonitor.log
${MARKER}         without NTP


*** Test Cases ***
Device Service Monitor Started Without NTP
    [Documentation]    Verifies the initial startup log message.
    [Tags]    smoke
    Log Should Contain    without NTP    FAIL: Log for 'DeviceServiceMonitor started without NTP' not found.

Device Service Monitor Initialized Ignition Monitor
    [Documentation]    Checks that all steps for ignition monitor initialization are logged.
    [Tags]    smoke
    Log Should Contain    Trying to initialize ignition monitor...    FAIL: Log for 'DSM starting initialization of ignition monitor' not found.
    Log Should Contain    Ignition monitor initialized successfully.    FAIL: Log for 'DSM initialized ignition monitor successfully' not found.
    Log Should Contain    Ignition State is 1                         FAIL: Log for 'DSM Ignition State is 1' not found.

Device Service Monitor Started Acquired Current Time
    [Documentation]    Verifies the entire NTP sync and time set process is logged.
    [Tags]    smoke
    Log Should Contain    DSM working on NTP Sync.                FAIL: Log for 'DSM started working on NTP Sync' not found.
    Log Should Contain    Attempting to retrieve ntp date         FAIL: Log for 'DSM Attempting to retrieve ntp date' not found.
    Log Should Contain    Got date information                    FAIL: Log for 'DSM Got date information from ntp server' not found.
    Log Should Contain    Time is set to                          FAIL: Log for 'DSM setting up the device time to current time' not found.

Device Service Monitor Started With NTP
    [Documentation]    Verifies the main start banner after NTP sync.
    [Tags]    smoke
    Log Should Contain    ====================== Starting DeviceServiceMonitor     FAIL: Log for 'DeviceServiceMonitor started with NTP' not found.

Device Service Monitor Initializing Leaderfollower Selection
    [Documentation]    Checks for the start of the leader/follower initialization.
    [Tags]    smoke
    Log Should Contain    DSM working on Leader/Follower initialization..    FAIL: Log for 'DSM started working on Leader/Follower initialization' not found.
    Log Should Contain    Trying to initialize LeaderFollower...             FAIL: Log for 'DSM trying to initialize LeaderFollower selection logic' not found.

Device Service Monitor Device Role Assigned
    [Documentation]    Ensures the device role is assigned and logged.
    [Tags]    smoke
    Log Should Contain    Current role has changed                                FAIL: Log for 'DSM changed the current role of device' not found.
    Log Should Contain    LeaderFollower initialized successfully. Current role:    FAIL: Log for 'DSM initialized LeaderFollower selection logic successfully' not found.

Device Service Monitor Application Management Started
    [Documentation]    Checks for the application management start log.
    Log Should Contain    DSM working on Application Management..    FAIL: Log for 'DSM started working on Application Management' not found.

Device Service Monitor Started Ntp Client
    [Documentation]    Verifies all log steps for starting the ntpclient application.
    Log Should Contain    Triggering NTP command = /afc/bin/ntpclient -t -s -l -h      FAIL: Log for 'DSM triggered NTP command' not found.
    Log Should Contain    [ntpclient] Modifying app state from NotRunning -> AboutToBeStarted    FAIL: Log for 'NTP client app state changed to AboutToBeStarted' not found.
    Log Should Contain    [ntpclient] Starting application ...                          FAIL: Log for 'DSM starting NTP client' not found.
    Log Should Contain    [ntpclient] Application started, pid:                         FAIL: Log for 'DSM started NTP client with a PID' not found.

Device Service Monitor Started User Interface
    [Documentation]    Verifies all log steps for starting the UserInterface application.
    Log Should Contain    [UserInterface] Modifying app state from NotRunning -> AboutToBeStarted    FAIL: Log for 'UserInterface app state changed to AboutToBeStarted' not found.
    Log Should Contain    [UserInterface] Starting application ...                                   FAIL: Log for 'DSM starting User Interface' not found.
    Log Should Contain    [UserInterface] Application started, pid:                                  FAIL: Log for 'DSM started User Interface with a PID' not found.
    Log Should Contain    [UserInterface] Modifying app state from AboutToBeStarted -> Running       FAIL: Log for 'UserInterface app state changed to Running' not found.

Device Service Monitor Started Validator
    [Documentation]    Verifies all log steps for starting the Validator application.
    Log Should Contain    [Validator] Modifying app state from NotRunning -> AboutToBeStarted    FAIL: Log for 'Validator app state changed to AboutToBeStarted' not found.
    Log Should Contain    [Validator] Starting application ...                                   FAIL: Log for 'DSM starting Validator' not found.
    Log Should Contain    [Validator] Application started, pid:                                  FAIL: Log for 'DSM started Validator with a PID' not found.
    Log Should Contain    [Validator] Modifying app state from AboutToBeStarted -> Running       FAIL: Log for 'Validator app state changed to Running' not found.

Device Service Monitor Started Local Support Function
    [Documentation]    Verifies all log steps for starting the LocalSupportFunction application.
    Log Should Contain    [LocalSupportFunction] Modifying app state from NotRunning -> AboutToBeStarted    FAIL: Log for 'LocalSupportFunction app state changed to AboutToBeStarted' not found.
    Log Should Contain    [LocalSupportFunction] Starting application ...                                   FAIL: Log for 'DSM starting LocalSupportFunction' not found.
    Log Should Contain    [LocalSupportFunction] Application started, pid:                                  FAIL: Log for 'DSM started LocalSupportFunction with a PID' not found.
    Log Should Contain    [LocalSupportFunction] Modifying app state from AboutToBeStarted -> Running       FAIL: Log for 'LocalSupportFunction app state changed to Running' not found.

Device Service Monitor Started Heartbeat360
    [Documentation]    Verifies all log steps for starting the Heartbeat360Client application.
    Log Should Contain    [Heartbeat360Client] Modifying app state from NotRunning -> AboutToBeStarted    FAIL: Log for 'Heartbeat360Client app state changed to AboutToBeStarted' not found.
    Log Should Contain    [Heartbeat360Client] Starting application ...                                   FAIL: Log for 'DSM starting Heartbeat360Client' not found.
    Log Should Contain    [Heartbeat360Client] Application started, pid:                                  FAIL: Log for 'DSM started Heartbeat360Client with a PID' not found.
    Log Should Contain    [Heartbeat360Client] Modifying app state from AboutToBeStarted -> Running       FAIL: Log for 'Heartbeat360Client app state changed to Running' not found.

Device Service Monitor Started Update Handler
    [Documentation]    Verifies all log steps for starting the UpdateHandler application.
    Log Should Contain    [UpdateHandler] Modifying app state from NotRunning -> AboutToBeStarted    FAIL: Log for 'UpdateHandler app state changed to AboutToBeStarted' not found.
    Log Should Contain    [UpdateHandler] Starting application ...                                   FAIL: Log for 'DSM starting UpdateHandler' not found.
    Log Should Contain    [UpdateHandler] Application started, pid:                                  FAIL: Log for 'DSM started UpdateHandler with a PID' not found.
    Log Should Contain    [UpdateHandler] Modifying app state from AboutToBeStarted -> Running       FAIL: Log for 'UpdateHandler app state changed to Running' not found.


*** Keywords ***
Connect And Prepare Log Streaming
    [Documentation]    Performs all setup steps from the Pytest conftest fixture.
    Log To Console    Starting suite setup...

    # 1. Open the connection
    RemoteSSH.Open Connection    host=${HOST}    user=${USERNAME}    password=${PASSWORD}

    # 2. Crash detection before running tests
    ${is_crashing}=    RemoteSSH.Is Service Crashing    log_path=${LOG_PATH}    log_name=${LOG_NAME}    marker=${MARKER}
    IF    ${is_crashing}
        Fail    Aborting tests: Service is restarting repeatedly (possible crash).
    END

    # 3. Ensure the marker is present in the log
    ${line_number}=    RemoteSSH.Get Latest Service Start Line    log_path=${LOG_PATH}    log_name=${LOG_NAME}    marker=${MARKER}
    IF    ${line_number} is None or ${line_number} <= 0
        Fail    Aborting tests: Restart marker '${MARKER}' not found in log.
    END

    # 4. Start log streaming from that point
    RemoteSSH.Start Log Stream From Latest Restart    log_path=${LOG_PATH}    log_name=${LOG_NAME}    marker=${MARKER}
    Log To Console    Suite setup complete. Log streaming has started.

    # 5. Wait for the log buffer to populate before running tests.
    Log To Console    Waiting for 5 seconds for initial logs to be captured...
    Sleep    5s

Disconnect From Server
    [Documentation]    Performs the teardown by closing the connection.
    Log To Console    Starting suite teardown...
    RemoteSSH.Close Connection
    Log To Console    Suite teardown complete.

Log Should Contain
    [Documentation]    A wrapper keyword that checks if the log buffer contains a specific text.
    [Arguments]    ${text_to_find}    ${custom_error_message}
    ${found}=    RemoteSSH.Validate In Logs    text_to_find=${text_to_find}
    Should Be True    ${found}    ${custom_error_message}
